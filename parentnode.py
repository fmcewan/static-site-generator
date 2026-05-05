from htmlnode import HTMLNode

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(self, tag, None, children, props)

    # TODO: Implement .to_html() 
