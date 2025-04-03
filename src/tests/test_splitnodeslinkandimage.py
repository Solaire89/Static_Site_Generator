import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from splitnodesimage import split_nodes_image
from splitnodeslink import split_nodes_link
from textnode import TextType, TextNode

class TestSplitImagesAndLinks(unittest.TestCase):
    def test_split_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_single_link(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_malformed_and_no_images(self):
    # Test with no images in the text
        node_no_images = TextNode(
            "This is just plain text with no images or links.",
            TextType.TEXT,
        )
        result_no_images = split_nodes_image([node_no_images])
        self.assertListEqual([node_no_images], result_no_images)

        # Test with malformed image markdown
        node_malformed_image = TextNode(
            "Here is a broken image syntax ![alt text missing parenthesis",
            TextType.TEXT,
        )
        result_malformed_image = split_nodes_image([node_malformed_image])
        self.assertListEqual([node_malformed_image], result_malformed_image)

        # Test with mixed valid and invalid markdown
        node_mixed_image = TextNode(
            "Valid ![alt](https://valid.url) and invalid ![broken image link",
            TextType.TEXT,
        )
        result_mixed_image = split_nodes_image([node_mixed_image])
        self.assertListEqual(
            [
                TextNode("Valid ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "https://valid.url"),
                TextNode(" and invalid ![broken image link", TextType.TEXT),
            ],
            result_mixed_image,
        )