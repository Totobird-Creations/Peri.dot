##########################################
# TOKENS                                 #
##########################################

TT_INT        = 'INT'
TT_FLOAT      = 'FLOAT'
TT_STRING     = 'STRING'

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
            self.end = start.copy()
            self.end.advance()
        if end:
            self.end = end.copy()

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