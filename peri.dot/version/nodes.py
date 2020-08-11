##########################################
# NODES                                  #
##########################################

class IntNode():
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return(f'I{self.token.value}')


class FloatNode():
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return(f'F{self.token.value}')


class StringNode():
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return(f'"{self.token.value}"')


class UnaryOpNode():
    def __init__(self, optoken, node):
        self.optoken = optoken
        self.node   = node

    def __repr__(self):
        return(f'({self.optoken.type} {self.node})')


class BinaryOpNode():
    def __init__(self, lnode, optoken, rnode):
        self.lnode   = lnode
        self.optoken = optoken
        self.rnode   = rnode

    def __repr__(self):
        return(f'({self.lnode} {self.optoken.type} {self.rnode})')