from htmlnode import LeafNode


text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, target) -> bool:
        return (
            self.text == target.text
            and self.text_type == target.text_type
            and self.url == target.url
        )
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode):
    text = text_node.text
    text_type = text_node.text_type
    url = text_node.url
    if text_type == text_type_text:
        return LeafNode(None, text)
    if text_type == text_type_bold:
        return LeafNode("b", text)
    if text_type == text_type_italic:
        return LeafNode("i", text)
    if text_type == text_type_code:
        return LeafNode("code", text)
    if text_type == text_type_link:
        return LeafNode("a", text, { "href": url})
    if text_type == text_type_image:
        return LeafNode("tag", "", { "src": url, "alt": text })
    raise ValueError(f"Invalid text type: {text_type}")
