import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLnode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com" target="_blank"')
    
    def test_empty_node(self):
        node = HTMLNode()
        self.assertEqual(str(node), 'HTMLNode(None, None, None, None)')

    def test_empty_function(self):
        with self.assertRaises(NotImplementedError):
            HTMLNode().to_html()

class TestLeafnode(unittest.TestCase):
    def test_no_value_error(self):
        with self.assertRaises(ValueError):
            LeafNode('test', None).to_html()
    def test_to_html_no_tag(self):
        self.assertEqual(LeafNode(None, 'test input').to_html(), 'test input')
    def test_to_html_no_prop(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), '<p>This is a paragraph of text.</p>')
    def test_to_html_with_prop(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

class TestParentnode(unittest.TestCase):
    def test_no_child_error(self):
        with self.assertRaises(ValueError):
            ParentNode('p', None).to_html()
    def test_no_tag_error(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode(None, 'this is a test')]).to_html()
    def test_parent_with_prop(self):
        child_list = [
            LeafNode("b", "Bold text")
        ]
        node = ParentNode('a', child_list, {'href': 'https://www.example.com'})
        self.assertEqual(node.to_html(), '<a href="https://www.example.com"><b>Bold text</b></a>')
    def test_to_html_all_leaves(self):
        child_list = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text")
        ]
        node = ParentNode('p', child_list)
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')
    def test_to_html_with_sub_parents(self):
        child_list = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text")
        ]
        sub_parent1 = ParentNode('body', child_list)

        super_parent = ParentNode('html', [LeafNode('h1', 'This is a header'), sub_parent1])

        self.assertEqual(super_parent.to_html(), '<html><h1>This is a header</h1><body><b>Bold text</b>Normal text<i>italic text</i>Normal text</body></html>')
