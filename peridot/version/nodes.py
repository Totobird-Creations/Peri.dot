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
    def __init__(self, token, valnode):
        self.token = token
        self.valnode = valnode

        self.start = token.start
        self.end = token.end

    def __repr__(self):
        return(f'{self.token.value}:{self.valnode}')


class VarCreateNode():
    def __init__(self, token, valnode):
        self.token = token
        self.valnode = valnode

        self.start = token.start
        self.end = token.end

    def __repr__(self):
        return(f'{self.token.value}={self.valnode}')


class VarNullNode():
    def __init__(self, token):
        self.token = token

        self.start = token.start
        self.end = token.end

    def __repr__(self):
        return(f'{self.token.value}=Null')


class VarCallNode():
    def __init__(self, node, argnodes, optionnodes):
        self.node = node
        self.name = self.node.token.value
        self.argnodes = argnodes
        self.optionnodes = optionnodes

        self.start = node.start
        self.end = node.end

    def __repr__(self):
        return(f'{self.node.token.value}()')


class FuncCreateNode():
    def __init__(self, argtokens, bodynodes):
        self.argtokens = argtokens
        self.bodynodes = bodynodes

        if len(self.argtokens) > 0:
            self.start = self.argtokens[0].start
        elif len(self.bodynodes) > 0:
            self.start = self.bodynodes[0].start

        if len(self.bodynodes) > 0:
            self.end = self.bodynodes[-1].end

    def __repr__(self):
        return(f'<Function>')



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