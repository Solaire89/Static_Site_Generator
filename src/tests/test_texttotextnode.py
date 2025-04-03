import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from texttotextnodes import text_to_text_nodes  # The function you're testing
from textnode import TextNode, TextType  # For assertions and result validation

class TestTextToTextNode(unittest.TestCase):
    def test_text_to_textnodes(self):
    # Test basic text
        assert text_to_text_nodes("Just plain text") == [
            TextNode("Just plain text", TextType.TEXT)
        ]
        
        # Test bold text
        assert text_to_text_nodes("Some **bold** text") == [
            TextNode("Some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        
        # Test italic text
        assert text_to_text_nodes("Some _italic_ text") == [
            TextNode("Some ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        
        # Test code blocks
        assert text_to_text_nodes("Some `code` here") == [
            TextNode("Some ", TextType.TEXT),
            TextNode("code", TextType.CODE_TEXT),
            TextNode(" here", TextType.TEXT)
        ]
        
        # Test images
        assert text_to_text_nodes("An image: ![alt text](https://example.com/image.jpg)") == [
            TextNode("An image: ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.jpg")
        ]
        
        # Test links
        assert text_to_text_nodes("A [link](https://example.com) here") == [
            TextNode("A ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" here", TextType.TEXT)
        ]
        
        # Test multiple types combined
        # Test multiple elements in sequence
        assert text_to_text_nodes("**Bold** then _italic_") == [
            TextNode("Bold", TextType.BOLD),
            TextNode(" then ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC)
        ]

        # Test all element types together
        test_text = "Text with **bold**, _italic_, `code`, ![img](url.jpg), and [link](https://example.com)"
        result = text_to_text_nodes(test_text)
        assert result == [
            TextNode("Text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", ", TextType.TEXT),
            TextNode("code", TextType.CODE_TEXT),
            TextNode(", ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url.jpg"),
            TextNode(", and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com")
        ]

    def test_empty_text(self):
        nodes = text_to_text_nodes("")  # Use the correct function name
        assert len(nodes) == 1
        assert nodes[0].text == ""
        assert nodes[0].text_type == TextType.TEXT

    def test_unclosed_bold(self):
        with self.assertRaises(Exception) as context:
            text_to_text_nodes("This has an **unclosed bold")
        self.assertIn("No closing delimiter", str(context.exception))
    
    def test_unclosed_italic(self):
        with self.assertRaises(Exception) as context:
            text_to_text_nodes("This has an _unclosed italic")
        self.assertIn("No closing delimiter", str(context.exception))
    
    def test_unclosed_code(self):
        with self.assertRaises(Exception) as context:
            text_to_text_nodes("This has an `unclosed code")
        self.assertIn("No closing delimiter", str(context.exception))
    
    def test_malformed_link(self):
        # This has an unclosed link
        text = "Here's a [bad link without closing parenthesis"
        nodes = text_to_text_nodes(text)
        # Since extract_markdown_links probably won't find any valid links,
        # we expect the entire text to be treated as plain text
        self.assertEqual(1, len(nodes))
        self.assertEqual(text, nodes[0].text)
        self.assertEqual(TextType.TEXT, nodes[0].text_type)
    
    def test_malformed_image(self):
        # This has an unclosed image
        text = "Here's a ![bad image without closing parenthesis"
        nodes = text_to_text_nodes(text)
        # Similar to links, we expect this to be plain text
        self.assertEqual(1, len(nodes))
        self.assertEqual(text, nodes[0].text)
        self.assertEqual(TextType.TEXT, nodes[0].text_type)
    
    def test_incomplete_link_format(self):
        # Tests a link with brackets but no parentheses
        text = "Here's a [link text] without url"
        nodes = text_to_text_nodes(text)
        self.assertEqual(1, len(nodes))
        self.assertEqual(text, nodes[0].text)
        self.assertEqual(TextType.TEXT, nodes[0].text_type)

    def test_mix_of_valid_and_invalid(self):
    # Test a mix of valid and invalid markdown
        text = "Valid [link](https://example.com) and invalid [link without url"
        nodes = text_to_text_nodes(text)
        # We expect the valid link to be processed, but not the invalid one
        self.assertTrue(len(nodes) > 1)
        # The first node should be "Valid "
        self.assertEqual("Valid ", nodes[0].text)
        # The second node should be the link
        self.assertEqual("link", nodes[1].text)
        self.assertEqual(TextType.LINK, nodes[1].text_type)
        self.assertEqual("https://example.com", nodes[1].url)
        # The rest should include the invalid markdown as text
        self.assertIn(" and invalid [link without url", nodes[2].text)

if __name__ == "__main__":
    unittest.main()