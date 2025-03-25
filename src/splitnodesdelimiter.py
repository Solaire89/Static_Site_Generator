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
        
        # Now you can create three nodes:
        # 1. Text before the first delimiter
        # 2. Text between delimiters (with the specified text_type)
        # 3. Text after the second delimiter
        
        # Extract the three parts
        before_text = text[:start_index]
        delimited_text = text[start_index + len(delimiter):end_index]
        after_text = text[end_index + len(delimiter):]
        
        # Create nodes for each part
        if before_text:
            new_nodes.append(TextNode(before_text, TextType.TEXT))
        
        new_nodes.append(TextNode(delimited_text, text_type))
        
        if after_text:
            # This might contain more delimiters! 
            # We should process it further
            new_nodes.extend(split_nodes_delimiter([TextNode(after_text, TextType.TEXT)], delimiter, text_type))
        
    return new_nodes