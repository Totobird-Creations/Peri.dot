from .types import *

def defaultvariables(symbols):
    symbols.assign('True',  BooleanType(True))
    symbols.assign('False', BooleanType(False))
    symbols.assign('Null',  NullType())
    symbols.assign('print', BuiltInFunctionType('print'))

    return(symbols)