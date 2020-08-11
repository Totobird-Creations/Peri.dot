##########################################
# DEPENDENCIES                           #
##########################################

from .tokens import *
from .types  import *

##########################################
# RUNTIME RESULT                         #
##########################################

class RTResult():
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error:
            self.error = res.error

        return(res.value)

    def success(self, value):
        self.value = value

        return(self)

    def failure(self, error):
        self.error = error

        return(self)

##########################################
# INTERPRETER                            #
##########################################

class Interpreter():
    def visit(self, node):
        method = f'visit_{type(node).__name__}'
        method = getattr(self, method)

        return(
            method(node)
        )


    def visit_IntNode(self, node):
        return(
            RTResult().success(
                IntType(node.token.value)
                    .setpos(node.start, node.end)
            )
        )

    def visit_FloatNode(self, node):
        return(
            RTResult().success(
                FloatType(node.token.value)
                    .setpos(node.start, node.end)
            )
        )

    def visit_StringNode(self, node):
        return(
            RTResult().success(
                StringType(node.token.value)
                    .setpos(node.start, node.end)
            )
        )

    def visit_UnaryOpNode(self, node):
        res = RTResult()
        number = res.register(self.visit(node.node))

        if res.error:
            return(res)

        error = None

        if node.optoken.type == TT_DASH:
            number, error = number.multiply(IntType(-1))

        if error:
            return(
                res.failure(
                    error
                )
            )

        return(
            res.success(
                number.setpos(
                    node.start,
                    node.end
                )
            )
        )

    def visit_BinaryOpNode(self, node):
        res = RTResult()

        left = res.register(self.visit(node.lnode))
        if res.error:
            return(res)

        right = res.register(self.visit(node.rnode))
        if res.error:
            return(res)

        if node.optoken.type == TT_PLUS:
            result, error = left.add(right)
        elif node.optoken.type == TT_DASH:
            result, error = left.subtract(right)
        elif node.optoken.type == TT_ASTRISK:
            result, error = left.multiply(right)
        elif node.optoken.type == TT_FSLASH:
            result, error = left.divide(right)
        elif node.optoken.type == TT_CARAT:
            result, error = left.raised(right)

        if error:
            return(
                res.failure(error)
            )

        return(
            res.success(
                result.setpos(
                    node.start,
                    node.end
                )
            )
        )