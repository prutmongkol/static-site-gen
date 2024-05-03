import re

from htmlnode import ParentNode

from textnode import (
    text_node_to_html_node,
)

from inline_markdown import text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    div_children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        div_children.append(html_node)
    return ParentNode("div", div_children)


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        cleaned_blocks.append(block)    
    return cleaned_blocks


def block_to_html_node(block: str):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_block_to_html_node(block)
    if block_type == block_type_heading:
        return heading_block_to_html_node(block)
    if block_type == block_type_code:
        return code_block_to_html_node(block)
    if block_type == block_type_quote:
        return quote_block_to_html_node(block)
    if block_type == block_type_unordered_list:
        return unordered_list_block_to_html_node(block)
    if block_type == block_type_ordered_list:
        return ordered_list_block_to_html_node(block)
    raise ValueError("Invalid block type")


def block_to_block_type(block: str) -> str:
    if re.match(r"^#{1,6}\s.", block):
        return block_type_heading
    elif re.match(r"^`{3}[\s\S]+`{3}$", block, flags=re.MULTILINE):
        return block_type_code
    elif re.match(r"^>[^\n]*(?:\n>[^\n]*)*$", block):
        return block_type_quote
    elif re.match(r"^(?:\s*[-\*\+]\s+.+(\n|$))+", block):
        return block_type_unordered_list
    elif re.match(r"^1.[ \t]", block):
        ordered_list = block.split("\n")
        for i in range(len(ordered_list)):
            regex = f"^{i + 1}.[ \\t]"
            if not re.match(regex, ordered_list[i]):
                return block_type_paragraph
        return block_type_ordered_list
    else:
        return block_type_paragraph


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_block_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_block_to_html_node(markdown: str) -> ParentNode:
    heading_text_tup = re.findall(r"^(#{1,6})\s(.*)", markdown)
    tag = f"h{len(heading_text_tup[0][0])}"
    text = heading_text_tup[0][1]
    children = text_to_children(text)
    return ParentNode(tag, children)


def code_block_to_html_node(block: str) -> ParentNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    return ParentNode(
        "pre", 
        [
            ParentNode("code", children)
        ]
    )


def quote_block_to_html_node(block: str) -> ParentNode:
    quote_list = block.splitlines()
    text = ""
    for quote in quote_list:
        text += re.findall(r"^>[\s]*(.*)", quote)[0]
        text += "<br/>"
    text = text[:-5]
    children = text_to_children(text)
    return ParentNode("blockquote", children)


def unordered_list_block_to_html_node(block: str) -> ParentNode:
    text_items = block.splitlines()
    list_items = []
    for item in text_items:
        text = item[2:]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ul", list_items)


def ordered_list_block_to_html_node(block: str) -> ParentNode:
    text_items = block.splitlines()
    list_items = []
    for item in text_items:
        text = item[3:]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ol", list_items)
