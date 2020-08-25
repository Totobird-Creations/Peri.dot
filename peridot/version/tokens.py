##########################################
# TOKENS                                 #
##########################################

TT_INT         = 'INT'
TT_FLOAT       = 'FLOAT'
TT_STRING      = 'STRING'

TT_PLUS        = '+'
TT_DASH        = '-'
TT_ASTRISK     = '*'
TT_FSLASH      = '/'
TT_CARAT       = '^'

TT_LPAREN      = 'LPAREN'
TT_RPAREN      = 'RPAREN'
TT_LCURLY      = 'LCURLY'
TT_RCURLY      = 'RCURLY'
TT_LSQUARE     = 'LSQUARE'
TT_RSQUARE     = 'RSQUARE'

TT_EQUALS      = 'EQUALS'
TT_COMMA       = 'COMMA'
TT_COLON       = 'COLON'
TT_ARROW       = 'ARROW'
TT_PERIOD      = 'PERIOD'

TT_EQEQUALS    = '=='
TT_BANGEQUALS  = '!='
TT_LESSTHAN    = '<'
TT_LTEQUALS    = '<='
TT_GREATERTHAN = '>'
TT_GTEQUALS    = '>='

TT_KEYWORD     = 'KEYWORD'
TT_IDENTIFIER  = 'IDENTIFIER'

TT_EOL         = 'EOL'
TT_EOF         = 'EOF'

##########################################
# TOKEN OBJECT                           #
##########################################

class Token():
    def __init__(self, type_, value=None, start=None, end=None):
        self.type = type_
        self.value = value
        if start:
            self.start = start.copy()

        if end:
            self.end = end.copy()
        else:
            self.end = start.copy()
            self.end.advance()

    def __repr__(self):
        if isinstance(self.value, str):
            value = f'"{self.value}"'
        else:
            value = self.value

        if self.value:
            return(f'<{self.type}: {value}>')
        else:
            return(f'<{self.type}>')

    def matches(self, type_, value):
        return(self.type == type_ and self.value == value)
