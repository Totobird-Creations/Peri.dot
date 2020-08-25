##########################################
# DEPENDENCIES                           #
##########################################

from colorama    import init, Fore, Style, Back
init()

from .constants  import * # type: ignore
from .exceptions import * # type: ignore
from .tokens     import * # type: ignore

##########################################
# POSITION                               #
##########################################

class Position():
    def __init__(self, file_, ftext, index=-1, line=0, column=-1):
        self.index = index
        self.line = line
        self.column = column
        self.file = file_
        self.ftext = ftext
        self.lntext = self.ftext.split('\n')[self.line]

    def advance(self, char=None):
        self.index += 1
        self.column += 1
        if char == '\n':
            self.line += 1
            self.column = 0
        self.lntext = self.ftext.split('\n')[self.line]

        return(self)

    def retreat(self, char=None):
        self.index -= 1
        self.column -= 1
        if char == '\n':
            self.line -= 1
            self.column = len(self.ftext.split('\n')[self.line]) - 1
        self.lntext = self.ftext.split('\n')[self.line]

        return(self)

    def copy(self):
        return(Position(self.file, self.ftext, index=self.index, line=self.line, column=self.column))

##########################################
# LEXER                                  #
##########################################

class Lexer():
    def __init__(self, file_, text):
        self.file = file_
        self.text = text
        self.pos = Position(file_, text)
        self.char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.char)
        if self.pos.index < len(self.text):
            self.char = self.text[self.pos.index]
        else:
            self.char = None

    def retreat(self):
        self.pos.retreat(self.char)
        self.char = self.text[self.pos.index]



    def maketokens(self):
        tokens = []
        while self.char != None:


            if self.char in ' \t':
                self.advance()

            elif self.char == '\n':
                tokens.append(Token(TT_EOL, start=self.pos))
                self.advance()


            elif self.char in DIGITS:
                tokens.append(self.makenumber())

            elif self.char in '"\'':
                token, error = self.makestring(self.char)

                if error:
                    return(([], error))

                tokens.append(token)


            elif self.char == '+':
                tokens.append(Token(TT_PLUS, start=self.pos))
                self.advance()

            elif self.char == '-':
                token, error = self.makedash()

                if error:
                    return(([], error))

                tokens.append(token)

            elif self.char == '*':
                tokens.append(Token(TT_ASTRISK, start=self.pos))
                self.advance()

            elif self.char == '/':
                tokens.append(Token(TT_FSLASH, start=self.pos))
                self.advance()

            elif self.char == '^':
                tokens.append(Token(TT_CARAT, start=self.pos))
                self.advance()

            elif self.char == '=':
                token, error = self.makeequals()

                if error:
                    return(([], error))

                tokens.append(token)

            elif self.char == '!':
                token, error = self.makebang()

                if error:
                    return(([], error))

                tokens.append(token)

            elif self.char == '<':
                token, error = self.makelessthan()

                if error:
                    return(([], error))

                tokens.append(token)

            elif self.char == '>':
                token, error = self.makegreaterthan()

                if error:
                    return(([], error))

                tokens.append(token)


            elif self.char == ',':
                tokens.append(Token(TT_COMMA, start=self.pos))
                self.advance()

            elif self.char == ':':
                tokens.append(Token(TT_COLON, start=self.pos))
                self.advance()

            elif self.char == '.':
                tokens.append(Token(TT_PERIOD, start=self.pos))
                self.advance()


            elif self.char == '(':
                tokens.append(Token(TT_LPAREN, start=self.pos))
                self.advance()

            elif self.char == ')':
                tokens.append(Token(TT_RPAREN, start=self.pos))
                self.advance()

            elif self.char == '{':
                tokens.append(Token(TT_LCURLY, start=self.pos))
                self.advance()

            elif self.char == '}':
                tokens.append(Token(TT_RCURLY, start=self.pos))
                self.advance()

            elif self.char == '[':
                tokens.append(Token(TT_LSQUARE, start=self.pos))
                self.advance()

            elif self.char == ']':
                tokens.append(Token(TT_RSQUARE, start=self.pos))
                self.advance()


            elif self.char in ALPHABET + '_':
                token, error = self.makeidentifier()

                if error:
                    return(([], error))

                tokens.append(token)


            elif self.char == '#':
                self.advance()

                if self.char == '=':
                    while True:
                        self.advance()

                        if self.char == None:
                            break

                        if self.char == '=':
                            self.advance()
                            if self.char == '#':
                                self.advance()
                                break
                else:
                    while self.char not in ['\n', None]:
                        self.advance()

            else:
                start = self.pos.copy()
                char = self.char
                self.advance()

                return(([], Syn_SyntaxError(f'Illegal character "{char}" was found', start=start, end=self.pos)))


        tokens.append(Token(TT_EOL, start=self.pos))
        tokens.append(Token(TT_EOF, start=self.pos))
        return((tokens, None))



    def makenumber(self):
        num = ''
        dots = 0
        start = self.pos.copy()

        while self.char != None and self.char in DIGITS + '.':
            if self.char == '.':
                if dots >= 1: break
                dots += 1
                num += '.'
            else:
                num += self.char
            self.advance()

        if dots == 0:
            return(Token(TT_INT, int(num), start=start, end=self.pos))
        else:
            return(Token(TT_FLOAT, float(num), start=start, end=self.pos))


    def makestring(self, quotetype):
        string = ''
        start = self.pos.copy()
        escstart = self.pos.copy()

        chars = {
            '\\' : '\\',
            'n'  : '\n',
            '\n' : '\n',
            't'  : '\t',
            '\'' : '\'',
            '\"' : '\"',
            'x20': Style.NORMAL,
            'x30': Fore.BLACK,
            'x31': Fore.RED,
            'x32': Fore.GREEN,
            'x33': Fore.YELLOW,
            'x34': Fore.BLUE,
            'x35': Fore.MAGENTA,
            'x36': Fore.CYAN,
            'x37': Fore.WHITE,
            'x39': Fore.RESET,
            'x40': Back.BLACK,
            'x41': Back.RED,
            'x42': Back.GREEN,
            'x43': Back.YELLOW,
            'x44': Back.BLUE,
            'x45': Back.MAGENTA,
            'x46': Back.CYAN,
            'x47': Back.WHITE,
            'x49': Back.RESET,
            'x90': Fore.LIGHTBLACK_EX,
            'x91': Fore.LIGHTRED_EX,
            'x92': Fore.LIGHTGREEN_EX,
            'x93': Fore.LIGHTYELLOW_EX,
            'x94': Fore.LIGHTBLUE_EX,
            'x95': Fore.LIGHTMAGENTA_EX,
            'x96': Fore.LIGHTCYAN_EX,
            'x97': Fore.LIGHTWHITE_EX,
            'x100': Back.LIGHTBLACK_EX,
            'x101': Back.LIGHTRED_EX,
            'x102': Back.LIGHTGREEN_EX,
            'x103': Back.LIGHTYELLOW_EX,
            'x104': Back.LIGHTBLUE_EX,
            'x105': Back.LIGHTMAGENTA_EX,
            'x106': Back.LIGHTCYAN_EX,
            'x107': Back.LIGHTWHITE_EX,
            'x0' : Style.RESET_ALL,
            'x1' : Style.BRIGHT,
            'x2' : Style.DIM
        }
        escaped = False

        self.advance()

        while self.char != None and (self.char != quotetype or escaped):
            if escaped:
                char = None
                escchars = ''
                for i in list(chars.keys()):
                    escchars = ''
                    for j in range(len(i)):
                        escchars += f'{self.char}'
                        if i[j] != self.char: break
                        elif j == len(i) - 1:
                            char = chars[escchars]
                            break
                        self.advance()

                    if char: break

                    for i in range(j):
                        self.retreat()

                if not char:
                    end = self.pos.copy()
                    for i in range(len(escchars)):
                        end.advance()
                    return((None, Syn_EscapeError(f'\'{escchars}\' can not be escaped', start=escstart, end=end)))
                string += char

                escaped = False
            else:
                if self.char == '\\':
                    escstart = self.pos.copy()
                    escaped = True
                elif self.char == '\n':
                    end = self.pos.copy()
                    end.advance()
                    return((None, Syn_SyntaxError(f'Invalid EOL, expected \'{quotetype}\'', start=self.pos, end=end)))
                else:
                    string += self.char
            self.advance()

        if not self.char:
            end = self.pos.copy()
            end.advance()
            return((None, Syn_SyntaxError(f'Invalid EOF, expected \'{quotetype}\'', start=self.pos, end=end)))

        self.advance()

        return((Token(TT_STRING, string, start=start, end=self.pos), None))


    def makedash(self):
        start = self.pos.copy()

        self.advance()

        if self.char == '>':
            self.advance()
            return((Token(TT_ARROW, string, start=start, end=self.pos), None))

        return((Token(TT_DASH, string, start=start, end=self.pos), None))


    def makeequals(self):
        start = self.pos.copy()

        self.advance()

        if self.char == '=':
            self.advance()
            return((Token(TT_EQEQUALS, string, start=start, end=self.pos), None))

        return((Token(TT_EQUALS, string, start=start, end=self.pos), None))


    def makebang(self):
        start = self.pos.copy()

        self.advance()

        if self.char == '=':
            self.advance()
            return((Token(TT_BANGEQUALS, string, start=start, end=self.pos), None))

        return((None, Syn_EscapeError(f'Expected \'=\' not found', start=self.pos, end=self.pos.copy())))


    def makelessthan(self):
        start = self.pos.copy()

        self.advance()

        if self.char == '=':
            self.advance()
            return((Token(TT_LTEQUALS, string, start=start, end=self.pos), None))

        return((Token(TT_LESSTHAN, string, start=start, end=self.pos), None))


    def makegreaterthan(self):
        start = self.pos.copy()

        self.advance()

        if self.char == '=':
            self.advance()
            return((Token(TT_GTEQUALS, string, start=start, end=self.pos), None))

        return((Token(TT_GREATERTHAN, string, start=start, end=self.pos), None))


    def makeidentifier(self):
        identifier = ''
        start = self.pos.copy()

        while self.char != None and self.char in ALPHANUMERIC + '_':
            identifier += self.char

            self.advance()

        if identifier in [KEYWORDS[i] for i in KEYWORDS.keys()]:
            return((Token(TT_KEYWORD, identifier, start=start, end=self.pos), None))

        return((Token(TT_IDENTIFIER, identifier, start=start, end=self.pos), None))
