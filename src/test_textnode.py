import unittest

from textnode import *


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
class TestExtractionFunctions(unittest.TestCase):
    def test_link_extratction(self):
        sample = "this is an image in markdown [image](www.example.com) here"
        image = extratct_markdown_links(sample)
        comparison = [("image", "www.example.com")]
        self.assertEqual(image, comparison)
    def test_image_extraction(self):
        sample = "this is one picture ![image1](www.example.com/x.png) and this is a second one ![image2](www.example.com/y.png)"
        image = extract_markdown_image(sample)
        comparison = [('image1', 'www.example.com/x.png'), ('image2', 'www.example.com/y.png')]
        self.assertEqual(image, comparison)
class TestImageAndLinkSplitters(unittest.TestCase):
    def test_link_node_splitter(self):
        sample = [
            TextNode("[x](sample.com) at the start of the string", TextType.normal_text),
            TextNode("no url inside", TextType.normal_text),
            TextNode("url [x](sample.com) mid string", TextType.normal_text),
            TextNode("multiple [x](sample.com) urls [x](sample.com) in [x](sample.com) one [x](sample.com) node", TextType.normal_text),
            TextNode("link at end of text [x](sample.com)", TextType.normal_text),
            TextNode("[link by itself](sample.com)", TextType.normal_text)
        ]
        split_nodes = split_nodes_link(sample)
        comparison = [
            TextNode('x', TextType.links, 'sample.com'),
            TextNode(" at the start of the string", TextType.normal_text),
            TextNode("no url inside", TextType.normal_text),
            TextNode("url ", TextType.normal_text),
            TextNode('x', TextType.links, 'sample.com'),
            TextNode(" mid string", TextType.normal_text),
            TextNode("multiple ", TextType.normal_text),            
            TextNode('x', TextType.links, 'sample.com'),
            TextNode(" urls ", TextType.normal_text),
            TextNode('x', TextType.links, 'sample.com'),
            TextNode(" in ", TextType.normal_text),
            TextNode('x', TextType.links, 'sample.com'),
            TextNode(" one ", TextType.normal_text),
            TextNode('x', TextType.links, 'sample.com'),
            TextNode(" node", TextType.normal_text),
            TextNode("link at end of text ", TextType.normal_text),
            TextNode('x', TextType.links, 'sample.com'),
            TextNode("link by itself", TextType.links, "sample.com")
        ]
        self.assertListEqual(split_nodes, comparison)
    def test_image_node_splitter(self):
        sample = [
            TextNode("![1](sample.com) at the start of the string", TextType.normal_text),
            TextNode("no url inside", TextType.normal_text),
            TextNode("url ![2](sample.com) mid string", TextType.normal_text),
            TextNode("multiple ![3](sample.com) urls ![4](sample.com) in ![5](sample.com) one ![6](sample.com) node", TextType.normal_text),
            TextNode("link at end of text ![7](sample.com)", TextType.normal_text)
        ]
        split_nodes = split_nodes_image(sample)
        comparison = [
            TextNode('1', TextType.images, 'sample.com'),
            TextNode(" at the start of the string", TextType.normal_text),
            TextNode("no url inside", TextType.normal_text),
            TextNode("url ", TextType.normal_text),
            TextNode('2', TextType.images, 'sample.com'),
            TextNode(" mid string", TextType.normal_text),
            TextNode("multiple ", TextType.normal_text),            
            TextNode('3', TextType.images, 'sample.com'),
            TextNode(" urls ", TextType.normal_text),
            TextNode('4', TextType.images, 'sample.com'),
            TextNode(" in ", TextType.normal_text),
            TextNode('5', TextType.images, 'sample.com'),
            TextNode(" one ", TextType.normal_text),
            TextNode('6', TextType.images, 'sample.com'),
            TextNode(" node", TextType.normal_text),
            TextNode("link at end of text ", TextType.normal_text),
            TextNode('7', TextType.images, 'sample.com')
        ]
        self.assertListEqual(split_nodes, comparison)

class TestTextToTextNodes(unittest.TestCase):
    def test_large_block_multiple_types(self):
        text_sample = (
            "This is a sample of markdown text with multiple types " 
            "**here it is bold** and here is *italic* is **bold** again "
            "this is `code block` [a link](example.com) and "
            "![a image](sample.com/png) some more `code` for good measure"
        )
        test_nodes = text_to_text_node(text_sample)
        comparison = [
            TextNode("This is a sample of markdown text with multiple types ", TextType.normal_text),
            TextNode("here it is bold", TextType.bold_text),
            TextNode(" and here is ", TextType.normal_text),
            TextNode("italic", TextType.italic_text),
            TextNode(' is ', TextType.normal_text), 
            TextNode('bold', TextType.bold_text),
            TextNode(' again this is ', TextType.normal_text),
            TextNode('code block', TextType.code_text),
            TextNode(' ', TextType.normal_text),
            TextNode('a link', TextType.links, 'example.com'),
            TextNode(' and ', TextType.normal_text),
            TextNode('a image', TextType.images, 'sample.com/png'),
            TextNode(' some more ', TextType.normal_text),
            TextNode('code', TextType.code_text),
            TextNode(' for good measure', TextType.normal_text)
        ]
        self.assertListEqual(test_nodes, comparison)




if __name__ == "__main__":
    unittest.main()