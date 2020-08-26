import sys as _sys

from .types import TYPES as TypeNames
from .types import NamespaceType, TypeObj as Type
from .types import RTResult as _RTResult
from .catch import InternalPeridotError

class Exceptions():
    from .exceptions import Exc_Error, Exc_ArgumentError, Exc_AssertionError, Exc_AttributeError, Exc_BreakError, Exc_ContinueError, Exc_FileAccessError, Exc_IdentifierError, Exc_IncludeError, Exc_IndexError, Exc_IterationError, Exc_KeyError, Exc_OperationError, Exc_PanicError, Exc_PatternError, Exc_ReturnError, Exc_ThrowError, Exc_TypeError, Exc_ValueError

class Types():
    from .types import NullType, IntType, FloatType, StringType, BooleanType, ArrayType, DictionaryType, TupleType, FunctionType, BuiltInFunctionType, ExceptionType, IdType, NamespaceType

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
