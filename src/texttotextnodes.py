from textnode import TextNode, TextType
from splitnodeslink import split_nodes_link
from splitnodesimage import split_nodes_image
from splitnodesdelimiter import split_nodes_delimiter
from extractmarkdown import extract_markdown_images, extract_markdown_links

def text_to_text_nodes(text):
    # Start with a single text node containing all the raw text
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Apply each splitting function in sequence
    # Each one will further split the nodes from the previous step
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    
    return nodes