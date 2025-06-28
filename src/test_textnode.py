import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq_text(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_not_eq_text(self):
        node1 = TextNode("Text 1", TextType.ITALIC)
        node2 = TextNode("Text 2", TextType.ITALIC)
        self.assertNotEqual(node1, node2)
    
    def test_eq_type(self):
        node1 = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(node1, node2)

    def test_not_eq_type(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_eq_url(self):
        node1 = TextNode("Link", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Link", TextType.LINK, "https://boot.dev")
        self.assertEqual(node1, node2)

    def test_not_eq_url(self):
        node1 = TextNode("Link", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Link", TextType.LINK, "https://github.com")
        self.assertNotEqual(node1, node2)

    def test_default_url_none(self):
        node = TextNode("Text", TextType.BOLD)
        self.assertIsNone(node.url)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_img(self):
        node = TextNode("Boot.dev logo", TextType.IMAGE, "https://boot.dev/path/to/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://boot.dev/path/to/image.png", "alt": "Boot.dev logo"})

    def test_img_missing_url(self):
        node = TextNode("Alt text", TextType.IMAGE, None)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_img_empty_alt(self):
        node = TextNode("", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props["alt"], "")
        
if __name__ == "__main__":
    unittest.main()