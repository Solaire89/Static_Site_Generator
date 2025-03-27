import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from splitnodesdelimiter import split_nodes_delimiter
from textnode import TextType, TextNode

class TestSplitNodes(unittest.TestCase):
    def test_single_node(self):
        # Input node
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        
        # Expected output after using split_nodes_delimiter
        expected_output = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        
        # Call the function under test
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        # Assert the function's output matches the expected output
        self.assertEqual(result, expected_output)

    def test_single_text(self):
        node = TextNode("This is just regular text.", TextType.TEXT)

        # Expected output after using split_nodes_delimiter
        expected_output = [
            TextNode("This is just regular text.", TextType.TEXT)
        ]

        # Call the function
        result = split_nodes_delimiter([node], "**", TextType.TEXT)

        # Assert the function's output matches the expected output
        self.assertEqual(result, expected_output)

    def test_two_bold_markdowns(self):
        node = TextNode("This is a line with **two** **bold** words.", TextType.TEXT)

        # Make sure to inclue spaces and punctuation in the nodes
        expected_output = [
            TextNode("This is a line with ", TextType.TEXT),
            TextNode("two", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" words.", TextType.TEXT)
        ]

        # Our primary text type we're using is BOLD, so the TextType should be BOLD
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(result, expected_output)