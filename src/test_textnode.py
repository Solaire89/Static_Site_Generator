import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("This is a test node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_none(self):
        node = TextNode("This is a test node", TextType.BOLD, None)
        node2 = TextNode("This is a test node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_noteq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, None)
        self.assertNotEqual(node, node2)

    def test_empty_vs_none_url(self):
        node = TextNode("Sample text", TextType.BOLD, None)
        node2 = TextNode("Sample text", TextType.BOLD, "")
        self.assertNotEqual(node, node2)

    def test_explicit_vs_implicit_none(self):
        node = TextNode("Sample text", TextType.BOLD, None)
        node2 = TextNode("Sample text", TextType.BOLD)
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()