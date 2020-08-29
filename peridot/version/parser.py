##########################################
# DEPENDENCIES                           #
##########################################

def _parserinit(conf, tokens, exceptions, constants, nodes):
    global lang
    lang = conf
    global TT_EOF, TT_EOL, TT_KEYWORD, TT_LPAREN, TT_RPAREN, TT_IDENTIFIER, TT_EQUALS, TT_EQEQUALS, TT_BANGEQUALS, TT_LESSTHAN, TT_LTEQUALS, TT_GREATERTHAN, TT_GTEQUALS, TT_PLUS, TT_DASH, TT_ASTRISK, TT_FSLASH, TT_CARAT, TT_LSQUARE, TT_RSQUARE, TT_PERIOD, TT_COMMA, TT_INT, TT_FLOAT, TT_STRING, TT_LCURLY, TT_RCURLY, TT_COLON, TT_ARROW
    TT_EOF          = tokens.TT_EOF
    TT_EOL          = tokens.TT_EOL
    TT_KEYWORD      = tokens.TT_KEYWORD
    TT_LPAREN       = tokens.TT_LPAREN
    TT_RPAREN       = tokens.TT_RPAREN
    TT_IDENTIFIER   = tokens.TT_IDENTIFIER
    TT_EQUALS       = tokens.TT_EQUALS
    TT_EQEQUALS     = tokens.TT_EQEQUALS
    TT_BANGEQUALS   = tokens.TT_BANGEQUALS
    TT_LESSTHAN     = tokens.TT_LESSTHAN
    TT_LTEQUALS     = tokens.TT_LTEQUALS
    TT_GREATERTHAN  = tokens.TT_GREATERTHAN
    TT_GTEQUALS     = tokens.TT_GTEQUALS
    TT_PLUS         = tokens.TT_PLUS
    TT_DASH         = tokens.TT_DASH
    TT_ASTRISK      = tokens.TT_ASTRISK
    TT_FSLASH       = tokens.TT_FSLASH
    TT_CARAT        = tokens.TT_CARAT
    TT_LSQUARE      = tokens.TT_LSQUARE
    TT_RSQUARE      = tokens.TT_RSQUARE
    TT_PERIOD       = tokens.TT_PERIOD
    TT_COMMA        = tokens.TT_COMMA
    TT_INT          = tokens.TT_INT
    TT_FLOAT        = tokens.TT_FLOAT
    TT_STRING       = tokens.TT_STRING
    TT_LCURLY       = tokens.TT_LCURLY
    TT_RCURLY       = tokens.TT_RCURLY
    TT_COLON        = tokens.TT_COLON
    TT_ARROW        = tokens.TT_ARROW
    global Syn_SyntaxError
    Syn_SyntaxError = exceptions.Syn_SyntaxError
    global KEYWORDS
    KEYWORDS        = constants.KEYWORDS
    global BinaryOpNode, ReturnNode, BreakNode, ContinueNode, IncludeNode, VarNullNode, VarCreateNode, UnaryOpNode, FuncCallNode, IndicieNode, AttributeNode, IntNode, FloatNode, StringNode, TupleNode, VarAssignNode, VarAccessNode, ArrayNode, DictionaryNode, FuncCreateNode, HandlerNode, IfNode, SwitchNode, ForLoopNode, WhileLoopNode
    BinaryOpNode    = nodes.BinaryOpNode
    ReturnNode      = nodes.ReturnNode
    BreakNode       = nodes.BreakNode
    ContinueNode    = nodes.ContinueNode
    IncludeNode     = nodes.IncludeNode
    VarNullNode     = nodes.VarNullNode
    VarCreateNode   = nodes.VarCreateNode
    UnaryOpNode     = nodes.UnaryOpNode
    FuncCallNode    = nodes.FuncCallNode
    IndicieNode     = nodes.IndicieNode
    AttributeNode   = nodes.AttributeNode
    IntNode         = nodes.IntNode
    FloatNode       = nodes.FloatNode
    StringNode      = nodes.StringNode
    TupleNode       = nodes.TupleNode
    VarAssignNode   = nodes.VarAssignNode
    VarAccessNode   = nodes.VarAccessNode
    ArrayNode       = nodes.ArrayNode
    DictionaryNode  = nodes.DictionaryNode
    FuncCreateNode  = nodes.FuncCreateNode
    HandlerNode     = nodes.HandlerNode
    IfNode          = nodes.IfNode
    SwitchNode      = nodes.SwitchNode
    ForLoopNode     = nodes.ForLoopNode
    WhileLoopNode   = nodes.WhileLoopNode

##########################################
# PARSE RESULT                           #
##########################################

