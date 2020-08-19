##########################################
# DEPENDENCIES                           #
##########################################

from .constants  import * # type: ignore
from .exceptions import * # type: ignore
from .nodes      import * # type: ignore
from .tokens     import * # type: ignore

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
                return(
                    res.failure(
                        Syn_SyntaxError(
                            'Invalid EOL',
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
                return(
                    res.failure(
                        Syn_SyntaxError(
                            'Expected \'(\' not found',
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            res.registeradvancement()
            self.advance()

            expr = res.tryregister(
                self.expr()
            )

            if not expr:
                for i in range(2):
                    res.registerretreat()
                    self.retreat()

            if self.curtoken.type != TT_RPAREN:
                return(
                    res.failure(
                        Syn_SyntaxError(
                            'Expected \')\' not found',
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            res.registeradvancement()
            self.advance()

            return(
                res.success(
                    ReturnNode(expr, start, self.curtoken.start.copy())
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
                return(
                    res.failure(
                        Syn_SyntaxError(
                            'Expected identifier not found',
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
            return(
                res.failure(
                    Syn_SyntaxError(
                        'Expected identifier, keyword, operator, type not found',
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
            return(
                res.failure(
                    Syn_SyntaxError(
                        'Expected identifier, keyword, operator, type not found',
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

        return(self.call())


    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())

        if res.error:
            return(res)

        if self.curtoken.type == TT_LPAREN:
            res.registeradvancement()
            self.advance()

            args = []
            options = {}

            if self.curtoken.type == TT_RPAREN:
                end = self.curtoken.end.copy()
                res.registeradvancement()
                self.advance()
            else:
                args.append(
                    res.register(
                        self.statement()
                    )
                )

                if res.error:
                    return(
                        res.failure(
                            Syn_SyntaxError(
                                'Expected \')\', identifier, keyword, operation, type not found',
                                self.curtoken.start, self.curtoken.end
                            )
                        )
                    )


                while self.curtoken.type == TT_COMMA:
                    res.registeradvancement()
                    self.advance()

                    if self.curtoken.type == TT_IDENTIFIER:
                        token = self.curtoken
                        res.registeradvancement()
                        self.advance()

                        if self.curtoken.type == TT_EQUALS:
                            res.registeradvancement()
                            self.advance()

                            options[token.value] = res.register(
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


                if self.curtoken.type != TT_RPAREN:
                    return(
                        res.failure(
                            Syn_SyntaxError(
                                f'Expected \',\', \')\' not found',
                                self.curtoken.start, self.curtoken.end
                            )
                        )
                    )

                end = self.curtoken.end.copy()
                res.registeradvancement()
                self.advance()

            return(
                res.success(
                    VarCallNode(
                        atom,
                        args, options,
                        end=end
                    )
                )
            )

        return(res.success(atom))


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
            res.registeradvancement()
            self.advance()

            expr = res.register(
                self.statement()
            )

            if res.error:
                return(res)

            if self.curtoken.type == TT_RPAREN:
                res.registeradvancement()
                self.advance()

                return(
                    res.success(
                        expr
                    )
                )

            return(
                res.failure(
                    'Expected \')\' not found',
                    token.start, token.end
                )
            )

        elif token.type == TT_LSQUARE:
            listexpr = res.register(
                self.listexpr()
            )

            if res.error:
                return(res)

            return(
                res.success(
                    listexpr
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

        elif token.matches(TT_KEYWORD, KEYWORDS['funccreate']):
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

        return(
            res.failure(
                Syn_SyntaxError(
                    'Expected identifier, keyword, operator, type not found',
                    token.start, token.end 
                )
            )
        )


    def listexpr(self):
        res = ParseResult()
        elmnodes = []
        start = self.curtoken.start.copy()

        if not self.curtoken.type == TT_LSQUARE:
            return(
                res.failure(
                    Syn_SyntaxError(
                        f'Expected \'[\' not found',
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

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
                return(
                    res.failure(
                        Syn_SyntaxError(
                            'Expected \']\', identifier, keyword, operation, type not found',
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            while self.curtoken.type == TT_COMMA:
                res.registeradvancement()
                self.advance()

                elmnodes.append(
                    res.register(
                        self.statement()
                    )
                )

                if res.error:
                    return(res)

            if self.curtoken.type != TT_RSQUARE:
                return(
                    res.failure(
                        Syn_SyntaxError(
                            'Expected \',\', \']\' not found',
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


    def funcdef(self):
        res = ParseResult()

        if not self.curtoken.matches(TT_KEYWORD, KEYWORDS['funccreate']):
            return(
                res.failure(
                    Syn_SyntaxError(
                        f'Expected \'{KEYWORDS["funccreate"]}\' not found',
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        token = self.curtoken

        res.registeradvancement()
        self.advance()

        if self.curtoken.type != TT_LPAREN:
            return(
                res.failure(
                    Syn_SyntaxError(
                        f'Expected \'(\' not found',
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        res.registeradvancement()
        self.advance()

        argtokens = []

        if self.curtoken.type == TT_IDENTIFIER:
            argtokens.append(self.curtoken)

            res.registeradvancement()
            self.advance()

            while self.curtoken.type == TT_COMMA:
                res.registeradvancement()
                self.advance()

                if self.curtoken.type != TT_IDENTIFIER:
                    return(
                        res.failure(
                            Syn_SyntaxError(
                                f'Expected identifier not found',
                                self.curtoken.start, self.curtoken.end
                            )
                        )
                    )

                argtokens.append(self.curtoken)
                res.registeradvancement()
                self.advance()

            if self.curtoken.type != TT_RPAREN:
                return(
                    res.failure(
                        Syn_SyntaxError(
                            f'Expected \')\', \',\' not found',
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

        elif self.curtoken.type != TT_RPAREN:
            return(
                res.failure(
                    Syn_SyntaxError(
                        f'Expected \')\', identifier not found',
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        res.registeradvancement()
        self.advance()

        codeblock = res.register(
            self.codeblock()
        )

        if res.error:
            return(res)

        return(
            res.success(
                FuncCreateNode(
                    token,
                    argtokens,
                    codeblock,
                    False
                )
            )
        )


    def handler(self):
        res = ParseResult()

        if not self.curtoken.matches(TT_KEYWORD, KEYWORDS['handler']):
            return(
                res.failure(
                    Syn_SyntaxError(
                        f'Expected \'{KEYWORDS["handler"]}\' not found',
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        token = self.curtoken

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


    def codeblock(self):
        res = ParseResult()
        tokens = []

        if self.curtoken.type != TT_LCURLY:
            return(
                res.failure(
                    Syn_SyntaxError(
                        'Expected \'{\' not found',
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        res.registeradvancement()
        self.advance()

        if self.curtoken.type == TT_EOL:
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

        elif self.curtoken.type != TT_RCURLY:
            expr = res.register(
                self.statement()
            )

            if res.error:
                return(res)
            tokens.append(expr)

        if self.curtoken.type != TT_RCURLY:
            return(
                res.failure(
                    Syn_SyntaxError(
                        'Expected \'}\' not found',
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        res.registeradvancement()
        self.advance()

        return(
            res.success(tokens)
        )