class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if not self.props:
            return ""
        props_string = []
        for key, value in self.props.items():
            strings = f'{key}="{value}"'
            props_string.append(strings)
        return " " + " ".join(props_string)
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        return (self.tag == other.tag 
                and self.value == other.value 
                and self.children == other.children 
                and self.props == other.props)
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode requires a value to render")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
    def __eq__(self, other):
        return (self.tag == other.tag 
                and self.value == other.value 
                and self.props == other.props)
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("You have not provided Tag")
        elif self.children is None:
            raise ValueError("You have not provided Children")
        else:
            string_storage = f"<{self.tag}>"
            for child in self.children:
                string_storage += f"{child.to_html()}"
            return string_storage + f"</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
