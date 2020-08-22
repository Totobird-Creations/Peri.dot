##########################################
# DEPENDENCIES                           #
##########################################

from .constants  import * # type: ignore
from .context    import * # type: ignore
from .exceptions import * # type: ignore
from .tokens     import * # type: ignore
from .types      import typesinit, TYPES, ArrayType, DictionaryType, ExceptionType, FloatType, FunctionType, IntType, NullType, StringType, TupleType # type: ignore

##########################################
# RUNTIME RESULT                         #
##########################################

class RTResult():
    def __init__(self):
        self.reset()

    def reset(self):
        self.value = None
        self.funcvalue = None
        self.shouldbreak = False
        self.shouldcontinue = False
        self.error = None

    def register(self, res):
        self.error = res.error
        self.funcvalue = res.funcvalue
        self.shouldbreak = res.shouldbreak
        self.shouldcontinue = res.shouldcontinue

        return(res.value)

    def success(self, value):
        self.reset()
        self.value = value

        return(self)

    def successreturn(self, value):
        self.reset()
        self.funcvalue = value

        return(self)

    def successbreak(self, value):
        self.reset()
        self.shouldbreak = value

        return(self)

    def successcontinue(self, value):
        self.reset()
        self.shouldcontinue = value

        return(self)

    def failure(self, error):
        self.error = error

        return(self)

    def shouldreturn(self):
        return(
            self.error or self.funcvalue or self.shouldbreak or self.shouldcontinue
        )

##########################################
# INTERPRETER                            #
##########################################

