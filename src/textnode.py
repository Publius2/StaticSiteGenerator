from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    normal_text = 'normal'
    bold_text = 'bold'
    italic_text = 'italic'
    code_text = 'code'
    links = 'Links'
    images = 'Images'

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        if (
            self.text == value.text and
            self.text_type == value.text_type and
            self.url == value.url
        ):
            return True
        else: return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    tag = None
    property = None
    match text_node.text_type:
        case TextType.normal_text: tag = None
        case TextType.bold_text: tag = 'b'
        case TextType.italic_text: tag = 'i'
        case TextType.code_text: tag = 'code'
        case TextType.links: 
            tag = 'a'
            property = {'href': text_node.url}
        case TextType.images:
            tag = 'img'
            property = {'src': text_node.url, 'alt': text_node.text}
            return LeafNode(tag, '', props=property)
        case _:
            raise Exception(f'{text_node.text_type} is not a valid text type')
        
    return LeafNode(tag, text_node.text, props=property)
