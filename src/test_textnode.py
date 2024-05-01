import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
        
    def test_eq2(self):
        node = TextNode("This is a text node", "bold", "https://example.com")
        node2 = TextNode("This is a text node", "bold", "https://example.com")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)
        
    def test_not_eq2(self):
        node = TextNode("This is TextA", "bold")
        node2 = TextNode("This is TextB", "bold")
        self.assertNotEqual(node, node2)
    
    def test_not_eq3(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold", "https://example.com")
        self.assertNotEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("This is a text node", "bold", "https://prutmongkol.dev")
        self.assertEqual(
            "TextNode(This is a text node, bold, https://prutmongkol.dev)",
            repr(node)
        )

if __name__ == "__main__":
    unittest.main()
    