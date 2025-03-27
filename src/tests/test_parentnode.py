import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html(self):
        parent_node = ParentNode(
            "div",
            [
                LeafNode("p", "Paragraph text"),
                ParentNode("ul", [
                    LeafNode("li", "Item 1"),
                    LeafNode("li", "Item 2")
                ])
            ]
        )
        self.assertEqual(
            parent_node.to_html(),
            "<div><p>Paragraph text</p><ul><li>Item 1</li><li>Item 2</li></ul></div>",
        )

    def test_to_html_raises_error_with_no_tag(self):
        # Create a ParentNode with a None tag
        node = ParentNode(None, [LeafNode("span", "child")])
        
        # Test that ValueError is raised with the expected message
        with self.assertRaises(ValueError) as context:
            node.to_html()
        
        # Check the error message
        self.assertEqual(str(context.exception), "ParentNode missing required tag")

    def test_to_html_raises_error_with_no_children(self):
        # Create a ParentNode with an empty children list
        node = ParentNode("div", [])
        
        # Test that ValueError is raised with the expected message
        with self.assertRaises(ValueError) as context:
            node.to_html()
        
        # Check the error message
        self.assertEqual(str(context.exception), "ParentNode missing required children")

    def test_constructor_requires_tag_and_children(self):
        # Test that creating a ParentNode with missing children raises a TypeError
        with self.assertRaises(TypeError):
            ParentNode("div")  # Missing children argument

    def test_to_html_with_five_levels_of_nesting(self):
        # Level 5 (deepest)
        deepest_node = LeafNode("code", "Hello World")
        
        # Level 4
        level4_node = ParentNode("pre", [deepest_node])
        
        # Level 3
        level3_node = ParentNode("div", [
            LeafNode("p", "Before nested content"),
            level4_node,
            LeafNode("p", "After nested content")
        ])
        
        # Level 2
        level2_node = ParentNode("section", [
            LeafNode("h2", "Section Title"),
            level3_node
        ])
        
        # Level 1 (root)
        root_node = ParentNode("article", [
            LeafNode("h1", "Article Title"),
            level2_node,
            LeafNode("footer", "Copyright 2023")
        ])
        
        expected_html = (
            "<article>"
                "<h1>Article Title</h1>"
                "<section>"
                    "<h2>Section Title</h2>"
                    "<div>"
                        "<p>Before nested content</p>"
                        "<pre><code>Hello World</code></pre>"
                        "<p>After nested content</p>"
                    "</div>"
                "</section>"
                "<footer>Copyright 2023</footer>"
            "</article>"
        )
        
        self.assertEqual(root_node.to_html(), expected_html)

    def test_parent_node_with_props(self):
        node = ParentNode("div", [LeafNode("span", "text")], {"class": "container", "id": "main"})
        self.assertEqual(node.to_html(), '<div class="container" id="main"><span>text</span></div>')

    def test_empty_string_tag_raises_error(self):
        node = ParentNode("", [LeafNode("span", "text")])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "ParentNode missing required tag")

    def test_mixed_node_types(self):
        node = ParentNode("div", [
            LeafNode("h1", "Title"),
            ParentNode("ul", [
                LeafNode("li", "Item 1"),
                LeafNode("li", "Item 2")
            ]),
            LeafNode("p", "Footer")
        ])
        self.assertEqual(
            node.to_html(),
            "<div><h1>Title</h1><ul><li>Item 1</li><li>Item 2</li></ul><p>Footer</p></div>"
        )