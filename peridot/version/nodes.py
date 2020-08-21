##########################################
# NODES                                  #
##########################################

### TYPES
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


class ArrayNode():
    def __init__(self, elmnodes, start, end):
        self.elmnodes = elmnodes

        self.start = start
        self.end   = end

    def __repr__(self):
        return(f'"{self.token.value}"')



### VARIABLE CONTROL
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
        return(f'VarAssign:{self.token.value}={self.valnode}')


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
        return(f'VarNull:{self.token.value}')


class VarCallNode():
    def __init__(self, node, argnodes, optionnodes, end=None):
        self.node = node
        self.name = self.node.token.value
        self.argnodes = argnodes
        self.optionnodes = optionnodes

        self.start = node.start
        if end:
            self.end = end
        else:
            self.end = node.end

    def __repr__(self):
        return(f'VarCall:{self.node.token.value}')



### FUNCTIONS
class FuncCreateNode():
    def __init__(self, token, argtokens, bodynodes, shouldreturn):
        self.token = token
        self.argtokens = argtokens
        self.bodynodes = bodynodes
        self.shouldreturn = shouldreturn

        self.start = self.token.start
        self.end = self.token.end

        if len(self.bodynodes) > 0:
            self.end = self.bodynodes[-1].end

    def __repr__(self):
        return(f'Function')


class ReturnNode():
    def __init__(self, returnnode, start, end):
        self.returnnode = returnnode

        self.start = start
        self.end = end

    def __repr__(self):
        return(f'Return:{self.returnnode}')



### HANDLER
class HandlerNode():
    def __init__(self, token, bodynodes):
        self.token = token
        self.bodynodes = bodynodes

        self.start = self.token.start
        self.end = self.token.end

        if len(self.bodynodes) > 0:
            self.end = self.bodynodes[-1].end

    def __repr__(self):
        return(f'Handler')


### FLOW CONTROL
class IfNode():
    def __init__(self, cases, elsecase):
        self.cases = cases
        self.elsecase = elsecase

        self.start = self.cases[0][0].start
        if self.elsecase:
            self.end = self.elsecase[-1].end
        else:
            self.end = self.cases[-1][0].end



### OPERATIONS
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