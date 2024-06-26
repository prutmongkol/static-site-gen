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
    ordered_list_block_to_html_node,
    markdown_to_html_node,
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
        block = "This is a paragraph.\n*Awesome*"
        self.assertEqual(
            f"{ParentNode(
                "p", 
                [
                    LeafNode(None, "This is a paragraph. "),
                    LeafNode("i", "Awesome")
                ]
                )}",
            f"{paragraph_block_to_html_node(block)}"
        )
        
    def test_heading(self):
        block = "# Heading **Banana**"
        self.assertEqual(
            f"{ParentNode(
                "h1", 
                [
                    LeafNode(None, "Heading "),
                    LeafNode("b", "Banana"),
                ]
                )}",
            f"{heading_block_to_html_node(block)}"
        )
        
    def test_code(self):
        block = "```\nCode Block\n```"
        self.assertEqual(
            f"{ParentNode(
                "pre", 
                [
                    ParentNode(
                        "code", 
                        [
                            LeafNode(
                                None, 
                                "Code Block\n"
                            )
                        ]
                    )
                ]
            )}",
            f"{code_block_to_html_node(block)}"
        )
        
    def test_quote(self):
        block = "> Sublime message"
        self.assertEqual(
            f"{ParentNode("blockquote", [LeafNode(None, "Sublime message")])}",
            f"{quote_block_to_html_node(block)}"
        )
        
    def test_quote_multiline(self):
        block = "> Wow\n> Such *salmon*"
        self.assertEqual(
            f"{ParentNode(
                "blockquote",
                [
                    LeafNode(None, "Wow<br/>Such "),
                    LeafNode("i", "salmon")
                ]
            )}",
            f"{quote_block_to_html_node(block)}"
        )

    def test_unordered_list(self):
        block = "- apple\n- *orange*"
        self.assertEqual(
            f"{ParentNode(
                "ul", 
                [
                    ParentNode("li", [LeafNode(None, "apple")]),
                    ParentNode("li", [LeafNode("i", "orange")]),
                ]
            )}",
            f"{unordered_list_block_to_html_node(block)}"
        )
        
    def test_ordered_list(self):
        block = "1. apple\n2. *orange*"
        self.assertEqual(
            f"{ParentNode(
                "ol", 
                [
                    ParentNode("li", [LeafNode(None, "apple")]),
                    ParentNode("li", [LeafNode("i", "orange")]),
                ]
            )}",
            f"{ordered_list_block_to_html_node(block)}"
        )

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraph_html(self):
        markdown = """
This is
a *fragmented* 
paragraph
"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            "<div><p>This is a <i>fragmented</i> paragraph</p></div>",
            html
        )
        
    def test_paragraphs_html(self):
        markdown = """
This is
a *fragmented* 
paragraph

This is **another** paragraph with some `code`
"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            "<div><p>This is a <i>fragmented</i> paragraph</p><p>This is <b>another</b> paragraph with some <code>code</code></p></div>",
            html
        )
        
    def test_headings_html(self):
        markdown = """
# This is H1

This is a paragraph

## This is H2
"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            "<div><h1>This is H1</h1><p>This is a paragraph</p><h2>This is H2</h2></div>",
            html
        )
        
    def test_lists_html(self):
        markdown = """
- apple
- orange
- *banana*

1. Ichi
2. **Ni**
3. San
"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            "<div><ul><li>apple</li><li>orange</li><li><i>banana</i></li></ul><ol><li>Ichi</li><li><b>Ni</b></li><li>San</li></ol></div>",
            html
        )
        
    def test_blockquote_html(self):
        markdown = """
> This is
> a blockquote

Blockquote above
"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            "<div><blockquote>This is<br/>a blockquote</blockquote><p>Blockquote above</p></div>",
            html
        )
        
    def test_codeblock_html(self):
        markdown = """
```
Coding is great.
Back-end is fun.
```
"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            "<div><pre><code>Coding is great.\nBack-end is fun.\n</code></pre></div>",
            html
        )