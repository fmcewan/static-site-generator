import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):

    def test_equal(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node1, node2)

    def test_not_equal(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not a test node", TextType.LINK)
        
        self.assertNotEqual(node1, node2)

    def test_url_equal(self):
        node1 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")

        self.assertEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
