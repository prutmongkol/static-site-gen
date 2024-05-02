import re

from htmlnode import HTMLNode, LeafNode, ParentNode

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        cleaned_blocks.append(block)    
    return cleaned_blocks


def block_to_block_type(markdown: str) -> str:
    if re.match(r"^#{1,6}\s.", markdown):
        return block_type_heading
    elif re.match(r"^`{3}[\s\S]+`{3}$", markdown, flags=re.MULTILINE):
        return block_type_code
    elif re.match(r"^>[^\n]*(?:\n>[^\n]*)*$", markdown):
        return block_type_quote
    elif re.match(r"^(?:\s*[-\*\+]\s+.+(\n|$))+", markdown):
        return block_type_unordered_list
    elif re.match(r"^1.[ \t]", markdown):
        ordered_list = markdown.split("\n")
        for i in range(len(ordered_list)):
            regex = f"^{i + 1}.[ \\t]"
            if not re.match(regex, ordered_list[i]):
                return block_type_paragraph
        return block_type_ordered_list
    else:
        return block_type_paragraph


def paragraph_block_to_html_node(markdown: str) -> LeafNode:
    return LeafNode("p", markdown)


def heading_block_to_html_node(markdown: str) -> LeafNode:
    heading_text_tup = re.findall(r"^(#{1,6})\s(.*)", markdown)
    tag = f"h{len(heading_text_tup[0][0])}"
    value = heading_text_tup[0][1]
    return LeafNode(tag, value)


def code_block_to_html_node(markdown: str) -> ParentNode:
    code_list = re.findall(r"^`{3}([\s\S]+)`{3}$", markdown)
    value = code_list[0].strip()
    return ParentNode("pre", [LeafNode("code", value)])


def quote_block_to_html_node(markdown: str) -> LeafNode:
    quote_list = markdown.splitlines()
    value = ""
    for quote in quote_list:
        value += re.findall(r"^>[\s]*(.*)", quote)[0]
        value += "<br/>"
    value = value[:-5]
    return LeafNode("blockquote", value)


def unordered_list_block_to_html_node(markdown: str) -> ParentNode:
    list_items = markdown.splitlines()
    children = []
    for item in list_items:
        children.append(LeafNode("li", item[2:]))
    return ParentNode("ul", children)