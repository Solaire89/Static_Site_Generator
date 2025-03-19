from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        # Call parent constructor with tag and props, but no children
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode must have a value")
        if not self.tag:
            return self.value
        props_str = ""
        if self.props:
            props_str = "".join(f' {key}="{value}"' for key, value in self.props.items())
        result = f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
        return result