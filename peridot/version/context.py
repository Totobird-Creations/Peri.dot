##########################################
# DEPENDENCIES                           #
##########################################

from typing import Any as _Any

##########################################
# CONTEXT                                #
##########################################

class Context():
    def __init__(self, display, symbols=None, parent=None, parententry=None, caughterrors=None):
        self.display      = display
        self.parent       = parent
        self.parententry  = parententry

        self.symbols      = symbols

        self.caughterrors = []

    def caughterror(self, error):
        if self.parent:
            self.parent.caughterror(error)
        self.caughterrors.append(error)

    def copy(self):
        ctx = Context(self.display, self.symbols.copy(), self.parent, self.parententry, self.caughterrors)
        return(ctx)

##########################################
# SYMBOL TABLE                           #
##########################################

class SymbolTable():
    def __init__(self, parent=None):
        self.symbols = {}

        self.parent = parent


    def access(self, name: str) -> _Any:
        value = self.symbols.get(name, None)

        if value == None and self.parent:
            return(
                self.parent.access(name)
            )

        return(value)


    def assign(self, name: str, value: _Any):
        self.symbols[name] = value


    def remove(self, name: str):
        del self.symbols[name]

    def copy(self):
        sym = SymbolTable(self.parent)
        sym.symbols = self.symbols.copy()
        return(sym)