"""Data models for motifs and instances.

These models represent the core structures for defining musical motifs
and tracking their instances throughout a score.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Motif:
    """A musical motif definition.

    Attributes:
        id: Unique identifier for the motif
        description: Human-readable description of the motif's character
        rhythm: List of note durations (e.g., ["eighth", "eighth", "half"])
        intervals: List of pitch intervals in semitones (relative to first note)
        confidence: Overall confidence in this motif definition (0.0 to 1.0)
        emotion: Optional emotional character tag
    """

    id: str
    description: str
    rhythm: list[str]
    intervals: list[int]
    confidence: float = 1.0
    emotion: Optional[str] = None

    def __post_init__(self):
        """Validate motif data."""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")

        # Intervals should be one less than rhythm length
        # (first note has no interval relative to itself)
        if len(self.intervals) != len(self.rhythm) - 1:
            raise ValueError(
                f"Intervals length ({len(self.intervals)}) should be "
                f"rhythm length - 1 ({len(self.rhythm) - 1})"
            )

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        result = {
            "id": self.id,
            "description": self.description,
            "rhythm": self.rhythm,
            "intervals": self.intervals,
            "confidence": self.confidence,
        }
        if self.emotion:
            result["emotion"] = self.emotion
        return result


@dataclass
class MotifInstance:
    """An instance of a motif appearing in the score.

    Attributes:
        motif_id: Reference to the motif this is an instance of
        measure: Measure number where this instance begins
        part: Instrument/part name where this instance appears
        start_beat: Beat within the measure where this instance starts
        confidence: How closely this instance matches the motif (0.0 to 1.0)
        variations: Optional description of variations from the motif
    """

    motif_id: str
    measure: int
    part: str
    start_beat: float
    confidence: float
    variations: Optional[str] = None

    def __post_init__(self):
        """Validate instance data."""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        if self.measure < 1:
            raise ValueError("Measure must be >= 1")
        if self.start_beat < 1:
            raise ValueError("Start beat must be >= 1")

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        result = {
            "motif_id": self.motif_id,
            "measure": self.measure,
            "part": self.part,
            "start_beat": self.start_beat,
            "confidence": self.confidence,
        }
        if self.variations:
            result["variations"] = self.variations
        return result


@dataclass
class MotifAnalysis:
    """Complete analysis result for a musical score.

    Attributes:
        meta: Metadata about the work (title, composer, etc.)
        motifs: List of identified motifs
        instances: List of motif instances found in the score
    """

    meta: dict[str, str]
    motifs: list[Motif] = field(default_factory=list)
    instances: list[MotifInstance] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "meta": self.meta,
            "motifs": [m.to_dict() for m in self.motifs],
            "instances": [i.to_dict() for i in self.instances],
        }
