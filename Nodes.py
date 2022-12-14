import Functions
class KeyNode:        
    #node means node type, didn't want to udse type since that's a keyword
    def __init__(self, id=None, text=None, previous=None, no=None, yes=None, node_type=None):
        self.id = id
        self.text = text
        self.previous = previous
        self.no = no
        self.yes = yes
        self.node_type = node_type