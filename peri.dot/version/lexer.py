##########################################
# DEPENDENCIES                           #
##########################################

from .constants  import *
from .exceptions import *
from .tokens     import *

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

    def advance(self, char=None):
        self.index += 1
        self.column += 1
        if char == '\n':
            self.line += 1
            self.column = 0

        return(self)

    def retreat(self, char=None):
        self.index -= 1
        self.column += 1
        if char == '\n':
            self.line -= 1
            self.column = len(self.ftext.split('\n')[self.line]) - 1

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

            elif self.char in '\n':
                tokens.append(Token(TT_EOL, start=self.pos))
                self.advance()

            elif self.char in DIGITS + '.':
                tokens.append(self.makenumber())

            else:
                start = self.pos.copy()
                char = self.char
                self.advance()

                return(([], E_SyntaxError(f'Illegal character "{char}" was found', start, self.pos.column, self.text)))

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