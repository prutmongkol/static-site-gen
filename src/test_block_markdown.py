import unittest

from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
)


class TestBlockMarkdown(unittest.TestCase):
    def test_block_markdown(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item
"""
        self.assertEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is a list item\n* This is another list item",
            ],
            markdown_to_blocks(text)
        )
        
    def test_block_markdown_empty(self):
        text = ""
        self.assertEqual(
            [],
            markdown_to_blocks(text)
        )
    
    def test_block_markdown_multiple_lines(self):
        text = """Paragraph 1

Paragraph 2, line 1
Paragraph 2, line 2

Paragraph 3
"""
        self.assertEqual(
            [
                "Paragraph 1",
                "Paragraph 2, line 1\nParagraph 2, line 2",
                "Paragraph 3"
            ],
            markdown_to_blocks(text)
        )

    def test_block_type_heading1(self):
        text = "# Heading"
        self.assertEqual(
            block_type_heading,
            block_to_block_type(text)
        )
        
    def test_block_type_heading6(self):
        text = "###### Heading"
        self.assertEqual(
            block_type_heading,
            block_to_block_type(text)
        )
        
    def test_block_type_not_heading1(self):
        text = "#Not Heading"
        self.assertEqual(
            block_type_paragraph,
            block_to_block_type(text)
        )
        
    def test_block_type_not_heading7(self):
        text = "####### Not Heading"
        self.assertEqual(
            block_type_paragraph,
            block_to_block_type(text)
        )

    def test_block_type_code(self):
        text="```\nCode Block\n```"
        self.assertEqual(
            block_type_code,
            block_to_block_type(text)
        )
        
    def test_block_type_code2(self):
        text="```Code Block```"
        self.assertEqual(
            block_type_code,
            block_to_block_type(text)
        )
        
    def test_block_type_not_code(self):
        text="``````"
        self.assertEqual(
            block_type_paragraph,
            block_to_block_type(text)
        )
        
    def test_block_type_quote(self):
        text=">This is a quote"
        self.assertEqual(
            block_type_quote,
            block_to_block_type(text)
        )
    
    def test_block_type_quote_multiline(self):
        text=">Quote line 1\n> Quote line 2\n>Quote line 3"
        self.assertEqual(
            block_type_quote,
            block_to_block_type(text)
        )
        
    
