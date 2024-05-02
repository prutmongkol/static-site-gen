import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold, 
    text_type_italic, 
    text_type_code, 
    text_type_link, 
    text_type_image
)


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        splitted_text_list = old_node.text.split(delimiter)
        if len(splitted_text_list) % 2 == 0:
            raise ValueError("A closing delimiter is missing")
        in_delimiter = True
        for splitted_text in splitted_text_list:
            in_delimiter = not in_delimiter
            if splitted_text == "":
                continue
            if in_delimiter:
                new_nodes.append(TextNode(splitted_text, text_type))
            else:
                new_nodes.append(TextNode(splitted_text, text_type_text))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        splitted_text = []
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for image in images:
            splitted_text = text.split(f"![{image[0]}]({image[1]})", 1)
            if len(splitted_text) != 2:
                raise ValueError("Invalid markdown: image section not closed")
            if splitted_text[0] != "":
                new_nodes.append(TextNode(splitted_text[0], text_type_text))
            new_nodes.append(TextNode(image[0], text_type_image, image[1]))
            text = splitted_text[1]

        if text != "":
            new_nodes.append(TextNode(text, text_type_text))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []
    for old_node in old_nodes:

        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        splitted_text = []
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for link in links:
            splitted_text = text.split(f"[{link[0]}]({link[1]})", 1)
            if len(splitted_text) != 2:
                raise ValueError("Invalid markdown: link section not closed")
            if splitted_text[0] != "":
                new_nodes.append(TextNode(splitted_text[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            text = splitted_text[1]

        if text != "":
            new_nodes.append(TextNode(text, text_type_text))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
