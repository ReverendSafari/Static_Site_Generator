import unittest
from inline_md import *
from textnode import *

class test_parse_markdown(unittest.TestCase):
    #Test no delim present
    def test_no_delim(self):
        result_nodes = split_nodes_delimiter([TextNode("Of mice and men", TextType.TEXT), TextNode("of lice and len", TextType.TEXT)], "*", TextType.BOLD)
        self.assertEqual(result_nodes, [TextNode("Of mice and men", TextType.TEXT), TextNode("of lice and len", TextType.TEXT)])

    #Test wrong delim
    def test_wrong_delim(self):
        result_nodes = split_nodes_delimiter([TextNode("_Of mice and men_", TextType.TEXT), TextNode("_of lice and len_", TextType.TEXT)], "*", TextType.BOLD)
        self.assertEqual(result_nodes, [TextNode("_Of mice and men_", TextType.TEXT), TextNode("_of lice and len_", TextType.TEXT)])
  
    #Test bold
    def test_bold_delim(self):
        result_nodes = split_nodes_delimiter([TextNode("This thing *DRIVES* boy!", TextType.TEXT)], "*", TextType.BOLD)
        self.assertEqual(result_nodes, [TextNode("This thing ", TextType.TEXT), TextNode("DRIVES", TextType.BOLD), TextNode(" boy!", TextType.TEXT)])
    
    #Test italic
    def test_bold_delim(self):
        result_nodes = split_nodes_delimiter([TextNode("This thing _DRIVES_ boy!", TextType.TEXT)], "_", TextType.ITALIC)
        self.assertEqual(result_nodes, [TextNode("This thing ", TextType.TEXT), TextNode("DRIVES", TextType.ITALIC), TextNode(" boy!", TextType.TEXT)])
    
    #Test empty strings
    def test_empty_strings_images(self):
        text = ""
        self.assertEqual(extract_markdown_images(text), [])

    def test_empty_strings_images(self):
        text = ""
        self.assertEqual(extract_markdown_links(text) ,[])
            
    #Test single image
    def test_single_image_extraction(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and"
        self.assertEqual(extract_markdown_images(text), [('rick roll', 'https://i.imgur.com/aKaOqIh.gif')])
        
    #Test multiple images
    def test_multiple_image_extraction(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])
        
    #Test single link
    def test_single_link_extraction(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and"
        self.assertEqual(extract_markdown_links(text), [('rick roll', 'https://i.imgur.com/aKaOqIh.gif')])
        
    #Test multiple links
    def test_multiple_links(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_links(text), [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])
        
    #Test only image in link function
    def test_image_no_link(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and"
        self.assertEqual(extract_markdown_links(text), [])
        
    #Test only link in image function
    def test_link_no_image(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and"
        self.assertEqual(extract_markdown_images(text), [])
        
    #Test no images
    def test_no_image(self):
        nodes = [TextNode("This is a string with no image", TextType.TEXT), TextNode("some other string with NO image [but heres](a LINK!)", TextType.TEXT)]
        self.assertEqual(split_nodes_image(nodes), [TextNode("This is a string with no image", TextType.TEXT), TextNode("some other string with NO image [but heres](a LINK!)", TextType.TEXT)])

    #Test no links
    def test_no_link(self):
        nodes = [TextNode("This is a string with no link", TextType.TEXT), TextNode("some other string with NO link ![but heres](an IMAGE!)", TextType.TEXT)]
        self.assertEqual(split_nodes_link(nodes), [TextNode("This is a string with no link", TextType.TEXT), TextNode("some other string with NO link ![but heres](an IMAGE!)", TextType.TEXT)])

    #Test single image
    def test_single_image(self):
        nodes = [TextNode("Some image is here > ![img text](SWELLSEEKER.COM) <<<<", TextType.TEXT)]
        self.assertListEqual(split_nodes_image(nodes), [
            TextNode("Some image is here > ", TextType.TEXT),
            TextNode("img text", TextType.IMAGE, "SWELLSEEKER.COM"),
            TextNode(" <<<<", TextType.TEXT)
        ])

    #Test single link
    def test_single_link(self):
        nodes = [TextNode("Some link is here > [link text](SWELLSEEKER.COM) <<<<", TextType.TEXT)]
        self.assertListEqual(split_nodes_link(nodes), [
            TextNode("Some link is here > ", TextType.TEXT),
            TextNode("link text", TextType.LINK, "SWELLSEEKER.COM"),
            TextNode(" <<<<", TextType.TEXT)
        ])

    #Test multi images
    def test_mutli_images(self):
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

    #Test multi links
    def test_mutli_links(self):
        node = TextNode(
            "This is text with an [some link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("some link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    #Test mixed for images
    def test_mixed_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another [link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
            ],
            new_nodes,
        )

    #Test mixed for links
    def test_mixed_links(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes,
        )
    
    #Test empty string for images
    def test_empty_string_images(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [])

    #Test empty string for links
    def test_empty_string_links(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [])
        
    #Test plain text
    def test_plain_conversion(self):
        text = "This is just some plain ol' text"
        self.assertEqual(text_to_textnodes(text), [TextNode("This is just some plain ol' text", TextType.TEXT)])

    #Test with a bold
    def test_bold_conversion(self):
        text = "Text getting **BOLD** out here"
        self.assertListEqual(text_to_textnodes(text), [
            TextNode("Text getting ", TextType.TEXT),
            TextNode("BOLD", TextType.BOLD),
            TextNode(" out here", TextType.TEXT)
        ])

    #Test with an italic
    def test_italic_conversion(self):
        text = "I love _italians_"
        self.assertListEqual(text_to_textnodes(text),
                [TextNode("I love ", TextType.TEXT),
                TextNode("italians", TextType.ITALIC)
        ])
        
    #Test with image and link
    def test_image_and_link_conversion(self):
        text = "An ![image](imageLINKhere), and a [link](swellseeker.com)"
        self.assertListEqual(text_to_textnodes(text), [
            TextNode("An ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "imageLINKhere"),
            TextNode(", and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "swellseeker.com")
        ])
    
    #Test empty text (Scared)  
    def test_empty_string_conversion(self):
        text = ""
        self.assertEqual(text_to_textnodes(text), [])