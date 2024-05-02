import unittest

from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
    paragraph_block_to_html_node,
    heading_block_to_html_node,
    code_block_to_html_node,
    quote_block_to_html_node,
    unordered_list_block_to_html_node,
)

from htmlnode import LeafNode, ParentNode


class TestMarkdownBlocks(unittest.TestCase):
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
        
    def test_block_type_unordered_list(self):
        text="- Apple\n* Banana\n+ Orange"
        self.assertEqual(
            block_type_unordered_list,
            block_to_block_type(text)
        )
        
    def test_block_type_unordered_list_one_line(self):
        text="- Apple"
        self.assertEqual(
            block_type_unordered_list,
            block_to_block_type(text)
        )

    def test_block_type_ordered_list(self):
        text = "1. Wake up at 7\n2.\tBrush my teeth\n3. Bake salmon"
        self.assertEqual(
            block_type_ordered_list,
            block_to_block_type(text)
        )
        
    def test_block_type_ordered_list_one_line(self):
        text = "1. Bake salmon"
        self.assertEqual(
            block_type_ordered_list,
            block_to_block_type(text)
        )
    
    def test_block_type_not_ordered_list(self):
        text = "1. This list\n4. Is a bit sus"
        self.assertEqual(
            block_type_paragraph,
            block_to_block_type(text)
        )

class TestBlockToHTMLNode(unittest.TestCase):
    def test_paragraph(self):
        markdown = "This is a paragraph"
        self.assertEqual(
            f"{LeafNode("p", "This is a paragraph")}",
            f"{paragraph_block_to_html_node(markdown)}"
        )
        
    def test_heading(self):
        markdown = "# Heading"
        self.assertEqual(
            f"{LeafNode("h1", "Heading")}",
            f"{heading_block_to_html_node(markdown)}"
        )
        
    def test_code(self):
        markdown = "```\nCode Block\n```"
        self.assertEqual(
            f"{ParentNode("pre", [LeafNode("code", "Code Block")])}",
            f"{code_block_to_html_node(markdown)}"
        )
        
    def test_quote(self):
        markdown = "> Sublime message"
        self.assertEqual(
            f"{LeafNode("blockquote", "Sublime message")}",
            f"{quote_block_to_html_node(markdown)}"
        )
        
    def test_quote_multiline(self):
        markdown = "> Wow\n> Such salmon"
        self.assertEqual(
            f"{LeafNode("blockquote", "Wow<br/>Such salmon")}",
            f"{quote_block_to_html_node(markdown)}"
        )

    def test_unordered_list(self):
        markdown = "- apple\n- orange"
        self.assertEqual(
            f"{ParentNode(
                "ul", 
                [
                    LeafNode("li", "apple"),
                    LeafNode("li", "orange"),
                ]
            )}",
            f"{unordered_list_block_to_html_node(markdown)}"
        )