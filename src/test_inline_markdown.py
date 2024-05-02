import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_code,
)
from inline_markdown import split_nodes_delimiter

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