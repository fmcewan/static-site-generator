import re

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

import re

def split_nodes_image(old_nodes):

    new_nodes = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text

        matches = extract_markdown_images(text)

        if not matches:
            new_nodes.append(node)
            continue

        remaining = text

        for alt, url in matches:

            markdown = f"![{alt}]({url})"

            parts = remaining.split(markdown, 1)

            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(
                TextNode(alt, TextType.IMAGE, url)
            )

            remaining = parts[1]

        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):

    new_nodes = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text

        matches = extract_markdown_links(text)

        if not matches:
            new_nodes.append(node)
            continue

        remaining = text

        for link_text, url in matches:

            markdown = f"[{link_text}]({url})"

            parts = remaining.split(markdown, 1)

            if parts[0] != "":
                new_nodes.append(
                    TextNode(parts[0], TextType.TEXT)
                )

            new_nodes.append(
                TextNode(link_text, TextType.LINK, url)
            )

            remaining = parts[1]

        if remaining != "":
            new_nodes.append(
                TextNode(remaining, TextType.TEXT)
            )

    return new_nodes

def extract_markdown_images(text):

    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
