"""Tests for data models."""

import pytest

from musicxml_to_motif.models import Motif, MotifAnalysis, MotifInstance


def test_motif_creation():
    """Test creating a valid motif."""
    motif = Motif(
        id="m1",
        description="Test motif",
        rhythm=["eighth", "eighth", "quarter"],
        intervals=[2, -1],
        confidence=0.9,
        emotion="joyful",
    )

    assert motif.id == "m1"
    assert motif.description == "Test motif"
    assert motif.rhythm == ["eighth", "eighth", "quarter"]
    assert motif.intervals == [2, -1]
    assert motif.confidence == 0.9
    assert motif.emotion == "joyful"


def test_motif_interval_validation():
    """Test that motif validates interval length."""
    with pytest.raises(ValueError, match="Intervals length"):
        Motif(
            id="m1",
            description="Invalid",
            rhythm=["quarter", "quarter"],
            intervals=[2, 3, 4],  # Too many intervals
        )


def test_motif_confidence_validation():
    """Test that motif validates confidence range."""
    with pytest.raises(ValueError, match="Confidence must be"):
        Motif(
            id="m1",
            description="Invalid",
            rhythm=["quarter", "quarter"],
            intervals=[2],
            confidence=1.5,  # Out of range
        )


def test_motif_to_dict():
    """Test motif serialization to dict."""
    motif = Motif(
        id="m1",
        description="Test",
        rhythm=["eighth", "eighth"],
        intervals=[2],
        confidence=0.8,
    )

    result = motif.to_dict()
    assert result["id"] == "m1"
    assert result["description"] == "Test"
    assert result["rhythm"] == ["eighth", "eighth"]
    assert result["intervals"] == [2]
    assert result["confidence"] == 0.8
    assert "emotion" not in result  # Optional field not included


def test_motif_instance_creation():
    """Test creating a valid motif instance."""
    instance = MotifInstance(
        motif_id="m1",
        measure=5,
        part="Violin I",
        start_beat=2.5,
        confidence=0.95,
        variations="transposed",
    )

    assert instance.motif_id == "m1"
    assert instance.measure == 5
    assert instance.part == "Violin I"
    assert instance.start_beat == 2.5
    assert instance.confidence == 0.95
    assert instance.variations == "transposed"


def test_motif_instance_validation():
    """Test instance validation."""
    with pytest.raises(ValueError, match="Confidence must be"):
        MotifInstance(
            motif_id="m1",
            measure=1,
            part="Piano",
            start_beat=1.0,
            confidence=2.0,  # Out of range
        )

    with pytest.raises(ValueError, match="Measure must be"):
        MotifInstance(
            motif_id="m1",
            measure=0,  # Invalid
            part="Piano",
            start_beat=1.0,
            confidence=0.8,
        )


def test_motif_analysis_creation():
    """Test creating a complete analysis."""
    motif = Motif(
        id="m1",
        description="Test",
        rhythm=["quarter", "quarter"],
        intervals=[2],
    )

    instance = MotifInstance(
        motif_id="m1", measure=1, part="Piano", start_beat=1.0, confidence=0.9
    )

    analysis = MotifAnalysis(
        meta={"work": "Test Piece", "composer": "Test Composer"},
        motifs=[motif],
        instances=[instance],
    )

    assert len(analysis.motifs) == 1
    assert len(analysis.instances) == 1
    assert analysis.meta["work"] == "Test Piece"


def test_motif_analysis_to_dict():
    """Test analysis serialization."""
    motif = Motif(
        id="m1",
        description="Test",
        rhythm=["quarter"],
        intervals=[],
    )

    analysis = MotifAnalysis(meta={"source": "test"}, motifs=[motif], instances=[])

    result = analysis.to_dict()
    assert "meta" in result
    assert "motifs" in result
    assert "instances" in result
    assert len(result["motifs"]) == 1
    assert result["meta"]["source"] == "test"
