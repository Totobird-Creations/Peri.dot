##########################################
# DEPENDENCIES                           #
##########################################

import sys as _sys

def _perimodinit(types, interpreter):
    global NamespaceType
    NamespaceType = types.NamespaceType
    global _RTResult
    _RTResult     = interpreter.RTResult

##########################################
# PERIMOD                           #
##########################################

_namespace = None
_error = None
Context = None
Symbols = None
Position = None
File = None
BuiltInFuncs = {}

def module(func):
    global _namespace, _error
    try:
        func()
        _namespace = NamespaceType(Context.symbols)
    except:
        exc_type, exc_obj, exc_tb = _sys.exc_info()

        filename = File
        lineno   = exc_tb  .tb_lineno
        exctype  = exc_type.__name__.replace('Error', 'Exception')
        message  = str(exc_obj)

        _error = (filename, lineno, exctype, message)
        _namespace = None

def success(value):
    return(
        _RTResult().success(value)
    )

def failure(value):
    return(
        _RTResult().failure(value)
    )
