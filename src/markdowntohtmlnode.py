import re
from markdowntoblocks import markdown_to_blocks
from blocktoblocktype import block_to_block_type
from textnode import TextNode, text_node_to_html_node
from splitnodesdelimiter import split_nodes_delimiter
from htmlnode import HTMLNode



# ----- Block Identification Functions -----

# ----- Block Processing Functions -----
def create_paragraph_node(block):

    # Create a paragraph node
    block_node = HTMLNode("p", None, None, [])
    
    # Process inline markdown and add children
    # Clear whitespace of the block
    block_node.children = text_to_children(block.strip())

    return block_node
        

def create_heading_node(block):

    # Counting the number of #'s in the header
    match = re.match(r"^([#]+)", block)
    header_markers = len(match.group(1))

    # Splitting the header markers from the content
    _, text_content = block.split(" ", 1) # Discard markers and focus on content
    
    # Creating the node
    block_node = HTMLNode(f"h{header_markers}", text_content, None, [])
    return block_node

# Not for inline processing
def create_code_block(block):
    # Remove the surrounding backticks (```)
    content = block.strip("`")

    # Create a child TextNode from the raw content (no inline parsing)
    child_node = TextNode(content, "code_text")

    # Return an HTMLNode for `<pre><code>` with the TextNode as its child
    code_node = HTMLNode("code", None, [child_node], None)  # <code> node contains the TextNode
    pre_node = HTMLNode("pre", None, [code_node], None)    # <pre> node contains the <code>
    return pre_node

def create_list_block(block, ordered=False):
    # Stripping the white space before and after the block
    # Also splitting the block line by line
    lines = block.strip().splitlines()
    li_nodes = []

    for line in lines:
        trimmed_line = line.lstrip()  # Remove leading whitespace
        if trimmed_line.startswith("- "):  # Checks for '- ' after any leading spaces
            content = line.lstrip()[2:]    # Removes exactly the first two characters ('- ')
        elif trimmed_line.startswith("* "):
            content = line.lstrip()[2:]   # Similar for '* '
        elif trimmed_line.startswith("+ "):
            content = line.lstrip()[2:]   # Similar for '+ '
        elif re.match(r"^\d+\. ", trimmed_line):  # Matches ordered list markers like "1. " or "25. "
            number_end_index = trimmed_line.index(". ") + 2  # Find where ". " ends
            content = trimmed_line[number_end_index:]  # Extract everything after the marker
        else:    
            continue  # If no valid list marker, skip this line

        li_node = HTMLNode("li", children=[HTMLNode("text", content)])
        li_nodes.append(li_node)

    # We're taking care of the logic of whether a list is ordered or 
    # unordered in the main markdown_to_HTML_node function.
    parent_tag = "ol" if ordered else "ul"
    list_node = HTMLNode(parent_tag, children=li_nodes)
    return list_node

def create_quote_block(block):

    processed_lines = []
    # Iterating over the lines in the block
    for line in block.split("\n"):
        if line.startswith(">"):
            # Remove ">" and strip whitespace
            processed_line = line[1:].strip()
        else:
            processed_line = line
        processed_lines.append(processed_line)
        
    content = "\n".join(processed_lines)

    return content


# ----- Inline Text Processing Functions -----
def text_to_children(text):
    # Start with a single text node containing all the text
    nodes = [TextNode(text, "text")]
    
    # Split by each inline delimiter and convert to appropriate TextNode types
    # For example, bold markdown
    nodes = split_nodes_delimiter(nodes, "**", "bold")
    
    # For italic markdown
    nodes = split_nodes_delimiter(nodes, "_", "italic")
    
    # For code markdown
    nodes = split_nodes_delimiter(nodes, "`", "code")
    
    # Convert each TextNode to an HTMLNode
    html_nodes = []
    for node in nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)
    
    return html_nodes

# ----- Main Conversion Function -----

def markdown_to_html_node(markdown):
    # Extract the blocks from the markdown
    blocks = markdown_to_blocks(markdown)
    
    parent = HTMLNode("div", None, None, [])
    # Loop through each block to create HTML nodes
    for block in blocks:
        # Establishing what type of block each blocks are
        block_type = block_to_block_type(block)

        # Create appropriate HTML node based on block_type
        # For example:
        if block_type == "paragraph":
            block_node = create_paragraph_node(block)
            
        if block_type == "code":
            # For a code block
            block_node = create_code_block(block)
        
        # Add the block node to the parent
        parent.children.append(block_node)
    
    return parent