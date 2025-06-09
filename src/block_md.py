from enum import Enum
from htmlnode import *
from textnode import *
from inline_md import *
import re


class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = list(map(lambda str: str.strip(), blocks))
    filtered_blocks = list(filter(lambda str: str != "", stripped_blocks))

    return filtered_blocks

def block_to_block_type(markdown):
    block_lines = markdown.split("\n")

    ol = True

    for index, str in enumerate(block_lines):
        if str.startswith(f"{index + 1}. "):
            continue
        else:
            ol = False

    if bool(block_lines[0].strip().startswith("```") and block_lines[-1].strip().endswith("```")):
        return BlockType.CODE
    elif bool(re.match(r"^\#{1,6}\s+.+$", markdown)):
        return BlockType.HEADING
    elif all(str.startswith(">") for str in block_lines):
        return BlockType.QUOTE
    elif all(str.startswith("- ") for str in block_lines):
        return BlockType.UNORDERED_LIST
    elif ol:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    #Split Markdown into blocks
    blocks = markdown_to_blocks(markdown)
    div_parent = ParentNode("div",[])

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.CODE:
            div_parent.children.append(create_code_block(block))
            continue

        if block_type == BlockType.HEADING:
            div_parent.children.append(create_header_block(block))
            continue
        
        if block_type == BlockType.QUOTE:
            div_parent.children.append(create_block_quote(block))
            continue

        if block_type == BlockType.PARAGRAPH:
            div_parent.children.append(create_paragraph_block(block))
            continue

        if block_type == BlockType.UNORDERED_LIST:
            div_parent.children.append(create_ul_block(block))
            continue

        if block_type == BlockType.ORDERED_LIST:
            div_parent.children.append(create_ol_block(block))
            continue

    return div_parent


def create_header_tag(block):
    prefix = block.strip().split(" ")[0]
    return (f"h{len(prefix.strip())}", prefix.strip())

def create_header_block(block):
    tag, prefix = create_header_tag(block)
    new_node = ParentNode(tag, [])
    text_node_list = text_to_textnodes(block.replace(prefix, "", 1).lstrip())
    child_node_list = [text_node_to_html_node(text_node) for text_node in text_node_list]
    new_node.children = child_node_list
    return new_node

def create_code_block(block):
    code_array = strip_markdown_from_code(block.split("\n"))
    code = "\n".join(code_array)
    code_node = LeafNode("code", code)
    pre_node = ParentNode("pre", [code_node])
    return pre_node

def strip_markdown_from_code(block_list):
    first_index, last_index = 0, -1

    for index, line in enumerate(block_list):
        if line.strip() == "":
            continue
        if line.strip() == "```":
            first_index = index + 1
            break            

    for index in range(len(block_list)-1, -1, -1):
        if block_list[index].strip() == "":
            continue
        if block_list[index].strip() == "```":
            last_index = index
            break

    return block_list[first_index:last_index]

def create_paragraph_block(block):
    new_node = ParentNode("p", [])
    text_node_list = text_to_textnodes(block)
    child_node_list = [text_node_to_html_node(text_node) for text_node in text_node_list]
    new_node.children = child_node_list
    return new_node

def create_ul_block(block):
    parent_node = ParentNode("ul", [])
    line_array = block.split("\n")

    for line in line_array:
        line = line.strip()[2:]
        parent_node.children.append(create_li_node(line))

    return parent_node

def create_ol_block(block):
    parent_node = ParentNode("ol", [])
    line_array = block.split("\n")

    for line in line_array:
        line = line.strip()[3:]
        parent_node.children.append(create_li_node(line))

    return parent_node

def create_li_node(line):
    list_node = ParentNode("li", [])
    inline_nodes = text_to_textnodes(line)
    for textnode in inline_nodes:
        list_node.children.append(text_node_to_html_node(textnode))

    return list_node

def create_block_quote(block):
    quote_node = ParentNode("blockquote", [])
    blocks = markdown_to_blocks(strip_quote_markdown(block))

    if not re.search(r"\S.*\n\n+.*\S", strip_quote_markdown(block)):
        child_nodes = text_to_textnodes(strip_quote_markdown(block))
        html_nodes = [text_node_to_html_node(node) for node in child_nodes]
        quote_node.children = html_nodes
        
        return quote_node

    for block in blocks:
        parent_paragraph = create_paragraph_block(block)
        quote_node.children.append(parent_paragraph)

    return quote_node

def strip_quote_markdown(block):
    lines = block.split("\n")

    for index, line in enumerate(lines):
        if line.lstrip().startswith("> "):
           lines[index] = line.lstrip().replace("> ", "", 1)
        elif line.lstrip().startswith(">"):
            lines[index] = line.lstrip().replace(">", "", 1)
    return "\n".join(lines)

def main():
    print(markdown_to_html_node("> COMPLEX **QUOTE**\n>MUST STAY CHEAP CAUSE\n>\n>okay okay `okay`").to_html())

if __name__ == "__main__":
    main()