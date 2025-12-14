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