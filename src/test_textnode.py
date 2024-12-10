import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()