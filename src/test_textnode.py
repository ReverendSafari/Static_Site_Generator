import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("Test Text", TextType.TEXT)
        node2 = TextNode("Test Text", TextType.TEXT)
        self.assertEqual(node1, node2)

    def test_noteq(self):
        node1 = TextNode("Test Text", TextType.BOLD)
        node2 = TextNode("Test Text", TextType.CODE)
        self.assertNotEqual(node1, node2)

    def test_noteq_url(self):
        node1 = TextNode("Test Text", TextType.LINK, "swellseeker.com")
        node2 = TextNode("Test Text", TextType.LINK)
        self.assertNotEqual(node1, node2)

    #Test conversion value
    def test_conversion_value(self):
        node1 = text_node_to_html_node(TextNode("Testing Testing...", TextType.TEXT))
        self.assertEqual(node1.value, "Testing Testing...")

    #Test conversion tag
    def test_conversion_tag(self):
        node1 = text_node_to_html_node(TextNode("Testing Testing...", TextType.BOLD))
        self.assertEqual(node1.tag, "b")

    #Test HTML conversion
    def test_conversion_string(self):
        node1 = text_node_to_html_node(TextNode("Testing Testing...", TextType.BOLD))
        self.assertEqual(node1.to_html(), "<b>Testing Testing...</b>")

    #Test link conversion
    def test_conversion_link(self):
        node1 = text_node_to_html_node(TextNode("Link to swellseeker", TextType.LINK, "swellseeker.com"))
        self.assertEqual(node1.to_html(), "<a href=\"swellseeker.com\">Link to swellseeker</a>")

    def test_conversion_img(self):
        node1 = text_node_to_html_node(TextNode("swellseeker.com", TextType.IMAGE, "/img.png"))
        self.assertEqual(node1.to_html(), "<img src=\"/img.png\" href=\"swellseeker.com\"></img>")

if __name__ == "__main__":
    unittest.main()
