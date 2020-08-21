##########################################
# DEPENDENCIES                           #
##########################################

from __future__ import annotations
from sys import exec_prefix
from types import BuiltinFunctionType
from typing import Any,Optional,Tuple, Type
from uuid import uuid4
from colorama import init, Fore, Style
init()

from .catch      import InternalPeridotError
from .context    import Context, SymbolTable
from .exceptions import Exc_ArgumentError, Exc_ArgumentTypeError, Exc_AssertionError, Exc_FileAccessError, Exc_IndexError, Exc_OperationError, Exc_PanicError, Exc_ReturnError, Exc_ThrowError, Exc_TypeError, Exc_OperationError, Exc_ValueError # type: ignore
from .nodes      import VarCallNode

def uuid():
    u = '00000000000000000000000000000000'
    while u == '00000000000000000000000000000000':
        u = str(uuid4()).replace('-', '')

    return(u)

def typesinit(interpreter):
    global Interpreter
    Interpreter = interpreter

##########################################
# CONSTANTS                              #
##########################################

TYPES = {
    'invalid'      : 'Invalid',
    'nonetype'     : 'Null',
    'integer'      : 'Int',
    'floatingpoint': 'Float',
    'string'       : 'Str',
    'list'         : 'Array',
    'tuple'        : 'Tuple',
    'boolean'      : 'Bool',
    'function'     : 'Function',
    'builtinfunc'  : 'Built-In Function',
    'exception'    : 'Exception',
    'id'           : 'Id'
}

##########################################
# RUNTIME RESULT                         #
##########################################

class RTResult():
    def __init__(self):
        self.reset()

    def reset(self):
        self.value = None
        self.funcvalue = None
        self.error = None

    def register(self, res):
        self.error = res.shouldreturn()
        self.funcvalue = res.funcvalue

        return(res.value)

    def success(self, value):
        self.reset()
        self.value = value

        return(self)

    def successreturn(self, value):
        self.reset()
        self.funcvalue = value

        return(self)

    def failure(self, error):
        self.error = error

        return(self)

    def shouldreturn(self):
        return(
            self.error or self.funcvalue
        )

##########################################
# TYPES                                  #
##########################################

