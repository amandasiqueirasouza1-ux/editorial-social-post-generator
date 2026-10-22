#!/usr/bin/env python3
"""Generate configurable editorial social posts as SVG files."""

from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "brand.json"
DEFAULT_CONTENT = ROOT / "content" / "posts.csv"
DEFAULT_OUTPUT = ROOT / "output"
REQUIRED_COLUMNS = {"filename", "title", "highlight", "category", "topic"}


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    return re.sub(r"[^A-Z0-9]+", " ", value.upper()).strip()


def wrap_words(text: str, max_chars: int = 19) -> list[list[str]]:
    lines: list[list[str]] = []
    current: list[str] = []
    current_length = 0

    for word in text.upper().split():
        projected = current_length + len(word) + (1 if current else 0)
        if current and projected > max_chars:
            lines.append(current)
            current = [word]
            current_length = len(word)
        else:
            current.append(word)
            current_length = projected

    if current:
        lines.append(current)
    return lines


def highlighted_flags(words: list[str], highlight: str) -> list[bool]:
    target = normalize(highlight).split()
    clean_words = [normalize(word) for word in words]
    flags = [False] * len(words)
    if not target:
        return flags

    for start in range(len(clean_words) - len(target) + 1):
        if clean_words[start : start + len(target)] == target:
            for index in range(start, start + len(target)):
                flags[index] = True
    return flags


def choose_layout(text: str) -> tuple[int, list[list[str]]]:
    options = ((154, 16), (142, 18), (130, 20), (118, 22), (106, 24), (96, 26))
    for size, max_chars in options:
        lines = wrap_words(text, max_chars)
        if len(lines) <= 6:
            return size, lines
    raise ValueError("Title is too long for this template.")


def title_svg(text: str, highlight: str, text_color: str, accent: str, font: str) -> str:
    size, lines = choose_layout(text)
    line_height = int(size * 1.08)
    total_height = len(lines) * line_height
    y = max(285, int(680 - total_height / 2))
    words = text.upper().split()
    flags = highlighted_flags(words, highlight)
    index = 0
    output: list[str] = []

    for line in lines:
        baseline = y + size
        output.append(
            f'<text x="72" y="{baseline}" font-family="{escape(font)}" '
            f'font-size="{size}" font-weight="700">'
        )
        for position, word in enumerate(line):
            fill = accent if flags[index] else text_color
            prefix = "" if position == 0 else " "
            output.append(f'<tspan fill="{fill}">{escape(prefix + word)}</tspan>')
            index += 1
        output.append("</text>")
        y += line_height
    return "\n    ".join(output)


def build_svg(row: dict[str, str], brand: dict[str, object], variant: str, number: int) -> str:
    dark = variant == "dark"
    background = str(brand["dark_background"] if dark else brand["light_background"])
    text_color = str(brand["dark_text"] if dark else brand["light_text"])
    support = str(brand["support"] if dark else "#555555")
    divider = "#343434" if dark else str(brand["support"])
    accent = str(brand["accent"])
    width = int(brand["width"])
    height = int(brand["height"])
    title_font = str(brand["title_font"])
    support_font = str(brand["support_font"])
    footer = f'{row["category"].upper()}  /  {row["topic"].upper()}'
    title = title_svg(row["title"], row["highlight"], text_color, accent, title_font)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 1080 1350">
  <rect width="1080" height="1350" fill="{background}"/>
  <text x="72" y="92" fill="{text_color}" font-family="{escape(support_font)}" font-size="22" font-weight="600" letter-spacing="2.4">{escape(str(brand["name"]))}</text>
  <text x="1008" y="92" fill="{support}" text-anchor="end" font-family="{escape(support_font)}" font-size="22" letter-spacing="1.6">{number:02d}</text>
  <line x1="72" y1="130" x2="1008" y2="130" stroke="{divider}" stroke-width="2"/>
  {title}
  <line x1="72" y1="1210" x2="292" y2="1210" stroke="{accent}" stroke-width="8"/>
  <text x="72" y="1272" fill="{support}" font-family="{escape(support_font)}" font-size="20" font-weight="600" letter-spacing="3">{escape(footer)}</text>
</svg>
'''


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or not REQUIRED_COLUMNS.issubset(reader.fieldnames):
            missing = REQUIRED_COLUMNS.difference(reader.fieldnames or [])
            raise ValueError(f"Missing CSV columns: {', '.join(sorted(missing))}")
        return list(reader)


def generate(config_path: Path, content_path: Path, output_path: Path) -> int:
    brand = json.loads(config_path.read_text(encoding="utf-8"))
    rows = load_rows(content_path)
    output_path.mkdir(parents=True, exist_ok=True)

    count = 0
    for number, row in enumerate(rows, start=1):
        for variant in ("light", "dark"):
            destination = output_path / f'{row["filename"]}-{variant}.svg'
            destination.write_text(build_svg(row, brand, variant, number), encoding="utf-8")
            count += 1
    return count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--content", type=Path, default=DEFAULT_CONTENT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.config.exists():
        raise SystemExit("Missing config/brand.json. Copy config/brand.example.json first.")
    if not args.content.exists():
        raise SystemExit("Missing content/posts.csv. Copy content/posts.example.csv first.")
    count = generate(args.config, args.content, args.output)
    print(f"Generated {count} SVG files in {args.output}")


if __name__ == "__main__":
    main()
