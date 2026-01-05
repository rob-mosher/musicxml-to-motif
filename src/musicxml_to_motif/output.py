"""Output formatting for motif analysis results.

This module handles formatting analysis results as JSON and other formats.
"""

import json
from pathlib import Path
from typing import Optional

from .models import MotifAnalysis


def format_as_json(
    analysis: MotifAnalysis, indent: int = 2, sort_keys: bool = False
) -> str:
    """Format a MotifAnalysis as JSON string.

    Args:
        analysis: The analysis result to format
        indent: Number of spaces for indentation (None for compact)
        sort_keys: Whether to sort keys alphabetically

    Returns:
        JSON string representation
    """
    return json.dumps(analysis.to_dict(), indent=indent, sort_keys=sort_keys)


def save_as_json(
    analysis: MotifAnalysis,
    output_path: str | Path,
    indent: int = 2,
    sort_keys: bool = False,
) -> None:
    """Save a MotifAnalysis to a JSON file.

    Args:
        analysis: The analysis result to save
        output_path: Path where to save the JSON file
        indent: Number of spaces for indentation
        sort_keys: Whether to sort keys alphabetically
    """
    output_path = Path(output_path)
    json_str = format_as_json(analysis, indent=indent, sort_keys=sort_keys)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json_str)


def create_analysis_from_score(
    parsed_score,
    motifs: list,
    instances: list,
    source: str = "musicxml-to-motif",
    notes: Optional[str] = None,
) -> MotifAnalysis:
    """Create a MotifAnalysis object from components.

    Args:
        parsed_score: The parsed score (for metadata)
        motifs: List of Motif objects
        instances: List of MotifInstance objects
        source: Source identifier
        notes: Optional notes about the analysis

    Returns:
        A MotifAnalysis object
    """
    meta = {
        "source": source,
    }

    if parsed_score.title:
        meta["work"] = parsed_score.title
    if parsed_score.composer:
        meta["composer"] = parsed_score.composer
    if notes:
        meta["notes"] = notes

    return MotifAnalysis(meta=meta, motifs=motifs, instances=instances)
