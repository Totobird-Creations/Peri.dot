##########################################
# DEPENDENCIES                           #
##########################################

from colorama    import init as _init, Fore as _Fore, Style as _Style, Back as _Back
_init()

def _lexerinit(conf, constants, tokens, exceptions):
    global lang
    lang            = conf
    global DIGITS, ALPHABET, ALPHANUMERIC, KEYWORDS
    DIGITS          = constants.DIGITS
    ALPHABET        = constants.ALPHABET
    ALPHANUMERIC    = constants.ALPHANUMERIC
    KEYWORDS        = constants.KEYWORDS
    global Token, TT_EOL, TT_PLUS, TT_ASTRISK, TT_FSLASH, TT_CARAT, TT_COMMA, TT_COLON, TT_PERIOD, TT_LPAREN, TT_RPAREN, TT_LCURLY, TT_RCURLY, TT_LSQUARE, TT_RSQUARE, TT_EOF, TT_INT, TT_FLOAT, TT_STRING, TT_ARROW, TT_DASH, TT_EQEQUALS, TT_EQUALS, TT_BANGEQUALS, TT_LTEQUALS, TT_LESSTHAN, TT_GTEQUALS, TT_GREATERTHAN, TT_KEYWORD, TT_IDENTIFIER
    Token           = tokens.Token
    TT_EOL          = tokens.TT_EOL
    TT_PLUS         = tokens.TT_PLUS
    TT_ASTRISK      = tokens.TT_ASTRISK
    TT_FSLASH       = tokens.TT_FSLASH
    TT_CARAT        = tokens.TT_CARAT
    TT_COMMA        = tokens.TT_COMMA
    TT_COLON        = tokens.TT_COLON
    TT_PERIOD       = tokens.TT_PERIOD
    TT_LPAREN       = tokens.TT_LPAREN
    TT_RPAREN       = tokens.TT_RPAREN
    TT_LCURLY       = tokens.TT_LCURLY
    TT_RCURLY       = tokens.TT_RCURLY
    TT_LSQUARE      = tokens.TT_LSQUARE
    TT_RSQUARE      = tokens.TT_RSQUARE
    TT_EOF          = tokens.TT_EOF
    TT_INT          = tokens.TT_INT
    TT_FLOAT        = tokens.TT_FLOAT
    TT_STRING       = tokens.TT_STRING
    TT_ARROW        = tokens.TT_ARROW
    TT_DASH         = tokens.TT_DASH
    TT_EQEQUALS     = tokens.TT_EQEQUALS
    TT_EQUALS       = tokens.TT_EQUALS
    TT_BANGEQUALS   = tokens.TT_BANGEQUALS
    TT_LTEQUALS     = tokens.TT_LTEQUALS
    TT_LESSTHAN     = tokens.TT_LESSTHAN
    TT_GTEQUALS     = tokens.TT_GTEQUALS
    TT_GREATERTHAN  = tokens.TT_GREATERTHAN
    TT_KEYWORD      = tokens.TT_KEYWORD
    TT_IDENTIFIER   = tokens.TT_IDENTIFIER
    global Syn_SyntaxError, Syn_EscapeError
    Syn_SyntaxError = exceptions.Syn_SyntaxError
    Syn_EscapeError = exceptions.Syn_EscapeError

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

                msg = lang['exceptions']['syntaxerror']['illegalchar']
                msg = msg.replace('%s', char, 1)
                return(([], Syn_SyntaxError(msg, start=start, end=self.pos)))


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

        self.retreat()
        if self.char != '.':
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
            '033[20m': _Style.NORMAL,
            '033[30m': _Fore.BLACK,
            '033[31m': _Fore.RED,
            '033[32m': _Fore.GREEN,
            '033[33m': _Fore.YELLOW,
            '033[34m': _Fore.BLUE,
            '033[35m': _Fore.MAGENTA,
            '033[36m': _Fore.CYAN,
            '033[37m': _Fore.WHITE,
            '033[39m': _Fore.RESET,
            '033[40m': _Back.BLACK,
            '033[41m': _Back.RED,
            '033[42m': _Back.GREEN,
            '033[43m': _Back.YELLOW,
            '033[44m': _Back.BLUE,
            '033[45m': _Back.MAGENTA,
            '033[46m': _Back.CYAN,
            '033[47m': _Back.WHITE,
            '033[49m': _Back.RESET,
            '033[90m': _Fore.LIGHTBLACK_EX,
            '033[91m': _Fore.LIGHTRED_EX,
            '033[92m': _Fore.LIGHTGREEN_EX,
            '033[93m': _Fore.LIGHTYELLOW_EX,
            '033[94m': _Fore.LIGHTBLUE_EX,
            '033[95m': _Fore.LIGHTMAGENTA_EX,
            '033[96m': _Fore.LIGHTCYAN_EX,
            '033[97m': _Fore.LIGHTWHITE_EX,
            '033[100m': _Back.LIGHTBLACK_EX,
            '033[101m': _Back.LIGHTRED_EX,
            '033[102m': _Back.LIGHTGREEN_EX,
            '033[103m': _Back.LIGHTYELLOW_EX,
            '033[104m': _Back.LIGHTBLUE_EX,
            '033[105m': _Back.LIGHTMAGENTA_EX,
            '033[106m': _Back.LIGHTCYAN_EX,
            '033[107m': _Back.LIGHTWHITE_EX,
            '033[0m' : _Style.RESET_ALL,
            '033[1m' : _Style.BRIGHT,
            '033[2m' : _Style.DIM
        }
        escaped = False

        self.advance()

        while self.char != None and (self.char != quotetype or escaped):
            if escaped:
                char = None
                escchars = ''
                for i in list(chars.keys()):
                    escchars = ''
                    j = 0
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
                    msg = lang['exceptions']['escapeerror']['cannot']
                    msg = msg.replace('%s', escchars, 1)
                    return((None, Syn_EscapeError(msg, start=escstart, end=end)))
                string += char

                escaped = False
            else:
                if self.char == '\\':
                    escstart = self.pos.copy()
                    escaped = True
                elif self.char == '\n':
                    end = self.pos.copy()
                    end.advance()
                    msg = lang['exceptions']['syntaxerror']['invalideofl']
                    msg = msg.replace('%s', 'L', 1)
                    msg = msg.replace('%s', f'\'{quotetype}\'', 1)
                    return((None, Syn_SyntaxError(msg, start=self.pos, end=end)))
                else:
                    string += self.char
            self.advance()

        if not self.char:
            end = self.pos.copy()
            end.advance()
            msg = lang['exceptions']['syntaxerror']['invalideofl']
            msg = msg.replace('%s', 'F', 1)
            msg = msg.replace('%s', f'\'{quotetype}\'', 1)
            return((None, Syn_SyntaxError(msg, start=self.pos, end=end)))

        self.advance()

        return((Token(TT_STRING, string, start=start, end=self.pos), None))


    def makedash(self):
        start = self.pos.copy()

        self.advance()

        if self.char == '>':
            self.advance()
            return((Token(TT_ARROW, None, start=start, end=self.pos), None))

        return((Token(TT_DASH, None, start=start, end=self.pos), None))


    def makeequals(self):
        start = self.pos.copy()

        self.advance()

        if self.char == '=':
            self.advance()
            return((Token(TT_EQEQUALS, None, start=start, end=self.pos), None))

        return((Token(TT_EQUALS, None, start=start, end=self.pos), None))


    def makebang(self):
        start = self.pos.copy()

        self.advance()

        if self.char == '=':
            self.advance()
            return((Token(TT_BANGEQUALS, None, start=start, end=self.pos), None))

        end = self.pos.copy()
        end.advance()
        msg = lang['exceptions']['syntaxerror']['notfound']
        msg = msg.replace('%s', '\'=\'', 1)
        return((None, Syn_EscapeError(msg, start=self.pos, end=end)))


    def makelessthan(self):
        start = self.pos.copy()

        self.advance()

        if self.char == '=':
            self.advance()
            return((Token(TT_LTEQUALS, None, start=start, end=self.pos), None))

        return((Token(TT_LESSTHAN, None, start=start, end=self.pos), None))


    def makegreaterthan(self):
        start = self.pos.copy()

        self.advance()

        if self.char == '=':
            self.advance()
            return((Token(TT_GTEQUALS, None, start=start, end=self.pos), None))

        return((Token(TT_GREATERTHAN, None, start=start, end=self.pos), None))


    def makeidentifier(self):
        identifier = ''
        start = self.pos.copy()

        while self.char != None and self.char in ALPHANUMERIC + '_':
            identifier += self.char

            self.advance()

        if identifier in [KEYWORDS[i] for i in KEYWORDS.keys()]:
            return((Token(TT_KEYWORD, identifier, start=start, end=self.pos), None))

        return((Token(TT_IDENTIFIER, identifier, start=start, end=self.pos), None))
