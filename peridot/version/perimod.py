##########################################
# DEPENDENCIES                           #
##########################################

import sys as _sys

def _perimodinit(types, interpreter):
    global _Types
    _Types = types
    global _RTResult
    _RTResult     = interpreter.RTResult

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
    except PermissionError:
        exc_type, exc_obj, exc_tb = _sys.exc_info()

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
    obj = _Types.toperidot(
        obj,
        _position.start, _position.end,
        _context
    )
    _symbols.assign(name, obj)

def success(value):
    return(
        _RTResult().success(value)
    )

def failure(value):
    return(
        _RTResult().failure(value)
    )
