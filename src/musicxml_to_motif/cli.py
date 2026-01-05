"""Command-line interface for musicxml-to-motif."""

import argparse
import sys
from pathlib import Path

from musicxml_to_motif import __version__
from musicxml_to_motif.detector import detect_motifs
from musicxml_to_motif.matcher import find_motif_instances
from musicxml_to_motif.output import create_analysis_from_score, save_as_json
from musicxml_to_motif.parser import parse_musicxml


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Analyze MusicXML files for recurring musical motifs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a MusicXML file and save results
  musicxml-to-motif analyze input.xml -o results.json

  # Adjust detection sensitivity
  musicxml-to-motif analyze input.xml --min-length 4 --max-length 6

  # Show version
  musicxml-to-motif --version
        """,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"musicxml-to-motif {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a MusicXML file for motifs",
    )
    analyze_parser.add_argument(
        "input",
        type=Path,
        help="Path to MusicXML file",
    )
    analyze_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output JSON file path (default: print to stdout)",
    )
    analyze_parser.add_argument(
        "--min-length",
        type=int,
        default=3,
        help="Minimum notes in a motif (default: 3)",
    )
    analyze_parser.add_argument(
        "--max-length",
        type=int,
        default=5,
        help="Maximum notes in a motif (default: 5)",
    )
    analyze_parser.add_argument(
        "--min-occurrences",
        type=int,
        default=2,
        help="Minimum times a pattern must occur (default: 2)",
    )
    analyze_parser.add_argument(
        "--min-confidence",
        type=float,
        default=0.5,
        help="Minimum confidence for instance matching (default: 0.5)",
    )
    analyze_parser.add_argument(
        "--interval-tolerance",
        type=int,
        default=0,
        help="Semitone tolerance for interval matching (default: 0)",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "analyze":
        try:
            analyze_file(
                input_path=args.input,
                output_path=args.output,
                min_length=args.min_length,
                max_length=args.max_length,
                min_occurrences=args.min_occurrences,
                min_confidence=args.min_confidence,
                interval_tolerance=args.interval_tolerance,
            )
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


def analyze_file(
    input_path: Path,
    output_path: Path | None,
    min_length: int,
    max_length: int,
    min_occurrences: int,
    min_confidence: float,
    interval_tolerance: int,
) -> None:
    """Analyze a MusicXML file for motifs.

    Args:
        input_path: Path to input MusicXML file
        output_path: Optional path to output JSON file
        min_length: Minimum motif length
        max_length: Maximum motif length
        min_occurrences: Minimum occurrences for a pattern to be a motif
        min_confidence: Minimum confidence for instance matches
        interval_tolerance: Semitone tolerance for matching
    """
    print(f"Parsing {input_path}...")
    parsed_score = parse_musicxml(input_path)

    print(
        f"Found {len(parsed_score.notes)} notes across {len(parsed_score.parts)} parts"
    )
    if parsed_score.title:
        print(f"Work: {parsed_score.title}")
    if parsed_score.composer:
        print(f"Composer: {parsed_score.composer}")

    print(f"\nDetecting motifs (length {min_length}-{max_length})...")
    motifs = detect_motifs(
        parsed_score,
        min_length=min_length,
        max_length=max_length,
        min_occurrences=min_occurrences,
    )

    print(f"Found {len(motifs)} recurring motifs")

    print("\nFinding motif instances...")
    all_instances = []
    for motif in motifs:
        instances = find_motif_instances(
            motif,
            parsed_score,
            interval_tolerance=interval_tolerance,
            min_confidence=min_confidence,
        )
        all_instances.extend(instances)
        print(f"  {motif.id}: {len(instances)} instances - {motif.description}")

    print(f"\nTotal instances found: {len(all_instances)}")

    # Create analysis object
    analysis = create_analysis_from_score(
        parsed_score,
        motifs,
        all_instances,
        notes=f"Detected with min_length={min_length}, max_length={max_length}, min_occurrences={min_occurrences}",
    )

    # Save or print
    if output_path:
        save_as_json(analysis, output_path)
        print(f"\nResults saved to {output_path}")
    else:
        from musicxml_to_motif.output import format_as_json

        print("\n" + format_as_json(analysis))
