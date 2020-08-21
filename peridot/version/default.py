from .types import *

def defaultvariables(symbols):
    symbols.assign('True'  , BooleanType(True))
    symbols.assign('False' , BooleanType(False))
    symbols.assign('Null'  , NullType())

    symbols.assign('throw' , BuiltInFunctionType('throw'))
    symbols.assign('assert', BuiltInFunctionType('assert'))
    symbols.assign('panic' , BuiltInFunctionType('panic'))
    symbols.assign('print' , BuiltInFunctionType('print'))

    symbols.assign('id'    , BuiltInFunctionType('id'))
    symbols.assign('str'   , BuiltInFunctionType('str'))
    symbols.assign('int'   , BuiltInFunctionType('int'))
    symbols.assign('float' , BuiltInFunctionType('float'))
    symbols.assign('bool'  , BuiltInFunctionType('bool'))
    symbols.assign('array' , BuiltInFunctionType('array'))
    symbols.assign('tuple' , BuiltInFunctionType('tuple'))

    return(symbols)