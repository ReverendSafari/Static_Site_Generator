from textnode import TextNode, TextType


def main():
    node1 = TextNode("Mouse man kills mice!", TextType.NORMAL_TEXT)
    node2 = TextNode("swellseeker.com", TextType.LINK_TEXT, "swellseeker.com")
    node3 = TextNode("BOLD THIS SHIT", TextType.BOLD_TEXT)

    print(node1)
    print(node2)
    print(node3)

if __name__ == "__main__":
    main()