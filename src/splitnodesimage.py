import re
from textnode import TextType, TextNode
from extractmarkdown import extract_markdown_images

# Extracting the following: ![alt text](link)
def split_nodes_image(old_nodes):
    new_nodes = [] # Making an empty list
    for old_node in old_nodes: # Iterating through the old_nodes list
        # Skip non-TEXT nodes
        if old_node.text_type != TextType.TEXT: # Checking if the text_type (from the enum list) doesn't equal TEXT
            new_nodes.append(old_node) # Adding the node to the list of new_nodes, since we don't have to separate the nodes.
            continue # Continuing on to the rest of the code

        text = old_node.text # Assigning the content of the text in the node to the variable text
        # Find all images in the text
        images = extract_markdown_images(text) # Using the function we created to extract the image_alt and image_url as a tuple
        
        # If no links found, keep the original node
        if not images: # Checking if there are no images
            new_nodes.append(old_node) # Adding the old_node to the new_nodes list, as there are no images to add
            continue
        
        # Process the text, splitting around images
        remaining_text = text 
        
        for image_alt, image_url in images:
            # Find where the full markdown image appears in the remaining text
            markdown_link = f"![{image_alt}]({image_url})"
            parts = remaining_text.split(markdown_link, 1)
            
            # Add a node for the text before the image (if it's not empty)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            # Add a node for the image itself
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            
            # Update the remaining text to be the part after the image
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
        
        # Add any remaining text after the last image (if it's not empty)
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes