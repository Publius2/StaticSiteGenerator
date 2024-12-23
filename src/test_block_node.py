import unittest
from block_node import *

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

class TestBlockTypeDetector(unittest.TestCase):
    def test_good_example_of_all_types(self):
        test_blocks = [
            '# H1',
            '## H2',
            '### H3',
            '#### H4',
            '##### H5',
            '###### H6',
            '```code```',
            '> quote',
            '* list with (*)',
            '- list with (-)',
            '1. ordered list',
            'I am a paragraph'
        ]
        test = list(map(block_to_block_type, test_blocks))
        comparison = [
            block_type.heading,
            block_type.heading,
            block_type.heading,
            block_type.heading,
            block_type.heading,
            block_type.heading,
            block_type.code,
            block_type.quote,
            block_type.unordered_list,
            block_type.unordered_list,
            block_type.ordered_list,
            block_type.paragraph
        ]
        self.assertListEqual(test, comparison)
    def test_bad_ordered_list_blocks(self):
        test = [
            """1. first
            2. second
            3. third
            5. fourth
            4. fifth""",
            """1. first
            2. second
            third""",
            """2. second
            3. third"""
        ]
        test_cases = list(map(block_to_block_type, test))
        comparison = [block_type.paragraph, block_type.paragraph, block_type.paragraph]
        self.assertListEqual(test_cases, comparison)
if __name__ == 'main':
    unittest.main()