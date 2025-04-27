from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        print(f"Creating LeafNode: tag='{tag}', value='{value}'")
        # Call parent constructor with tag and props, but no children
        super().__init__(tag, value, None, props)
        if value is None:
            value = ""  # Set empty string instead of None

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if not self.tag:
            return self.value
        props_str = ""
        if self.props:
            props_str = "".join(f' {key}="{value}"' for key, value in self.props.items())
        result = f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
        return result
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"