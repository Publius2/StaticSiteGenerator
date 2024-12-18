import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimeter


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

class TestTextNodeSplitter(unittest.TestCase):
    def test_single_node(self):
        testNode = TextNode("This is text with *italics* in it", TextType.normal_text)
        new_nodes = split_nodes_delimeter([testNode], '*', TextType.italic_text)
        comparison_nodes = [
            TextNode("This is text with ", TextType.normal_text),
            TextNode("italics", TextType.italic_text),
            TextNode(" in it", TextType.normal_text)
        ]
        self.assertEqual(new_nodes,comparison_nodes)
    def test_multiple_nodes(self):
        testNodes = [
            TextNode("This text is **BOLD** here", TextType.italic_text),
            TextNode("This text is **BOLD at the end**", TextType.normal_text),
            TextNode("**BOLD** from the start here", TextType.normal_text),
            TextNode("**Bold all the way through here**", TextType.normal_text)
        ]
        new_nodes = split_nodes_delimeter(testNodes, '**', TextType.bold_text)
        comparisonNodes = [
            TextNode("This text is ", TextType.italic_text), 
            TextNode("BOLD", TextType.bold_text),
            TextNode(" here", TextType.italic_text), 
            TextNode("This text is ", TextType.normal_text),
            TextNode("BOLD at the end", TextType.bold_text),
            TextNode("BOLD", TextType.bold_text),
            TextNode(" from the start here", TextType.normal_text),
            TextNode("Bold all the way through here", TextType.bold_text)
        ]
        self.assertEqual(new_nodes, comparisonNodes)
    
    def test_multiple_inline_delimeters(self):
        testNodes = [
            TextNode("**Bold** not **Bold** not **Bold** not ", TextType.normal_text)
        ]
        new_nodes = split_nodes_delimeter(testNodes, '**', TextType.bold_text)
        comparisonNodes = [
            TextNode('Bold', TextType.bold_text),
            TextNode(' not ', TextType.normal_text),
            TextNode('Bold', TextType.bold_text),
            TextNode(' not ', TextType.normal_text),
            TextNode('Bold', TextType.bold_text),
            TextNode(' not ', TextType.normal_text)
        ]
        self.assertEqual(new_nodes, comparisonNodes)

if __name__ == "__main__":
    unittest.main()