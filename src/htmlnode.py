class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method must be implemented by subclasses")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        if not self.props:
            return ""
        
        parts = []

        for key, value in self.props.items():
            parts.append(f'{key}="{value}"')
                
        return " " + " ".join(parts)
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        


        

    
        