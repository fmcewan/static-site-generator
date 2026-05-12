from leafnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node):

    match text_node.text_type:

        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("TextType not supported.")

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []

    for node in old_nodes:
        
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter == "":
            raise ValueError("A valid delimiter has to be specified.")

        text = node.text.split(delimiter)

        if (len(text) % 2 == 0):
            raise Exception("No matching delimiter found.")
        elif (len(text) == 2):
            raise Exception("No closing delimiter.") 

        index = 0
        for section in text:
            if index % 2 == 0:
                new_nodes.append(TextNode(section, TextType.TEXT))
            elif index % 2 == 1:
                new_nodes.append(TextNode(section, text_type))

            index += 1

    return new_nodes
