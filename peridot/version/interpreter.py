##########################################
# DEPENDENCIES                           #
##########################################

from pathlib import Path as _Path
from importlib import import_module as _import_module
import re as _re

def _interpreterinit(conf, tokens, context, default, constants, types, exceptions, runu, perimodu):
    global lang
    lang = conf
    global TT_ASTRISK, TT_BANGEQUALS, TT_CARAT, TT_DASH, TT_EQEQUALS, TT_FSLASH, TT_GREATERTHAN, TT_GTEQUALS, TT_KEYWORD, TT_LESSTHAN, TT_LTEQUALS, TT_PLUS
    TT_ASTRISK          = tokens.TT_ASTRISK
    TT_BANGEQUALS       = tokens.TT_BANGEQUALS
    TT_CARAT            = tokens.TT_CARAT
    TT_DASH             = tokens.TT_DASH
    TT_EQEQUALS         = tokens.TT_EQEQUALS
    TT_FSLASH           = tokens.TT_FSLASH
    TT_GREATERTHAN      = tokens.TT_GREATERTHAN
    TT_GTEQUALS         = tokens.TT_GTEQUALS
    TT_KEYWORD          = tokens.TT_KEYWORD
    TT_LESSTHAN         = tokens.TT_LESSTHAN
    TT_LTEQUALS         = tokens.TT_LTEQUALS
    TT_PLUS             = tokens.TT_PLUS
    global Context, SymbolTable
    Context             = context.Context
    SymbolTable         = context.SymbolTable
    global defaultvariables
    defaultvariables    = default.defaultvariables
    global KEYWORDS, RESERVED
    KEYWORDS            = constants.KEYWORDS
    RESERVED            = constants.RESERVED
    global TYPES, NullType, IntType, FloatType, StringType, ArrayType, TupleType, DictionaryType, FunctionType, BuiltInFunctionType, ExceptionType, NamespaceType
    TYPES               = types.TYPES
    NullType            = types.NullType
    IntType             = types.IntType
    FloatType           = types.FloatType
    StringType          = types.StringType
    ArrayType           = types.ArrayType
    TupleType           = types.TupleType
    DictionaryType      = types.DictionaryType
    FunctionType        = types.FunctionType
    BuiltInFunctionType = types.BuiltInFunctionType
    ExceptionType       = types.ExceptionType
    NamespaceType       = types.NamespaceType
    global Exc_BreakError, Exc_ContinueError, Exc_FileAccessError, Exc_IdentifierError, Exc_IncludeError, Exc_IterationError, Exc_PanicError, Exc_PatternError, Exc_ReservedError, Exc_ReturnError, Exc_TypeError, Exc_ValueError
    Exc_BreakError      = exceptions.Exc_BreakError
    Exc_ContinueError   = exceptions.Exc_ContinueError
    Exc_FileAccessError = exceptions.Exc_FileAccessError
    Exc_IdentifierError = exceptions.Exc_IdentifierError
    Exc_IncludeError    = exceptions.Exc_IncludeError
    Exc_IterationError  = exceptions.Exc_IterationError
    Exc_PatternError    = exceptions.Exc_PatternError
    Exc_PanicError      = exceptions.Exc_PanicError
    Exc_ReservedError   = exceptions.Exc_ReservedError
    Exc_ReturnError     = exceptions.Exc_ReturnError
    Exc_TypeError       = exceptions.Exc_TypeError
    Exc_ValueError      = exceptions.Exc_ValueError
    global run
    run = runu.run
    global perimod
    perimod = perimodu

##########################################
# RUNTIME RESULT                         #
##########################################

