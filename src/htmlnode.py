
class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        html_string = ""

        if self.props == None:
            return html_string

        for key, value in self.props.items():
            html_string += f' {key}="{value}"'

        return html_string
    
    def __repr__(self):
        return f"tag: {self.tag}\n value: {self.value}\n children: {self.children}\n props: {self.props}"
    
class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        
        if self.tag == None:
            return self.value
        
        if self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        
        prop_string = self.props_to_html()
        return f"<{self.tag}{prop_string}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent node must have a tag")
        
        if self.children == None:
            raise ValueError("Parent node must have children")
        

        full_html = f"<{self.tag}>" if self.props == None else f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            full_html += child.to_html()

        full_html += f"</{self.tag}>"

        return full_html