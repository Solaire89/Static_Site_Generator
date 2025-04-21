from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        # Skip non-TEXT nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Get the text content
        text = old_node.text
        
        # Find first delimiter
        start_index = text.find(delimiter)
        if start_index == -1:
            # No delimiter found, keep node as is
            new_nodes.append(old_node)
            continue
            
        # Find matching closing delimiter
        end_index = text.find(delimiter, start_index + len(delimiter))
        if end_index == -1:
            # No closing delimiter, handle error
            raise Exception(f"No closing delimiter '{delimiter}' found")
        
        # Extract the three parts
        before_text = text[:start_index]
        delimited_text = text[start_index + len(delimiter):end_index]
        after_text = text[end_index + len(delimiter):]
        
        # Create nodes for each part
        if before_text:
            new_nodes.append(TextNode(before_text, TextType.TEXT))
        
        # Create the delimited node with the specified text_type
        new_nodes.append(TextNode(delimited_text, text_type))
        
        # Process any remaining text as a new node with TEXT type
        if after_text:
            # This might contain more delimiters!
            # We should process it further with the original delimiter and text_type
            remaining_nodes = split_nodes_delimiter([TextNode(after_text, TextType.TEXT)], delimiter, text_type)
            new_nodes.extend(remaining_nodes)
        
    return new_nodes