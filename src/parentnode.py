from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode missing required tag")
        if not self.children:
            raise ValueError("ParentNode missing required children")
    # Start with opening tag (don't forget props if they exist!)
        html = f"<{self.tag}{self.props_to_html()}>"
    # Add each child's HTML (this is where recursion happens)
        child_html = ""
        for child in self.children:
            # Add each child's HTML to the parent
            html += child.to_html()
        # Add closing tag
        html += f"</{self.tag}>"
        return html
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
