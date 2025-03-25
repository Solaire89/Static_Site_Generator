import unittest

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