class RTResult():
    def __init__(self):
        self.reset()
        self.testreturn = None

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
        self.testreturn = res.testreturn

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
                    msg = lang['exceptions']['valueerror']['cannot']
                    msg = msg.replace('%s', TYPES['list'], 1)
                    msg = msg.replace('%s', type_.type, 1)
                    msg = msg.replace('%s', 'include', 1)
                    msg = msg.replace('%s', elm.type, 1)
                    return(
                        res.failure(
                            Exc_ValueError(
                                msg,
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

            if res.shouldreturn():
                return(res)

            if keytype:
                if type(key) != type(keytype):
                    msg = lang['exceptions']['typeerror']['cannot']
                    msg = msg.replace('%s', TYPES['dictionary'] + ' keys', 1)
                    msg = msg.replace('%s', keytype.type, 1)
                    msg = msg.replace('%s', 'include', 1)
                    msg = msg.replace('%s', key.type, 1)
                    return(
                        res.failure(
                            Exc_ValueError(
                                msg,
                                key.start, key.end,
                                context,
                                key.originstart, key.originend, key.origindisplay
                            )
                        )
                    )
            else:
                keytype = key

            if valuetype:
                msg = lang['exceptions']['typeerror']['cannot']
                msg = msg.replace('%s', TYPES['dictionary'], 1)
                msg = msg.replace('%s', valuetype.type, 1)
                msg = msg.replace('%s', 'include', 1)
                msg = msg.replace('%s', value.type, 1)
                if type(value) != type(valuetype):
                    return(
                        res.failure(
                            Exc_ValueError(
                                msg,
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



    ### VARIABLE CONTROL
    def visit_VarAccessNode(self, node, context, insideloop=False):
        res = RTResult()

        name = node.token.value
        value = context.symbols.access(name)

        if not value:
            msg = lang['exceptions']['identifiererror']['notdefined']
            msg = msg.replace('%s', name, 1)
            return(
                res.failure(
                    Exc_IdentifierError(
                        msg,
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

        if res.shouldreturn():
            return(res)

        prevvalue = context.symbols.access(name)

        if not prevvalue:
            msg = lang['exceptions']['identifiererror']['notdefined']
            msg = msg.replace('%s', name, 1)
            return(
                res.failure(
                    Exc_IdentifierError(
                        msg,
                        node.start, node.end,
                        context
                    )
                )
            )

        if name in RESERVED or prevvalue.reserved:
            msg = lang['exceptions']['reservederror']['reserved']
            msg = msg.replace('%s', str(value), 1)
            msg = msg.replace('%s', name, 1)
            return(
                res.failure(
                    Exc_ReservedError(
                        msg,
                        node.start, node.end,
                        context
                    )
                )
            )

        if type(prevvalue) != type(value) and not isinstance(prevvalue, NullType):
            value.originstart += prevvalue.originstart
            value.originend += prevvalue.originend
            value.origindisplay += prevvalue.origindisplay
            msg = lang['exceptions']['typeerror']['assigntype']
            msg = msg.replace('%s', value.type, 1)
            msg = msg.replace('%s', name, 1)
            msg = msg.replace('%s', prevvalue.type, 1)
            return(
                res.failure(
                    Exc_TypeError(
                        msg,
                        node.valnode.start, node.valnode.end,
                        context,
                        value.originstart, value.originend, value.origindisplay
                    )
                )
            )

        if res.shouldreturn():
            return(res)

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
                msg = lang['exceptions']['reservederror']['reserved']
                msg = msg.replace('%s', str(value), 1)
                msg = msg.replace('%s', name, 1)
                return(
                    res.failure(
                        Exc_ReservedError(
                            msg,
                            node.start, node.end,
                            context
                        )
                    )
                )

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
                msg = lang['exceptions']['reservederror']['reserved']
                msg = msg.replace('%s', TYPES['nonetype'], 1)
                msg = msg.replace('%s', name, 1)
                return(
                    res.failure(
                        Exc_ReservedError(
                            msg,
                            node.start, node.end,
                            context
                        )
                    )
                )

        value = NullType().setpos(node.start, node.end).setcontext(context)

        value.name = name

        context.symbols.assign(
            name.value,
            value
        )

        return(
            res.success(value)
        )



    ### FUNCTIONS
    def visit_FuncCreateNode(self, node, context, insideloop=False):
        res = RTResult()

        bodynodes = node.bodynodes
        arguments = node.arguments
        options = node.options
        returntype = node.returntype

        for key in list(arguments.keys()):
            i = arguments[key]
            
            i = res.register(
                self.visit(
                    i,
                    context,
                    insideloop=insideloop
                )
            )

            if res.shouldreturn():
                return(res)

            if i.type != TYPES['type'] and not isinstance(i, NullType):
                msg = lang['exceptions']['typeerror']['mustbe']
                msg = msg.replace('%s', 'Argument type', 1)
                msg = msg.replace('%s', f'{TYPES["type"]} or {TYPES["nonetype"]}', 1)
                msg = msg.replace('%s', i.type, 1)
                return(
                    res.failure(
                        Exc_TypeError(
                            msg,
                            i.start, i.end,
                            context
                        )
                    )
                )

            if isinstance(i, NullType):
                arguments[key] = NullType
            else:
                arguments[key] = i.returntype

        for key in list(options.keys()):
            i = options[key]

            i = res.register(
                self.visit(
                    i,
                    context,
                    insideloop=insideloop
                )
            )

            if res.shouldreturn():
                return(res)

            options[key] = i

        returntype = res.register(
            self.visit(
                returntype,
                context,
                insideloop=insideloop
            )
        )

        if res.shouldreturn():
            return(res)

        if returntype.type != TYPES['type'] and not isinstance(returntype, NullType):
            msg = lang['exceptions']['typeerror']['mustbe']
            msg = msg.replace('%s', 'Return type', 1)
            msg = msg.replace('%s', f'{TYPES["type"]} or {TYPES["nonetype"]}', 1)
            msg = msg.replace('%s', returntype.type, 1)
            return(
                res.failure(
                    Exc_TypeError(
                        msg,
                        returntype.start, returntype.end,
                        context
                    )
                )
            )

        if isinstance(returntype, NullType):
            funcvalue = FunctionType(bodynodes, arguments, options, NullType, node.shouldreturn)
        else:
            funcvalue = FunctionType(bodynodes, arguments, options, returntype, node.shouldreturn)
        funcvalue.setcontext(context).setpos(node.start, node.end)

        return(
            res.success(funcvalue)
        )


    def visit_FuncCallNode(self, node, context, insideloop=False):
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

        for i in node.calls:
            args = []
            for argnode in i[0]:
                args.append(
                    res.register(
                        self.visit(
                            argnode,
                            context,
                            insideloop=insideloop
                        )
                    )
                )
            opts = {}
            for optnode in list(i[1].keys()):
                opts[optnode] = res.register(
                    self.visit(
                        i[1][optnode],
                        context,
                        insideloop=insideloop
                    )
                )

            if res.shouldreturn():
                return(res)

            try:
                callvalue = value.name
            except AttributeError:
                callvalue = None

            value = res.register(
                value.call(
                    callvalue, args, opts, i[0]
                )
            )

            if res.shouldreturn():
                return(res)

            value = value.copy().setpos(node.start, node.end).setcontext(context)

        return(
            res.success(value)
        )


    def visit_ReturnNode(self, node, context, insideloop=False):
        res = RTResult()

        value = res.register(
            self.visit(
                node.returnnode,
                context,
                insideloop=insideloop
            )
        )

        if not context.parent:
            msg = lang['exceptions']['returnerror']['location']
            exc = Exc_ReturnError(
                msg,
                node.start, node.end,
                context
            )
            exc.returnvalue = value
            return(
                res.failure(
                    exc
                )
            )

        res.testreturn = value

        if res.shouldreturn():
            return(res)

        res.testreturn = value

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
            msg = lang['exceptions']['identifiererror']['notdefined']
            msg = msg.replace('%s', varname, 1)
            return(
                res.failure(
                    Exc_IdentifierError(
                        msg,
                        node.vartoken.start, node.vartoken.end,
                        context
                    )
                )
            )
        if type(value) != type(prevvalue) and not node.varoverwrite:
            msg = lang['exceptions']['typeerror']['assigntype']
            msg = msg.replace('%s', value.type, 1)
            msg = msg.replace('%s', varname, 1)
            msg = msg.replace('%s', prevvalue.type, 1)
            return(
                res.failure(
                    Exc_TypeError(
                        msg,
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
            msg = lang['exceptions']['identifiererror']['notdefined']
            msg = msg.replace('%s', varname, 1)
            return(
                res.failure(
                    Exc_IdentifierError(
                        msg,
                        node.vartoken.start, node.vartoken.end,
                        context
                    )
                )
            )

        try:
            shouldbreak = False
            for i in loopthrough.value:
                if type(i) != type(prevvalue) and not node.varoverwrite:
                    msg = lang['exceptions']['typeerror']['assigntype']
                    msg = msg.replace('%s', i.type, 1)
                    msg = msg.replace('%s', varname, 1)
                    msg = msg.replace('%s', prevvalue.type, 1)
                    return(
                        res.failure(
                            Exc_TypeError(
                                msg,
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
            msg = lang['exceptions']['iterationerror']['cannot']
            msg = msg.replace('%s', loopthrough.type, 1)
            return(
                res.failure(
                    Exc_IterationError(
                        msg,
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
            msg = lang['exceptions']['breakerror']['location']
            return(
                res.failure(
                    Exc_BreakError(
                        msg,
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
            msg = lang['exceptions']['continueerror']['location']
            return(
                res.failure(
                    Exc_ContinueError(
                        msg,
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
                    error.start,
                    error.end,
                    context
                )

                try:
                    exc.setcontext(context).setpos(error.start, error.end, error.originstart, error.originend, error.origindisplay)

                except AttributeError:
                    return(res)

                return(
                    res.success(exc)
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
            if isinstance(result, IntType):
                result, error = result.multiply(IntType(-1))
            else:
                result, error = result.multiply(FloatType(-1.0))
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
        else:
            result = NullType()
            error = None

        if error:
            return(
                res.failure(error)
            )

        return(
            res.success(
                result.setpos(
                    node.start,
                    node.end
                ).setcontext(
                    context
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
                    res.failure(error)
                )

        return(
            res.success(value)
        )

    def visit_AttributeNode(self, node, context, insideloop=False):
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

        for i in node.attributes:
            value, error = value.attribute(i)

            if error:
                return(
                    res.failure(error)
                )

            if isinstance(value, FunctionType):
                value.name = i.value

        return(
            res.success(value)
        )



    ### MODULES
    def visit_IncludeNode(self, node, context, insideloop=False):
        res = RTResult()

        file = res.register(
            self.visit(
                node.filenode,
                context,
                insideloop=insideloop
            )
        )

        if res.shouldreturn():
            return(res)

        if not isinstance(file, StringType):
            msg = lang['exceptions']['typeerror']['mustbe']
            msg = msg.replace('%s', '\'file\'', 1)
            msg = msg.replace('%s', TYPES['string'], 1)
            msg = msg.replace('%s', file.type, 1)
            return(
                res.failure(
                    Exc_TypeError(
                        msg,
                        file.start, file.end,
                        context,
                        file.originstart, file.originend, file.origindisplay
                    )
                )
            )

        if not _re.match(r'^([A-z][A-z0-9]*)(\.([A-z][A-z0-9]*))*$', file.value):
            msg = lang['exceptions']['patternerror']['nomatch']
            msg = msg.replace('%s', '\'file\'', 1)
            msg = msg.replace('%s', '/^([A-z][A-z0-9]*)(\.([A-z][A-z0-9]*))*$/', 1)
            return(
                res.failure(
                    Exc_PatternError(
                        msg,
                        file.start, file.end,
                        context,
                        file.originstart, file.originend, file.origindisplay
                    )
                )
            )

        script = None
        for i in context.symbols.access('__peridot__').symbols.access('path').value:
            i = i.value

            try:
                path = file.value + '.peri'
                path = _Path(i) / path
                with open(str(path), 'r') as f:
                    script = f.read()
                break

            except FileNotFoundError as e: pass
            except IsADirectoryError as e: pass
            except PermissionError   as e: pass

        result = NullType()
        result.setcontext(
            context
        ).setpos(
            node.start, node.end
        )

        if not script:
            try:
                symbols = defaultvariables(SymbolTable(context.symbols))
                perimod._context = Context('<file>', symbols, context, [node.start, node.end, [file.originstart], [file.originend], [file.origindisplay]])
                perimod._symbols = symbols
                perimod._position = node
                perimod._file = file.value
                mod = _import_module(f'.version.modules.{file.value}', package='peridot')
                result = perimod._namespace
                if result == None:
                    msg = lang['exceptions']['includeerror']['failed']
                    msg = msg.replace('%s', str(file), 1)
                    msg = msg.replace('%s', lang['exceptions']['module'], 1)
                    msg = msg.replace('%s', perimod._error[0], 1)
                    msg = msg.replace('%s', lang['exceptions']['line'], 1)
                    msg = msg.replace('%s', str(perimod._error[1]), 1)
                    msg = msg.replace('%s', perimod._error[2], 1)
                    msg = msg.replace('%s', perimod._error[3], 1)
                    return(
                        res.failure(
                            Exc_IncludeError(
                                msg,
                                node.start, node.end,
                                context
                            )
                        )
                    )
                for i in list(perimod._builtinfuncs.keys()):
                    BuiltInFunctionType.modules[i] = perimod._builtinfuncs[i]
                result.setpos(node.start, node.end)
                result.setcontext(context)
                script = True

            except PermissionError:
                msg = lang['exceptions']['includeerror']['doesnotexist']
                msg = msg.replace('%s', str(file), 1)
                return(
                    res.failure(
                        Exc_FileAccessError(
                            msg,
                            file.start, file.end,
                            context,
                            file.originstart, file.originend, file.origindisplay
                        )
                    )
                )

        if not script:
            symbols = defaultvariables(SymbolTable())
            result, exec_context, error = run(file.value, script, symbols)

            if error:
                return(
                    res.failure(error)
                )

            result = NamespaceType(symbols).setpos(node.start, node.end).setcontext(exec_context)

        return(
            res.success(result)
        )
