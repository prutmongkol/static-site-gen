import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

class TestInLineMarkDown(unittest.TestCase):
    def test_delimited(self):
        node = TextNode(
            "This is text with a `code block` word", text_type_text)
        self.assertEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            split_nodes_delimiter([node], "`", text_type_code)
        )

    def test_delimited_wrong_delimiter(self):
        node = TextNode(
            "This is text with a `code block` word", text_type_text)
        self.assertEqual(
            [
                TextNode(
                    "This is text with a `code block` word", text_type_text)
            ],
            split_nodes_delimiter([node], "*", text_type_code)
        )

    def test_delimited_bold(self):
        node = TextNode("This is text with a **bold** word", text_type_text)
        self.assertEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            split_nodes_delimiter([node], "**", text_type_bold)
        )
    
    def test_delimited_many(self):
        node = TextNode("This text has **many**, many **bold text**", text_type_text)
        self.assertEqual(
            [
                TextNode("This text has ", text_type_text),
                TextNode("many", text_type_bold),
                TextNode(", many ", text_type_text),
                TextNode("bold text", text_type_bold)
            ],
            split_nodes_delimiter([node], "**", text_type_bold)
        )

    def test_delimited_delimiter_start(self):
        node = TextNode(
            "`code block` this text is", text_type_text)
        self.assertEqual(
            [
                TextNode("code block", text_type_code),
                TextNode(" this text is", text_type_text),
            ],
            split_nodes_delimiter([node], "`", text_type_code)
        )
    
    def test_delimited_delimiter_end(self):
        node = TextNode(
            "This text ends with `code block`", text_type_text)
        self.assertEqual(
            [
                TextNode("This text ends with ", text_type_text),
                TextNode("code block", text_type_code),
            ],
            split_nodes_delimiter([node], "`", text_type_code)
        )
        
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        self.assertEqual(
            [
                ("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), 
                ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")
            ],
            extract_markdown_images(text)
        )
    
    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(
            [
                ("link", "https://www.example.com"), 
                ("another", "https://www.example.com/another")
            ],
            extract_markdown_links(text)
        )
    
    def test_split_node_one_image(self):
        node = TextNode(
            "This text has an ![image](https://placehold.co/600x400)",
            text_type_text,
        )
        self.assertEqual(
            [
                TextNode("This text has an ", text_type_text),
                TextNode("image", text_type_image, "https://placehold.co/600x400"),
            ],
            split_nodes_image([node])
        )
        
    def test_split_node_many_images(self):
        node = TextNode(
            "This text has this ![image](https://placehold.co/600x400) and ![another](https://placehold.co/300x300)",
            text_type_text,
        )
        self.assertEqual(
            [
                TextNode("This text has this ", text_type_text),
                TextNode("image", text_type_image, "https://placehold.co/600x400"),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_image, "https://placehold.co/300x300"),
            ],
            split_nodes_image([node])
        )
    
    def test_split_node_only_image(self):
        node = TextNode("image", text_type_image, "https://placehold.co/600x400")
        self.assertEqual(
            [TextNode("image", text_type_image, "https://placehold.co/600x400")],
            split_nodes_image([node])
        )
        
    def test_split_node_image_inbetween(self):
        node = TextNode("Look at ![this](https://placehold.co/600x400). Isn't it awesome?", text_type_text)
        self.assertEqual(
            [
                TextNode("Look at ", text_type_text),
                TextNode("this", text_type_image, "https://placehold.co/600x400"),
                TextNode(". Isn't it awesome?", text_type_text)
            ],
            split_nodes_image([node])
        )
        
    def test_split_node_one_link(self):
        node = TextNode(
            "This text has a [link](https://placehold.co/600x400)",
            text_type_text,
        )
        self.assertEqual(
            [
                TextNode("This text has a ", text_type_text),
                TextNode("link", text_type_link, "https://placehold.co/600x400"),
            ],
            split_nodes_link([node])
        )
    
    def test_split_node_many_links(self):
        node = TextNode(
            "This text has this [link](https://placehold.co/600x400) and [another](https://placehold.co/300x300)",
            text_type_text,
        )
        self.assertEqual(
            [
                TextNode("This text has this ", text_type_text),
                TextNode("link", text_type_link, "https://placehold.co/600x400"),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_link, "https://placehold.co/300x300"),
            ],
            split_nodes_link([node])
        )
    
    def test_split_node_only_link(self):
        node = TextNode("link", text_type_link, "https://placehold.co/600x400")
        self.assertEqual(
            [TextNode("link", text_type_link, "https://placehold.co/600x400")],
            split_nodes_link([node])
        )
    
    def test_split_node_link_inbetween(self):
        node = TextNode("Look at [this](https://placehold.co/600x400). Isn't it awesome?", text_type_text)
        self.assertEqual(
            [
                TextNode("Look at ", text_type_text),
                TextNode("this", text_type_link, "https://placehold.co/600x400"),
                TextNode(". Isn't it awesome?", text_type_text)
            ],
            split_nodes_link([node])
        )
    
    def test_text_to_textnode(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        self.assertEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
            text_to_textnodes(text)
        )
    
    def test_text_to_textnode_only_text(self):
        text = "Baked salmon is great"
        self.assertEqual(
            [TextNode("Baked salmon is great", text_type_text)],
            text_to_textnodes(text)
        )
        
    def test_text_to_textnode_only_markdown(self):
        text = "*Baked salmon is great*"
        self.assertEqual(
            [TextNode("Baked salmon is great", text_type_italic)],
            text_to_textnodes(text)
        )
    
    def test_text_to_textnode_markdown_start(self):
        text = "*Baked* salmon is great"
        self.assertEqual(
            [
                TextNode("Baked", text_type_italic),
                TextNode(" salmon is great", text_type_text)
            ],
            text_to_textnodes(text)
        )
    
    def test_text_to_textnode_markdown_middle(self):
        text = "Baked *salmon* is great"
        self.assertEqual(
            [
                TextNode("Baked ", text_type_text),
                TextNode("salmon", text_type_italic),
                TextNode(" is great", text_type_text)
            ],
            text_to_textnodes(text)
        )
    
    def test_text_to_textnode_markdown_end(self):
        text = "Baked salmon is *great*"
        self.assertEqual(
            [
                TextNode("Baked salmon is ", text_type_text),
                TextNode("great", text_type_italic)
            ],
            text_to_textnodes(text)
        )
    