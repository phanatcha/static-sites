import unittest
from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
    text_to_textnodes,
)

class TestInlineMarkdown(unittest.TestCase):
    def test_bold_delimiter(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])

    def test_italic_delimiter(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ])

    def test_code_delimiter(self):
        node = TextNode("This is `code` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ])

    def test_multiple_delimiters(self):
        node = TextNode("This **has** multiple **bold** words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This ", TextType.TEXT),
            TextNode("has", TextType.BOLD),
            TextNode(" multiple ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" words", TextType.TEXT),
        ])

    def test_delimiter_at_start(self):
        node = TextNode("**Start** with bold", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("Start", TextType.BOLD),
            TextNode(" with bold", TextType.TEXT),
        ])

    def test_delimiter_at_end(self):
        node = TextNode("End with *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("End with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ])

    def test_no_delimiters(self):
        node = TextNode("Plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [node])

    def test_non_text_node(self):
        node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [node])

    def test_unmatched_delimiters(self):
        node = TextNode("This has **unmatched delimiter", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_empty_text_between_delimiters(self):
        node = TextNode("Empty** **bold", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("Empty", TextType.TEXT),
            TextNode(" ", TextType.BOLD),
            TextNode("bold", TextType.TEXT),
        ])

    def test_multiple_node_input(self):
        nodes = [
            TextNode("First **bold**", TextType.TEXT),
            TextNode("Already italic", TextType.ITALIC),
            TextNode("Second *italic*", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("First ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("Already italic", TextType.ITALIC),
            TextNode("Second ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ])

    def test_markdown_image(self):
        text = "This is text with an ![woman sits](https://www.shutterstock.com/image-photo/young-woman-sitting-office-table-260nw-716829193.jpg) and ![man confuses](https://st2.depositphotos.com/3489481/5280/i/450/depositphotos_52802675-stock-photo-looking-clueless-business-man.jpg)"
        expected = [
            ("woman sits", "https://www.shutterstock.com/image-photo/young-woman-sitting-office-table-260nw-716829193.jpg"),
            ("man confuses", "https://st2.depositphotos.com/3489481/5280/i/450/depositphotos_52802675-stock-photo-looking-clueless-business-man.jpg")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_markdown_links(self):
        text = "This is [bootdev](https://www.boot.dev) and this is [github](https://github.com)"
        expected = [
            ("bootdev", "https://www.boot.dev"),
            ("github", "https://github.com")
        ]
        self.assertEqual(extract_markdown_links(text), expected)


    def test_markdown_not_image(self):
        text = "This is [bootdev](https://www.boot.dev) and this is [github](https://github.com)"
        not_expected = [
            ("bootdev", "https://www.boot.dev"),
            ("github", "https://github.com")
        ]
        self.assertNotEqual(extract_markdown_images(text), not_expected)

    def test_markdown_not_links(self):
        text = "This is text with an ![woman sits](https://www.shutterstock.com/image-photo/young-woman-sitting-office-table-260nw-716829193.jpg) and ![man confuses](https://st2.depositphotos.com/3489481/5280/i/450/depositphotos_52802675-stock-photo-looking-clueless-business-man.jpg)"
        not_expected = [
            ("woman sits", "https://www.shutterstock.com/image-photo/young-woman-sitting-office-table-260nw-716829193.jpg"),
            ("man confuses", "https://st2.depositphotos.com/3489481/5280/i/450/depositphotos_52802675-stock-photo-looking-clueless-business-man.jpg")
        ]        
        self.assertNotEqual(extract_markdown_links(text), not_expected)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and [another](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_no_links(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_mixed_content(self):
        node = TextNode(
            "Start ![image](url1) middle [link](url2) end ![image2](url3)",
            TextType.TEXT,
        )
        image_nodes = split_nodes_image([node])
        link_nodes = split_nodes_link([node])
        
        self.assertEqual(len(image_nodes), 4) 
        self.assertEqual(len(link_nodes), 3) 

    def test_split_with_non_text_nodes(self):
        nodes = [
            TextNode("![image](url)", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode("[link](url)", TextType.TEXT),
        ]
        image_nodes = split_nodes_image(nodes)
        link_nodes = split_nodes_link(nodes)
        
        self.assertEqual(image_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(link_nodes[1].text_type, TextType.BOLD)

    def test_split_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes_image = split_nodes_image([node])
        new_nodes_link = split_nodes_link([node])
        self.assertListEqual([node], new_nodes_image)
        self.assertListEqual([node], new_nodes_link)

    def test_text_to_textnodes_first(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_second(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)    


if __name__ == "__main__":
    unittest.main()