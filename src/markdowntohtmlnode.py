import re
from markdowntoblocks import markdown_to_blocks
from blocktoblocktype import block_to_block_type, BlockType
from textnode import TextNode, TextType, text_node_to_html_node
from splitnodesdelimiter import split_nodes_delimiter
from leafnode import LeafNode
from parentnode import ParentNode



# ----- Block Identification Functions -----

# ----- Block Processing Functions -----
def create_paragraph_node(block):

    # Replace newlines with spaces for paragraph text
    text = block.replace("\n", " ").strip()
    
    # Create children nodes from the text (with inline markdown parsing)
    children = text_to_children(text)
    
    # Create the paragraph node
    return ParentNode("p", children)
        

def create_heading_block(block):

    # Counting the number of #'s in the header
    match = re.match(r"^([#]+)", block)
    header_markers = len(match.group(1))

    # Splitting the header markers from the content
    text_content = block.lstrip('#').lstrip() # Discard markers and focus on content
    children = text_to_children(text_content)
    # Creating the node
    block_node = ParentNode(f"h{header_markers}", children)
    return block_node

# Not for inline processing
def create_code_block(block):
    ## Remove the triple backticks and get the content
    lines = block.split("\n")
    
    # Skip the first and last line (which contain the ```) 
    content_lines = lines[1:-1]
    
    # Join with newlines and ensure a trailing newline
    content = "\n".join(content_lines)

    # Ensure content ends with exactly one newline
    if not content.endswith("\n"):
        content += "\n"
    elif content.endswith("\n\n"):  # Avoid double newlines
        content = content[:-1]

    # Create a child TextNode from the raw content (no inline parsing)
    child_node = TextNode(content, TextType.TEXT)
    html_node = text_node_to_html_node(child_node)

    # Return an HTMLNode for `<pre><code>` with the TextNode as its child
    code_node = ParentNode("code", [html_node])  # <code> node contains the TextNode
    pre_node = ParentNode("pre", [code_node])    # <pre> node contains the <code>
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

        children = text_to_children(content)
        li_node = ParentNode("li", children)
        li_nodes.append(li_node)

    # We're taking care of the logic of whether a list is ordered or 
    # unordered in the main markdown_to_HTML_node function.
    parent_tag = "ol" if ordered else "ul"
    list_node = ParentNode(parent_tag, children=li_nodes)
    return list_node

def create_quote_block(block):

    processed_lines = []
    # Iterating over the lines in the block
    for line in block.split("\n"): # Splitting the lines by the \n character
        if line.startswith(">"):
            # Remove ">" and strip whitespace
            processed_line = line[1:].strip()
        else:
            processed_line = line
        processed_lines.append(processed_line)
        
    content = "\n".join(processed_lines)

    # Process inline markdown
    children = text_to_children(content)
    
    # Create the blockquote node
    return ParentNode("blockquote", children)


# ----- Inline Text Processing Functions -----
def text_to_children(text):
    # Start with a single text node containing all the text
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Split by each inline delimiter and convert to appropriate TextNode types
    # For example, bold markdown
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
    # For italic markdown
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    
    # For code markdown
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    
    # Convert each TextNode to an HTMLNode
    html_nodes = []
    for node in nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)
    
    return html_nodes

# ----- Main Conversion Function -----

def markdown_to_html_node(markdown):

    parent_node = ParentNode("div", [])
    # Extract the blocks from the markdown
    blocks = markdown_to_blocks(markdown)
    # Loop through each block to create HTML nodes
    for block in blocks:
        # Establishing what type of block each blocks are
        block_type = block_to_block_type(block)
        

        # Create appropriate HTML node based on block_type
        # For example:
        if block_type == BlockType.PARAGRAPH:
            block_node = create_paragraph_node(block)
            parent_node.children.append(block_node)
        elif block_type == BlockType.CODE:
            block_node = create_code_block(block)
            parent_node.children.append(block_node)
        elif block_type == BlockType.QUOTE:
            block_node = create_quote_block(block)
            parent_node.children.append(block_node)
        elif block_type == BlockType.UNORDERED_LIST:
            list_node = create_list_block(block, ordered=False)
            parent_node.children.append(list_node)
        elif block_type == BlockType.ORDERED_LIST:
            list_node = create_list_block(block, ordered=True)
            parent_node.children.append(list_node)
        elif block_type == BlockType.HEADING:
            block_node = create_heading_block(block)
            parent_node.children.append(block_node)
    return parent_node