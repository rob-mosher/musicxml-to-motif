# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Complete motif detection and analysis system with five core modules:
  - `models.py`: Data structures for Motif, MotifInstance, and MotifAnalysis with validation
  - `parser.py`: MusicXML parsing using music21, extracting notes with pitch, rhythm, and context
  - `detector.py`: Automatic motif detection by scanning for recurring patterns (3-5 notes)
  - `matcher.py`: Fuzzy matching engine with configurable interval/rhythm tolerance and confidence scoring
  - `output.py`: JSON formatting and file output functionality
- Full-featured CLI (`musicxml-to-motif analyze`) with parameters for detection sensitivity, tolerance, and output
- Comprehensive test suite with 17 passing tests covering models, detection, matching, and CLI
- Python API for programmatic access to all functionality (parse, detect, match, analyze, export)
- `music21>=9.1.0` dependency for MusicXML parsing
- Enhanced README with installation instructions, quick start guide, usage examples, and advanced configuration
- Roadmap doc (`docs/roadmap.md`) outlining phased motif detection milestones, inference possibilities, and community engagement steps
- Example motif-map JSON for Beethoven's Fifth in README to illustrate expected output structure

### Changed

- Updated package description to "Identify musical motifs in MusicXML files using heuristic analysis"
- Enhanced `pyproject.toml` with dependencies and additional classifiers
- Development status changed from "Pre-Alpha" to "Alpha"

## [0.1.1] - 2026-01-04

### Added

- CHANGELOG.md for tracking project history
- Python version file (`.python-version`) specifying Python 3.12
- MIT License
- Collaborator tagging guide (`.cursor/rules/collaborator-tagging.md`)
- COLLABORATORS.md establishing contributor acknowledgments using the Collaborators Framework
- Initial project structure with README.md
- Packaging skeleton for `musicxml-to-motif`, including `pyproject.toml`, versioned `__init__.py`, CLI stub, and module entrypoint
- Basic tests (`tests/test_version.py`, `tests/test_cli.py`) and `requirements.txt` for local pytest setup
- GitHub Actions publish workflow updated for the musicxml-to-motif package name and trusted publishing targets

[0.1.1]: https://github.com/rob-mosher/musicxml-to-motif/releases/tag/v0.1.1
