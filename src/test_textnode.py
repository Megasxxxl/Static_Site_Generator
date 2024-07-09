import unittest

from textnode import (TextNode,
                      text_type_bold,
                      text_type_image,
                      text_type_text,
                      text_node_to_html_node
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_bold, "3")
        node2 = TextNode("This is a text node", "bold", "3")
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", "bold", "3")
        node2 = TextNode("This is not a text node", "bold", "3")
        self.assertNotEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("This is a text node", text_type_text, "3")
        node2 = TextNode("This is a text node", text_type_image, "3")
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", "bold", "3")
        node2 = TextNode("This is a text node", "bold", "2")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node) 
        )

    
if __name__ == "__main__":
    unittest.main()
