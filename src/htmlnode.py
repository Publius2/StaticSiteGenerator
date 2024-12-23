from block_node import markdown_to_blocks, block_to_block_type, block_type
from textnode import text_to_text_node, text_node_to_html_node

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        result = []
        for x in self.props:
            result.append(f'{x}="{self.props[x]}"')
        return " ".join(result)
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value == None: raise ValueError("Leaf must have a value")
        if self.tag == None: return self.value
        else: return f"<{self.tag}{' ' + self.props_to_html() if self.props != None else ''}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        if self.tag == None: raise ValueError('Parent must have a tag')
        if self.children == None: raise ValueError('Parent must have children')
        
        result = f"<{self.tag}{' ' + self.props_to_html() if self.props != None else ''}>"
        for child  in self.children:
            result += child.to_html()
        result += f'</{self.tag}>'
        return result 

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    blocks_html_nodes = []
    for block in blocks:
        type = block_to_block_type(block)
        match type:
            case block_type.paragraph: tag = 'p'
            case block_type.heading: tag = 'h1'
            case block_type.code: tag = 'code'
            case block_type.quote: tag = 'blockquote'
            case block_type.unordered_list: tag = 'ul'
            case block_type.ordered_list: tag = 'ol'
            case _: raise ValueError('invalid block type')
        block_text_nodes = text_to_text_node(block)
        block_html_nodes = list(map(text_node_to_html_node, block_text_nodes))
        block_html_nodes.append(ParentNode(tag, block_html_nodes))
    return ParentNode('div', block_html_nodes)