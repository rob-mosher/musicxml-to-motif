"""MusicXML to motif converter library.

A heuristic-based library for identifying musical motifs in MusicXML files.
Designed for human-AI collaboration in music analysis and composition.
"""

from .detector import create_motif, detect_motifs
from .matcher import find_motif_instances
from .models import Motif, MotifAnalysis, MotifInstance
from .output import create_analysis_from_score, format_as_json, save_as_json
from .parser import parse_musicxml

__version__ = "0.1.1"

__all__ = [
    "__version__",
    # Models
    "Motif",
    "MotifInstance",
    "MotifAnalysis",
    # Parser
    "parse_musicxml",
    # Detection
    "detect_motifs",
    "create_motif",
    # Matching
    "find_motif_instances",
    # Output
    "create_analysis_from_score",
    "format_as_json",
    "save_as_json",
]
