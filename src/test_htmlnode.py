import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("1", "1", ["1"], {"1"})
        node2 = HTMLNode("1", "1", ["1"], {"1"})
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com", "target": "_blank"}) 
        self.assertTrue(type(node.props_to_html()) == str)

    def test_props_to_html2(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertNotEqual(node.props, node.props_to_html())
        
    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_parentnode(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"), 
                                LeafNode("i", "italic text"), 
                                LeafNode(None, "Normal text"),
                                ],)
        self.assertTrue(type(node.to_html()) == str)



    def test_parentnode_render(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"), 
                                LeafNode("i", "italic text"), 
                                LeafNode(None, "Normal text"),
                                ],)
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parentnode_no_tag(self):
        node = ParentNode(None, [LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"), 
                                LeafNode("i", "italic text"), 
                                LeafNode(None, "Normal text"),
                                ],)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parentnode_no_children(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parentnode_children_no_value(self):
        node = ParentNode(None, [LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"), 
                                LeafNode("i", None), 
                                LeafNode(None, "Normal text"),
                                ],)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parentnode_nesting(self):       
        node = ParentNode("p", [LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"), 
                                LeafNode("i", "italic text"), 
                                LeafNode(None, "Normal text"),
                                ], {"href": "https://www.google.com"})
        node3 = ParentNode("a", [LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"), 
                                LeafNode("i", "italic text"), 
                                LeafNode(None, "Normal text"),
                                ], {"href": "https://www.google.com"})  
        node4 = ParentNode("t", [LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"), 
                                LeafNode("i", "italic text"), 
                                LeafNode(None, "Normal text"),
                                ], {"href": "https://www.google.com"})
        
        node2 = ParentNode("y", [node, node3, node4], {"href": "https://www.google.com"})
        self.assertEqual(node2.to_html(), "<y><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><a><b>Bold text</b>Normal text<i>italic text</i>Normal text</a><t><b>Bold text</b>Normal text<i>italic text</i>Normal text</t></y>")
        
    def test_parentnode_nesting2(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"), 
                                LeafNode("i", "italic text"), 
                                LeafNode(None, "Normal text"),
                                ], {"href": "https://www.google.com"})
        
        node2 = ParentNode("a", [node], {"href": "https://www.google.com"})

        node3 = ParentNode("c", [node2], {"href": "https://www.google.com"})
        self.assertEqual(node3.to_html(), "<c><a><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></a></c>")

if __name__ == "__main__":
    unittest.main()
