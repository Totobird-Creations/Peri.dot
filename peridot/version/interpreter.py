##########################################
# DEPENDENCIES                           #
##########################################

from .constants  import * # type: ignore
from .exceptions import * # type: ignore
from .tokens     import * # type: ignore
from .types      import typesinit, TYPES, ArrayType, BooleanType, ExceptionType, FloatType, FunctionType, IntType, NullType, StringType # type: ignore

##########################################
# RUNTIME RESULT                         #
##########################################

class RTResult():
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if isinstance(res, tuple):
            if res[1]:
                self.error = res[1]

            return(res[1])

        else:
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


    def visit_ArrayNode(self, node, context):
        res = RTResult()
        elements = []
        type_ = None
        for i in node.elmnodes:
            elm = res.register(
                self.visit(
                    i,
                    context
                )
            )

            if res.error:
                return(res)

            if type_:
                if type(elm) != type(type_):
                    return(
                        res.failure(
                            Exc_TypeError(
                                f'{TYPES["list"]} of type {type_.type} can not include {elm.type}',
                                elm.start, elm.end,
                                context
                            )
                        )
                    )
            else:
                type_ = elm

            elements.append(elm)

        return(
            res.success(
                ArrayType(elements)
                    .setcontext(context)
                    .setpos(node.start, node.end)
            )
        )



    def visit_VarAccessNode(self, node, context):
        res = RTResult()

        name = node.token.value
        value = context.symbols.access(name)

        if not value:
            return(
                res.failure(
                    Exc_IdentifierError(
                        f'\'{name}\' is not defined',
                        node.start, node.end,
                        context
                    )
                )
            )

        value = value.copy().setcontext(context)

        value.start = node.start
        value.end = node.end

        return(
            res.success(
                value
            )
        )


    def visit_VarAssignNode(self, node, context):
        res = RTResult()

        name = node.token.value

        value = res.register(
            self.visit(
                node.valnode,
                context
            )
        )

        if name in RESERVED:
            return(
                res.failure(
                    Exc_TypeError(
                        f'Can not assign {value.type} to \'{name}\' (reserved)',
                        node.start, node.end,
                        context
                    )
                )
            )

        prevvalue = context.symbols.access(name)

        if not prevvalue:
            return(
                res.failure(
                    Exc_IdentifierError(
                        f'\'{name}\' is not defined',
                        node.start, node.end,
                        context
                    )
                )
            )

        if type(prevvalue) != type(value):
            return(
                res.failure(
                    Exc_TypeError(
                        f'Can not assign {value.type} to \'{name}\' ({prevvalue.type})',
                        node.valnode.token.start, node.valnode.token.end,
                        context
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

        name = node.token.value
        value = res.register(
            self.visit(
                node.valnode,
                context
            )
        )

        if res.error:
            return(res)

        if name in RESERVED:
            return(
                res.failure(
                    Exc_TypeError(
                        f'Can not assign {value.type} to \'{name}\' (reserved)',
                        node.start, node.end,
                        context
                    )
                )
            )

        context.symbols.assign(name, value)

        return(
            res.success(
                value
            )
        )


    def visit_VarNullNode(self, node, context):
        res = RTResult()

        for i in node.tokens:
            name = i.value

            if name in RESERVED:
                return(
                    res.failure(
                        Exc_TypeError(
                            f'Can not assign {TYPES["nonetype"]} to \'{name}\' (reserved)',
                            i.start, i.end,
                            context
                        )
                    )
                )

            context.symbols.assign(name, NullType())

        return(
            res.success(
                NullType()
            )
        )

    def visit_VarCallNode(self, node, context):
        res = RTResult()

        name = node.name
        argnodes = node.argnodes
        options = node.optionnodes

        callnode = res.register(
            self.visit(
                node.node, context
            )
        )

        if res.error:
            return(res)

        callnode = callnode.copy().setpos(node.start, node.end)

        args = []
        for argnode in argnodes:
            args.append(
                res.register(
                    self.visit(
                        argnode,
                        context
                    )
                )
            )

            if res.error:
                return(res)

        result = res.register(
            callnode.call(name, args)
        )

        if res.error:
            return(res)

        result = result.copy().setpos(node.start, node.end).setcontext(context)

        return(
            res.success(result)
        )


    def visit_FuncCreateNode(self, node, context):
        res = RTResult()

        bodynodes = node.bodynodes
        argnames = [i.value for i in node.argtokens]
        funcvalue = FunctionType(bodynodes, argnames)
        funcvalue.setcontext(context).setpos(node.start, node.end)

        return(
            res.success(funcvalue)
        )



    def visit_HandlerNode(self, node, context):
        res = RTResult()

        for i in node.bodynodes:
            bodyresult = self.visit(
                i, context
            )

            if bodyresult.error:
                error = bodyresult.error
                return(
                    res.success(
                        ExceptionType(
                            error.exc,
                            error.msg,
                            error.start
                        )
                    )
                )

        return(res.success(NullType()))



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
            result, error = result.not_()

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
            result, error = left.lessthan(right)
        elif node.optoken.type == TT_GREATERTHAN:
            result, error = left.greaterthan(right)
        elif node.optoken.type == TT_LTEQUALS:
            result, error = left.ltequals(right)
        elif node.optoken.type == TT_GTEQUALS:
            result, error = left.gtequals(right)
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

typesinit(Interpreter)
