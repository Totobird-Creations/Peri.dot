##########################################
# NODES                                  #
##########################################

### TYPES
class IntNode():
    def __init__(self, token):
        self.token = token

        self.start = self.token.start
        self.end   = self.token.end


class FloatNode():
    def __init__(self, token):
        self.token = token

        self.start = self.token.start
        self.end   = self.token.end


class StringNode():
    def __init__(self, token):
        self.token = token

        self.start = self.token.start
        self.end   = self.token.end


class ArrayNode():
    def __init__(self, elmnodes, start, end):
        self.elmnodes = elmnodes

        self.start = start
        self.end   = end


class DictionaryNode():
    def __init__(self, keynodes, valuenodes, start, end):
        self.keynodes = keynodes
        self.valuenodes = valuenodes

        self.start = start
        self.end   = end


class TupleNode():
    def __init__(self, elmnodes, start, end):
        self.elmnodes = elmnodes

        self.start = start
        self.end   = end



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


class VarCreateNode():
    def __init__(self, token, valnode):
        self.token = token
        self.valnode = valnode

        self.start = token.start
        self.end = token.end


class VarNullNode():
    def __init__(self, token):
        self.token = token

        self.start = token.start
        self.end = token.end



### FUNCTIONS
class FuncCreateNode():
    def __init__(self, token, arguments, returntype, bodynodes, shouldreturn, end=None):
        self.token = token
        self.arguments = arguments
        self.returntype = returntype
        self.bodynodes = bodynodes
        self.shouldreturn = shouldreturn

        self.start = self.token.start
        if end:
            self.end = end
        else:
            self.end = self.token.end


class FuncCallNode():
    def __init__(self, node, calls):
        self.node = node
        self.calls = calls

        self.start = node.start
        self.end = calls[-1][2]


class ReturnNode():
    def __init__(self, returnnode, start, end):
        self.returnnode = returnnode

        self.start = start
        self.end = end



### HANDLER
class HandlerNode():
    def __init__(self, token, bodynodes):
        self.token = token
        self.bodynodes = bodynodes

        self.start = self.token.start
        self.end = self.token.end

        if len(self.bodynodes) > 0:
            self.end = self.bodynodes[-1].end


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


class SwitchNode():
    def __init__(self, vartoken, varoverwrite, value, cases, elsecase, start, end):
        self.vartoken = vartoken
        self.varoverwrite = varoverwrite
        self.value = value
        self.cases = cases
        self.elsecase = elsecase

        self.start = start
        self.end = end


class ForLoopNode():
    def __init__(self, vartoken, varoverwrite, loopthrough, bodynodes):
        self.vartoken = vartoken
        self.varoverwrite = varoverwrite
        self.loopthrough = loopthrough
        self.bodynodes = bodynodes

        self.start = self.vartoken.start

        if len(self.bodynodes) > 0:
            self.end = self.bodynodes[-1].end
        else:
            self.end = self.vartoken.end


class WhileLoopNode():
    def __init__(self, condition, bodynodes):
        self.condition = condition
        self.bodynodes = bodynodes

        self.start = self.condition.start

        if len(self.bodynodes) > 0:
            self.end = self.bodynodes[-1].end
        else:
            self.end = self.condition.end


class BreakNode():
    def __init__(self, start, end):
        self.start = start
        self.end = end


class ContinueNode():
    def __init__(self, start, end):
        self.start = start
        self.end = end



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



### MISCELLANIOUS
class IndicieNode():
    def __init__(self, node, indicies, end=None):
        self.node = node
        self.indicies = indicies
        
        self.start = self.node.start
        if end:
            self.end = end
        else:
            self.end = self.node.end


class AttributeNode():
    def __init__(self, node, attributes, end=None):
        self.node = node
        self.attributes = attributes

        self.start = self.node.start
        if end:
            self.end = end
        else:
            self.end = self.node.end



### MODULES
class IncludeNode():
    def __init__(self, filenode, start, end):
        self.filenode = filenode

        self.start = start
        self.end = end
