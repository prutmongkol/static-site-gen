import unittest


from htmlnode import HTMLNode, LeafNode, ParentNode


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
            f"HTMLNode({tag}, {value}, children: {children}, {props})",
            repr(node)
        )
        
    def test_to_html_no_children(self):
        node = LeafNode("p", "Baked salmon is great",  { "class": "main-text" })
        self.assertEqual(
            "<p class=\"main-text\">Baked salmon is great</p>",
            node.to_html()
        )
        
    def test_to_html_no_tag(self):
        node = LeafNode(None, "Baked salmon is great")
        self.assertEqual(
            "Baked salmon is great",
            node.to_html()
        )
        
    def test_to_html_with_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
            node.to_html()
        )
        
    def test_to_html_with_grandchildren(self):
        """ 
        <div class="salmon-list">
            <span>Reasons why baked salmon is great</span>
            <ul class="list">
                <li>High protein</li>
                <li>Easy to make</li>
                <li>A great conversation starter</li>
            </ul>
        </div>
        """
        result = '<div class="salmon-list"><span>Reasons why baked salmon is great</span><ul class="list"><li>High protein</li><li>Easy to make</li><li>A great conversation starter</li></ul></div>'
        node = ParentNode(
            "div",
            [
                LeafNode("span", "Reasons why baked salmon is great"),
                ParentNode(
                    "ul",
                    [
                        LeafNode("li", "High protein"),
                        LeafNode("li", "Easy to make"),
                        LeafNode("li", "A great conversation starter"),
                    ],
                    { "class": "list" }
                ),
            ],
            { "class": "salmon-list" }
        )
        self.assertEqual(result, node.to_html())
        
    def test_to_html_with_one_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            "<div><span>child</span></div>",
            parent_node.to_html()
        )
        
    
if __name__ == "__main__":
    unittest.main()