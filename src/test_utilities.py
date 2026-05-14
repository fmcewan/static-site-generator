import unittest 

from utilities import *
from textnode import TextNode, TextType
from parentnode import ParentNode

class TestUtilities(unittest.TestCase):

    # Conversion tests
    def test_text(self):

        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):

        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node") 
    
    def test_italic(self):

        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):

        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")   

    def test_link(self):

        node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self):

        node = TextNode("This is an image node", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.google.com", "alt": "This is an image node"})

    # Delimiter tests
    def test_nodes_delimiter_text(self):

        node = TextNode("This is a text node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], ",", TextType.BOLD)

        correct_new_nodes = [
            TextNode("This is a text node", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, correct_new_nodes)
    
    def test_nodes_delimiter_bold(self):
    
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        correct_new_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, correct_new_nodes)

    def test_nodes_delimiter_italic(self):
        
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

        correct_new_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, correct_new_nodes)
    
    def test_nodes_delimiter_code(self):
        
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        correct_new_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ] 

        self.assertEqual(new_nodes, correct_new_nodes)

    def test_nodes_images(self):
        
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        
        new_nodes = split_nodes_image([node])
        
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
        new_nodes,
        )    

    def test_nodes_links(self):

        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube",
                    TextType.LINK,
                    "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        ) 

    # Image and link extraction tests 

    def test_markdown_images(self):
        
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)

        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], images)

    def test_markdown_links(self):
        
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], links)
    
    # Markdown blocks 

    def test_markdown_to_blocks(self):
        
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_paragraph(self):
        block = "This is a normal paragraph."
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_heading_h1(self):
        block = "# Heading"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING,
        )

    def test_heading_h6(self):
        block = "###### Small Heading"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING,
        )

    def test_invalid_heading_no_space(self):
        block = "##Invalid heading"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_invalid_heading_too_many_hashes(self):
        block = "####### Too many hashes"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_code_block(self):
        block = "```\ndef hello():\n    print('hi')\n```"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_quote_block(self):
        block = ">This is a quote\n>another quote line"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_quote_block_with_spaces(self):
        block = "> This is a quote\n> another quote line"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_unordered_list(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST,
        )

    def test_invalid_unordered_list(self):
        block = "- item one\nitem two"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_invalid_ordered_list_wrong_order(self):
        block = "1. first\n3. second\n4. third"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_invalid_ordered_list_not_starting_at_one(self):
        block = "2. second\n3. third"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )


    def test_mtohtml_paragraph(self):
        md = "This is a paragraph."

        node = markdown_to_html_node(md)

        html = node.to_html()

        self.assertEqual(
            html,
            "<div><p>This is a paragraph.</p></div>"
        )

    def test_mtohtml_heading(self):
        md = "# Heading"

        node = markdown_to_html_node(md)

        html = node.to_html()

        self.assertEqual(
            html,
            "<div><h1>Heading</h1></div>"
        )

    def test_mtohtml_code_block(self):
        md = "```\ncode block\n```"

        node = markdown_to_html_node(md)

        html = node.to_html()

        self.assertEqual(
            html,
            "<div><pre><code>code block\n</code></pre></div>"
        )

    def test_mtohtml_quote_block(self):
        md = "> quote line 1\n> quote line 2"

        node = markdown_to_html_node(md)

        html = node.to_html()

        self.assertEqual(
            html,
            "<div><blockquote>quote line 1 quote line 2</blockquote></div>"
        )

    def test_mtohtml_unordered_list(self):
        md = "- item 1\n- item 2"

        node = markdown_to_html_node(md)

        html = node.to_html()

        self.assertEqual(
            html,
            "<div><ul><li>item 1</li><li>item 2</li></ul></div>"
        )

    def test_mtohtml_ordered_list(self):
        md = "1. first\n2. second"

        node = markdown_to_html_node(md)

        html = node.to_html()

        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second</li></ol></div>"
        )

    def test_mtohtml_multiple_blocks(self):
        md = """
# Heading

This is a paragraph.

- item 1
- item 2
""".strip()

        node = markdown_to_html_node(md)

        html = node.to_html()

        self.assertEqual(
            html,
            (
                "<div>"
                "<h1>Heading</h1>"
                "<p>This is a paragraph.</p>"
                "<ul><li>item 1</li><li>item 2</li></ul>"
                "</div>"
            )
        )
    
if __name__ == "__main__":
    unittest.main()
