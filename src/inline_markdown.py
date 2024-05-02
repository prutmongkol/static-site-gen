from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
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