class ParseResult():
    def __init__(self):
        self.error = None
        self.node = None
        self.advancecount = 0

    def registeradvancement(self):
        self.advancecount += 1

    def registerretreat(self):
        self.advancecount -= 1

    def register(self, res):
        self.advancecount += res.advancecount
        if res.error:
            self.error = res.error

        return(res.node)

    def tryregister(self, res):
        if res.error:
            return(None)

        return(res.node)

    def success(self, node):
        self.node = node

        return(self)

    def failure(self, error):
        if not self.error or self.advancecount == 0:
            self.error = error

        return(self)

##########################################
# PARSER                                 #
##########################################

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.advance()

    def advance(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.curtoken = self.tokens[self.index]

        return(self.curtoken)

    def retreat(self):
        self.index -= 1
        if self.index >= 0:
            self.curtoken = self.tokens[self.index]

        return(self.curtoken)


    def parse(self):
        res = ParseResult()
        tokens = []

        while self.curtoken.type != TT_EOF:
            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            if self.curtoken.type == TT_EOF:
                break

            token = res.register(
                self.statement()
            )

            tokens.append(token)

            if res.error:
                return(
                    res
                )

            if self.curtoken.type != TT_EOL:
                msg = lang['exceptions']['syntaxerror']['invalideoflnoexp']
                msg = msg.replace('%s', 'L', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            res.registeradvancement()
            self.advance()

        return(
            res.success(
                tokens
            )
        )


    def binaryop(self, funca, optypes, funcb=None):
        if not funcb:
            funcb = funca

        res = ParseResult()

        lfactor = res.register(funca())

        if res.error:
            return(res)

        while self.curtoken.type in optypes or (self.curtoken.type, self.curtoken.value) in optypes:
            optoken = self.curtoken
            res.registeradvancement()
            self.advance()
            rfactor = res.register(funcb())

            if res.error:
                return(res)

            lfactor = BinaryOpNode(
                lfactor, optoken, rfactor
            )

        return(
            res.success(lfactor)
        )


    def statement(self):
        res = ParseResult()
        start = self.curtoken.start.copy()

        if self.curtoken.matches(TT_KEYWORD, KEYWORDS['return']):
            res.registeradvancement()
            self.advance()

            if self.curtoken.type != TT_LPAREN:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\'(\'', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            res.registeradvancement()
            self.advance()

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            statement = res.register(
                self.statement()
            )

            if res.error:
                return(res)

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            if self.curtoken.type != TT_RPAREN:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\')\'', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            end = self.curtoken.end.copy()
            res.registeradvancement()
            self.advance()

            return(
                res.success(
                    ReturnNode(statement, start, end)
                )
            )

        if self.curtoken.matches(TT_KEYWORD, KEYWORDS['break']):
            res.registeradvancement()
            self.advance()

            if self.curtoken.type != TT_LPAREN:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\'(\'', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            res.registeradvancement()
            self.advance()

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            if self.curtoken.type != TT_RPAREN:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\')\'', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            end = self.curtoken.end.copy()
            res.registeradvancement()
            self.advance()

            return(
                res.success(
                    BreakNode(start, end)
                )
            )

        if self.curtoken.matches(TT_KEYWORD, KEYWORDS['continue']):
            res.registeradvancement()
            self.advance()

            if self.curtoken.type != TT_LPAREN:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\'(\'', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            res.registeradvancement()
            self.advance()

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            if self.curtoken.type != TT_RPAREN:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\')\'', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            end = self.curtoken.end.copy()
            res.registeradvancement()
            self.advance()

            return(
                res.success(
                    ContinueNode(start, end)
                )
            )

        if self.curtoken.matches(TT_KEYWORD, KEYWORDS['import']):
            res.registeradvancement()
            self.advance()

            if self.curtoken.type != TT_LPAREN:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\'(\'', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            res.registeradvancement()
            self.advance()

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            file = res.register(
                self.statement()
            )

            if res.error:
                return(res)

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            if self.curtoken.type != TT_RPAREN:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\')\'', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            end = self.curtoken.end.copy()
            res.registeradvancement()
            self.advance()

            return(
                res.success(
                    IncludeNode(file, start, end)
                )
            )

        expr = res.register(
            self.expr()
        )

        if res.error:
            return(res)

        return(
            res.success(expr)
        )


    def expr(self):
        res = ParseResult()

        if self.curtoken.matches(TT_KEYWORD, KEYWORDS['varcreate']):
            res.registeradvancement()
            self.advance()

            if self.curtoken.type != TT_IDENTIFIER:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', 'identifier', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            token = self.curtoken
            res.registeradvancement()
            self.advance()

            if self.curtoken.type != TT_EQUALS:
                return(
                    res.success(
                        VarNullNode(
                            token
                        )
                    )
                )

            res.registeradvancement()
            self.advance()

            expr = res.register(self.statement())

            if res.error:
                return(res)

            return(
                res.success(
                    VarCreateNode(
                        token, expr
                    )
                )
            )

        node = res.register(
            self.binaryop(
                self.compexpr,
                ((TT_KEYWORD, KEYWORDS['logicaland']), (TT_KEYWORD, KEYWORDS['logicalor']))
            )
        )

        if res.error:
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', 'identifier, keyword, operator, type', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        return(
            res.success(node)
        )


    def compexpr(self):
        res = ParseResult()

        if self.curtoken.matches(TT_KEYWORD, KEYWORDS['logicalnot']):
            optoken = self.curtoken
            res.registeradvancement()
            self.advance()

            node = res.register(self.compexpr())

            if res.error:
                return(res)

            return(
                res.success(
                    UnaryOpNode(
                        optoken, node
                    )
                )
            )

        node = res.register(
            self.binaryop(
                self.arithexpr,
                (TT_EQEQUALS, TT_BANGEQUALS, TT_LESSTHAN, TT_LTEQUALS, TT_GREATERTHAN, TT_GTEQUALS)
            )
        )

        if res.error:
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', 'identifier, operator, keyword, type', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        return(
            res.success(
                node
            )
        )


    def arithexpr(self):
        return(
            self.binaryop(
                self.term,
                (TT_PLUS, TT_DASH)
            )
        )


    def term(self):
        return(
            self.binaryop(
                self.raised,
                (TT_ASTRISK, TT_FSLASH)
            )
        )


    def raised(self):
        return(
            self.binaryop(
                self.factor,
                tuple([TT_CARAT]),
                self.term
            )
        )


    def factor(self):
        res = ParseResult()
        token = self.curtoken

        if token.type in (TT_PLUS, TT_DASH):
            res.registeradvancement()
            self.advance()

            factor = res.register(self.factor())

            if res.error:
                return(res)

            return(
                res.success(
                    UnaryOpNode(
                        token, factor
                    )
                )
            )

        atom = res.register(
            self.atom()
        )

        if res.error:
            return(res)

        while self.curtoken.type in [TT_LPAREN, TT_LSQUARE, TT_PERIOD]:
            atom = res.register(
                self.calttricie(atom)
            )

            if res.error:
                return(res)

        return(
            res.success(atom)
        )


    def calttricie(self, prevnode):
        res = ParseResult()

        if self.curtoken.type == TT_LPAREN:
            calls = []

            while self.curtoken.type == TT_LPAREN:
                args = []
                opts = {}

                res.registeradvancement()
                self.advance()

                while self.curtoken.type == TT_EOL:
                    res.registeradvancement()
                    self.advance()

                if self.curtoken.type == TT_RPAREN:
                    end = self.curtoken.end.copy()
                    res.registeradvancement()
                    self.advance()
                else:
                    if self.curtoken.type == TT_IDENTIFIER:
                        token = self.curtoken
                        res.registeradvancement()
                        self.advance()

                        if self.curtoken.type == TT_EQUALS:
                            res.registeradvancement()
                            self.advance()

                            opts[token.value] = res.register(
                                self.statement()
                            )

                        else:
                            res.registerretreat()
                            self.retreat()

                            args.append(
                                res.register(
                                    self.statement()
                                )
                            )

                    else:
                        args.append(
                            res.register(
                                self.statement()
                            )
                        )

                    if res.error:
                        msg = lang['exceptions']['syntaxerror']['notfound']
                        msg = msg.replace('%s', '\')\', identifier, operator, keyword, type', 1)
                        return(
                            res.failure(
                                Syn_SyntaxError(
                                    msg,
                                    self.curtoken.start, self.curtoken.end
                                )
                            )
                        )


                    while self.curtoken.type == TT_COMMA:
                        res.registeradvancement()
                        self.advance()

                        while self.curtoken.type == TT_EOL:
                            res.registeradvancement()
                            self.advance()

                        if self.curtoken.type == TT_IDENTIFIER:
                            token = self.curtoken
                            res.registeradvancement()
                            self.advance()

                            if self.curtoken.type == TT_EQUALS:
                                res.registeradvancement()
                                self.advance()

                                opts[token.value] = res.register(
                                    self.statement()
                                )

                            else:
                                res.registerretreat()
                                self.retreat()

                                args.append(
                                    res.register(
                                        self.statement()
                                    )
                                )
                        else:
                            args.append(
                                res.register(
                                    self.statement()
                                )
                            )

                        if res.error:
                            return(res)

                    while self.curtoken.type == TT_EOL:
                        res.registeradvancement()
                        self.advance()

                    if self.curtoken.type != TT_RPAREN:
                        msg = lang['exceptions']['syntaxerror']['notfound']
                        msg = msg.replace('%s', '\',\', \')\'', 1)
                        return(
                            res.failure(
                                Syn_SyntaxError(
                                    msg,
                                    self.curtoken.start, self.curtoken.end
                                )
                            )
                        )

                    end = self.curtoken.end.copy()
                    res.registeradvancement()
                    self.advance()

                calls.append((args, opts, end))

            return(
                res.success(
                    FuncCallNode(
                        prevnode,
                        calls
                    )
                )
            )


        elif self.curtoken.type == TT_LSQUARE:
            indicies = []
            end = self.curtoken.end.copy()

            while self.curtoken.type == TT_LSQUARE:
                res.registeradvancement()
                self.advance()

                indicies.append(
                    res.register(
                        self.statement()
                    )
                )

                if res.error:
                    return(res)

                if not self.curtoken.type == TT_RSQUARE:
                    msg = lang['exceptions']['syntaxerror']['notfound']
                    msg = msg.replace('%s', '\']\'', 1)
                    return(
                        res.failure(
                            Syn_SyntaxError(
                                msg,
                                self.curtoken.start, self.curtoken.end
                            )
                        )
                    )

                end = self.curtoken.end.copy()
                res.registeradvancement()
                self.advance()

            return(
                res.success(
                    IndicieNode(
                        prevnode, indicies, end
                    )
                )
            )


        elif self.curtoken.type == TT_PERIOD:
            attributes = []
            end = self.curtoken.end.copy()

            while self.curtoken.type == TT_PERIOD:
                res.registeradvancement()
                self.advance()

                if not self.curtoken.type == TT_IDENTIFIER:
                    msg = lang['exceptions']['syntaxerror']['notfound']
                    msg = msg.replace('%s', 'identifier', 1)
                    return(
                        res.failure(
                            Syn_SyntaxError(
                                msg,
                                self.curtoken.start, self.curtoken.end
                            )
                        )
                    )

                attributes.append(
                    self.curtoken
                )

                end = self.curtoken.end.copy()
                res.registeradvancement()
                self.advance()

            return(
                res.success(
                    AttributeNode(
                        prevnode, attributes, end
                    )
                )
            )

        else:
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', '\'(\', \'[\', \'.\'', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )


    def atom(self):
        res = ParseResult()
        token = self.curtoken


        if token.type == TT_INT:
            res.registeradvancement()
            self.advance()

            return(
                res.success(
                    IntNode(token)
                )
            )

        elif token.type == TT_FLOAT:
            self.advance()

            return(
                res.success(
                    FloatNode(token)
                )
            )

        elif token.type == TT_STRING:
            self.advance()

            return(
                res.success(
                    StringNode(token)
                )
            )

        elif token.type == TT_LPAREN:
            start = self.curtoken.start.copy()
            res.registeradvancement()
            self.advance()

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            expr = res.register(
                self.statement()
            )

            if res.error:
                return(res)

            if self.curtoken.type == TT_COMMA:
                expr = [expr]

                while self.curtoken.type == TT_COMMA:
                    res.registeradvancement()
                    self.advance()

                    while self.curtoken.type == TT_EOL:
                        res.registeradvancement()
                        self.advance()

                    expr.append(
                        res.register(
                            self.statement()
                        )
                    )
                
                if self.curtoken.type != TT_RPAREN:
                    msg = lang['exceptions']['syntaxerror']['notfound']
                    msg = msg.replace('%s', '\',\', \')\'', 1)
                    return(
                    res.failure(
                            Syn_SyntaxError(
                                msg,
                                self.curtoken.start, self.curtoken.end
                            )
                        )
                    )

                end = self.curtoken.end.copy()
                res.registeradvancement()
                self.advance()

                return(
                    res.success(
                        TupleNode(
                            expr,
                            start, end
                        )
                    )
                )

            else:
                while self.curtoken.type == TT_EOL:
                    res.registeradvancement()
                    self.advance()

                if self.curtoken.type == TT_RPAREN:
                    res.registeradvancement()
                    self.advance()

                    return(
                        res.success(
                            expr
                        )
                    )

            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', '\')\'', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )


        elif token.type == TT_IDENTIFIER:
            res.registeradvancement()
            self.advance()

            if self.curtoken.type == TT_EQUALS:
                res.registeradvancement()
                self.advance()

                expr = res.register(
                    self.statement()
                )

                return(
                    res.success(
                        VarAssignNode(
                            token,
                            expr
                        )
                    )
                )

            return(
                res.success(
                    VarAccessNode(token)
                )
            )

        elif token.type == TT_LSQUARE:
            arrayexpr = res.register(
                self.arrayexpr()
            )

            if res.error:
                return(res)

            return(
                res.success(
                    arrayexpr
                )
            )

        elif token.type == TT_LCURLY:
            dictionaryexpr = res.register(
                self.dictionaryexpr()
            )

            if res.error:
                return(res)

            return(
                res.success(
                    dictionaryexpr
                )
            )

        elif token.matches(TT_KEYWORD, KEYWORDS['funccreate']) or token.matches(TT_KEYWORD, KEYWORDS['lambdacreate']):
            funcdef = res.register(self.funcdef())
            if res.error:
                return(res)

            return(
                res.success(
                    funcdef
                )
            )

        elif token.matches(TT_KEYWORD, KEYWORDS['handler']):
            funcdef = res.register(self.handler())
            if res.error:
                return(res)

            return(
                res.success(
                    funcdef
                )
            )

        elif token.matches(TT_KEYWORD, KEYWORDS['if']):
            ifexpr = res.register(self.ifexpr())
            if res.error:
                return(res)

            return(
                res.success(
                    ifexpr
                )
            )

        elif token.matches(TT_KEYWORD, KEYWORDS['case']):
            switchexpr = res.register(self.switchexpr())
            if res.error:
                return(res)

            return(
                res.success(
                    switchexpr
                )
            )

        elif token.matches(TT_KEYWORD, KEYWORDS['forloop']) or token.matches(TT_KEYWORD, KEYWORDS['whileloop']):
            loopexpr = res.register(self.loopexpr())
            if res.error:
                return(res)

            return(
                res.success(
                    loopexpr
                )
            )

        msg = lang['exceptions']['syntaxerror']['notfound']
        msg = msg.replace('%s', 'identifier, keyword, operator, type', 1)
        return(
            res.failure(
                Syn_SyntaxError(
                    msg,
                    self.curtoken.start, self.curtoken.end
                )
            )
        )


    def arrayexpr(self):
        res = ParseResult()
        elmnodes = []
        start = self.curtoken.start.copy()

        if self.curtoken.type != TT_LSQUARE:
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', '\'[\'', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        res.registeradvancement()
        self.advance()

        while self.curtoken.type == TT_EOL:
            res.registeradvancement()
            self.advance()

        if self.curtoken.type == TT_RSQUARE:
            end = self.curtoken.end.copy()
            res.registeradvancement()
            self.advance()

        else:
            elmnodes.append(
                res.register(
                    self.statement()
                )
            )

            if res.error:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\']\', identifier, keyword, operator, type', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            while self.curtoken.type == TT_COMMA:
                res.registeradvancement()
                self.advance()

                while self.curtoken.type == TT_EOL:
                    res.registeradvancement()
                    self.advance()

                elmnodes.append(
                    res.register(
                        self.statement()
                    )
                )

                if res.error:
                    return(res)

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            if self.curtoken.type != TT_RSQUARE:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\',\', \']\'', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            end = self.curtoken.end.copy()
            res.registeradvancement()
            self.advance()

        return(
            res.success(
                ArrayNode(
                    elmnodes,
                    start, end
                )
            )
        )


    def dictionaryexpr(self):
        res = ParseResult()
        keys = []
        values = []
        start = self.curtoken.start.copy()

        if self.curtoken.type != TT_LCURLY:
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', '\'{\'', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        res.registeradvancement()
        self.advance()

        while self.curtoken.type == TT_EOL:
            res.registeradvancement()
            self.advance()

        if self.curtoken.type == TT_RCURLY:
            end = self.curtoken.end.copy()
            res.registeradvancement()
            self.advance()
        
        else:
            keys.append(
                res.register(
                    self.statement()
                )
            )

            if res.error:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\'}\', identifier, keyword, operator, type', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            if self.curtoken.type != TT_COLON:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\':\'', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            res.registeradvancement()
            self.advance()

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            values.append(
                res.register(
                    self.statement()
                )
            )

            if res.error:
                return(res)

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            while self.curtoken.type == TT_COMMA:
                res.registeradvancement()
                self.advance()

                while self.curtoken.type == TT_EOL:
                    res.registeradvancement()
                    self.advance()

                keys.append(
                    res.register(
                        self.statement()
                    )
                )

                if res.error:
                    return(res)

                if self.curtoken.type != TT_COLON:
                    msg = lang['exceptions']['syntaxerror']['notfound']
                    msg = msg.replace('%s', '\':\'', 1)
                    return(
                        res.failure(
                            Syn_SyntaxError(
                                msg,
                                self.curtoken.start, self.curtoken.end
                            )
                        )
                    )

                res.registeradvancement()
                self.advance()

                while self.curtoken.type == TT_EOL:
                    res.registeradvancement()
                    self.advance()

                values.append(
                    res.register(
                        self.statement()
                    )
                )

                if res.error:
                    return(res)

                while self.curtoken.type == TT_EOL:
                    res.registeradvancement()
                    self.advance()

            if self.curtoken.type != TT_RCURLY:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\',\', \'}\'', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            end = self.curtoken.end.copy()
            res.registeradvancement()
            self.advance()

        return(
            res.success(
                DictionaryNode(
                    keys, values,
                    start, end
                )
            )
        )

            


    def funcdef(self):
        res = ParseResult()

        if not self.curtoken.matches(TT_KEYWORD, KEYWORDS['funccreate']) and not self.curtoken.matches(TT_KEYWORD, KEYWORDS['lambdacreate']):
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', f'{KEYWORDS["funccreate"]}', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        token = self.curtoken
        mode = self.curtoken.value

        res.registeradvancement()
        self.advance()

        if self.curtoken.type != TT_LPAREN:
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', '\'(\'', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        res.registeradvancement()
        self.advance()

        while self.curtoken.type == TT_EOL:
            res.registeradvancement()
            self.advance()

        arguments = {}
        options   = {}

        if self.curtoken.type == TT_IDENTIFIER:
            argname = self.curtoken

            res.registeradvancement()
            self.advance()


            if self.curtoken.type == TT_COLON:
                res.registeradvancement()
                self.advance()

                argtype = res.register(
                    self.statement()
                )

                if res.error:
                    return(res)

                arguments[argname.value] = argtype

            elif self.curtoken.type == TT_EQUALS:
                res.registeradvancement()
                self.advance()

                optdefault = res.register(
                    self.statement()
                )

                if res.error:
                    return(res)

                options[argname.value] = optdefault

            else:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\':\', \'=\'', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            while self.curtoken.type == TT_COMMA:
                res.registeradvancement()
                self.advance()

                while self.curtoken.type == TT_EOL:
                    res.registeradvancement()
                    self.advance()

                if self.curtoken.type != TT_IDENTIFIER:
                    msg = lang['exceptions']['syntaxerror']['notfound']
                    msg = msg.replace('%s', 'identifier', 1)
                    return(
                        res.failure(
                            Syn_SyntaxError(
                                msg,
                                self.curtoken.start, self.curtoken.end
                            )
                        )
                    )

                argname = self.curtoken

                res.registeradvancement()
                self.advance()

                if self.curtoken.type == TT_COLON:
                    res.registeradvancement()
                    self.advance()

                    argtype = res.register(
                        self.statement()
                    )

                    if res.error:
                        return(res)

                    arguments[argname.value] = argtype

                elif self.curtoken.type == TT_EQUALS:
                    res.registeradvancement()
                    self.advance()

                    optdefault = res.register(
                        self.statement()
                    )

                    if res.error:
                        return(res)

                    options[argname.value] = optdefault

                else:
                    msg = lang['exceptions']['syntaxerror']['notfound']
                    msg = msg.replace('%s', '\':\', \'=\'', 1)
                    return(
                        res.failure(
                            Syn_SyntaxError(
                                msg,
                                self.curtoken.start, self.curtoken.end
                            )
                        )
                    )

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            if self.curtoken.type != TT_RPAREN:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\',\', \')\'', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

        elif self.curtoken.type != TT_RPAREN:
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', '\')\', identifier', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        res.registeradvancement()
        self.advance()

        while self.curtoken.type == TT_EOL:
            res.registeradvancement()
            self.advance()

        if self.curtoken.type != TT_ARROW:
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', '\'->\'', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        res.registeradvancement()
        self.advance()

        while self.curtoken.type == TT_EOL:
            res.registeradvancement()
            self.advance()

        returntype = res.register(
            self.statement()
        )

        if res.error:
            return(res)

        while self.curtoken.type == TT_EOL:
            res.registeradvancement()
            self.advance()

        if mode == KEYWORDS['funccreate']:
            codeblock = res.register(
                self.codeblock()
            )

            if res.error:
                return(res)
        else:
            if self.curtoken.type != TT_LCURLY:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\'(\', identifier', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            res.registeradvancement()
            self.advance()

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()
                
            line = res.register(
                self.statement()
            )

            if res.error:
                return(res)

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            if self.curtoken.type != TT_RCURLY:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\'}\'', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            end = self.curtoken
            res.registeradvancement()
            self.advance()

            codeblock = [ReturnNode(
                line, token.start, end
            )]

        return(
            res.success(
                FuncCreateNode(
                    token,
                    arguments,
                    options,
                    returntype,
                    codeblock,
                    False
                )
            )
        )


    def handler(self):
        res = ParseResult()

        if not self.curtoken.matches(TT_KEYWORD, KEYWORDS['handler']):
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', f'{KEYWORDS["handler"]}', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        token = self.curtoken

        res.registeradvancement()
        self.advance()

        while self.curtoken.type == TT_EOL:
            res.registeradvancement()
            self.advance()

        codeblock = res.register(
            self.codeblock()
        )

        if res.error:
            return(res)

        return(
            res.success(
                HandlerNode(
                    token,
                    codeblock
                )
            )
        )


    def ifexpr(self):
        res = ParseResult()
        cases = []
        elsecase = None

        if not self.curtoken.matches(TT_KEYWORD, KEYWORDS['if']):
            
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', f'{KEYWORDS["if"]}', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        res.registeradvancement()
        self.advance()

        if self.curtoken.type != TT_LPAREN:
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', '\'(\'', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )
        
        res.registeradvancement()
        self.advance()

        while self.curtoken.type == TT_EOL:
            res.registeradvancement()
            self.advance()

        condition = res.register(self.statement())
        if res.error: return(res)

        while self.curtoken.type == TT_EOL:
            res.registeradvancement()
            self.advance()

        if self.curtoken.type != TT_RPAREN:
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', '\')\'', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )
        
        res.registeradvancement()
        self.advance()

        while self.curtoken.type == TT_EOL:
            res.registeradvancement()
            self.advance()

        codeblock = res.register(self.codeblock())

        if res.error:
            return(res)

        cases.append((condition, codeblock))

        while self.curtoken.matches(TT_KEYWORD, KEYWORDS['elif']):
            res.registeradvancement()
            self.advance()

            if self.curtoken.type != TT_LPAREN:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\'(\'', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )
        
            res.registeradvancement()
            self.advance()

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            condition = res.register(self.statement())
            if res.error: return(res)

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            if self.curtoken.type != TT_RPAREN:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\')\'', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )
        
            res.registeradvancement()
            self.advance()

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            codeblock = res.register(self.codeblock())

            if res.error:
                return(res)
            cases.append((condition, codeblock))

        if self.curtoken.matches(TT_KEYWORD, KEYWORDS['else']):
            res.registeradvancement()
            self.advance()

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()
            
            elsecase = res.register(self.codeblock())
            if res.error:
                return(res)

        return(
            res.success(
                IfNode(
                    cases, elsecase
                )
            )
        )


    def switchexpr(self):
        res = ParseResult()
        cases = []
        elsecase = None

        start = self.curtoken.start

        if not self.curtoken.matches(TT_KEYWORD, KEYWORDS['case']):
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', f'{KEYWORDS["case"]}', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        res.registeradvancement()
        self.advance()

        if self.curtoken.type != TT_LPAREN:
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', '\'(\'', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )
        
        res.registeradvancement()
        self.advance()

        while self.curtoken.type == TT_EOL:
            res.registeradvancement()
            self.advance()

        varoverwrite = False
        if self.curtoken.matches(TT_KEYWORD, KEYWORDS['varcreate']):
            varoverwrite = True

            res.registeradvancement()
            self.advance()

        if self.curtoken.type != TT_IDENTIFIER:
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', 'identifier', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        vartoken = self.curtoken

        res.registeradvancement()
        self.advance()

        if not self.curtoken.matches(TT_KEYWORD, KEYWORDS['as']):
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', f'{KEYWORDS["as"]}', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        res.registeradvancement()
        self.advance()

        value = res.register(
            self.statement()
        )

        if res.error:
            return(res)

        while self.curtoken.type == TT_EOL:
            res.registeradvancement()
            self.advance()

        if self.curtoken.type != TT_RPAREN:
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', '\')\'', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        res.registeradvancement()
        self.advance()

        while self.curtoken.type == TT_EOL:
            res.registeradvancement()
            self.advance()

        if self.curtoken.type != TT_LCURLY:
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', '\'{\'', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        res.registeradvancement()
        self.advance()

        while self.curtoken.type == TT_EOL:
            res.registeradvancement()
            self.advance()

        if not self.curtoken.matches(TT_KEYWORD, KEYWORDS['when']):
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', f'{KEYWORDS["when"]}', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        cases = []
        while self.curtoken.matches(TT_KEYWORD, KEYWORDS['when']):
            res.registeradvancement()
            self.advance()

            if self.curtoken.type != TT_LPAREN:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\'(\'', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            res.registeradvancement()
            self.advance()

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            condition = res.register(
                self.statement()
            )

            if res.error:
                return(res)

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            if self.curtoken.type != TT_RPAREN:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\')\'', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            res.registeradvancement()
            self.advance()

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            codeblock = res.register(
                self.codeblock()
            )

            if res.error:
                return(res)

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            cases.append((condition, codeblock))

        elsecase = None
        if self.curtoken.matches(TT_KEYWORD, KEYWORDS['else']):
            res.registeradvancement()
            self.advance()

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()
            
            elsecase = res.register(self.codeblock())
            if res.error:
                return(res)

        while self.curtoken.type == TT_EOL:
            res.registeradvancement()
            self.advance()

        if self.curtoken.type != TT_RCURLY:
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', '\'}\'', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        res.registeradvancement()
        self.advance()

        return(
            res.success(
                SwitchNode(
                    vartoken, varoverwrite, value,
                    cases, elsecase,
                    start, self.curtoken.end
                )
            )
        )



    def loopexpr(self):
        res = ParseResult()

        if self.curtoken.matches(TT_KEYWORD, KEYWORDS['forloop']):
            res.registeradvancement()
            self.advance()

            if self.curtoken.type != TT_LPAREN:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\'(\'', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            res.registeradvancement()
            self.advance()

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            varoverwrite = False
            if self.curtoken.matches(TT_KEYWORD, KEYWORDS['varcreate']):
                varoverwrite = True

                res.registeradvancement()
                self.advance()

            if self.curtoken.type != TT_IDENTIFIER:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', 'identifier', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            vartoken = self.curtoken

            res.registeradvancement()
            self.advance()

            if not self.curtoken.matches(TT_KEYWORD, KEYWORDS['in']):
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', f'{KEYWORDS["in"]}', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            res.registeradvancement()
            self.advance()

            loopthrough = res.register(
                self.statement()
            )

            if res.error:
                return(res)

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            if self.curtoken.type != TT_RPAREN:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\')\'', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            res.registeradvancement()
            self.advance()

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()
            
            codeblock = res.register(
                self.codeblock()
            )

            if res.error:
                return(res)

            return(
                res.success(
                    ForLoopNode(
                        vartoken, varoverwrite, loopthrough, codeblock
                    )
                )
            )


        elif self.curtoken.matches(TT_KEYWORD, KEYWORDS['whileloop']):
            res.registeradvancement()
            self.advance()

            if self.curtoken.type != TT_LPAREN:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\'(\'', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            res.registeradvancement()
            self.advance()

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()
            
            condition = res.register(
                self.statement()
            )

            if res.error:
                return(res)

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()
            
            if self.curtoken.type != TT_RPAREN:
                msg = lang['exceptions']['syntaxerror']['notfound']
                msg = msg.replace('%s', '\')\'', 1)
                return(
                    res.failure(
                        Syn_SyntaxError(
                            msg,
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            res.registeradvancement()
            self.advance()

            while self.curtoken.type == TT_EOL:
                res.registeradvancement()
                self.advance()

            codeblock = res.register(
                self.codeblock()
            )

            if res.error:
                return(res)

            return(
                res.success(
                    WhileLoopNode(
                        condition, codeblock
                    )
                )
            )


        else:
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', '\'{KEYWORDS["forloop"]}\', \'KEYWORDS["whileloop"]\'', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )



    def codeblock(self):
        res = ParseResult()
        tokens = []

        if self.curtoken.type != TT_LCURLY:
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', '\'{\'', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        res.registeradvancement()
        self.advance()

        while self.curtoken.type == TT_EOL:
            res.registeradvancement()
            self.advance()

        if self.curtoken.type != TT_RCURLY:
            expr = res.register(
                self.statement()
            )

            if res.error:
                return(res)
            tokens.append(expr)

            while self.curtoken.type == TT_EOL:
                while self.curtoken.type == TT_EOL:
                    res.registeradvancement()
                    self.advance()

                if self.curtoken.type == TT_RCURLY:
                    break

                expr = res.register(
                    self.statement()
                )

                if res.error:
                    return(res)
                tokens.append(expr)

        if self.curtoken.type != TT_RCURLY:
            msg = lang['exceptions']['syntaxerror']['notfound']
            msg = msg.replace('%s', '\'}\'', 1)
            return(
                res.failure(
                    Syn_SyntaxError(
                        msg,
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        res.registeradvancement()
        self.advance()

        return(
            res.success(tokens)
        )
