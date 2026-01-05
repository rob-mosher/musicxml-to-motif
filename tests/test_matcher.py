"""Tests for motif matching."""

from musicxml_to_motif.matcher import find_motif_instances
from musicxml_to_motif.models import Motif
from musicxml_to_motif.parser import ParsedNote, ParsedScore


def test_find_exact_matches():
    """Test finding exact motif matches."""
    motif = Motif(
        id="m1",
        description="Test pattern",
        rhythm=["quarter", "quarter", "quarter"],
        intervals=[2, 2],  # C-D-E pattern
    )

    notes = [
        # First match: C-D-E
        ParsedNote(60, "quarter", 1.0, 1, 1.0, "Piano", 0.0),
        ParsedNote(62, "quarter", 1.0, 1, 2.0, "Piano", 1.0),
        ParsedNote(64, "quarter", 1.0, 1, 3.0, "Piano", 2.0),
        # Some other notes
        ParsedNote(70, "eighth", 0.5, 2, 1.0, "Piano", 4.0),
        # Second match: F-G-A (same intervals)
        ParsedNote(65, "quarter", 1.0, 3, 1.0, "Piano", 5.0),
        ParsedNote(67, "quarter", 1.0, 3, 2.0, "Piano", 6.0),
        ParsedNote(69, "quarter", 1.0, 3, 3.0, "Piano", 7.0),
    ]

    score = ParsedScore(title="Test", composer="Test", notes=notes, parts=["Piano"])

    instances = find_motif_instances(motif, score, min_confidence=0.9)

    # Should find 2 instances
    assert len(instances) == 2
    assert all(i.confidence >= 0.9 for i in instances)
    assert instances[0].measure == 1
    assert instances[1].measure == 3


def test_find_with_tolerance():
    """Test finding matches with interval tolerance."""
    motif = Motif(
        id="m1",
        description="Test pattern",
        rhythm=["quarter", "quarter"],
        intervals=[2],  # Whole step up
    )

    notes = [
        # Exact match: C-D (interval = 2)
        ParsedNote(60, "quarter", 1.0, 1, 1.0, "Piano", 0.0),
        ParsedNote(62, "quarter", 1.0, 1, 2.0, "Piano", 1.0),
        # Another exact match: D-E (interval = 2, overlapping window)
        # Note: E is already included above at position 2
        ParsedNote(64, "quarter", 1.0, 2, 1.0, "Piano", 2.0),
        # Non-match: E-G (interval = 5, outside tolerance of 1)
        ParsedNote(69, "quarter", 1.0, 2, 2.0, "Piano", 3.0),
        # Close match: G-Bb (interval = 3, within tolerance of 1)
        ParsedNote(72, "quarter", 1.0, 3, 1.0, "Piano", 4.0),
    ]

    score = ParsedScore(title="Test", composer="Test", notes=notes, parts=["Piano"])

    # Without tolerance - only exact matches (C-D and D-E)
    instances = find_motif_instances(
        motif, score, interval_tolerance=0, min_confidence=0.9
    )
    assert len(instances) == 2  # C-D and D-E

    # With tolerance of 1 - includes close match G-A (interval=3)
    instances = find_motif_instances(
        motif, score, interval_tolerance=1, min_confidence=0.5
    )
    assert len(instances) == 3  # C-D, D-E, and G-A


def test_multi_part_detection():
    """Test detecting motifs across different parts."""
    motif = Motif(
        id="m1",
        description="Test",
        rhythm=["quarter", "quarter"],
        intervals=[2],
    )

    notes = [
        # Piano part
        ParsedNote(60, "quarter", 1.0, 1, 1.0, "Piano", 0.0),
        ParsedNote(62, "quarter", 1.0, 1, 2.0, "Piano", 1.0),
        # Violin part
        ParsedNote(67, "quarter", 1.0, 1, 1.0, "Violin", 0.0),
        ParsedNote(69, "quarter", 1.0, 1, 2.0, "Violin", 1.0),
    ]

    score = ParsedScore(
        title="Test", composer="Test", notes=notes, parts=["Piano", "Violin"]
    )

    instances = find_motif_instances(motif, score, min_confidence=0.8)

    # Should find instances in both parts
    assert len(instances) == 2
    parts = {i.part for i in instances}
    assert "Piano" in parts
    assert "Violin" in parts


def test_confidence_threshold():
    """Test that confidence threshold filters results."""
    motif = Motif(
        id="m1",
        description="Test",
        rhythm=["quarter", "quarter"],
        intervals=[2],
    )

    notes = [
        # Exact match
        ParsedNote(60, "quarter", 1.0, 1, 1.0, "Piano", 0.0),
        ParsedNote(62, "quarter", 1.0, 1, 2.0, "Piano", 1.0),
        # Very different rhythm (won't match with high confidence)
        ParsedNote(64, "whole", 4.0, 2, 1.0, "Piano", 2.0),
        ParsedNote(66, "whole", 4.0, 2, 2.0, "Piano", 6.0),
    ]

    score = ParsedScore(title="Test", composer="Test", notes=notes, parts=["Piano"])

    # High confidence threshold - only exact match
    instances = find_motif_instances(motif, score, min_confidence=0.9)
    assert len(instances) == 1

    # Low confidence threshold - may include more
    instances = find_motif_instances(motif, score, min_confidence=0.3)
    assert len(instances) >= 1
