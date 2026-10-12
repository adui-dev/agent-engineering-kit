import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from app import greet


class AppTests(unittest.TestCase):
    def test_greeting(self):
        self.assertEqual(greet("Agent"), "Hello, Agent!")

    def test_rejects_empty_name(self):
        with self.assertRaises(ValueError):
            greet(" ")


if __name__ == "__main__":
    unittest.main()
