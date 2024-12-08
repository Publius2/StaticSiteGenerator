from enum import Enum

class TextType(Enum):
    Normal_text = 'Normal text'
    Bold_text = 'Bold text'
    Italic_text = 'Italic text'
    Code_text = 'Code text'
    Links = 'Links'
    Images = 'Images'

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
        return f"TextNode({self.text}, {self.text_type.value()}, {self.url})"