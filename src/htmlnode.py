

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
