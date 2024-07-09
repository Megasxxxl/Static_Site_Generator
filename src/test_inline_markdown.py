import unittest

from inline_markdown import (TextNode, 
                      text_type_bold, 
                      text_type_italic, 
                      text_type_code, 
                      text_type_text,
                      text_type_image,
                      text_type_link,
                      split_nodes_delimiter,
                      split_nodes_image,
                      split_nodes_link,
                      extract_markdown_images,
                      extract_markdown_links,
                      text_to_textnodes
)

class TestInLineMarkdown(unittest.TestCase):
    def test_delimiter_code(self):
        node = TextNode("This is a `code` node", text_type_text)
        self.assertEqual(split_nodes_delimiter([node], "`", text_type_code), [TextNode("This is a ", text_type_text, None), TextNode("code", text_type_code, None), TextNode(" node", text_type_text, None)])

    def test_delimiter_italic(self):
        node = TextNode("This is a *italic* node", text_type_text)
        self.assertEqual(split_nodes_delimiter([node], "*", text_type_italic), [TextNode("This is a ", text_type_text, None), TextNode("italic", text_type_italic, None), TextNode(" node", text_type_text, None)])

    def test_delimiter_bold(self):
        node = TextNode("This is a **bold** node", text_type_text)
        self.assertEqual(split_nodes_delimiter([node], "**", text_type_bold), [TextNode("This is a ", text_type_text, None), TextNode("bold", text_type_bold, None), TextNode(" node", text_type_text, None)])

    def test_delimiter_multiple_types(self):
        node = TextNode("Is **This** is `a` crazy *node*", text_type_text)
        new_node = split_nodes_delimiter([node], "**", text_type_bold)
        new_node_1 = split_nodes_delimiter(new_node, "`", text_type_code)

        self.assertEqual(split_nodes_delimiter(new_node_1, "*", text_type_italic), [TextNode("Is ", text_type_text, None),
                                                                                        TextNode("This", text_type_bold, None),
                                                                                        TextNode(" is ", text_type_text, None), 
                                                                                        TextNode("a", text_type_code, None),
                                                                                        TextNode(" crazy ", text_type_text, None),
                                                                                        TextNode("node", text_type_italic, None),
                                                                                        TextNode("", text_type_text, None),])

    def test_delimiter_multiple_nodes(self):
        node_1 = TextNode("This is a `code` node_1", text_type_text)
        node_2 = TextNode("This is a `code` node_2", text_type_text)
        node_3 = TextNode("This is a `code` node_3", text_type_text)
        self.assertEqual(split_nodes_delimiter([node_1, node_2, node_3], "`", text_type_code), [TextNode("This is a ", text_type_text, None), TextNode("code", text_type_code, None), TextNode(" node_1", text_type_text, None),
                                                                                                TextNode("This is a ", text_type_text, None), TextNode("code", text_type_code, None), TextNode(" node_2", text_type_text, None),
                                                                                                TextNode("This is a ", text_type_text, None), TextNode("code", text_type_code, None), TextNode(" node_3", text_type_text, None)])
    
    def test_multiple_delimiters(self):
        node = TextNode("This `is` a `code` node", text_type_text)
        self.assertEqual(split_nodes_delimiter([node], "`", text_type_code), [TextNode("This ", text_type_text, None), TextNode("is", text_type_code, None), TextNode(" a " , text_type_text, None), TextNode("code", text_type_code, None), TextNode(" node", text_type_text, None)])

    def test_delimiter_not_pair(self):
        node = TextNode("This `is a code node", text_type_text)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", text_type_code)

    def test_extract_image(self):
        node = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], node)

    def test_extract_link(self):
        node = extract_markdown_links("This is text with an [link](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], node)

    def test_split_nodes_image(self):
        node = TextNode("This `is` a `code` node, This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", text_type_text)
        self.assertListEqual(split_nodes_image([node]), [TextNode("This `is` a `code` node, This is text with an ", text_type_text), TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png")])
    
    def test_split_nodes_image_multiple(self):
        node_1 = TextNode("This is text with an ![image_1](https://i.imgur.com/zjjcJKZ.png)", text_type_text)
        node_2 = TextNode("Another text with  ![image_2](https://imgur.com/gallery/new-toy-QoKYfNP.png)", text_type_text)
        node_3 = TextNode("And last ![image_3](https://imgur.com/gallery/mountainous-seas-qI8HgBe.png), And for that reason i'm out", text_type_text)
        self.assertListEqual(split_nodes_image([node_1, node_2, node_3]), [TextNode("This is text with an ", text_type_text),
                                                                            TextNode("image_1", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                                                                            TextNode("Another text with  ", text_type_text),
                                                                            TextNode("image_2", text_type_image, "https://imgur.com/gallery/new-toy-QoKYfNP.png"),
                                                                            TextNode("And last ", text_type_text),
                                                                            TextNode("image_3", text_type_image, "https://imgur.com/gallery/mountainous-seas-qI8HgBe.png"),
                                                                            TextNode(", And for that reason i'm out", text_type_text)])
    
    def test_split_nodes_image_3_picture(self):
        node = TextNode("This is text with an ![image_1](https://i.imgur.com/zjjcJKZ.png), Another text with ![image_2](https://imgur.com/gallery/new-toy-QoKYfNP.png) ,And last ![image_3](https://imgur.com/gallery/mountainous-seas-qI8HgBe.png), And for that reason i'm out", text_type_text)
        self.assertListEqual(split_nodes_image([node]), [TextNode("This is text with an ", text_type_text),
                                                         TextNode("image_1", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                                                         TextNode(", Another text with ", text_type_text),
                                                         TextNode("image_2", text_type_image, "https://imgur.com/gallery/new-toy-QoKYfNP.png"),
                                                         TextNode(" ,And last ", text_type_text),
                                                         TextNode("image_3", text_type_image, "https://imgur.com/gallery/mountainous-seas-qI8HgBe.png"),
                                                         TextNode(", And for that reason i'm out", text_type_text)])
        
    def test_split_nodes_link(self):
        node = TextNode("This `is` a `code` node, This is text with an [link](https://i.imgur.com/zjjcJKZ.png)", text_type_text)
        self.assertListEqual(split_nodes_link([node]), [TextNode("This `is` a `code` node, This is text with an ", text_type_text), TextNode("link", text_type_link, "https://i.imgur.com/zjjcJKZ.png")])
    
    def test_split_nodes_link_multiple(self):
        node_1 = TextNode("This is text with an [link_1](https://i.imgur.com/zjjcJKZ.png)", text_type_text)
        node_2 = TextNode("Another text with  [link_2](https://imgur.com/gallery/new-toy-QoKYfNP.png)", text_type_text)
        node_3 = TextNode("And last [link_3](https://imgur.com/gallery/mountainous-seas-qI8HgBe.png), And for that reason i'm out", text_type_text)
        self.assertListEqual(split_nodes_link([node_1, node_2, node_3]), [TextNode("This is text with an ", text_type_text),
                                                                            TextNode("link_1", text_type_link, "https://i.imgur.com/zjjcJKZ.png"),
                                                                            TextNode("Another text with  ", text_type_text),
                                                                            TextNode("link_2", text_type_link, "https://imgur.com/gallery/new-toy-QoKYfNP.png"),
                                                                            TextNode("And last ", text_type_text),
                                                                            TextNode("link_3", text_type_link, "https://imgur.com/gallery/mountainous-seas-qI8HgBe.png"),
                                                                            TextNode(", And for that reason i'm out", text_type_text)])
    
    def test_split_nodes_link_3_picture(self):
        node = TextNode("This is text with an [link_1](https://i.imgur.com/zjjcJKZ.png), Another text with [link_2](https://imgur.com/gallery/new-toy-QoKYfNP.png) ,And last [link_3](https://imgur.com/gallery/mountainous-seas-qI8HgBe.png), And for that reason i'm out", text_type_text)
        self.assertListEqual(split_nodes_link([node]), [TextNode("This is text with an ", text_type_text),
                                                         TextNode("link_1", text_type_link, "https://i.imgur.com/zjjcJKZ.png"),
                                                         TextNode(", Another text with ", text_type_text),
                                                         TextNode("link_2", text_type_link, "https://imgur.com/gallery/new-toy-QoKYfNP.png"),
                                                         TextNode(" ,And last ", text_type_text),
                                                         TextNode("link_3", text_type_link, "https://imgur.com/gallery/mountainous-seas-qI8HgBe.png"),
                                                         TextNode(", And for that reason i'm out", text_type_text)])

    def test_split_nodes_image_text_type(self):
        node = TextNode("code", text_type_code)
        self.assertListEqual(split_nodes_image([node]), [TextNode("code", text_type_code)])

    def test_split_nodes_link_text_type(self):
        node = TextNode("code", text_type_code)
        self.assertListEqual(split_nodes_link([node]), [TextNode("code", text_type_code)])

    def test_text_to_textnode(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        self.assertListEqual(text_to_textnodes(text), [TextNode("This is ", text_type_text, None),
                                                       TextNode("text", text_type_bold, None),
                                                       TextNode(" with an ", text_type_text, None),
                                                       TextNode("italic", text_type_italic, None),
                                                       TextNode(" word and a ", text_type_text, None),
                                                       TextNode("code block", text_type_code, None),
                                                       TextNode(" and an ", text_type_text, None),
                                                       TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                                                       TextNode(" and a ", text_type_text, None),
                                                       TextNode("link", text_type_link, "https://boot.dev")])
        
if __name__ == "__main__":
    unittest.main()