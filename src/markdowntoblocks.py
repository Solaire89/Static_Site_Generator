def markdown_to_blocks(markdown):
    # First normalize line endings by stripping the whitespace
    normalized_md = markdown.strip()
    
    # Split by two or more newlines (which creates a blank line)
    # This may be more reliable than just splitting by \n\n
    import re # Importing regular expression
    # Using regular expression to split the markdowns by 2 \n or more
    blocks = re.split(r'\n{2,}', normalized_md) 
    
    result = [] # Creating a new list
    for block in blocks: # Iterating over the list blocks
        if block.strip():  # Skip empty blocks
            # Process each line in the block
            lines = block.split('\n') # Splitting each line by \n
            clean_lines = [line.strip() for line in lines]
            clean_block = '\n'.join(clean_lines)
            result.append(clean_block)
    
    return result