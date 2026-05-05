import unittest 

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_equal(self):

        node1 = LeafNode("", "", {})
        node2 = LeafNode("", "", {})

        self.assertEqual(node1, node2)
    
    def test_not_equal(self):

        node1 = LeafNode("", "",  {})
        node2 = LeafNode("a", "Hi", {"target":"_blank"})
        
        self.assertNotEqual(node1, node2)

    def test_to_html(self):

        correct_html = '<a href="https://www.google.com">Click me!</a>'
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        html  = node.to_html()

        self.assertEqual(html, correct_html)

if __name__ == "__main__":
    unittest.main()
