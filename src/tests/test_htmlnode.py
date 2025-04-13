import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    # def test_to_html_not_implemented(self):
    #     node = HTMLNode()
    #     with self.assertRaises(NotImplementedError):
    #         node.to_html()

    def test_props_to_html(self):
        node = HTMLNode(props={"class": "my-class", "id": "unique"})
        expected_html = ' class="my-class" id="unique"'
        self.assertEqual(node.props_to_html(), expected_html)

    def test_children_initialization(self):
        child1 = HTMLNode(tag="p", value="Child 1")
        child2 = HTMLNode(tag="span", value="Child 2")
        parent = HTMLNode(tag="div", children=[child1, child2])

        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.children[0].tag, "p")
        self.assertEqual(parent.children[1].tag, "span")

if __name__ == "__main__":
    unittest.main()