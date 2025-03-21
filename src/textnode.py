from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"  # Normal text
    BOLD = "bold"  # Bold text
    ITALIC = "italic"  # Italic text
    CODE_TEXT = "code_text"  # Code text
    LINK = "link"  # Link text
    IMAGE = "image"  # Images

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (self.text == other.text and 
                self.text_type == other.text_type and 
                self.url == other.url)
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE_TEXT:  # Note: using your enum value
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        # For links, we need the href property
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        # For images, we need src and alt properties
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Invalid TextType: {text_node.text_type}")