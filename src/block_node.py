from enum import Enum
import re

class block_type(Enum):
    paragraph = 'paragraph'
    heading = 'heading'
    code = 'code'
    quote = 'quote'
    unordered_list = 'unordered list'
    ordered_list = 'ordered list'

def markdown_to_blocks(text):
    blocks = text.split('\n\n')
    firltered_blocks =[]
    for block in blocks:
        if block == '': continue
        block = block.strip()
        firltered_blocks.append(block)
    return firltered_blocks

def block_to_block_type(block):
    if re.search(r'^#{1,6}', block): return block_type.heading
    elif re.search(r"```.*```$", block, flags=re.DOTALL): return block_type.code
    elif re.search(r'^> ', block, flags=re.MULTILINE): return block_type.quote
    elif len(re.findall(r'^(\*|-) ', block, flags=re.MULTILINE)) == len(block.split('\n')): return block_type.unordered_list
    elif len(re.findall(r'^\d\. ', block, flags=re.MULTILINE)) == len(block.split('\n')):
        expected_digit = 1
        lines = block.split('\n')
        for line in lines:
            if int(line[0]) != expected_digit: 
                break
            expected_digit += 1
            if line == lines[-1]: return block_type.ordered_list
    else: return block_type.paragraph