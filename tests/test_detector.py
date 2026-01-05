"""Tests for motif detection."""

from musicxml_to_motif.detector import create_motif, detect_motifs
from musicxml_to_motif.parser import ParsedNote, ParsedScore


def test_create_motif():
    """Test manual motif creation."""
    motif = create_motif(
        motif_id="beethoven_5th",
        description="Short-short-short-long",
        rhythm=["eighth", "eighth", "eighth", "half"],
        intervals=[-3, 0, 0],
        confidence=0.95,
        emotion="fateful",
    )

    assert motif.id == "beethoven_5th"
    assert motif.description == "Short-short-short-long"
    assert len(motif.rhythm) == 4
    assert len(motif.intervals) == 3
    assert motif.emotion == "fateful"


def test_detect_motifs_simple():
    """Test detecting a simple recurring pattern."""
    # Create a simple score with a repeating pattern
    notes = [
        # Pattern 1: C-D-E (intervals: [2, 2])
        ParsedNote(60, "quarter", 1.0, 1, 1.0, "Piano", 0.0),
        ParsedNote(62, "quarter", 1.0, 1, 2.0, "Piano", 1.0),
        ParsedNote(64, "quarter", 1.0, 1, 3.0, "Piano", 2.0),
        # Pattern 1 repeated: F-G-A (same intervals: [2, 2])
        ParsedNote(65, "quarter", 1.0, 2, 1.0, "Piano", 4.0),
        ParsedNote(67, "quarter", 1.0, 2, 2.0, "Piano", 5.0),
        ParsedNote(69, "quarter", 1.0, 2, 3.0, "Piano", 6.0),
    ]

    score = ParsedScore(
        title="Test",
        composer="Test Composer",
        notes=notes,
        parts=["Piano"],
    )

    motifs = detect_motifs(score, min_length=3, max_length=3, min_occurrences=2)

    # Should find the repeating pattern
    assert len(motifs) >= 1

    # Check the detected motif
    found_pattern = False
    for motif in motifs:
        if motif.intervals == [2, 2]:
            found_pattern = True
            assert len(motif.rhythm) == 3
            assert all(r == "quarter" for r in motif.rhythm)

    assert found_pattern, "Did not find the expected pattern"


def test_detect_motifs_min_occurrences():
    """Test that patterns below min_occurrences are filtered out."""
    notes = [
        # Unique pattern (occurs once)
        ParsedNote(60, "quarter", 1.0, 1, 1.0, "Piano", 0.0),
        ParsedNote(62, "quarter", 1.0, 1, 2.0, "Piano", 1.0),
        ParsedNote(64, "quarter", 1.0, 1, 3.0, "Piano", 2.0),
        # Different pattern
        ParsedNote(70, "eighth", 0.5, 2, 1.0, "Piano", 4.0),
        ParsedNote(71, "eighth", 0.5, 2, 1.5, "Piano", 4.5),
        ParsedNote(72, "eighth", 0.5, 2, 2.0, "Piano", 5.0),
    ]

    score = ParsedScore(
        title="Test",
        composer="Test",
        notes=notes,
        parts=["Piano"],
    )

    motifs = detect_motifs(score, min_length=3, max_length=3, min_occurrences=2)

    # Should find no motifs since no pattern repeats
    assert len(motifs) == 0
