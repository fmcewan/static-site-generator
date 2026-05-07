from htmlnode import HTMLNode

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):

        if (self.tag == None):
            raise ValueError("ParentNode object does not have a tag.")
        if (self.children == None):
            raise ValueError("ParentNode object does not have children.")

        html = ""
        for child in self.children:
            html += child.to_html()
        
        html = f"<{self.tag}>{html}</{self.tag}>"


        return html 

