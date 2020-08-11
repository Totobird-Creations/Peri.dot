##########################################
# TOKENS                                 #
##########################################

TT_INT        = 'INT'
TT_FLOAT      = 'FLOAT'
TT_STRING     = 'STRING'

TT_PLUS       = 'PLUS'
TT_DASH       = 'MINUS'
TT_ASTRISK    = 'TIMES'
TT_FSLASH     = 'DIVBY'
TT_CARAT      = 'RAISED'

TT_LPAREN     = 'LPAREN'
TT_RPAREN     = 'RPAREN'

TT_KEYWORD    = 'KEYWORD'
TT_IDENTIFIER = 'IDENTIFIER'

TT_EOL        = 'EOL'
TT_EOF        = 'EOF'

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
