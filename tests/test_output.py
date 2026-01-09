"""Tests for output serialization."""

import json
from fractions import Fraction

from musicxml_to_motif.models import Motif, MotifAnalysis, MotifInstance
from musicxml_to_motif.output import format_as_json


def test_format_as_json_handles_fraction_values():
    """Ensure Fraction values in analysis serialize to JSON."""
    motif = Motif(
        id="m1",
        description="Test motif",
        rhythm=["quarter"],
        intervals=[],
    )
    instance = MotifInstance(
        motif_id="m1",
        measure=1,
        part="Piano",
        start_beat=Fraction(3, 2),
        confidence=0.9,
    )
    analysis = MotifAnalysis(
        meta={"source": "test"},
        motifs=[motif],
        instances=[instance],
    )

    result = format_as_json(analysis)
    data = json.loads(result)

    assert data["instances"][0]["start_beat"] == 1.5
