from enum import Enum

from htmlnode import (
    ParentNode
)
from textnode import (
    text_node_to_html_node,
    TextNode, 
    TextType,
)
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    result = []
    split_on_newline = markdown.split("\n\n")
    for block in split_on_newline:
        addline = block.strip()
        if addline != "":
            result.append(addline)
    return result

def block_to_block_type(block):
    lines = block.split("\n")
    if lines[0].startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    if lines[0].startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if lines[0].startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if lines[0].startswith("1. "):
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i+1}. "):
                return BlockType.PARAGRAPH
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                block_nodes.append(paragraph_to_node(block))
            case BlockType.HEADING:
                block_nodes.append(heading_to_node(block))
            case BlockType.CODE:
                block_nodes.append(code_to_node(block))
            case BlockType.QUOTE:
                block_nodes.append(quote_to_node(block))
            case BlockType.ULIST:
                block_nodes.append(ulist_to_node(block))
            case BlockType.OLIST:
                block_nodes.append(olist_to_node(block))
            case _:
                raise ValueError("invalid BlockType")
    final_node = ParentNode("div", block_nodes, None)
    return final_node

def paragraph_to_node(block):
    lines = block.split('\n')
    child_nodes = []
    paragraph = " ".join(lines)
    text_node_list = text_to_textnodes(paragraph)
    for node in text_node_list:
        leaf_node = text_node_to_html_node(node)
        child_nodes.append(leaf_node)
    return ParentNode("p", child_nodes)

def heading_to_node(block):
    sections = block.split(' ', 1)
    child_nodes = []
    count = len(sections[0])
    text_node_list = text_to_textnodes(sections[1])
    for node in text_node_list:
        leaf_node = text_node_to_html_node(node)
        child_nodes.append(leaf_node)
    f = ParentNode(f"h{count}", child_nodes)
    return f

def code_to_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("incorrect code block formatting")
    code_text = block[4:-3]
    text_node = TextNode(code_text, TextType.TEXT)
    leaf_node = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [leaf_node])
    return ParentNode("pre", [code_node])

def quote_to_node(block):
    lines = block.split('\n')
    quote_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("incorrect quote block formatting")
        quote_lines.append(line.lstrip(">").strip())
    combined_quote = " ".join(quote_lines)
    text_node_list = text_to_textnodes(combined_quote)
    child_nodes = []
    for node in text_node_list:
        leaf_node = text_node_to_html_node(node)
        child_nodes.append(leaf_node)
    f = ParentNode("blockquote", child_nodes)
    #print(f"result1: {f}")
    return f

def ulist_to_node(block):
    #print(f"ublock: {block}")
    lines = block.split('\n')
    child_nodes = []
    for line in lines:
        #print(f"ul line: {line}")
        if not line.startswith("- "):
            raise ValueError("incorrect ulist formatting")
        item_text = line.split(' ', 1)[1]
        text_node_list = text_to_textnodes(item_text)
        #print(f"tnl: {text_node_list}")
        li_children = [text_node_to_html_node(node) for node in text_node_list]
        child_nodes.append(ParentNode("li", li_children))
    #print(f"cn: {child_nodes}")
    f = ParentNode("ul", child_nodes)
    #print(f"result u: {f}")
    return f

def olist_to_node(block):
    #print(f"oblock: {block}")
    lines = block.split('\n')
    child_nodes = []
    for i in range(len(lines)):
        if not lines[i].startswith(f"{i+1}. "):
            raise ValueError("incorrect ulist formatting")
        item_text = lines[i].split(' ', 1)[1]
        text_node_list = text_to_textnodes(item_text)
        li_children = [text_node_to_html_node(node) for node in text_node_list]
        child_nodes.append(ParentNode("li", li_children))
    #print(f"cn: {child_nodes}")
    f = ParentNode("ol", child_nodes)
    #print(f"result o: {f}")
    return f











def ulist_to_node_old(block):
    #print(f"ublock: {block}")
    lines = block.split('\n')
    text_node_list = []
    child_nodes = []
    for line in lines:
        #print(f"ul line: {line}")
        if not line.startswith("- "):
            raise ValueError("incorrect ulist formatting")
        item_text = line.split(' ', 1)[1]
        text_node_list.extend(text_to_textnodes(item_text))
    #print(f"tnl: {text_node_list}")
    for node in text_node_list:
        #print(f"ulist node: {node}")
        li_node = text_node_to_html_node(node)
        child_nodes.append(ParentNode("li", [li_node]))
    #print(f"cn: {child_nodes}")
    f = ParentNode("ul", child_nodes)
    #print(f"result u: {f}")
    return f

def olist_to_node_old(block):
    #print(f"oblock: {block}")
    lines = block.split('\n')
    text_node_list = []
    child_nodes = []
    for i in range(len(lines)):
        if not lines[i].startswith(f"{i+1}. "):
            raise ValueError("incorrect ulist formatting")
        item_text = lines[i].split(' ', 1)[1]
        text_node_list.extend(text_to_textnodes(item_text))
    for node in text_node_list:
        #print(f"ulist node: {node}")
        li_node = text_node_to_html_node(node)
        child_nodes.append(ParentNode("li", [li_node]))
    #print(f"cn: {child_nodes}")
    f = ParentNode("ol", child_nodes)
    #print(f"result o: {f}")
    return f