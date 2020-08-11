# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
'''
This module generates ANSI character codes to printing colors to terminals.
See: http://en.wikipedia.org/wiki/ANSI_escape_code
'''

CSI = '\033['
OSC = '\033]'
BEL = '\a'


def code_to_chars(code):
    return CSI + str(code) + 'm'

def set_title(title):
    return OSC + '2;' + title + BEL

def clear_screen(mode=2):
    return CSI + str(mode) + 'J'

def clear_line(mode=2):
    return CSI + str(mode) + 'K'


class AnsiCodes(object):
    def __init__(self):
        # the subclasses declare class attributes which are numbers.
        # Upon instantiation we define instance attributes, which are the same
        # as the class attributes but wrapped with the ANSI escape sequence
        for name in dir(self):
            if not name.startswith('_'):
                value = getattr(self, name)
                setattr(self, name, code_to_chars(value))


class AnsiCursor(object):
    def UP(self, n=1):
        return CSI + str(n) + 'A'
    def DOWN(self, n=1):
        return CSI + str(n) + 'B'
    def FORWARD(self, n=1):
        return CSI + str(n) + 'C'
    def BACK(self, n=1):
        return CSI + str(n) + 'D'
    def POS(self, x=1, y=1):
        return CSI + str(y) + ';' + str(x) + 'H'


class AnsiFore(AnsiCodes):
    BLACK           = 30
    RED             = 31
    GREEN           = 32
    YELLOW          = 33
    BLUE            = 34
    MAGENTA         = 35
    CYAN            = 36
    WHITE           = 37
    RESET           = 39

    # These are fairly well supported, but not part of the standard.
    LIGHTBLACK   = 90
    LIGHTRED     = 91
    LIGHTGREEN   = 92
    LIGHTYELLOW  = 93
    LIGHTBLUE    = 94
    LIGHTMAGENTA = 95
    LIGHTCYAN    = 96
    LIGHTWHITE   = 97


class AnsiBack(AnsiCodes):
    BLACK           = 40
    RED             = 41
    GREEN           = 42
    YELLOW          = 43
    BLUE            = 44
    MAGENTA         = 45
    CYAN            = 46
    WHITE           = 47
    RESET           = 49

    # These are fairly well supported, but not part of the standard.
    LIGHTBLACK   = 100
    LIGHTRED     = 101
    LIGHTGREEN   = 102
    LIGHTYELLOW  = 103
    LIGHTBLUE    = 104
    LIGHTMAGENTA = 105
    LIGHTCYAN    = 106
    LIGHTWHITE   = 107


class AnsiStyle(AnsiCodes):
    BRIGHT          = 1
    DIM             = 2
    ITALIC          = 3
    UNDERLINE       = 4
    BLINK           = 5
    FASTBLINK       = 6
    REVERSE         = 7
    HIDDEN          = 8
    STRIKETHROUGH   = 9
    DOUBLEUNDERLINE = 21
    NORMAL          = 22
    OVERLINE        = 53
    RESET_ALL       = 0

Fore   = AnsiFore()
Back   = AnsiBack()
Style  = AnsiStyle()
Cursor = AnsiCursor()