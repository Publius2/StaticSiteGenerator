from enum import Enum
import re
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

def split_nodes_delimeter(old_nodes, delimeter, text_type):
    new_nodes = []
    for node in old_nodes:
        text_in_node_split = node.text.split(delimeter)
        for i in range(len(text_in_node_split)):
            if text_in_node_split[i] == '': continue
            if i%2 == 0: new_nodes.append(TextNode(text_in_node_split[i], node.text_type))
            else: new_nodes.append(TextNode(text_in_node_split[i], text_type))
    return new_nodes

def extratct_markdown_links(text):
    return re.findall(r'(?<!!)\[(.*?)\]\((.*?)\)', text)  
    

def extract_markdown_image(text):
    return re.findall(r'!\[(.*?)\]\((.*?)\)', text)

def split_nodes_link(old_nodes):      
    new_nodes = []
    for node in old_nodes:
        links = extratct_markdown_links(node.text)
        new_nodes += split_node_image_and_link_helper(node, links)
    return new_nodes
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_image(node.text)
        new_nodes += split_node_image_and_link_helper(node, links, image=True)
    return new_nodes

def split_node_image_and_link_helper(node, links, image=False):
    text_type = TextType.images if image else TextType.links
    # doesn't make a node if their is no text
    if node.text == '': return []
    # if there are no links just return node
    if len(links) == 0: return [node]
    else:
    #split by first incident of first link in links
        alt_text = links[0][0]
        url = links[0][1]
        node_text_split = node.text.split(f'{"!" if image else ""}[{alt_text}]({url})', 1)
    #if there is text before the link create a text node add it to list followed by link node otherwise just create + add link node 
        if node_text_split[0] != '': result = [TextNode(node_text_split[0], node.text_type), TextNode(alt_text, text_type, url)]
        else: result = [TextNode(alt_text, text_type, url)]
    #recurese wtih a node made from remaining text and remaining links
        result += split_node_image_and_link_helper(TextNode(node_text_split[1], node.text_type), links[1:], image)
        return result

def text_to_text_node(text):
    old_nodes = [TextNode(text, TextType.normal_text)]
    split_by_bold = split_nodes_delimeter(old_nodes, '**', TextType.bold_text)
    split_by_italic = split_nodes_delimeter(split_by_bold, '*', TextType.italic_text)
    split_by_code = split_nodes_delimeter(split_by_italic, '`', TextType.code_text)
    split_by_image = split_nodes_image(split_by_code)
    split_by_link = split_nodes_link(split_by_image)
    return split_by_link

def markdown_to_blocks(text):
    lines = text.split('\n')
    blocks = []
    block = ''
    for line in lines:
        if line == '' and block != '':
            blocks.append(block)
            blocks = ''
        blocks += line.strip() + '\n'
    return blocks