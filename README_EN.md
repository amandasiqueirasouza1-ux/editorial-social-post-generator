# Editorial Social Post Generator

A local, configurable SVG generator for editorial social media posts.

It reads post content from CSV, applies brand settings from JSON, and creates light and dark variants. It uses only the Python standard library and sends no data to external services.

## Quick start

```bash
cp config/brand.example.json config/brand.json
cp content/posts.example.csv content/posts.csv
python3 src/generate.py
```

Generated SVG files are written to `output/`.

Run the test suite with:

```bash
python3 -m unittest discover -s tests -v
```

See the Portuguese [README](README.md) for the complete field and configuration reference.
