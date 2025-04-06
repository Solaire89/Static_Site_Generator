import unittest
import sys
import os
from blocktoblocktype import BlockType, block_to_block_type
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_paragraph(self):
        block = "example_block"
        expected_type = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(block), expected_type)

    def test_block_to_heading(self):
        block = "# Heading text"
        expected_type = BlockType.HEADING
        self.assertEqual(block_to_block_type(block), expected_type)

    def test_block_to_code_block(self):
        block = "```Code text```"
        expected_type = BlockType.CODE
        self.assertEqual(block_to_block_type(block), expected_type)

    def test_block_to_quote(self):
        block = "> Quote text"
        expected_type = BlockType.QUOTE
        self.assertEqual(block_to_block_type(block), expected_type)

    def test_block_to_unordered_list(self):
        block = "- Unordered\n- List"
        expected_type = BlockType.UNORDERED_LIST
        self.assertEqual(block_to_block_type(block), expected_type)

    def test_block_to_ordered_list(self):
        block = "1. Ordered\n2. List"
        expected_type = BlockType.ORDERED_LIST
        self.assertEqual(block_to_block_type(block), expected_type)

    def test_block_to_wrong_order_list(self):
        block = "2. Wrong\n1. Order\n3. List"
        expected_type = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(block), expected_type)

    def test_too_many_heading_characters(self):
        block = "####### Should be a paragraph"
        expected_type = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(block), expected_type)

    def test_not_enough_dashes_list(self):
        block = "- A list item\nNo dash\n- Another list item"
        expected_type = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(block), expected_type)

    def test_not_enough_quote_lists(self):
        block = "> A quote\nNo symbol\n> Another quote"
        expected_type = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(block), expected_type)

if __name__ == "__main__":
    unittest.main()