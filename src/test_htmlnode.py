import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_equal(self):

        node1 = HTMLNode("", "", [], {})
        node2 = HTMLNode("", "", [], {})

        self.assertEqual(node1, node2)
    
    def test_not_equal(self):

        node1 = HTMLNode("", "", [], {})
        node2 = HTMLNode("a", "Hi", [node1], {"target":"_blank"})

        self.assertNotEqual(node1, node2)

    def test_html_to_props(self):

        correct_html = ' href="https://www.google.com" target="_blank"'
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props = props)
        html  = node.props_to_html()

        self.assertEqual(html, correct_html)

if __name__ == "__main__":
    unittest.main()
