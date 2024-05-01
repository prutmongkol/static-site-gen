import unittest


from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
            }
        node = HTMLNode(props=props)
        self.assertEqual(
            " href=\"https://www.google.com\" target=\"_blank\"",
            node.props_to_html()
        )
        
    def test_repr(self):
        tag = "p"
        value = "Baked salmon is great"
        children = [HTMLNode(tag="div", value="Yup")]
        props = {
            "class": "main-text"
        }
        node = HTMLNode(tag, value, children, props)
        self.assertEqual(
            f"HTMLNode({tag}, {value}, {children}, {props})",
            repr(node)
        )
    
if __name__ == "__main__":
    unittest.main()