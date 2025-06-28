import unittest
from block_markdown import (
    markdown_to_html_node,
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
)


class TestHTMLNode(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )



    def test_markdown_to_blocks_newlines(self):
        md = """



    
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_paragraph_block(self):
        block = "This is just a paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_block(self):
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "######## Not a heading"
        self.assertNotEqual(block_to_block_type(block), BlockType.HEADING)

        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block(self):
        block = "```not a closed block"
        self.assertNotEqual(block_to_block_type(block), BlockType.CODE)

        block = "```single line```"
        self.assertNotEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> Quote line 1\n> Quote line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        
        block = "> Single quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        
        block = "> Mixed\nNot quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        
        block = "- Single item"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        
        block = "- Item 1\n* Not a list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)        

    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        
        block = "1. Single item"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        
        block = "1. First\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        block = "1. First\n2. Second\n4. Fourth" 
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
if __name__ == "__main__":
    unittest.main()


