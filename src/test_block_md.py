import unittest
from block_md import *

class test_block_md(unittest.TestCase):
    #Test empty string
    def test_empty_string(self):
        md = ""

        self.assertEqual(markdown_to_blocks(md), [])

    #Test normal md
    def test_normal_md(self):
        md = "This is the first block right here\n\nHere is the second block ...\n\nand FINALLY the third block"

        self.assertListEqual(markdown_to_blocks(md), [
            "This is the first block right here",
            "Here is the second block ...",
            "and FINALLY the third block"
        ])

    #Test extra spaces and new lines
    def test_bad_md(self):
        md = "BUH BUH BAHHH\n\n\n\n       \nbad md I hate markdown\n  \n"

        self.assertListEqual(markdown_to_blocks(md), [
            "BUH BUH BAHHH",
            "bad md I hate markdown"
        ])


    #Test code
    def test_code_type(self):
        md = "``` This is a code block ```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)

    #Test quote
    def test_quote_type(self):
        md = "> This is" \
        "> A quote " \
        "> block"
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

    #Test heading 
    def test_header_type(self):
        md = "#### HEADER 4 BABY"
        self.assertEqual(block_to_block_type(md), BlockType.HEADING)

    #Test ol
    def test_ol_type(self):
        md = "1. ordered" \
        "2. list " \
        "3. TYPE"
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)

    #Test ul
    def test_ul_type(self):
        md = "- some" \
        "- unORDERED" \
        "- LIST"
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)

    #Test paragraph
    def test_paragraph_type(self):
        md = "``` NOT CODE" \
        "> NOT QUOTE" \
        "## NOT HEADER" \
        "1. NOT OL" \
        "- NOT UL"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)


    '''
    @markdown_to_html_node
    Tests for full conversion
    '''

    #test paragraph
    def test_paragraph_conversion(self):
        converted_md = markdown_to_html_node(
            "This is a simple paragraph block!"
            ).to_html()

        self.assertEqual(converted_md, "<div><p>This is a simple paragraph block!</p></div>")

    #test heading
    def test_h1_conversion(self):
        converted_md = markdown_to_html_node("# This is an h1").to_html()
        self.assertEqual(converted_md ,"<div><h1>This is an h1</h1></div>")

    def test_h3_conversion(self):
        converted_md = markdown_to_html_node("### This is an h3").to_html()
        self.assertEqual(converted_md ,"<div><h3>This is an h3</h3></div>")

    #test OL
    def test_ol_conversion(self):
        converted_md = markdown_to_html_node("1. first item\n" \
        "2. second item\n" \
        "3. third item").to_html()

        self.assertEqual(converted_md,"<div><ol><li>first item</li><li>second item</li><li>third item</li></ol></div>")

    #test UL
    def test_ul_conversion(self):
        converted_md = markdown_to_html_node("- first item\n" \
        "- second item\n" \
        "- third item").to_html()

        self.assertEqual(converted_md,"<div><ul><li>first item</li><li>second item</li><li>third item</li></ul></div>")


    #test simple block quote
    def test_simple_quote_conversion(self):
        converted_md = markdown_to_html_node("> Simple quote block **here!**").to_html()
        self.assertEqual(converted_md, "<div><blockquote>Simple quote block <b>here!</b></blockquote></div>")

    #test big block quote
    def test_complex_quote_conversion(self):
        converted_md = markdown_to_html_node("> COMPLEX **QUOTE**\n>MUST STAY CHEAP CAUSE\n>\n>okay okay `okay`").to_html()
        self.assertEqual(converted_md, "<div><blockquote><p>COMPLEX <b>QUOTE</b>\nMUST STAY CHEAP CAUSE</p><p>okay okay <code>okay</code></p></blockquote></div>")
    
    #test code
    def test_code_conversion(self):
        converted_md = markdown_to_html_node("```\nThis is a **code** block\n```").to_html()
        self.assertEqual(converted_md ,"<div><pre><code>This is a **code** block</code></pre></div>")