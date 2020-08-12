##########################################
# NODES                                  #
##########################################

class IntNode():
    def __init__(self, token):
        self.token = token

        self.start = self.token.start
        self.end   = self.token.end

    def __repr__(self):
        return(f'{self.token.value}')


class FloatNode():
    def __init__(self, token):
        self.token = token

        self.start = self.token.start
        self.end   = self.token.end

    def __repr__(self):
        return(f'{self.token.value}')


class StringNode():
    def __init__(self, token):
        self.token = token

        self.start = self.token.start
        self.end   = self.token.end

    def __repr__(self):
        return(f'"{self.token.value}"')



class VarAccessNode():
    def __init__(self, token):
        self.token = token

        self.start = self.token.start
        self.end   = self.token.end

    def __repr__(self):
        return(f'{self.token.value}')


class VarAssignNode():
    def __init__(self, tokens, valnode):
        self.tokens = tokens
        self.valnode = valnode

        self.start = []
        self.end = []
        for i in self.tokens:
            self.start.append(i.start)
            self.end.append  (i.end)

    def __repr__(self):
        return(f'{self.token.value}:{self.valnode}')


class VarCreateNode():
    def __init__(self, tokens, valnode):
        self.tokens = tokens
        self.valnode = valnode

        self.start = []
        self.end = []
        for i in self.tokens:
            self.start.append(i.start)
            self.end.append  (i.end)

    def __repr__(self):
        return(f'{self.token.value}={self.valnode}')


class VarNullNode():
    def __init__(self, tokens):
        self.tokens = tokens

        self.start = []
        self.end = []
        for i in self.tokens:
            self.start.append(i.start)
            self.end.append  (i.end)

    def __repr__(self):
        return(f'{self.token.value}=Null')



class UnaryOpNode():
    def __init__(self, optoken, node):
        self.optoken = optoken
        self.node   = node

        self.start = self.optoken.start
        self.end   = self.node.end

    def __repr__(self):
        return(f'({self.optoken.type} {self.node})')


class BinaryOpNode():
    def __init__(self, lnode, optoken, rnode):
        self.lnode   = lnode
        self.optoken = optoken
        self.rnode   = rnode

        self.start = self.lnode.start
        self.end   = self.rnode.end

    def __repr__(self):
        return(f'({self.lnode} {self.optoken.type} {self.rnode})')