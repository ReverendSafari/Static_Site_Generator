import unittest
from parse_markdown import split_nodes_delimiter
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
    

    