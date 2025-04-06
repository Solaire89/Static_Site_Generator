from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

"""
•	Headings start with 1-6 # characters, followed by a space and then the heading text.
•	Code blocks must start with 3 backticks and end with 3 backticks.
•	Every line in a quote block must start with a > character.
•	Every line in an unordered list block must start with a - character, followed by a space.
•	Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
•	If none of the above conditions are met, the block is a normal paragraph.
"""

def block_to_block_type(block):
    # Check if it's a code block
    if block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    # Check if it's a heading
    elif block.startswith('#'):
        # Count how many # at the start
        heading_level = 0
        for char in block:
            if char == '#':
                heading_level += 1
            else:
                break
        
        # Check if it's a valid heading (1-6 # followed by space)
        if 1 <= heading_level <= 6 and block[heading_level] == ' ':
        # Count how many # at the start and check if followed by space
            return BlockType.HEADING
        
    # Check if it's a quote block
    lines = block.split('\n')
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    # Check if it's an ordered list
    lines = block.split('\n')
    is_ordered_list = True
    for i, line in enumerate(lines):
        expected_prefix = f"{i+1}. "
        if not line.startswith(expected_prefix):
            is_ordered_list = False
            break
        
    # Make sure there's at least one line
    if is_ordered_list and lines:
        return BlockType.ORDERED_LIST
    
    # Check if it's an unordered list
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    
    # If none of the above, it's a paragraph
    return BlockType.PARAGRAPH