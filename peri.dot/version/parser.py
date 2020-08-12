##########################################
# DEPENDENCIES                           #
##########################################

from .constants  import *
from .exceptions import *
from .nodes      import *
from .tokens     import *

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
        res = self.expr()
        if not res.error and self.curtoken.type != TT_EOF:
            return(
                res.failure(
                    Exc_SyntaxError(
                        'Expected operation not found',
                        self.curtoken.start, self.curtoken.end
                    )
                )
            )

        return(res)


    def binaryop(self, funca, optypes, funcb=None):
        if not funcb:
            funcb = funca

        res = ParseResult()

        lfactor = res.register(funca())

        if res.error:
            return(res)

        while self.curtoken.type in optypes:
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


    def expr(self):
        res = ParseResult()

        if self.curtoken.matches(TT_KEYWORD, KEYWORDS['varcreate']):
            res.registeradvancement()
            self.advance()

            if self.curtoken.type != TT_IDENTIFIER:
                return(
                    res.failure(
                        Exc_SyntaxError(
                            'Expected identifier not found',
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            variables = [self.curtoken]
            res.registeradvancement()
            self.advance()

            while self.curtoken.type == TT_COMMA:
                res.registeradvancement()
                self.advance()

                if self.curtoken.type != TT_IDENTIFIER:
                    return(
                        res.failure(
                            Exc_SyntaxError(
                                'Expected identifier not found',
                                self.curtoken.start, self.curtoken.end
                            )
                        )
                    )

                variables.append(self.curtoken)

                res.registeradvancement()
                self.advance()

            if self.curtoken.type != TT_EQUALS:
                return(
                    res.success(
                        VarNullNode(
                            variables
                        )
                    )
                )

            res.registeradvancement()
            self.advance()

            expr = res.register(self.expr())

            if res.error:
                return(res)

            return(
                res.success(
                    VarCreateNode(
                        variables, expr
                    )
                )
            )

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
                (TT_CARAT)
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

        return(self.atom())


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

            expr = res.register(self.expr())

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


        elif token.type == TT_IDENTIFIER:
            variables = [token]
            res.registeradvancement()
            self.advance()

            while self.curtoken.type == TT_COMMA:
                res.registeradvancement()
                self.advance()

                if self.curtoken.type != TT_IDENTIFIER:
                    return(
                        res.failure(
                            Exc_SyntaxError(
                                'Expected identifier not found',
                                self.curtoken.start, self.curtoken.end
                            )
                        )
                    )

                variables.append(self.curtoken)

                res.registeradvancement()
                self.advance()

            if self.curtoken.type == TT_EQUALS:
                res.registeradvancement()
                self.advance()

                expr = res.register(self.expr())

                return(
                    res.success(
                        VarAssignNode(
                            variables, expr
                        )
                    )
                )
            elif len(variables) > 1:
                return(
                    res.failure(
                        Exc_SyntaxError(
                            'Expected \'=\' not found',
                            self.curtoken.start, self.curtoken.end
                        )
                    )
                )

            return(
                res.success(
                    VarAccessNode(token)
                )
            )


        return(
                res.failure(
                    Exc_SyntaxError(
                        'Expected identifier, keyword, operation, type not found',
                        token.start, token.end 
                    )
                )
            )
