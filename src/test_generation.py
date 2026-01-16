import unittest
from generation import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_eq(self):
        md = """
# This is an h1 line

This is a paragraph with text
This is the same paragraph on a new line
"""
        title = extract_title(md)
        self.assertEqual(title, "This is an h1 line")