class TypeObj():
    def __init__(self, value=None, type_=TYPES['invalid']):
        self.value = value
        self.type  = type_
        self.id = uuid()

        self.originstart = []
        self.originend = []
        self.origindisplay = []

        self.setpos()
        self.setcontext()

    def setpos(self, start=None, end=None, originstart=None, originend=None, origindisplay=None):
        if originstart:
            if not originend:
                raise InternalPeridotError('OriginEnd not passed.')
            elif not origindisplay:
                raise InternalPeridotError('OriginDisplay not passed.')
            self.originstart.append(originstart)
            self.originend.append(originend)
            self.origindisplay.append(origindisplay)

        self.start         = start
        self.end           = end

        return(self)

    def setorigin(self, originstart=None, originend=None, origindisplay=None):
        if originstart:
            if not originend:
                raise InternalPeridotError('OriginEnd not passed.')
            elif not origindisplay:
                raise InternalPeridotError('OriginDisplay not passed.')
            self.originstart   = originstart
            self.originend     = originend
            self.origindisplay = origindisplay

        return(self)

    def setcontext(self, context=None):
        self.context = context

        return(self)


    def add(self, other: Any) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be added to', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def subtract(self, other: Any) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be subtracted from', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def multiply(self, other: Any) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be multiplied', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def divide(self, other: Any) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be divided', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def raised(self, other: Any) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be raised', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def eqequals(self: Any, other: Any) -> Tuple[BooleanType, None]:
        if type(self) == type(other):
            return((
                BooleanType(
                    self.value == other.value
                )
                    .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)
                    .setcontext(self.context),
                None
            ))
        else:
            return((
                BooleanType(
                    False
                )
                    .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)
                    .setcontext(self.context),
                None
            ))
    def bangequals(self, other: Any) -> Tuple[BooleanType, None]:
        if type(self) != type(other):
            return((
                BooleanType(
                    True
                )
                    .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)
                    .setcontext(self.context),
                None
            ))
        else:
            return((
                BooleanType(
                    self.value != other.value
                )
                    .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)
                    .setcontext(self.context),
                None
            ))
    def lessthan(self, other: Any) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be compared with \'<\'', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def ltequals(self, other: Any) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be compared with \'<=\'', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def greaterthan(self, other: Any) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be compared with \'>\'', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def gtequals(self, other: Any) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be compared with \'>=\'', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def and_(self, other: Any) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be combined with \'and\'', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def or_(self, other: Any) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be combined with \'or\'', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def not_(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be inverted', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def call(self, name, args) -> Tuple[Any, Optional[Exc_TypeError]]:
        res = RTResult()
        try:
            self.originstart = self.originstart[0]
            self.originend = self.originend[0]
            self.origindisplay = self.origindisplay[0]
        except IndexError: pass
        return(
            res.failure(
                Exc_TypeError(
                    f'{self.type} can not be called',
                    self.start, self.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            )
        )
    def istrue(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be interpreted as {TYPES["boolean"]}', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def tostr(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be converted to {TYPES["string"]}', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def toint(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be converted to {TYPES["integer"]}', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def tofloat(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be converted to {TYPES["floatingpoint"]}', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def tobool(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be converted to {TYPES["boolean"]}', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def toarray(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be converted to {TYPES["list"]}', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def totuple(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be converted to {TYPES["tuple"]}', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))

    def indicie(self, indicie) -> Tuple[Any, Optional[Exc_TypeError]]:
        self.originstart += indicie.originstart
        self.originend += indicie.originend
        self.origindisplay += indicie.origindisplay
        return((None, Exc_TypeError(f'{self.type} can not be indexed', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))

    def __clean__(self):
        return(self.__repr__())

    def __repr__(self):
        return(f'{self.value}')



class NullType(TypeObj):
    def __init__(self):
        super().__init__(type_=TYPES['nonetype'])

    def tostr(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((
            StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay),
            None
        ))

    def tobool(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((
            BooleanType(False)
                .setcontext(self.context)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay),
            None
        ))

    def copy(self):
        copy = NullType()
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)
        copy.id = self.id

        return(copy)

    def __repr__(self):
        return(f'Null')



class IntType(TypeObj):
    def __init__(self, value):
        if isinstance(value, bool) or not isinstance(value, int):
            raise InternalPeridotError(f'Non int value receievd ({type(value).__name__})')
        super().__init__(value, type_=TYPES['integer'])


    def add(self, other: Any) -> Tuple[Optional[IntType], Optional[Exc_TypeError]]:
        if isinstance(other, IntType):
            return((
                IntType(self.value + other.value)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            self.originstart += other.originstart
            self.originend += other.originend
            self.origindisplay += other.origindisplay
            return((
                None,
                Exc_TypeError(
                    f'{other.type} can not be added to {self.type}',
                    self.start, other.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

    def subtract(self, other: Any) -> Tuple[Optional[IntType], Optional[Exc_TypeError]]:
        if isinstance(other, IntType):
            return((
                IntType(self.value - other.value)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            self.originstart += other.originstart
            self.originend += other.originend
            self.origindisplay += other.origindisplay
            return((
                None,
                Exc_TypeError(
                    f'{other.type} can not be subtracted from {self.type}',
                    self.start, other.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

    def multiply(self, other: Any) -> Tuple[Optional[IntType], Optional[Exc_TypeError]]:
        if isinstance(other, IntType):
            return((
                IntType(self.value * other.value)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            self.originstart += other.originstart
            self.originend += other.originend
            self.origindisplay += other.origindisplay
            return((
                None,
                Exc_TypeError(
                    f'{self.type} can not be multiplied by {other.type}',
                    self.start, other.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

    def divide(self, other: Any) -> Tuple[Optional[IntType], Any]:
        if isinstance(other, IntType):
            if other.value == 0:
                return((
                    None,
                    Exc_OperationError(
                        f'Division by zero',
                        other.start, other.end,
                        self.context,
                        other.originstart, other.originend, other.origindisplay
                    )
                ))

            return((
                IntType(int(self.value / other.value))
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            self.originstart += other.originstart
            self.originend += other.originend
            self.origindisplay += other.origindisplay
            return((
                None,
                Exc_TypeError(
                    f'{self.type} can not be divided by {other.type}',
                    self.start, other.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

    def raised(self, other: Any) -> Tuple[Optional[IntType], Optional[Exc_TypeError]]:
        if isinstance(other, IntType):
            return((
                IntType(
                    pow(
                        self.value,
                        other.value
                    )
                )
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            self.originstart += other.originstart
            self.originend += other.originend
            self.origindisplay += other.origindisplay
            return((
                None,
                Exc_TypeError(
                    f'{self.type} can not be raised to {other.type}',
                    self.start, other.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

    def lessthan(self, other: Any) -> Tuple[Optional[BooleanType], Optional[Exc_TypeError]]:
        if type(self) == type(other):
            return((
                BooleanType(
                    self.value < other.value
                )
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            self.originstart += other.originstart
            self.originend += other.originend
            self.origindisplay += other.origindisplay
            return((
                None,
                Exc_TypeError(
                    f'{self.type} can not be compared with {other.type}',
                    self.start, other.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

    def ltequals(self, other: Any) -> Tuple[Optional[BooleanType], Optional[Exc_TypeError]]:
        if type(self) == type(other):
            return((
                BooleanType(
                    self.value <= other.value
                )
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            self.originstart += other.originstart
            self.originend += other.originend
            self.origindisplay += other.origindisplay
            return((
                None,
                Exc_TypeError(
                    f'{self.type} can not be compared with {other.type}',
                    self.start, other.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

    def greaterthan(self, other: Any) -> Tuple[Optional[BooleanType], Optional[Exc_TypeError]]:
        if type(self) == type(other):
            return((
                BooleanType(
                    self.value > other.value
                )
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            self.originstart += other.originstart
            self.originend += other.originend
            self.origindisplay += other.origindisplay
            return((
                None,
                Exc_TypeError(
                    f'{self.type} can not be compared with {other.type}',
                    self.start, other.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

    def gtequals(self, other: Any) -> Tuple[Optional[BooleanType], Optional[Exc_TypeError]]:
        if type(self) == type(other):
            return((
                BooleanType(
                    self.value >= other.value
                )
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            self.originstart += other.originstart
            self.originend += other.originend
            self.origindisplay += other.origindisplay
            return((
                None,
                Exc_TypeError(
                    f'{self.type} can not be compared with {other.type}',
                    self.start, other.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

    def tostr(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((
            StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def toint(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((
            IntType(self.value)
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def tofloat(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((
            FloatType(float(self.value))
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def copy(self):
        copy = IntType(self.value)
        copy.setcontext(self.context)
        copy.setpos(
            self.start, self.end,
            self.originstart, self.originend, self.origindisplay
        )
        copy.id = self.id

        return(copy)


class FloatType(TypeObj):
    def __init__(self, value):
        if not isinstance(value, float):
            raise InternalPeridotError(f'Non float value receievd ({type(value).__name__})')
        super().__init__(value, type_=TYPES['floatingpoint'])


    def add(self, other: Any) -> Tuple[Optional[FloatType], Optional[Exc_TypeError]]:
        if isinstance(other, FloatType):
            return((
                FloatType(self.value + other.value)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            self.originstart += other.originstart
            self.originend += other.originend
            self.origindisplay += other.origindisplay
            return((
                None,
                Exc_TypeError(
                    f'{other.type} can not be added to {self.type}',
                    self.start, other.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

    def subtract(self, other: Any) -> Tuple[Optional[FloatType], Optional[Exc_TypeError]]:
        if isinstance(other, FloatType):
            return((
                FloatType(self.value - other.value)
                    .setpos(self.start, self.en)
                    .setcontext(self.context),
                None
            ))
        else:
            self.originstart += other.originstart
            self.originend += other.originend
            self.origindisplay += other.origindisplay
            return((
                None,
                Exc_TypeError(
                    f'{other.type} can not be subtracted from {self.type}',
                    self.start, other.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

    def multiply(self, other: Any) -> Tuple[Optional[FloatType], Optional[Exc_TypeError]]:
        if isinstance(other, FloatType):
            return((
                FloatType(self.value * other.value)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            self.originstart += other.originstart
            self.originend += other.originend
            self.origindisplay += other.origindisplay
            return((
                None,
                Exc_TypeError(
                    f'{self.type} can not be multiplied by {other.type}',
                    self.start, other.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

    def divide(self, other: Any) -> Tuple[Optional[FloatType], Any]:
        if isinstance(other, FloatType):
            if other.value == 0:
                return((
                    None,
                    Exc_OperationError(
                        f'Division by zero',
                        self.start, other.end,
                        self.context,
                        other.originstart, other.originend, other.origindisplay
                    )
                ))

            return((
                FloatType(self.value / other.value)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            self.originstart += other.originstart
            self.originend += other.originend
            self.origindisplay += other.origindisplay
            return((
                None,
                Exc_TypeError(
                    f'{self.type} can not be divided by {other.type}',
                    self.start, other.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

    def raised(self, other: Any) -> Tuple[Optional[FloatType], Optional[Exc_TypeError]]:
        if isinstance(other, FloatType):
            return((
                FloatType(
                    pow(
                        self.value,
                        other.value
                    )
                )
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            self.originstart += other.originstart
            self.originend += other.originend
            self.origindisplay += other.origindisplay
            return((
                None,
                Exc_TypeError(
                    f'{self.type} can not be raised to {other.type}',
                    self.start, other.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

    def lessthan(self, other: Any) -> Tuple[Optional[BooleanType], Optional[Exc_TypeError]]:
        if type(self) == type(other):
            return((
                BooleanType(
                    self.value < other.value
                )
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            self.originstart += other.originstart
            self.originend += other.originend
            self.origindisplay += other.origindisplay
            return((
                None,
                Exc_TypeError(
                    f'{self.type} can not be compared with {other.type}',
                    self.start, other.end, 
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

    def ltequals(self, other: Any) -> Tuple[Optional[BooleanType], Optional[Exc_TypeError]]:
        if type(self) == type(other):
            return((
                BooleanType(
                    self.value <= other.value
                )
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            self.originstart += other.originstart
            self.originend += other.originend
            self.origindisplay += other.origindisplay
            return((
                None,
                Exc_TypeError(
                    f'{self.type} can not be compared with {other.type}',
                    self.start, other.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

    def greaterthan(self, other: Any) -> Tuple[Optional[BooleanType], Optional[Exc_TypeError]]:
        if type(self) == type(other):
            return((
                BooleanType(
                    self.value > other.value
                )
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            self.originstart += other.originstart
            self.originend += other.originend
            self.origindisplay += other.origindisplay
            return((
                None,
                Exc_TypeError(
                    f'{self.type} can not be compared with {other.type}',
                    self.start, other.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

    def gtequals(self, other: Any) -> Tuple[Optional[BooleanType], Optional[Exc_TypeError]]:
        if type(self) == type(other):
            return((
                BooleanType(
                    self.value >= other.value
                )
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            self.originstart += other.originstart
            self.originend += other.originend
            self.origindisplay += other.origindisplay
            return((
                None, 
                Exc_TypeError(
                    f'{self.type} can not be compared with {other.type}',
                    self.start, other.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

    def tostr(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((
            StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def toint(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        if int(self.value) != self.value:
            return((None,
                Exc_ValueError(
                    f'{self.__repr__()} ({self.type}) can not be converted to {TYPES["integer"]}',
                    self.start, self.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))
        return((
            IntType(int(self.value))
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def tofloat(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((
            FloatType(self.value)
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def copy(self):
        copy = FloatType(self.value)
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)
        copy.id = self.id

        return(copy)




class StringType(TypeObj):
    def __init__(self, value):
        if not isinstance(value, str):
            raise InternalPeridotError(f'Non str value receievd ({type(value).__name__})')
        super().__init__(value, type_=TYPES['string'])


    def add(self, other: Any) -> Tuple[Optional[StringType], Optional[Exc_TypeError]]:
        if isinstance(other, StringType):
            return((
                StringType(self.value + other.value)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            self.originstart += other.originstart
            self.originend += other.originend
            self.origindisplay += other.origindisplay
            return((
                None,
                Exc_TypeError(
                    f'{other.type} can not be added to {self.type}',
                    self.start, other.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

    def tostr(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((
            StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def toint(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        try:
            value = int(self.value)
        except:
            return((
                None,
                Exc_ValueError(
                    f'{self.__repr__()} ({self.type}) can not be converted to {TYPES["integer"]}',
                    self.start, self.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))
        return((
            IntType(value)
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def tofloat(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        try:
            value = float(self.value)
        except:
            return((None,
                    Exc_ValueError(
                        f'{self.__repr__()} ({self.type}) can not be converted to {TYPES["floatingpoint"]}',
                        self.start, self.end,
                        self.context,
                        self.originstart, self.originend, self.origindisplay
                    )
                ))
        return((
            FloatType(value)
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def indicie(self, indicie):
        if not isinstance(indicie, IntType):
            return((
                None,
                Exc_TypeError(
                    f'{self.type} index must be of type {TYPES["integer"]}',
                    self.start, self.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))
        
        try:
            value = self.value[indicie.value]

        except IndexError:
            return((
                None,
                Exc_IndexError(
                    f'{self.type} index out of range',
                    self.start, self.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

        value = StringType(value).setpos(self.start, self.end).setcontext(self.context)

        return((
            value,
            None
        ))

    def copy(self):
        copy = StringType(self.value)
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)
        copy.id = self.id

        return(copy)

    def __clean__(self):
        return(f'{self.value}')

    def __repr__(self):
        return(f'\'{self.value}\'')




class BooleanType(TypeObj):
    def __init__(self, value):
        if not isinstance(value, bool):
            raise InternalPeridotError(f'Non bool value receievd ({type(value).__name__})')
        super().__init__(value, type_=TYPES['boolean'])

    def and_(self, other: Any) -> Tuple[Optional[BooleanType], Optional[Exc_TypeError]]:
        if type(self) == type(other):
            return((
                BooleanType(
                    self.value and other.value
                )
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            self.originstart += other.originstart
            self.originend += other.originend
            self.origindisplay += other.origindisplay
            return((
                None, 
                Exc_TypeError(
                    f'{self.type} can not be combined with {other.type}',
                    self.start, other.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

    def or_(self, other: Any) -> Tuple[Optional[BooleanType], Optional[Exc_TypeError]]:
        if type(self) == type(other):
            return((
                BooleanType(
                    self.value or other.value
                )
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            self.originstart += other.originstart
            self.originend += other.originend
            self.origindisplay += other.origindisplay
            return((
                None, 
                Exc_TypeError(
                    f'{self.type} can not be combined with {other.type}',
                    self.start, other.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

    def not_(self) -> Tuple[BooleanType, None]:
        return((
            BooleanType(
                not self.value
            )
                .setpos(self.start, self.end)
                .setcontext(self.context),
            None
        ))

    def istrue(self) -> Tuple[BooleanType, None]:
        return((
            self.value,
            None
        ))

    def tostr(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((
            StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def toint(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((
            IntType(int(self.value))
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def tofloat(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((
            FloatType(float(self.value))
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def copy(self):
        copy = BooleanType(self.value)
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)
        copy.id = self.id

        return(copy)


class ArrayType(TypeObj):
    def __init__(self, elements):
        if not isinstance(elements, list):
            raise InternalPeridotError(f'Non list value received')
        if len(elements):
            self.elmtype = type(elements[0])
            if not all(type(x) == self.elmtype for x in elements):
                raise InternalPeridotError(f'Array element recieved non {self.elmtype.__name__} value')

        super().__init__(elements, type_=TYPES['list'])

    def tostr(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((
            StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def indicie(self, indicie):
        if not isinstance(indicie, IntType):
            return((
                None,
                Exc_TypeError(
                    f'{self.type} index must be of type {TYPES["integer"]}',
                    self.start, self.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))
        
        try:
            value = self.value[indicie.value]

        except IndexError:
            return((
                None,
                Exc_IndexError(
                    f'{self.type} index out of range',
                    self.start, self.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

        value = value.setpos(self.start, self.end).setcontext(self.context)

        return((
            value,
            None
        ))

    def copy(self):
        copy = ArrayType(self.value.copy())
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)
        copy.id = self.id

        return(copy)

    def __repr__(self):
        return(f'[{", ".join([str(i) for i in self.value])}]')


class TupleType(TypeObj):
    def __init__(self, elements):
        if not isinstance(elements, tuple):
            raise InternalPeridotError(f'Non tuple value received')

        super().__init__(elements, type_=TYPES['tuple'])

    def tostr(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((
            StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def indicie(self, indicie):
        if not isinstance(indicie, IntType):
            return((
                None,
                Exc_TypeError(
                    f'{self.type} index must be of type {TYPES["integer"]}',
                    self.start, self.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))
        
        try:
            value = self.value[indicie.value]

        except IndexError:
            return((
                None,
                Exc_IndexError(
                    f'{self.type} index out of range',
                    self.start, self.end,
                    self.context,
                    self.originstart, self.originend, self.origindisplay
                )
            ))

        value = value.setpos(self.start, self.end).setcontext(self.context)

        return((
            value,
            None
        ))

    def copy(self):
        copy = TupleType(self.value)
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)
        copy.id = self.id

        return(copy)

    def __repr__(self):
        return(f'({", ".join([str(i) for i in self.value])})')



class BaseFunction(TypeObj):
    def __init__(self, name=None, type_=TYPES['builtinfunc']):
        if not isinstance(name, str) and name:
            raise InternalPeridotError(f'Non str value receievd ({type(name).__name__})')

        super().__init__(type_=type_)
        self.name = name or '<Anonymous>'

    def gencontext(self, display):
        self.display = display
        context = Context(
            display,
            SymbolTable(self.context.symbols),
            self.context,
            [self.start, self.end, self.originstart, self.originend, self.origindisplay]
        )
        context.caughterrors = self.context.caughterrors

        return(context)

    def checkargs(self, argnames, args):
        res = RTResult()

        if len(args) != len(argnames):
            return(
                res.failure(
                    Exc_ArgumentError(
                        f'\'{self.name}\' takes {len(argnames)} arguments, {len(args)} given',
                        self.start, self.end,
                        self.context,
                        self.originstart[0], self.originend[0], self.origindisplay[0]
                    )
                )
            )

        return(
            res.success(
                None
            )
        )

    def popargs(self, argnames, args, exec_context):
        for i in range(len(args)):
            argname = argnames[i]
            argvalue = args[i]

            argvalue.setcontext(exec_context)
            exec_context.symbols.assign(argname, argvalue)

    def checkpopargs(self, argnames, args, exec_context):
        res = RTResult()

        res.register(
            self.checkargs(
                argnames,
                args
            )
        )

        if res.shouldreturn():
            return(res)

        self.popargs(argnames, args, exec_context)

        return(
            res.success(None)
        )

    def tostr(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((
            StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay),
            None
        ))


class FunctionType(BaseFunction):
    def __init__(self, bodynodes, argnames, shouldreturn):
        super().__init__(type_=TYPES['function'])
        self.bodynodes = bodynodes
        self.argnames = argnames
        self.shouldreturn = shouldreturn

    def call(self, name, args):
        res = RTResult()
        interpreter = Interpreter()

        exec_context = self.gencontext((name, self.id))
        res.register(
            self.checkpopargs(
                self.argnames, args,
                exec_context
            )
        )

        if res.shouldreturn():
            return(res)

        for i in self.bodynodes:
            result = res.register(
                interpreter.visit(
                    i,
                    exec_context
                )
            )

            if res.funcvalue:
                break

            if res.error:
                return(res)

        result = res.funcvalue

        if result:
            return(
                res.success(result)
            )
        else:
            return(
                res.failure(
                    Exc_ReturnError(
                        f'\'{self.name}\' did not return a value',
                        self.start, self.end,
                        self.context
                    )
                )
            )

    def copy(self):
        copy = FunctionType(self.bodynodes, self.argnames, self.shouldreturn)
        copy.id = self.id
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)

        return(copy)

    def tostr(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((
            StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay),
            None
        ))

    def __repr__(self):
        return(f'<{TYPES["function"]} {self.name} <{self.id}>>')


class BuiltInFunctionType(BaseFunction):
    def __init__(self, name, value=None):
        super().__init__(name, type_=TYPES['builtinfunc'])
        if value:
            self.value = value
        else:
            self.value = name

    def call(self, name, args):
        res = RTResult()

        #exec_context = self.gencontext(('Built-In Function', name))
        exec_context = self.context

        method = f'exec_{self.value}'
        method = getattr(self, method)

        res.register(
            self.checkpopargs(
                method.argnames, args,
                exec_context
            )
        )

        if res.shouldreturn():
            return(res)

        result = res.register(
            method(exec_context)
        )

        if res.shouldreturn():
            return(res)

        return(
            res.success(result)
        )

    def tostr(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((
            StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay),
            None
        ))

    def copy(self):
        copy = BuiltInFunctionType(self.name, self.value)
        copy.id = self.id
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)

        return(copy)

    def __repr__(self):
        return(f'<{TYPES["builtinfunc"]} {self.name}>')


    def exec_throw(self, exec_context):
        res = RTResult()

        exc = exec_context.symbols.access('exception')

        if not isinstance(exc, ExceptionType):
            return(
                res.failure(
                    Exc_TypeError(
                        f'\'exception\' must be of type {TYPES["exception"]}, {exc.type} given',
                        exc.start, exc.end,
                        exec_context,
                        exc.originstart, exc.originend, exc.origindisplay
                    )
                )
            )
        
        return(
            res.failure(
                Exc_ThrowError(
                    exc.exc,
                    exc.msg,
                    self.start, self.end,
                    exec_context,
                    exc.originstart, exc.originend, exc.origindisplay
                )
            )
        )
    exec_throw.argnames = ['exception']


    def exec_assert(self, exec_context):
        res = RTResult()

        condition = exec_context.symbols.access('condition')
        message   = exec_context.symbols.access('message')

        if not isinstance(condition, BooleanType):
            return(
                res.failure(
                    Exc_ArgumentTypeError(
                        f'\'condition\' must be of type {TYPES["boolean"]}, {condition.type} given',
                        condition.start, condition.end,
                        exec_context,
                        condition.originstart, condition.originend, condition.origindisplay
                    )
                )
            )

        if not isinstance(message, StringType):
            return(
                res.failure(
                    Exc_ArgumentTypeError(
                        f'\'message\' must be of type {TYPES["string"]}, {message.type} given',
                        message.start, message.end,
                        exec_context,
                        message.originstart, message.originend, message.origindisplay
                    )
                )
            )

        if condition.istrue()[0]:
            return(
                res.success(
                    NullType()
                )
            )
        else:
            try:
                condition.originstart = condition.originstart[0]
                condition.originend = condition.originend[0]
                condition.origindisplay = condition.origindisplay[0]
            except IndexError: pass

            return(
                res.failure(
                    Exc_AssertionError(
                        f'{message.__clean__()}',
                        condition.start, condition.end,
                        exec_context,
                        condition.originstart, condition.originend, condition.origindisplay
                    )
                )
            )
    exec_assert.argnames = ['condition', 'message']


    def exec_panic(self, exec_context):
        res = RTResult()

        message = exec_context.symbols.access('message')

        if not isinstance(message, StringType):
            return(
                res.failure(
                    Exc_ArgumentTypeError(
                        f'\'message\' must be of type {TYPES["string"]}, {message.type} given',
                        message.start, message.end,
                        exec_context,
                        message.originstart, message.originend, message.origindisplay
                    )
                )
            )

        return(
            res.failure(
                Exc_PanicError(
                    f'{message.__clean__()}',
                    self.start, self.end,
                    exec_context,
                    self.originstart[0], self.originend[0], self.origindisplay[0]
                )
            )
        )
    exec_panic.argnames = ['message']


    def exec_print(self, exec_context):
        res = RTResult()

        text = exec_context.symbols.access('text')

        if not isinstance(text, StringType):
            return(
                res.failure(
                    Exc_ArgumentTypeError(
                        f'\'message\' must be of type {TYPES["string"]}, {text.type} given',
                        text.start, text.end,
                        exec_context,
                        text.originstart, text.originend, text.origindisplay
                    )
                )
            )

        print(text.__clean__())

        return(
            RTResult().success(
                NullType()
            )
        )
    exec_print.argnames = ['text']


    def exec_range(self, exec_context):
        res = RTResult()

        start = exec_context.symbols.access('start')
        stop = exec_context.symbols.access('stop')
        step = exec_context.symbols.access('step')

        if not isinstance(start, IntType):
            return(
                res.failure(
                    Exc_ArgumentTypeError(
                        f'\'start\' must be of type {TYPES["int"]}, {start.type} given',
                        start.start, start.end,
                        exec_context,
                        start.originstart, start.originend, start.origindisplay
                    )
                )
            )

        if not isinstance(stop, IntType):
            return(
                res.failure(
                    Exc_ArgumentTypeError(
                        f'\'start\' must be of type {TYPES["int"]}, {stop.type} given',
                        stop.start, stop.end,
                        exec_context,
                        stop.originstart, stop.originend, stop.origindisplay
                    )
                )
            )

        if not isinstance(step, IntType):
            return(
                res.failure(
                    Exc_ArgumentTypeError(
                        f'\'start\' must be of type {TYPES["int"]}, {step.type} given',
                        step.start, step.end,
                        exec_context,
                        step.originstart, step.originend, step.origindisplay
                    )
                )
            )

        returnlist = []

        i = start.value

        while i < stop.value:
            returnlist.append(
                IntType(i)
            )

            i += step.value



        return(
            RTResult().success(
                ArrayType(returnlist)
            )
        )
    exec_range.argnames = ['start', 'stop', 'step']


    def exec_str(self, exec_context):
        res = RTResult()

        value = exec_context.symbols.access('obj')
        result, error = value.tostr()

        if error:
            return(
                RTResult().failure(
                    error
                )
            )

        return(
            RTResult().success(
                result
            )
        )
    exec_str.argnames = ['obj']


    def exec_int(self, exec_context):
        res = RTResult()

        value = exec_context.symbols.access('obj')
        result, error = value.toint()

        if error:
            return(
                RTResult().failure(
                    error
                )
            )

        return(
            RTResult().success(
                result
            )
        )
    exec_int.argnames = ['obj']


    def exec_float(self, exec_context):
        res = RTResult()

        value = exec_context.symbols.access('obj')
        result, error = value.tofloat()

        if error:
            return(
                RTResult().failure(
                    error
                )
            )

        return(
            RTResult().success(
                result
            )
        )
    exec_float.argnames = ['obj']


    def exec_bool(self, exec_context):
        res = RTResult()

        value = exec_context.symbols.access('obj')
        result, error = value.tobool()

        if error:
            return(
                RTResult().failure(
                    error
                )
            )

        return(
            RTResult().success(
                result
            )
        )
    exec_bool.argnames = ['obj']


    def exec_array(self, exec_context):
        res = RTResult()

        value = exec_context.symbols.access('obj')
        result, error = value.toarray()

        if error:
            return(
                RTResult().failure(
                    error
                )
            )

        return(
            RTResult().success(
                result
            )
        )
    exec_array.argnames = ['obj']


    def exec_tuple(self, exec_context):
        res = RTResult()

        value = exec_context.symbols.access('obj')
        result, error = value.totuple()

        if error:
            return(
                RTResult().failure(
                    error
                )
            )

        return(
            RTResult().success(
                result
            )
        )
    exec_tuple.argnames = ['obj']


    def exec_id(self, exec_context):
        res = RTResult()

        obj = exec_context.symbols.access('obj')
        return(
            RTResult().success(
                IdType(obj.id)
            )
        )
    exec_id.argnames = ['obj']


class ExceptionType(TypeObj):
    def __init__(self, exc, msg, start):
        super().__init__(type_=TYPES['exception'])
        self.exc = exc
        self.msg = msg
        self.exc_start = start
        self.line = start.line
        self.column = start.column

    def copy(self):
        copy = ExceptionType(self.exc, self.msg, self.exc_start)
        copy.id = self.id
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)

        return(copy)

    def tostr(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((
            StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def totuple(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((
            TupleType((
                StringType(self.exc)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                StringType(self.msg)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                IntType(self.line)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                IntType(self.column)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
            ))
        ), None)

    def __repr__(self):
        return(f'<{self.exc}:{self.msg}, {self.line + 1}:{self.column + 1}>')


class IdType(TypeObj):
    def __init__(self, value):
        super().__init__(value, type_=TYPES['id'])

    def tostr(self):
        return((
            StringType(self.value)
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def toint(self):
        return((
            IntType(int(self.value, 16))
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def copy(self):
        copy = IdType(self.value)
        copy.id = self.id
        copy.setcontext(self.context)
        self.setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)

        return(copy)

    def __repr__(self):
        return(f'<Id {self.value}>')