class Interpreter():
    def visit(self, node, context, insideloop=False):
        method = f'visit_{type(node).__name__}'
        meth = method
        method = getattr(self, method)

        result = method(node, context, insideloop=insideloop)

        return(result)



    ### TYPES
    def visit_IntNode(self, node, context, insideloop=False):
        return(
            RTResult().success(
                IntType(node.token.value)
                    .setcontext(context)
                    .setpos(node.start, node.end)
            )
        )


    def visit_FloatNode(self, node, context, insideloop=False):
        return(
            RTResult().success(
                FloatType(node.token.value)
                    .setcontext(context)
                    .setpos(node.start, node.end)
            )
        )


    def visit_StringNode(self, node, context, insideloop=False):
        return(
            RTResult().success(
                StringType(node.token.value)
                    .setcontext(context)
                    .setpos(node.start, node.end)
            )
        )


    def visit_ArrayNode(self, node, context, insideloop=False):
        res = RTResult()
        elements = []
        type_ = None
        for i in node.elmnodes:
            elm = res.register(
                self.visit(
                    i,
                    context,
                    insideloop=insideloop
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
                    .setpos(node.start, node.end)
            )
        )


    def visit_TupleNode(self, node, context, insideloop=False):
        res = RTResult()
        elements = []
        for i in node.elmnodes:
            elm = res.register(
                self.visit(
                    i,
                    context,
                    insideloop=insideloop
                )
            )

            if res.shouldreturn():
                return(res)

            elements.append(elm)

        return(
            res.success(
                TupleType(tuple(elements))
                    .setcontext(context)
                    .setpos(node.start, node.end)
            )
        )


    def visit_DictionaryNode(self, node, context, insideloop=False):
        res = RTResult()
        elements = {}
        keytype = None
        valuetype = None
        for i in range(len(node.keynodes)):
            key = res.register(
                self.visit(
                    node.keynodes[i],
                    context,
                    insideloop=insideloop
                )
            )

            if res.shouldreturn():
                return(res)

            value = res.register(
                self.visit(
                    node.valuenodes[i],
                    context,
                    insideloop=insideloop
                )
            )

            if keytype:
                if type(key) != type(keytype):
                    return(
                        res.failure(
                            Exc_TypeError(
                                f'{TYPES["dictionary"]} keys of type {keytype.type} can not include {key.type}',
                                key.start, key.end,
                                context,
                                key.originstart, key.originend, key.origindisplay
                            )
                        )
                    )
            else:
                keytype = key

            if valuetype:
                if type(value) != type(valuetype):
                    return(
                        res.failure(
                            Exc_TypeError(
                                f'{TYPES["dictionary"]} of type {valuetype.type} can not include {value.type}',
                                value.start, value.end,
                                context,
                                value.originstart, value.originend, value.origindisplay
                            )
                        )
                    )
            else:
                valuetype = value

            if res.shouldreturn():
                return(res)

            elements[key] = value

        return(
            res.success(
                DictionaryType(elements)
                    .setcontext(context)
                    .setpos(node.start, node.end)
            )
        )



    ### VARIABLE CONTROL
    def visit_VarAccessNode(self, node, context, insideloop=False):
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


    def visit_VarAssignNode(self, node, context, insideloop=False):
        res = RTResult()

        name = node.token.value

        value = res.register(
            self.visit(
                node.valnode,
                context,
                    insideloop=insideloop
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

        if name in RESERVED or prevvalue.reserved:
            return(
                res.failure(
                    Exc_TypeError(
                        f'Can not assign {value.type} to \'{name}\' (reserved)',
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


    def visit_VarCreateNode(self, node, context, insideloop=False):
        res = RTResult()

        name = node.token.value
        value = res.register(
            self.visit(
                node.valnode,
                context,
                insideloop=insideloop
            )
        )

        if res.shouldreturn():
            return(res)

        prevvalue = context.symbols.access(name)

        if prevvalue:
            if name in RESERVED or prevvalue.reserved:
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


    def visit_VarNullNode(self, node, context, insideloop=False):
        res = RTResult()

        name = node.token

        prevvalue = context.symbols.access(name)

        if prevvalue:
            if name in RESERVED or prevvalue.reserved:
                return(
                    res.failure(
                        Exc_TypeError(
                            f'Can not assign {TYPES["nonetype"]} to \'{name}\' (reserved)',
                            node.start, node.end,
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
                    .setpos(node.start, node.end)
                    .setcontext(context)
            )
        )

    def visit_VarCallNode(self, node, context, insideloop=False):
        res = RTResult()

        name = node.name
        argnodes = node.argnodes
        options = node.optionnodes

        callnode = res.register(
            self.visit(
                node.node,
                context,
                insideloop=insideloop
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
                        context,
                        insideloop=insideloop
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



    ### FUNCTIONS
    def visit_FuncCreateNode(self, node, context, insideloop=False):
        res = RTResult()

        bodynodes = node.bodynodes
        argnames = [i.value for i in node.argtokens]
        funcvalue = FunctionType(bodynodes, argnames, node.shouldreturn)
        funcvalue.setcontext(context).setpos(node.start, node.end)

        return(
            res.success(funcvalue)
        )


    def visit_ReturnNode(self, node, context, insideloop=False):
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
                    context,
                    insideloop=insideloop
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
    def visit_IfNode(self, node, context, insideloop=False):
        res = RTResult()
        #returnval = NullType().setpos(node.start, node.end).setcontext(context)

        for condition, codeblock in node.cases:
            condvalue = res.register(
                self.visit(
                    condition,
                    context,
                    insideloop=insideloop
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
                            context,
                            insideloop=insideloop
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
                        context,
                        insideloop=insideloop
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


    def visit_SwitchNode(self, node, context, insideloop=False):
        res = RTResult()

        varname = node.vartoken.value
        value = res.register(
            self.visit(
                node.value,
                context,
                insideloop=insideloop
            )
        )

        if res.shouldreturn():
            return(res)

        prevvalue = context.symbols.access(varname)
        if not node.varoverwrite and not prevvalue:
            return(
                res.failure(
                    Exc_IdentifierError(
                        f'\'{varname}\' is not defined',
                        node.vartoken.start, node.vartoken.end,
                        context
                    )
                )
            )
        if type(value) != type(prevvalue) and not node.varoverwrite:
            return(
                res.failure(
                    Exc_TypeError(
                        f'Can not assign {value.type} to \'{varname}\' ({prevvalue.type})',
                        value.start, value.end,
                        context,
                        value.originstart, value.originend, value.origindisplay
                    )
                )
            )

        value.reserved = True

        exec_symbols = SymbolTable(context.symbols.parent)
        exec_symbols.assign(varname, value)
        exec_context = Context(context.display, exec_symbols, context.parent, context.parententry)

        context.symbols.assign(varname, value)

        for condition, codeblock in node.cases:
            condvalue = res.register(
                self.visit(
                    condition,
                    exec_context,
                    insideloop=insideloop
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
                            context,
                            insideloop=insideloop
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
                        context,
                        insideloop=insideloop
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


    def visit_ForLoopNode(self, node, context, insideloop=False):
        res = RTResult()

        varname = node.vartoken.value

        loopthrough = res.register(
            self.visit(
                node.loopthrough,
                context,
                insideloop=insideloop
            )
        )

        if res.shouldreturn():
            return(res)

        prevvalue = context.symbols.access(varname)
        if not node.varoverwrite and not prevvalue:
            return(
                res.failure(
                    Exc_IdentifierError(
                        f'\'{varname}\' is not defined',
                        node.vartoken.start, node.vartoken.end,
                        context
                    )
                )
            )

        try:
            shouldbreak = False
            for i in loopthrough.value:
                if type(i) != type(prevvalue) and not node.varoverwrite:
                    return(
                        res.failure(
                            Exc_TypeError(
                                f'Can not assign {i.type} to \'{varname}\' ({prevvalue.type})',
                                i.start, i.end,
                                context,
                                i.originstart, i.originend, i.origindisplay
                            )
                        )
                    )

                i.reserved = True
                context.symbols.assign(varname, i)

                for j in node.bodynodes:
                    res.register(
                        self.visit(
                            j,
                            context,
                            insideloop=True
                        )
                    )

                    if res.error:
                        return(res)

                    if res.shouldbreak:
                        shouldbreak = True
                        break
                
                    if res.shouldcontinue:
                        break

                if shouldbreak:
                    break

        except TypeError:
            return(
                res.failure(
                    Exc_IterationError(
                        f'{loopthrough.type} is not iterable',
                        loopthrough.start, loopthrough.end,
                        context
                    )
                )
            )

        return(
            res.success(
                NullType()
                    .setpos(node.start, node.end)
                    .setcontext(context)
            )
        )


    def visit_WhileLoopNode(self, node, context, insideloop=False):
        res = RTResult()

        while True:
            condition = res.register(
                self.visit(
                    node.condition,
                    context,
                    insideloop=insideloop
                )
            )

            if res.error:
                return(res)

            istrue, error = condition.istrue()

            if error:
                return(
                    res.failure(error)
                )

            if not istrue: break

            for j in node.bodynodes:
                res.register(
                    self.visit(
                        j,
                        context,
                        insideloop=insideloop
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


    def visit_BreakNode(self, node, context, insideloop=False):
        res = RTResult()

        if not insideloop:
            return(
                res.failure(
                    Exc_BreakError(
                        'Can not break from outside loop',
                        node.start, node.end,
                        context
                    )
                )
            )

        res.successbreak(True)

        return(res)


    def visit_ContinueNode(self, node, context, insideloop=False):
        res = RTResult()

        if not insideloop:
            return(
                res.failure(
                    Exc_ContinueError(
                        'Can not continue from outside loop',
                        node.start, node.end,
                        context
                    )
                )
            )

        res.successcontinue(True)

        return(res)



    ### HANDLER
    def visit_HandlerNode(self, node, context, insideloop=False):
        res = RTResult()

        for i in node.bodynodes:
            res.register(
                self.visit(
                    i,
                    context,
                    insideloop=insideloop
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
    def visit_UnaryOpNode(self, node, context, insideloop=False):
        res = RTResult()
        result = res.register(
            self.visit(
                node.node,
                context,
                insideloop=insideloop
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


    def visit_BinaryOpNode(self, node, context, insideloop=False):
        res = RTResult()

        left = res.register(
            self.visit(
                node.lnode,
                context,
                insideloop=insideloop
            )
        )
        if res.shouldreturn():
            return(res)

        right = res.register(
            self.visit(
                node.rnode,
                context,
                insideloop=insideloop
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



    ### MISCELLANIOUS
    def visit_IndicieNode(self, node, context, insideloop=False):
        res = RTResult()

        value = res.register(
            self.visit(
                node.node,
                context,
                insideloop=insideloop
            )
        )

        if res.shouldreturn():
            return(res)

        for i in node.indicies:
            i = res.register(
                self.visit(
                    i,
                    context,
                    insideloop=insideloop
                )
            )

            value, error = value.indicie(i)

            if error:
                return(
                    res.failure(
                        error
                    )
                )

        return(
            res.success(value)
        )

typesinit(Interpreter)
