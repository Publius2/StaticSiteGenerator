import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.bold_text)
        node2 = TextNode("This is a text node", TextType.bold_text)
        self.assertEqual(node, node2)
    
    def test_eq_url(self):
        node = TextNode('this is a node with a url', TextType.links, 'https://test.io')
        node2 = TextNode('this is a node with a url', TextType.links, 'https://test.io')
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode('this is a bold node', TextType.bold_text)
        node2 = TextNode('this is a norma node', TextType.normal_text)
        self.assertNotEqual(node, node2)
class TestText2HTML(unittest.TestCase):
    def test_invalid_type(self):
        with self.assertRaises(Exception):
            text_node_to_html_node(TextNode('this is text', 'not real text type'))
    
    def test_normal_text(self):
        testNode = TextNode('normal text', TextType.normal_text)
        self.assertEqual(str(text_node_to_html_node(testNode)), 'HTMLNode(None, normal text, None, None)')
    
    def test_link(self):
        testNode = TextNode('example', TextType.links, 'www.example.com')
        self.assertEqual(str(text_node_to_html_node(testNode)), "HTMLNode(a, example, None, {'href': 'www.example.com'})")
    
    def test_img(self):
        testNode = TextNode('example', TextType.images, 'www.image.com')
        self.assertEqual(str(text_node_to_html_node(testNode)), "HTMLNode(img, , None, {'src': 'www.image.com', 'alt': 'example'})")

if __name__ == "__main__":
    unittest.main()