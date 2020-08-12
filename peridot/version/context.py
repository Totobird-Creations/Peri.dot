##########################################
# CONTEXT                                #
##########################################

class Context():
    def __init__(self, display, symbols=None, parent=None, parententry=None):
        self.display     = display
        self.parent      = parent
        self.parententry = parententry

        self.symbols     = symbols

##########################################
# SYMBOL TABLE                           #
##########################################

class SymbolTable():
    def __init__(self):
        self.symbols = {}

        self.parent = None


    def access(self, name):
        value = self.symbols.get(name, None)

        if value == None and self.parent:
            return(
                self.parent.get(name)
            )

        return(value)


    def assign(self, name, value):
        self.symbols[name] = value


    def remove(self, name):
        del self.symbols[name]