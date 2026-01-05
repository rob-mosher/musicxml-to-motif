# musicxml-to-motif

## Example Output

From MusicXML file:

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
