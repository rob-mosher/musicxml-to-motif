# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Roadmap doc (`docs/roadmap.md`) outlining phased motif detection milestones, inference possibilities, and community engagement steps

### Added

- Example motif-map JSON for Beethoven's Fifth in README to illustrate expected output structure

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
