import csv
import json
import tempfile
import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from generate import generate, highlighted_flags, normalize, wrap_words  # noqa: E402


class GeneratorTests(unittest.TestCase):
    def test_normalize_removes_accents(self):
        self.assertEqual(normalize("Ação prática"), "ACAO PRATICA")

    def test_highlight_matches_multiple_words(self):
        words = "CLARITY CREATES BETTER ACTION".split()
        self.assertEqual(highlighted_flags(words, "better action"), [False, False, True, True])

    def test_wrap_preserves_all_words(self):
        text = "A useful process is easier to repeat"
        lines = wrap_words(text, max_chars=12)
        self.assertEqual(" ".join(word for line in lines for word in line), text.upper())

    def test_generate_creates_light_and_dark_files(self):
        brand = {
            "name": "TEST",
            "accent": "#FF0066",
            "support": "#AAAAAA",
            "light_background": "#FFFFFF",
            "light_text": "#111111",
            "dark_background": "#111111",
            "dark_text": "#FFFFFF",
            "title_font": "Arial",
            "support_font": "Arial",
            "width": 1080,
            "height": 1350,
        }
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            config = base / "brand.json"
            content = base / "posts.csv"
            output = base / "output"
            config.write_text(json.dumps(brand), encoding="utf-8")
            with content.open("w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=["filename", "title", "highlight", "category", "topic"],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "filename": "sample",
                        "title": "Clarity creates action",
                        "highlight": "Clarity",
                        "category": "Strategy",
                        "topic": "Focus",
                    }
                )
            self.assertEqual(generate(config, content, output), 2)
            self.assertTrue((output / "sample-light.svg").exists())
            self.assertTrue((output / "sample-dark.svg").exists())


if __name__ == "__main__":
    unittest.main()
