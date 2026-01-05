"""Motif matching and instance finding.

This module finds instances of defined motifs throughout a score,
with fuzzy matching and confidence scoring.
"""

from typing import Optional

from .models import Motif, MotifInstance
from .parser import ParsedNote, ParsedScore, notes_to_intervals, notes_to_rhythm


def find_motif_instances(
    motif: Motif,
    parsed_score: ParsedScore,
    interval_tolerance: int = 0,
    rhythm_tolerance: float = 0.0,
    min_confidence: float = 0.5,
) -> list[MotifInstance]:
    """Find all instances of a motif in a parsed score.

    Args:
        motif: The motif to search for
        parsed_score: The parsed score to search in
        interval_tolerance: How many semitones of variation to allow in intervals
        rhythm_tolerance: Tolerance for rhythm matching (0.0 = exact, 1.0 = very loose)
        min_confidence: Minimum confidence score to include an instance

    Returns:
        List of motif instances found
    """
    instances = []
    motif_length = len(motif.rhythm)

    # Search through each part
    for part_name in parsed_score.parts:
        part_notes = [n for n in parsed_score.notes if n.part_name == part_name]

        # Sliding window search
        for i in range(len(part_notes) - motif_length + 1):
            window = part_notes[i : i + motif_length]

            # Calculate confidence for this window
            confidence = _calculate_match_confidence(
                window=window,
                motif=motif,
                interval_tolerance=interval_tolerance,
                rhythm_tolerance=rhythm_tolerance,
            )

            if confidence >= min_confidence:
                # Identify any variations
                variations = _describe_variations(window, motif)

                instance = MotifInstance(
                    motif_id=motif.id,
                    measure=window[0].measure_number,
                    part=part_name,
                    start_beat=window[0].beat,
                    confidence=confidence,
                    variations=variations if variations else None,
                )
                instances.append(instance)

    return instances


def _calculate_match_confidence(
    window: list[ParsedNote],
    motif: Motif,
    interval_tolerance: int,
    rhythm_tolerance: float,
) -> float:
    """Calculate how well a window of notes matches a motif.

    Args:
        window: Sequence of notes to match
        motif: The motif to match against
        interval_tolerance: Semitone tolerance for intervals
        rhythm_tolerance: Tolerance for rhythm matching

    Returns:
        Confidence score between 0.0 and 1.0
    """
    if len(window) != len(motif.rhythm):
        return 0.0

    # Extract pattern from window
    window_intervals = notes_to_intervals(window)
    window_rhythm = notes_to_rhythm(window)

    # Calculate interval match score
    interval_score = _interval_match_score(
        window_intervals, motif.intervals, interval_tolerance
    )

    # Calculate rhythm match score
    rhythm_score = _rhythm_match_score(window_rhythm, motif.rhythm, rhythm_tolerance)

    # Combined score (weighted average: 60% interval, 40% rhythm)
    # This weighting reflects that pitch patterns are often more defining
    # than rhythm for motif identity, but both matter
    confidence = (interval_score * 0.6) + (rhythm_score * 0.4)

    return confidence


def _interval_match_score(
    window_intervals: list[int], motif_intervals: list[int], tolerance: int
) -> float:
    """Score how well intervals match.

    Args:
        window_intervals: Intervals from the candidate window
        motif_intervals: Intervals from the motif definition
        tolerance: Allowed semitone deviation

    Returns:
        Score between 0.0 and 1.0
    """
    if len(window_intervals) != len(motif_intervals):
        return 0.0

    if not window_intervals:  # Empty intervals (single note motif)
        return 1.0

    matches = 0
    for w_int, m_int in zip(window_intervals, motif_intervals):
        diff = abs(w_int - m_int)
        if diff <= tolerance:
            # Full credit for exact match or within tolerance
            # Partial credit for near misses
            if diff == 0:
                matches += 1.0
            else:
                matches += 1.0 - (diff / (tolerance + 1))

    return matches / len(window_intervals)


def _rhythm_match_score(
    window_rhythm: list[str], motif_rhythm: list[str], tolerance: float
) -> float:
    """Score how well rhythms match.

    Args:
        window_rhythm: Rhythm from the candidate window
        motif_rhythm: Rhythm from the motif definition
        tolerance: How loose to be with rhythm matching

    Returns:
        Score between 0.0 and 1.0
    """
    if len(window_rhythm) != len(motif_rhythm):
        return 0.0

    if tolerance >= 1.0:
        # Very loose - any rhythm is acceptable
        return 1.0

    exact_matches = sum(
        1 for w, m in zip(window_rhythm, motif_rhythm) if w == m
    )

    if tolerance == 0.0:
        # Exact rhythm required
        return exact_matches / len(motif_rhythm)

    # Partial tolerance - give some credit for similar durations
    # (e.g., eighth vs sixteenth are closer than eighth vs whole)
    similarity_score = 0.0
    duration_order = [
        "1024th", "512th", "256th", "128th", "64th", "32nd", "16th",
        "eighth", "quarter", "half", "whole", "breve", "long"
    ]

    for w, m in zip(window_rhythm, motif_rhythm):
        if w == m:
            similarity_score += 1.0
        else:
            # Calculate distance in duration space
            try:
                w_idx = duration_order.index(w)
                m_idx = duration_order.index(m)
                distance = abs(w_idx - m_idx)
                # Apply tolerance: closer durations get higher scores
                similarity_score += max(0.0, 1.0 - (distance * (1.0 - tolerance)))
            except ValueError:
                # Unknown duration type, no partial credit
                pass

    return similarity_score / len(motif_rhythm)


def _describe_variations(window: list[ParsedNote], motif: Motif) -> Optional[str]:
    """Describe how a window differs from the motif.

    Args:
        window: The sequence of notes
        motif: The motif definition

    Returns:
        Description of variations, or None if exact match
    """
    window_intervals = notes_to_intervals(window)
    window_rhythm = notes_to_rhythm(window)

    variations = []

    # Check for interval variations
    if window_intervals != motif.intervals:
        # Check for transposition (all intervals same, but different starting pitch)
        # Actually, intervals are relative so they should be the same for transposition
        # Check for inversions or other transformations
        if all(
            w == -m for w, m in zip(window_intervals, motif.intervals)
        ):
            variations.append("inverted")
        elif any(w != m for w, m in zip(window_intervals, motif.intervals)):
            variations.append("altered intervals")

    # Check for rhythm variations
    if window_rhythm != motif.rhythm:
        variations.append("rhythmic variation")

    return ", ".join(variations) if variations else None
