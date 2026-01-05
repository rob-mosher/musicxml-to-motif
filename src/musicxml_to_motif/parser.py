"""MusicXML parsing utilities.

This module handles parsing MusicXML files and extracting musical elements
using the music21 library.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from music21 import converter, note, stream


@dataclass
class ParsedNote:
    """A parsed musical note with its context.

    Attributes:
        pitch: MIDI pitch number (e.g., C4 = 60)
        duration_type: Duration type (e.g., "quarter", "eighth", "half")
        duration_quarters: Duration in quarter note units
        measure_number: Measure where this note appears
        beat: Beat position within the measure
        part_name: Name of the part/instrument
        offset: Offset in quarter notes from the start of the piece
    """

    pitch: int
    duration_type: str
    duration_quarters: float
    measure_number: int
    beat: float
    part_name: str
    offset: float


@dataclass
class ParsedScore:
    """A parsed musical score with metadata and notes.

    Attributes:
        title: Title of the work
        composer: Composer name
        notes: List of all parsed notes in chronological order
        parts: List of part names in the score
    """

    title: Optional[str]
    composer: Optional[str]
    notes: list[ParsedNote]
    parts: list[str]


def parse_musicxml(file_path: str | Path) -> ParsedScore:
    """Parse a MusicXML file and extract musical elements.

    Args:
        file_path: Path to the MusicXML file

    Returns:
        ParsedScore containing metadata and all notes

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file cannot be parsed
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        score = converter.parse(str(file_path))
    except Exception as e:
        raise ValueError(f"Failed to parse MusicXML file: {e}") from e

    # Extract metadata
    title = score.metadata.title if score.metadata else None
    composer = score.metadata.composer if score.metadata else None

    # Extract all notes from all parts
    parsed_notes = []
    parts = []

    for part in score.parts:
        part_name = part.partName or f"Part {len(parts) + 1}"
        parts.append(part_name)

        # Flatten the part to get all notes in order
        flat_part = part.flatten()

        for element in flat_part.notesAndRests:
            if isinstance(element, note.Note):
                # Get measure number - music21 measure numbers start at 0 or 1
                measure_num = element.measureNumber or 1

                # Get beat position
                beat_pos = element.beat or 1.0

                # Create parsed note
                parsed_note = ParsedNote(
                    pitch=element.pitch.midi,
                    duration_type=element.duration.type,
                    duration_quarters=element.duration.quarterLength,
                    measure_number=measure_num,
                    beat=beat_pos,
                    part_name=part_name,
                    offset=element.offset,
                )
                parsed_notes.append(parsed_note)

            # Note: We're currently ignoring rests, but they could be important
            # for rhythm-based motif detection in future enhancements

    return ParsedScore(
        title=title, composer=composer, notes=parsed_notes, parts=parts
    )


def get_note_sequence(
    parsed_score: ParsedScore, part_name: Optional[str] = None
) -> list[ParsedNote]:
    """Get a sequence of notes, optionally filtered by part.

    Args:
        parsed_score: The parsed score
        part_name: Optional part name to filter by

    Returns:
        List of notes in chronological order
    """
    if part_name:
        return [n for n in parsed_score.notes if n.part_name == part_name]
    return parsed_score.notes


def notes_to_intervals(notes: list[ParsedNote]) -> list[int]:
    """Convert a sequence of notes to pitch intervals.

    Calculates consecutive intervals (difference between each note and the next).
    This represents the melodic motion between adjacent notes.

    Args:
        notes: List of notes in sequence

    Returns:
        List of intervals in semitones between consecutive notes
        Length will be len(notes) - 1

    Example:
        For notes C-D-E (pitches 60, 62, 64):
        Returns [2, 2] (C→D is +2, D→E is +2)
    """
    if len(notes) < 2:
        return []

    return [notes[i + 1].pitch - notes[i].pitch for i in range(len(notes) - 1)]


def notes_to_rhythm(notes: list[ParsedNote]) -> list[str]:
    """Extract rhythm pattern from a sequence of notes.

    Args:
        notes: List of notes in sequence

    Returns:
        List of duration types (e.g., ["eighth", "eighth", "quarter"])
    """
    return [n.duration_type for n in notes]
