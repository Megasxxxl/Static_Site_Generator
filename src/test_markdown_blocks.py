import unittest

from markdown_blocks import (markdown_to_blocks,
                             block_to_block_type,
                             block_type_code,
                             block_type_heading,
                             block_type_ordered_list,
                             block_type_paragraph,
                             block_type_quote,
                             block_type_unordered_list)

class TestInLineMarkdown(unittest.TestCase):
    def test_markdown_to_block(self):
        markdown = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""

        self.assertListEqual(markdown_to_blocks(markdown), ["This is **bolded** paragraph", """This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line""", """* This is a list
* with items"""])
        

    def test_block_to_block_paragraph(self):
        block = "This is **bolded** paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)
    
    def test_block_to_block_heading(self):
        block = "## This is **bolded** heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)

    def test_block_to_block_code(self):
        block = "``` This is **bolded** code ```"
        self.assertEqual(block_to_block_type(block), block_type_code)

    def test_block_to_block_quote(self):
        block = ">This is **bolded** quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)

    def test_block_to_block_unordered_list(self):
        block ="""* This is a list
* with items"""
        self.assertEqual(block_to_block_type(block), block_type_unordered_list)
    
    def test_block_to_block_ordered_list(self):
        block = """1. This is a list
2. with items"""
        self.assertEqual(block_to_block_type(block), block_type_ordered_list)
    
    def test_block_to_block_heading_wrong(self):
        block = "##@ This is **bolded** heading"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_block_to_block_code_wrong(self):
        block = "``` This is **bolded** code ``"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_block_to_block_quote_wrong(self):
        block = ">This is **bolded** quote\n>This is hellafunny\n!>Im telling you"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_block_to_block_unordered_list_wrong(self):
        block ="""* This is a list
& with items"""
        self.assertEqual(block_to_block_type(block), block_type_paragraph)
    
    def test_block_to_block_ordered_list_wrong(self):
        block = """1. This is a list
3. with items"""
        self.assertEqual(block_to_block_type(block), block_type_paragraph)
    

if __name__ == "__main__":
    unittest.main()