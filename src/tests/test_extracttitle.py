import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extracttitle import extract_title

class TestExtractMarkdown(unittest.TestCase):
    def test_simple_title(self):
        actual = extract_title("# Hello!")
        expected = "Hello!"
        self.assertEqual(actual, expected)

    def test_missing_markdown(self):
        
        with self.assertRaises(Exception):
            extract_title("Hello!")

    def test_character_at_end(self):
        with self.assertRaises(Exception):
            extract_title("Hello! #")

    def test_two_characters_at_beginning(self):
        with self.assertRaises(Exception):
            extract_title("## Hello!")