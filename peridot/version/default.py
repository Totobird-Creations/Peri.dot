from .types import *

def defaultvariables(symbols):
    symbols.assign('True'  , BooleanType(True))
    symbols.assign('False' , BooleanType(False))
    symbols.assign('Null'  , NullType())

    symbols.assign('throw' , BuiltInFunctionType('throw'))
    symbols.assign('assert', BuiltInFunctionType('assert'))
    symbols.assign('panic' , BuiltInFunctionType('panic'))
    symbols.assign('print' , BuiltInFunctionType('print'))
    symbols.assign('range' , BuiltInFunctionType('range'))

    symbols.assign('type'  , BuiltInFunctionType('type', type_=TYPES['type'], returntype=TYPES['type']))
    symbols.assign('id'    , BuiltInFunctionType('id', type_=TYPES['type'], returntype=TYPES['id']))
    symbols.assign('str'   , BuiltInFunctionType('str', type_=TYPES['type'], returntype=TYPES['string']))
    symbols.assign('int'   , BuiltInFunctionType('int', type_=TYPES['type'], returntype=TYPES['integer']))
    symbols.assign('float' , BuiltInFunctionType('float', type_=TYPES['type'], returntype=TYPES['floatingpoint']))
    symbols.assign('bool'  , BuiltInFunctionType('bool', type_=TYPES['type'], returntype=TYPES['boolean']))
    symbols.assign('array' , BuiltInFunctionType('array', type_=TYPES['type'], returntype=TYPES['list']))
    symbols.assign('tuple' , BuiltInFunctionType('tuple', type_=TYPES['type'], returntype=TYPES['tuple']))

    return(symbols)