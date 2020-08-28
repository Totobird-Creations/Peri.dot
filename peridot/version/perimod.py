##########################################
# DEPENDENCIES                           #
##########################################

import sys as _sys

def _perimodinit(catch, types, interpreter, exceptions):
    global InternalPeridotError
    InternalPeridotError = catch.InternalPeridotError
    global _Types, Type, NullType, IntType, FloatType, StringType, BooleanType, ArrayType, DictionaryType, TupleType, FunctionType, BuiltInFunctionType, ExceptionType, IdType, NamespaceType
    _Types               = types
    Type                 = types.TypeObj
    NullType             = types.NullType
    IntType              = types.IntType
    FloatType            = types.FloatType
    StringType           = types.StringType
    BooleanType          = types.BooleanType
    ArrayType            = types.ArrayType
    DictionaryType       = types.DictionaryType
    TupleType            = types.TupleType
    FunctionType         = types.FunctionType
    BuiltInFunctionType  = types.BuiltInFunctionType
    ExceptionType        = types.ExceptionType
    IdType               = types.IdType
    Namespacetype        = types.NamespaceType
    global _RTResult
    _RTResult            = interpreter.RTResult
    global Exc
    class Exceptions():
        ArgumentError    = exceptions.Exc_ArgumentError
        AttributeError   = exceptions.Exc_AttributeError
        AssertionError   = exceptions.Exc_AssertionError
        BreakError       = exceptions.Exc_BreakError
        ContinueError    = exceptions.Exc_ContinueError
        FileAccessError  = exceptions.Exc_FileAccessError
        IdentifierError  = exceptions.Exc_IdentifierError
        IncludeError     = exceptions.Exc_IncludeError
        IndexError       = exceptions.Exc_IndexError
        IterationError   = exceptions.Exc_IterationError
        KeyError         = exceptions.Exc_KeyError
        OperationError   = exceptions.Exc_OperationError
        PanicError       = exceptions.Exc_PanicError
        PatternError     = exceptions.Exc_PatternError
        ReservedError    = exceptions.Exc_ReservedError
        ReturnError      = exceptions.Exc_ReturnError
        ThrownError      = exceptions.Exc_ThrowError
        TypeError        = exceptions.Exc_TypeError
        ValueError       = exceptions.Exc_ValueError
    Exc = Exceptions()

##########################################
# PERIMOD                                #
##########################################

_namespace = None
_error = None
_context = None
_symbols = None
_position = None
_file = None
_builtinfuncs = {}

def module(func):
    global _namespace, _error
    try:
        func(_context, _position)
        _namespace = _Types.NamespaceType(_context.symbols)
    except:
        exc_type, exc_obj, exc_tb = _sys.exc_info()

        while exc_tb.tb_next != None:
            exc_tb = exc_tb.tb_next

        filename = _file
        lineno   = exc_tb  .tb_lineno
        exctype  = exc_type.__name__.replace('Error', 'Exception')
        message  = str(exc_obj)

        _error = (filename, lineno, exctype, message)
        _namespace = None

def assign(name, obj):
    if callable(obj):
        key = f'{_file}.{obj.__name__}'
        _builtinfuncs[key] = obj
        obj = _Types.BuiltInFunctionType(key, type_=_Types.TYPES['function'])
        obj.setpos(_position.start, _position.end).setcontext(_context)
    else:
        obj = _Types.toperidot(
            obj,
            _position.start, _position.end,
            _context
        )
    _symbols.assign(name, obj)

def typeattr(func):
    key = f'{_file}.{func.__name__}'
    _builtinfuncs[key] = func


def success(value):
    return(
        _RTResult().success(value)
    )

def failure(value):
    return(
        _RTResult().failure(value)
    )
