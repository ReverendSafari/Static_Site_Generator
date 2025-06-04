import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    #Test object intilization
    def test_createObject(self):
        node1 = HTMLNode("<p>", "a paragraph here",None,{"href":"some_link.com"})
        assert node1.tag == "<p>"
        assert node1.value == "a paragraph here"
        assert node1.children == None
        assert node1.props == {"href":"some_link.com"}

    #Test empty props
    def test_emptyProps(self):
        node1 = HTMLNode("<p>", "a paragraph here",None)
        self.assertEqual(node1.props_to_html(), "")

    #Test single prop 
    def test_singleProp(self):
        node1 = HTMLNode("<p>", "a paragraph here",None,{"href":"some_link.com"})
        self.assertEqual(node1.props_to_html(),' href="some_link.com"')
    
    #Test multiple props
    def test_multiProps(self):
        node1 = HTMLNode("<p>", "a paragraph here",None,{"href":"some_link.com", "kissme":"sixpence none the richer"})
        self.assertEqual(node1.props_to_html(), ' href="some_link.com" kissme="sixpence none the richer"')

        #test tagless to HTML
    def test_no_tag(self):
        node1 = LeafNode(None, "Raw text baby")
        self.assertEqual(node1.to_html(), "Raw text baby")

    #test no value HTML?
    def test_no_value(self):
        node1 = LeafNode("p",None,None)
        with self.assertRaises(ValueError):
            node1.to_html()

    #test p tag to HTML
    def test_p_tag(self):
        node1 = LeafNode("p", "some text here")
        self.assertEqual(node1.to_html(), "<p>some text here</p>")

    #test p tag with props
    def test_props(self):
        node1 = LeafNode("p", "some text here", {"href":"swellseeker.com"})
        self.assertEqual(node1.to_html(), "<p href=\"swellseeker.com\">some text here</p>")

    #test p with several props
    def test_multi_props(self):
        node1 = LeafNode("p", "some text here", {"href":"swellseeker.com", "color":"gray"})
        self.assertEqual(node1.to_html(), "<p href=\"swellseeker.com\" color=\"gray\">some text here</p>")

        #Test props work
    def test_props(self):
        node1 = ParentNode("p",[LeafNode("h1","See")], {"href":"swellseeker.com"})
        self.assertEqual(node1.to_html(), "<p href=\"swellseeker.com\"><h1>See</h1></p>")

    #Test to_html no tag
    def test_no_tag(self):
        node1 = ParentNode(None,[LeafNode("h1","See")], {"href":"swellseeker.com"})
        with self.assertRaises(ValueError):
            node1.to_html()

    #Test to_html no children
    def test_no_children(self):
        node1 = ParentNode("p", None, {"href":"swellseeker.com"})
        with self.assertRaises(ValueError):
            node1.to_html()

    #Test to_html single child
    def test_single_child(self):
        node1 = ParentNode("p",[LeafNode("h1","See")])
        self.assertEqual(node1.to_html(), "<p><h1>See</h1></p>")

    #Test to_html multiple children
    def test_multiple_children(self):
        node1 = ParentNode("p", [LeafNode("h1","See"), LeafNode("h2","ya")])
        self.assertEqual(node1.to_html(), "<p><h1>See</h1><h2>ya</h2></p>")

    #Test to_html nested children
    def test_nested_children(self):
        node1 = ParentNode("p",[LeafNode("h1","nest")])
        node2 = ParentNode("div",[node1])

        self.assertEqual(node2.to_html(), "<div><p><h1>nest</h1></p></div>")
    
