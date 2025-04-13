import unittest
import sys
import os
from markdowntohtmlnode import create_heading_node, create_code_block, create_list_block
from textnode import TextNode
from htmlnode import HTMLNode
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_header_count(self):
        block = "### This is a heading"
        node = create_heading_node(block)  # Call the function to create the node
        pass

    def test_create_code_block(self):
        block = "```print('Hello')```"
        result = create_code_block(block)

        # Check outer <pre> tag
        assert isinstance(result, HTMLNode)
        assert result.tag == "pre"

        # Check it has one child: the <code> block
        code_node = result.children[0]
        assert code_node.tag == "code"
        assert isinstance(code_node, HTMLNode)

        # Check that the <code> has one child: the text node
        text_node = code_node.children[0]
        assert isinstance(text_node, TextNode)
        assert text_node.text == "print('Hello')"
        assert text_node.text_type == "code_text"

        print("test_create_code_block passed!")

    def test_create_list_block(self):
        
        unordered_block = """
        - Item 1
        - Item 2
        - Item 3
        """
        unordered_node = create_list_block(unordered_block)
        assert unordered_node.tag == "ul", "Parent tag should be 'ul' for unordered lists"
        assert len(unordered_node.children) == 3, "Should have 3 list items"
        assert unordered_node.children[0].children[0].value == "Item 1", "First <li> should contain 'Item 1'"
        assert unordered_node.children[1].children[0].value == "Item 2", "Second <li> should contain 'Item 2'"
        assert unordered_node.children[2].children[0].value == "Item 3", "Third <li> should contain 'Item 3'"

        md_block_ordered = """
        1. First
        2. Second
        3. Third
        """
        ordered_node = create_list_block(md_block_ordered, ordered=True)
        assert ordered_node.tag == "ol", "Parent tag should be 'ol' for ordered lists"
        assert len(ordered_node.children) == 3, "Should have 3 list items"
        assert ordered_node.children[0].children[0].value == "First", "First <li> should contain 'First'"
        assert ordered_node.children[1].children[0].value == "Second", "Second <li> should contain 'Second'"
        assert ordered_node.children[2].children[0].value == "Third", "Third <li> should contain 'Third'"

        print("All tests passed!")
