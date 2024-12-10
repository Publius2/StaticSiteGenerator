import unittest
from htmlnode import HTMLNode

class TestHTMLnode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com" target="_blank"')
    
    def test_empty_node(self):
        node = HTMLNode()
        self.assertEqual(str(node), 'HTMLNode(None, None, None, None, None)')

    def test_empty_function(self):
        with self.assertRaises(NotImplementedError):
            HTMLNode().to_html()
