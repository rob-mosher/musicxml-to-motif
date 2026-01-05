"""Motif detection logic.

This module provides functionality for detecting recurring musical patterns
(motifs) within a parsed score.
"""

from collections import defaultdict
from typing import Optional

from .models import Motif
from .parser import ParsedNote, ParsedScore, notes_to_intervals, notes_to_rhythm


def detect_motifs(
    parsed_score: ParsedScore,
    min_length: int = 3,
    max_length: int = 5,
    min_occurrences: int = 2,
) -> list[Motif]:
    """Detect recurring motifs in a parsed score.

    This is a heuristic approach that looks for recurring patterns
    of pitch intervals and rhythms.

    Args:
        parsed_score: The parsed musical score
        min_length: Minimum notes in a motif
        max_length: Maximum notes in a motif
        min_occurrences: Minimum times a pattern must occur to be a motif

    Returns:
        List of detected motifs
    """
    # Track pattern occurrences
    # Key: (interval_tuple, rhythm_tuple), Value: count
    pattern_counts: defaultdict[tuple, int] = defaultdict(int)
    pattern_examples: dict[tuple, list[ParsedNote]] = {}

    # Scan through the score looking for patterns
    for part_name in parsed_score.parts:
        part_notes = [n for n in parsed_score.notes if n.part_name == part_name]

        for length in range(min_length, max_length + 1):
            for i in range(len(part_notes) - length + 1):
                window = part_notes[i : i + length]

                # Extract pattern signature
                intervals = tuple(notes_to_intervals(window))
                rhythm = tuple(notes_to_rhythm(window))
                pattern_key = (intervals, rhythm)

                pattern_counts[pattern_key] += 1

                # Keep first example of each pattern
                if pattern_key not in pattern_examples:
                    pattern_examples[pattern_key] = window

    # Convert recurring patterns to Motif objects
    motifs = []
    motif_id = 1

    for (intervals, rhythm), count in pattern_counts.items():
        if count >= min_occurrences:
            # Generate description
            description = _generate_motif_description(list(intervals), list(rhythm))

            motif = Motif(
                id=f"m{motif_id}",
                description=description,
                rhythm=list(rhythm),
                intervals=list(intervals),
                confidence=min(0.7 + (count * 0.05), 1.0),  # Higher for more occurrences
            )
            motifs.append(motif)
            motif_id += 1

    # Sort by confidence (most prominent motifs first)
    motifs.sort(key=lambda m: m.confidence, reverse=True)

    return motifs


def _generate_motif_description(intervals: list[int], rhythm: list[str]) -> str:
    """Generate a human-readable description of a motif.

    Args:
        intervals: List of pitch intervals
        rhythm: List of rhythm values

    Returns:
        A descriptive string
    """
    # Describe rhythm pattern
    rhythm_desc = "-".join(rhythm)

    # Describe melodic contour
    if not intervals:
        contour_desc = "single note"
    elif all(i == 0 for i in intervals):
        contour_desc = "repeated note"
    elif all(i > 0 for i in intervals):
        contour_desc = "ascending"
    elif all(i < 0 for i in intervals):
        contour_desc = "descending"
    else:
        # Mixed contour
        ups = sum(1 for i in intervals if i > 0)
        downs = sum(1 for i in intervals if i < 0)
        if ups > downs:
            contour_desc = "mostly ascending"
        elif downs > ups:
            contour_desc = "mostly descending"
        else:
            contour_desc = "wave-like"

    # Describe interval characteristics
    if intervals:
        max_interval = max(abs(i) for i in intervals)
        if max_interval <= 2:
            interval_desc = "stepwise"
        elif max_interval <= 4:
            interval_desc = "small leaps"
        else:
            interval_desc = "wide leaps"
    else:
        interval_desc = ""

    # Combine descriptions
    parts = [rhythm_desc, contour_desc]
    if interval_desc:
        parts.append(interval_desc)

    return f"{' '.join(parts)} pattern"


def create_motif(
    motif_id: str,
    description: str,
    rhythm: list[str],
    intervals: list[int],
    confidence: float = 1.0,
    emotion: Optional[str] = None,
) -> Motif:
    """Create a motif manually (for user-defined motifs).

    Args:
        motif_id: Unique identifier
        description: Human-readable description
        rhythm: List of duration types
        intervals: List of pitch intervals
        confidence: Confidence score (0.0 to 1.0)
        emotion: Optional emotional character

    Returns:
        A Motif object
    """
    return Motif(
        id=motif_id,
        description=description,
        rhythm=rhythm,
        intervals=intervals,
        confidence=confidence,
        emotion=emotion,
    )
