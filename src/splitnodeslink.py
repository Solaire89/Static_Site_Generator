import re
from textnode import TextType, TextNode
from extractmarkdown import extract_markdown_links

# Extracting the following: [to boot dev](https://www.boot.dev)
def split_nodes_link(old_nodes):
    new_nodes = [] # Making an empty list
    for old_node in old_nodes: # Iterating through the old_nodes list
        # Skip non-TEXT nodes
        if old_node.text_type != TextType.TEXT: # Checking if the text_type (from the enum list) doesn't equal TEXT
            new_nodes.append(old_node) # Adding the node to the list of new_nodes, since we don't have to separate the nodes.
            continue # Continuing on to the rest of the code

        text = old_node.text # Assigning the content of the text in the node to the variable text
        # Find all links in the text
        links = extract_markdown_links(text) # Using the function we created to extract the text and link as a tuple
        
        # If no links found, keep the original node
        if not links: # Checking if there are no links
            new_nodes.append(old_node) # Adding the old_node to the new_nodes list, as there are no links to add
            continue
        
        # Process the text, splitting around links
        remaining_text = text 
        
        for link_text, link_url in links:
            # Find where the full markdown link appears in the remaining text
            markdown_link = f"[{link_text}]({link_url})"
            parts = remaining_text.split(markdown_link, 1)
            
            # Add a node for the text before the link (if it's not empty)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            # Add a node for the link itself
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            
            # Update the remaining text to be the part after the link
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
        
        # Add any remaining text after the last link (if it's not empty)
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes