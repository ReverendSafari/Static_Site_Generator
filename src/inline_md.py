import re
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

def extract_markdown_images(text):
    if text == "":
        return []
    
    matches = re.findall(r"!\[([^\]]+)\]\(([^\]]+)\)",text)
    return matches

def extract_markdown_links(text):
    if text == "":
        return []
    
    matches = re.findall(r"(?<!!)\[([^\]]+)\]\(([^\]]+)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        images = extract_markdown_images(node.text)

        if node.text == "":
            continue

        if images == []:
            new_nodes.append(node)
            continue

        master_list = node.text.split(f"![{images[0][0]}]({images[0][1]})", maxsplit=1)

        while images:
            if master_list[0] != "":
                new_nodes.append(TextNode(master_list[0],TextType.TEXT))

            new_nodes.append(TextNode(images[0][0],TextType.IMAGE,images[0][1]))
            images.pop(0)
            
            if images != [] and master_list != []:
                master_list = master_list[1].split(f"![{images[0][0]}]({images[0][1]})", maxsplit=1)

        #Append any remaining text
        if master_list[1] != "":
            new_nodes.append(TextNode(master_list[1], TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        links = extract_markdown_links(node.text)

        if node.text == "":
            continue

        if links == []:
            new_nodes.append(node)
            continue

        master_list = node.text.split(f"[{links[0][0]}]({links[0][1]})", maxsplit=1)

        while links:
            if master_list[0] != "":
                new_nodes.append(TextNode(master_list[0],TextType.TEXT))

            new_nodes.append(TextNode(links[0][0],TextType.LINK, links[0][1]))
            links.pop(0)
            
            if links != [] and master_list != []:
                master_list = master_list[1].split(f"[{links[0][0]}]({links[0][1]})", maxsplit=1)

        #Append any remaining text
        if master_list[1] != "":
            new_nodes.append(TextNode(master_list[1], TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    #intialize text into first node
    node_list = [TextNode(text, TextType.TEXT)]

    #Split for bold
    bold_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    
    #Split for italic
    italic_list = split_nodes_delimiter(bold_list, "_", TextType.ITALIC)
    
    #Split for code
    code_list = split_nodes_delimiter(italic_list, "`", TextType.CODE)
    
    #Split for image
    image_list = split_nodes_image(code_list)

    #Split for link
    final_list = split_nodes_link(image_list)

    return final_list

