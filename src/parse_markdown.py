
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if not delimiter in node.text:
            new_nodes.append(node)
            continue


        for index, str in enumerate(node.text.split(delimiter)):
            if str == "":
                continue

            if index % 2 == 0:
                new_nodes.append(TextNode(str, TextType.TEXT))
            else:
                new_nodes.append(TextNode(str, text_type))
        
    return new_nodes