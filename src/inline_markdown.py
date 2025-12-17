import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
        else:
            wip_nodes = node.text.split(delimiter)
            if len(wip_nodes) % 2 == 0:
                raise Exception("Closing delimiter not found")
            for i in range(len(wip_nodes)):
                if wip_nodes[i] == "":
                    continue
                if i % 2 == 0:
                    result.append(TextNode(wip_nodes[i], TextType.TEXT))
                else:
                    result.append(TextNode(wip_nodes[i], text_type))
    return result

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        og_text = node.text

        extracted = extract_markdown_images(og_text)
        if len(extracted) == 0:
            result.append(node)
            continue

        for img in extracted:
            split_on_img = og_text.split(f"![{img[0]}]({img[1]})", 1)

            if len(img) != 2:
                raise Exception("invalid image markdown")
            if split_on_img[0] != "":
                result.append(TextNode(split_on_img[0], TextType.TEXT))
            result.append(TextNode(img[0], TextType.IMAGE, img[1]))
            og_text = split_on_img[1]
        if og_text != "":
            result.append(TextNode(og_text, TextType.TEXT))
    return result

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        og_text = node.text

        extracted = extract_markdown_links(og_text)
        if len(extracted) == 0:
            result.append(node)
            continue

        for link in extracted:
            split_on_link = og_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(link) != 2:
                raise Exception("invalid link markdown")
            if split_on_link[0] != "":
                result.append(TextNode(split_on_link[0], TextType.TEXT))
            result.append(TextNode(link[0], TextType.LINK, link[1]))
            og_text = split_on_link[1]
        if og_text != "":
            result.append(TextNode(og_text, TextType.TEXT))
    return result