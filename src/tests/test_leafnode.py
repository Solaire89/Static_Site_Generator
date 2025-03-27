import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        # Test basic paragraph tag
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_with_props(self):
        # Test tag with properties
        node = LeafNode("a", "Click me!", {"href": "https://www.example.com", "target": "_blank"})
        # The order of attributes might vary, so we can check for substrings
        html = node.to_html()
        self.assertIn("<a ", html)
        self.assertIn('href="https://www.example.com"', html)
        self.assertIn('target="_blank"', html)
        self.assertIn(">Click me!</a>", html)
    
    def test_leaf_to_html_no_tag(self):
        # Test with no tag (raw text)
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")
    
    def test_leaf_to_html_no_value(self):
        # Test with no value (should raise ValueError)
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()