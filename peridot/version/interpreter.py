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
        self.reset()

    def reset(self):
        self.value = None
        self.funcvalue = None
        self.error = None

    def register(self, res):
        self.error = res.error
        self.funcvalue = res.funcvalue

        return(res.value)

    def success(self, value):
        self.reset()
        self.value = value

        return(self)

    def successreturn(self, value):
        self.reset()
        self.funcvalue = value

        return(self)

    def failure(self, error):
        self.error = error

        return(self)

    def shouldreturn(self):
        return(
            self.error or self.funcvalue
        )

##########################################
# INTERPRETER                            #
##########################################

class Interpreter():
    def visit(self, node, context):
        method = f'visit_{type(node).__name__}'
        meth = method
        method = getattr(self, method)

        result = method(node, context)

        return(result)



    ### TYPES
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

            if res.shouldreturn():
                return(res)

            if type_:
                if type(elm) != type(type_):
                    return(
                        res.failure(
                            Exc_TypeError(
                                f'{TYPES["list"]} of type {type_.type} can not include {elm.type}',
                                elm.start, elm.end,
                                context,
                                elm.originstart, elm.originend, elm.origindisplay
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
                    .setpos(node.start, node.end, node.start, node.end, context.display)
            )
        )



    ### VARIABLE CONTROL
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

        value.originstart.append(value.start)
        value.originend.append(value.end)
        value.origindisplay.append(context.display)

        value.start = node.start
        value.end = node.end

        value.name = name

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

        if type(prevvalue) != type(value) and not isinstance(prevvalue, NullType):
            return(
                res.failure(
                    Exc_TypeError(
                        f'Can not assign {value.type} to \'{name}\' ({prevvalue.type})',
                        node.valnode.start, node.valnode.end,
                        context,
                        value.originstart, value.originend, value.origindisplay
                    )
                )
            )

        if res.shouldreturn():
            return(res)

        if isinstance(value, FunctionType):
            value.name = name

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

        if res.shouldreturn():
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

        if isinstance(value, FunctionType):
            value.name = name

        context.symbols.assign(name, value)

        return(
            res.success(
                value
            )
        )


    def visit_VarNullNode(self, node, context):
        res = RTResult()

        name = node.token
        if name.value in RESERVED:
            return(
                res.failure(
                    Exc_TypeError(
                        f'Can not assign {TYPES["nonetype"]} to \'{name.value}\' (reserved)',
                        name.start, name.end,
                        context
                    )
                )
            )

        context.symbols.assign(
            name.value,
            NullType()
                .setpos(node.start, node.end)
                .setcontext(context)
        )

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

        if res.shouldreturn():
            return(res)

        callnode = callnode.copy().setpos(node.start, node.end)

        if isinstance(callnode, FunctionType):
            callnode.name = name

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

            if res.shouldreturn():
                return(res)

        callvalue = callnode.value

        result = res.register(
            callnode.call(
                callvalue, args
            )
        )

        if res.shouldreturn():
            return(res)

        result = result.copy().setpos(node.start, node.end).setcontext(context)

        return(
            res.success(result)
        )
    
    def visit_VarIndicieNode(self, node, context):
        res = RTResult()

        name = node.token.value
        indicie = res.register(
            self.visit(
                node.indicie, context
            )
        )
        
        if res.shouldreturn():
            return(res)

        value = context.symbols.access(name)

        returnval, error = value.indicie(
            indicie
        )

        if error:
            return(
                res.failure(error)
            )
        
        return(
            res.success(returnval)
        )



    ### FUNCTIONS
    def visit_FuncCreateNode(self, node, context):
        res = RTResult()

        bodynodes = node.bodynodes
        argnames = [i.value for i in node.argtokens]
        funcvalue = FunctionType(bodynodes, argnames, node.shouldreturn)
        funcvalue.setcontext(context).setpos(node.start, node.end)

        return(
            res.success(funcvalue)
        )


    def visit_ReturnNode(self, node, context):
        res = RTResult()

        if not context.parent:
            return(
                res.failure(
                    Exc_ReturnError(
                        'Can not return from outside function',
                        node.start, node.end,
                        context
                    )
                )
            )

        if node.returnnode:
            value = res.register(
                self.visit(
                    node.returnnode,
                    context
                )
            )

            if res.shouldreturn():
                return(res)
        else:
            value = NullType()

        return(
            res.successreturn(value)
        )
    


    ### FLOW CONTROL
    def visit_IfNode(self, node, context):
        res = RTResult()
        #returnval = NullType().setpos(node.start, node.end).setcontext(context)

        for condition, codeblock in node.cases:
            condvalue = res.register(
                self.visit(
                    condition, context
                )
            )
            if res.shouldreturn():
                return(res)

            istrue, error = condvalue.istrue()

            if error:
                return(
                    res.failure(
                        error
                    )
                )

            if istrue:
                for j in codeblock:
                    res.register(
                        self.visit(
                            j,
                            context
                        )
                    )

                    if res.shouldreturn():
                        return(res)

                return(
                    res.success(
                        NullType()
                            .setpos(node.start, node.end)
                            .setcontext(context)
                    )
                )

        if node.elsecase:
            for i in node.elsecase:
                res.register(
                    self.visit(
                        i,
                        context
                    )
                )

                if res.shouldreturn():
                    return(res)
            
        return(
            res.success(
                NullType()
                    .setpos(node.start, node.end)
                    .setcontext(context)
            )
        )
            
            




    ### HANDLER
    def visit_HandlerNode(self, node, context):
        res = RTResult()

        for i in node.bodynodes:
            res.register(
                self.visit(
                    i,
                    context
                )
            )

            if res.error:
                error = res.error
                if isinstance(error, Exc_PanicError):
                    return(res)

                context.caughterror(error)
                exc = ExceptionType(
                    error.exc,
                    error.msg,
                    error.start
                ).setcontext(context).setpos(error.start, error.end, error.originstart, error.originend, error.origindisplay)
                return(
                    res.success(exc)
                )

            if res.shouldreturn():
                return(res)

        return(
            res.success(
                NullType()
            )
        )



    ### OPERATIONS
    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        result = res.register(
            self.visit(
                node.node,
                context
            )
        )

        if res.shouldreturn():
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
        if res.shouldreturn():
            return(res)

        right = res.register(
            self.visit(
                node.rnode,
                context
            )
        )
        if res.shouldreturn():
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
