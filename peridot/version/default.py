##########################################
# DEPENDENCIES                           #
##########################################

def _defaultinit(appversion, file, types, context):
    global  __file__, version,SymbolTable
    __file__            = file
    version             = appversion
    SymbolTable         = context.SymbolTable
    global TYPES, ArrayType, BooleanType, BuiltInFunctionType, FloatType, IdType, IntType, NamespaceType, NullType, StringType, TupleType
    TYPES               = types.TYPES
    ArrayType           = types.ArrayType
    BooleanType         = types.BooleanType
    BuiltInFunctionType = types.BuiltInFunctionType
    FloatType           = types.FloatType
    IdType              = types.IdType
    IntType             = types.IntType
    NamespaceType       = types.NamespaceType
    NullType            = types.NullType
    StringType          = types.StringType
    TupleType           = types.TupleType

##########################################
# DEFAULT VARIABLES                      #
##########################################

import xdgappdirs as _xdgappdirs
from pathlib import Path as _Path

def defaultvariables(symbols):
    perisymbols = SymbolTable(symbols)
    perisymbols.assign('path', ArrayType([
        StringType(__file__),
        StringType(str(_xdgappdirs.user_data_dir('Peridot', 'TotobirdCreations', as_path=True) / 'modules' / version)),
        StringType(str(_xdgappdirs.site_data_dir('Peridot', 'TotobirdCreations', as_path=True) / 'modules' / version))
    ]))
    symbols.assign('__peridot__', NamespaceType(perisymbols))

    symbols.assign('True'  , BooleanType(True))
    symbols.assign('False' , BooleanType(False))
    symbols.assign('Null'  , NullType())

    symbols.assign('throw' , BuiltInFunctionType('throw'))
    symbols.assign('assert', BuiltInFunctionType('assert'))
    symbols.assign('panic' , BuiltInFunctionType('panic'))
    symbols.assign('print' , BuiltInFunctionType('print'))
    symbols.assign('range' , BuiltInFunctionType('range'))

    symbols.assign('type'  , BuiltInFunctionType('type', type_=TYPES['type'], returntype=BuiltInFunctionType))
    symbols.assign('id'    , BuiltInFunctionType('id', type_=TYPES['type'], returntype=IdType))
    symbols.assign('str'   , BuiltInFunctionType('str', type_=TYPES['type'], returntype=StringType))
    symbols.assign('int'   , BuiltInFunctionType('int', type_=TYPES['type'], returntype=IntType))
    symbols.assign('float' , BuiltInFunctionType('float', type_=TYPES['type'], returntype=FloatType))
    symbols.assign('bool'  , BuiltInFunctionType('bool', type_=TYPES['type'], returntype=BooleanType))
    symbols.assign('array' , BuiltInFunctionType('array', type_=TYPES['type'], returntype=ArrayType))
    symbols.assign('tuple' , BuiltInFunctionType('tuple', type_=TYPES['type'], returntype=TupleType))

    return(symbols)