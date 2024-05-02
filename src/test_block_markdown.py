import unittest

from block_markdown import markdown_to_blocks


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
            