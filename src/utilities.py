import re
from enum import Enum

from leafnode import LeafNode
from textnode import TextNode, TextType
from parentnode import ParentNode

class BlockType(Enum):
    PARAGRAPH = "paragraph" 
    HEADING = "heading" 
    CODE = "code" 
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

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

def markdown_to_blocks(text):

    return [string.strip() for string in text.split("\n\n") if string != ""]

def block_to_block_type(block):
    
    lines = block.split("\n")

    # Heading
    if block.startswith("#"):
        heading_level = 0

        for char in block:
            if char == "#":
                heading_level += 1
            else:
                break

        if 1 <= heading_level <= 6 and len(block) > heading_level and block[heading_level] == " ":
            return BlockType.HEADING

    # Code block
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Quote block
    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break

    if is_quote:
        return BlockType.QUOTE

    # Unordered list
    is_unordered = True
    for line in lines:
        if not line.startswith("- "):
            is_unordered = False
            break

    if is_unordered:
        return BlockType.UNORDERED_LIST

    # Ordered list
    is_ordered = True
    expected_num = 1

    for line in lines:
        if not line.startswith(f"{expected_num}. "):
            is_ordered = False
            break
        expected_num += 1

    if is_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def text_to_children(text):

    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return [text_node_to_html_node(node) for node in nodes]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:

            case BlockType.PARAGRAPH:
                paragraph = " ".join(block.split("\n"))
                node = ParentNode(
                    "p",
                    text_to_children(paragraph),
                )

            case BlockType.HEADING:
                level = 0

                for char in block:
                    if char == "#":
                        level += 1
                    else:
                        break

                text = block[level + 1:]

                node = ParentNode(
                    f"h{level}",
                    text_to_children(text),
                )

            case BlockType.CODE:
                text = block[4:-3]

                text_node = TextNode(text, TextType.TEXT)
                code_child = text_node_to_html_node(text_node)

                code_node = ParentNode(
                    "code",
                    [code_child],
                )

                node = ParentNode(
                    "pre",
                    [code_node],
                )

            case BlockType.QUOTE:
                lines = block.split("\n")

                cleaned = []

                for line in lines:
                    cleaned.append(line.lstrip(">").strip())

                text = " ".join(cleaned)

                node = ParentNode(
                    "blockquote",
                    text_to_children(text),
                )

            case BlockType.UNORDERED_LIST:
                items = []

                for line in block.split("\n"):
                    text = line[2:]

                    items.append(
                        ParentNode(
                            "li",
                            text_to_children(text),
                        )
                    )

                node = ParentNode("ul", items)

            case BlockType.ORDERED_LIST:
                items = []

                for line in block.split("\n"):
                    text = line.split(". ", 1)[1]

                    items.append(
                        ParentNode(
                            "li",
                            text_to_children(text),
                        )
                    )

                node = ParentNode("ol", items)

        children.append(node)

    return ParentNode("div", children)
