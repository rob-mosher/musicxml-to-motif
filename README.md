# musicxml-to-motif

A Python library for identifying musical motifs in MusicXML files using heuristic analysis. Designed for human-AI collaboration in music analysis and composition.

## Features

- **Parse MusicXML files** - Extract notes, rhythms, and musical structure
- **Detect recurring motifs** - Identify patterns of 3-5 notes that repeat throughout a score
- **Fuzzy matching** - Find motif instances even with minor variations
- **Confidence scoring** - Each match includes a confidence score (0.0 to 1.0)
- **Multi-part analysis** - Track motifs across different instruments
- **Flexible CLI and API** - Use as a command-line tool or Python library

## Installation

```bash
pip install musicxml-to-motif
```

## Quick Start

### Command Line

```bash
# Analyze a MusicXML file
musicxml-to-motif analyze input.xml -o results.json

# Adjust detection sensitivity
musicxml-to-motif analyze input.xml --min-length 4 --max-length 6

# See all options
musicxml-to-motif analyze --help
```

### Python API

```python
from musicxml_to_motif import (
    parse_musicxml,
    detect_motifs,
    find_motif_instances,
    create_analysis_from_score,
    save_as_json,
)

# Parse a MusicXML file
score = parse_musicxml("input.xml")

# Detect recurring motifs
motifs = detect_motifs(score, min_length=3, max_length=5)

# Find instances of each motif
all_instances = []
for motif in motifs:
    instances = find_motif_instances(motif, score)
    all_instances.extend(instances)

# Create and save analysis
analysis = create_analysis_from_score(score, motifs, all_instances)
save_as_json(analysis, "output.json")
```

## Example Output

Analyzing a MusicXML file produces structured JSON:

```json
{
  "meta": {
    "work": "Symphony No. 5 in C minor, Op. 67",
    "composer": "Ludwig van Beethoven",
    "source": "musicxml-to-motif",
    "notes": "Motif map inspired by the famous four-note opening motif"
  },
  "motifs": [
    {
      "id": "m1",
      "description": "Short-short-short-long rhythm with descending minor third",
      "rhythm": ["eighth", "eighth", "eighth", "half"],
      "intervals": [-3, 0, 0], 
      "confidence": 0.95,
      "emotion": "fateful"
    }
  ],
  "instances": [
    {
      "motif_id": "m1",
      "measure": 1,
      "part": "Violin I",
      "start_beat": 1,
      "confidence": 0.98
    },
    {
      "motif_id": "m1",
      "measure": 2,
      "part": "Violin I",
      "start_beat": 1,
      "confidence": 0.91
    },
    {
      "motif_id": "m1",
      "measure": 4,
      "part": "Cello + Bass",
      "start_beat": 1,
      "confidence": 0.88
    }
  ]
}
```

### Understanding the Output

- **intervals**: Consecutive pitch intervals in semitones between notes
  - Example: For notes G-G-G-E♭, intervals are `[0, 0, -3]` (G→G, G→G, G→E♭)
- **rhythm**: Duration types (e.g., "eighth", "quarter", "half")
- **confidence**: Match quality from 0.0 to 1.0
  - 1.0 = perfect match
  - 0.7-0.9 = good match with minor variations
  - < 0.7 = loose match

## How It Works

The library uses a heuristic approach to identify motifs:

1. **Parsing**: Extracts notes, rhythms, and structure from MusicXML using music21
2. **Pattern Detection**: Scans for recurring sequences of notes with matching:
   - Pitch intervals (melodic shape)
   - Rhythm patterns
3. **Instance Matching**: Finds all occurrences with fuzzy matching
   - Allows configurable tolerance for interval and rhythm variations
   - Calculates confidence scores based on similarity
4. **Output**: Generates structured JSON with motifs and their instances

This is **interpretable and transparent** - no machine learning black boxes, just clear musical pattern matching.

## Advanced Usage

### Custom Motif Definition

Create and search for specific motifs:

```python
from musicxml_to_motif import create_motif, find_motif_instances, parse_musicxml

# Define Beethoven's 5th opening motif manually
motif = create_motif(
    motif_id="fate_motif",
    description="The famous 'fate knocking' motif",
    rhythm=["eighth", "eighth", "eighth", "half"],
    intervals=[0, 0, -3],  # G-G-G-Eb
    confidence=1.0,
    emotion="fateful"
)

# Find this motif in a score
score = parse_musicxml("symphony.xml")
instances = find_motif_instances(
    motif,
    score,
    interval_tolerance=1,  # Allow 1 semitone variation
    min_confidence=0.7
)
```

### Tolerance and Sensitivity

Adjust detection parameters:

```python
# Strict matching - exact patterns only
motifs = detect_motifs(
    score,
    min_length=3,
    max_length=5,
    min_occurrences=3  # Must appear at least 3 times
)

# Loose matching - find variations
instances = find_motif_instances(
    motif,
    score,
    interval_tolerance=2,    # Allow ±2 semitones
    rhythm_tolerance=0.3,    # Allow some rhythm variation
    min_confidence=0.5
)
```

## Contributing

This project is part of the [Collaborators Framework](https://collaborators.group/) and welcomes contributions from humans and AI alike.

See [COLLABORATORS.md](COLLABORATORS.md) for our collaboration philosophy.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

Built with:
- [music21](https://web.mit.edu/music21/) - Music analysis toolkit
- The Collaborators Framework philosophy

Part of a broader vision for human-AI co-creation in music.
