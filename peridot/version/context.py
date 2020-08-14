##########################################
# DEPENDENCIES                           #
##########################################

from typing import Any

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
    def __init__(self, parent=None):
        self.symbols = {}

        self.parent = parent


    def access(self, name: str) -> Any:
        value = self.symbols.get(name, None)

        if value == None and self.parent:
            return(
                self.parent.get(name)
            )

        return(value)


    def assign(self, name: str, value: Any):
        self.symbols[name] = value


    def remove(self, name: str):
        del self.symbols[name]