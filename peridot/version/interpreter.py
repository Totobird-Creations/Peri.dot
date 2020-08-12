##########################################
# DEPENDENCIES                           #
##########################################

from .constants  import *
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
    def visit(self, node, context):
        method = f'visit_{type(node).__name__}'
        method = getattr(self, method)

        return(
            method(node, context)
        )



    def visit_IntNode(self, node, context):
        return(
            RTResult().success(
                IntType(node.token.value)
                    .setcontext(context)
                    .setpos(node.start, node.end)
            )
        )


    def visit_FloatNode(self, node, context):
        return(
            RTResult().success(
                FloatType(node.token.value)
                    .setcontext(context)
                    .setpos(node.start, node.end)
            )
        )


    def visit_StringNode(self, node, context):
        return(
            RTResult().success(
                StringType(node.token.value)
                    .setcontext(context)
                    .setpos(node.start, node.end)
            )
        )



    def visit_VarAccessNode(self, node, context):
        res = RTResult()

        name = node.token.value

        value = BUILTINS.get(name, None)
        if value:
            return(
                res.success(
                    value
                )
            )

        value = context.symbols.access(name)

        if not value:
            return(
                res.failure(
                    Exc_IdentifierError(
                        f'\'{name}\' is not defined',
                        node.token.start, node.token.end
                    )
                )
            )

        return(
            res.success(
                value
            )
        )


    def visit_VarAssignNode(self, node, context):
        res = RTResult()

        for name in [i.value for i in node.tokens]:
            prevvalue = context.symbols.access(name)

            if not prevvalue:
                return(
                    res.failure(
                        Exc_IdentifierError(
                            f'\'{name}\' is not defined',
                            node.token.start, node.token.end
                        )
                    )
                )

            value = res.register(
                self.visit(
                    node.valnode,
                    context
                )
            )

            if type(prevvalue) != type(value):
                return(
                    res.failure(
                        Exc_TypeError(
                            f'Can not assign {value.type} to \'{name}\' ({prevvalue.type})',
                            node.valnode.token.start, node.valnode.token.end
                        )
                    )
                )

            if res.error:
                return(res)

            context.symbols.assign(name, value)

        return(
            res.success(
                value
            )
        )


    def visit_VarCreateNode(self, node, context):
        res = RTResult()

        for name in [i.value for i in node.tokens]:
            value = res.register(
                self.visit(
                    node.valnode,
                    context
                )
            )

            if res.error:
                return(res)

            context.symbols.assign(name, value)

        return(
            res.success(
                value
            )
        )


    def visit_VarNullNode(self, node, context):
        res = RTResult()

        for name in [i.value for i in node.tokens]:
            context.symbols.assign(name, NullType())

        return(
            res.success(
                NullType()
            )
        )



    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        result = res.register(
            self.visit(
                node.node,
                context
            )
        )

        if res.error:
            return(res)

        error = None

        if node.optoken.type == TT_DASH:
            result, error = result.multiply(IntType(-1))
        elif node.optoken.matches(TT_KEYWORD, KEYWORDS['logicalnot']):
            result, error = result.not_(IntType(-1))

        if error:
            return(
                res.failure(
                    error
                )
            )

        return(
            res.success(
                result.setpos(
                    node.start,
                    node.end
                )
            )
        )


    def visit_BinaryOpNode(self, node, context):
        res = RTResult()

        left = res.register(
            self.visit(
                node.lnode,
                context
            )
        )
        if res.error:
            return(res)

        right = res.register(
            self.visit(
                node.rnode,
                context
            )
        )
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
        elif node.optoken.type == TT_EQEQUALS:
            result, error = left.eqequals(right)
        elif node.optoken.type == TT_BANGEQUALS:
            result, error = left.bangequals(right)
        elif node.optoken.type == TT_LESSTHAN:
            result, error = left.eqequals(right)
        elif node.optoken.type == TT_GREATERTHAN:
            result, error = left.eqequals(right)
        elif node.optoken.type == TT_LTEQUALS:
            result, error = left.eqequals(right)
        elif node.optoken.type == TT_GTEQUALS:
            result, error = left.eqequals(right)
        elif node.optoken.matches(TT_KEYWORD, KEYWORDS['logicaland']):
            result, error = left.and_(right)
        elif node.optoken.matches(TT_KEYWORD, KEYWORDS['logicalor']):
            result, error = left.or_(right)

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