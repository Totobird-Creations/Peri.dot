##########################################
# DEPENDENCIES                           #
##########################################

from __future__ import annotations
from sys import exec_prefix
from types import BuiltinFunctionType
from typing import Any,Optional,Tuple, Type
from uuid import uuid4

from .catch      import PeridotPanic
from .context    import Context, SymbolTable
from .exceptions import Exc_ArgumentError, Exc_ArgumentTypeError, Exc_AssertionError, Exc_FileAccessError, Exc_OperationError, Exc_TypeError, Exc_OperationError, Exc_ValueError # type: ignore
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

        self.setpos()
        self.setcontext()

    def setpos(self, start=None, end=None):
        self.start = start
        self.end   = end

        return(self)

    def setcontext(self, context=None):
        self.context = context

        return(self)


    def add(self, other: Any) -> Tuple[Any, Optional[Exc_OperationError]]:
        return((None, Exc_OperationError(f'{self.type} can not be added to', self.start, self.end, self.context)))
    def subtract(self, other: Any) -> Tuple[Any, Optional[Exc_OperationError]]:
        return((None, Exc_OperationError(f'{self.type} can not be subtracted from', self.start, self.end, self.context)))
    def multiply(self, other: Any) -> Tuple[Any, Optional[Exc_OperationError]]:
        return((None, Exc_OperationError(f'{self.type} can not be multiplied', self.start, self.end, self.context)))
    def divide(self, other: Any) -> Tuple[Any, Optional[Exc_OperationError]]:
        return((None, Exc_OperationError(f'{self.type} can not be divided', self.start, self.end, self.context)))
    def raised(self, other: Any) -> Tuple[Any, Optional[Exc_OperationError]]:
        return((None, Exc_OperationError(f'{self.type} can not be raised', self.start, self.end, self.context)))
    def eqequals(self: Any, other: Any) -> Tuple[BooleanType, None]:
        if type(self) == type(other):
            return((
                BooleanType(
                    self.value == other.value
                )
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            return((
                BooleanType(
                    False
                )
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
    def bangequals(self, other: Any) -> Tuple[BooleanType, None]:
        if type(self) != type(other):
            return((
                BooleanType(
                    True
                )
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            return((
                BooleanType(
                    self.value != other.value
                )
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
    def lessthan(self, other: Any) -> Tuple[Any, Optional[Exc_OperationError]]:
        return((None, Exc_OperationError(f'{self.type} can not be compared with \'<\'', self.start, self.end, self.context)))
    def ltequals(self, other: Any) -> Tuple[Any, Optional[Exc_OperationError]]:
        return((None, Exc_OperationError(f'{self.type} can not be compared with \'<=\'', self.start, self.end, self.context)))
    def greaterthan(self, other: Any) -> Tuple[Any, Optional[Exc_OperationError]]:
        return((None, Exc_OperationError(f'{self.type} can not be compared with \'>\'', self.start, self.end, self.context)))
    def gtequals(self, other: Any) -> Tuple[Any, Optional[Exc_OperationError]]:
        return((None, Exc_OperationError(f'{self.type} can not be compared with \'>=\'', self.start, self.end, self.context)))
    def and_(self, other: Any) -> Tuple[Any, Optional[Exc_OperationError]]:
        return((None, Exc_OperationError(f'{self.type} can not be combined with \'and\'', self.start, self.end, self.context)))
    def or_(self, other: Any) -> Tuple[Any, Optional[Exc_OperationError]]:
        return((None, Exc_OperationError(f'{self.type} can not be combined with \'or\'', self.start, self.end, self.context)))
    def not_(self) -> Tuple[Any, Optional[Exc_OperationError]]:
        return((None, Exc_OperationError(f'{self.type} can not be inverted', self.start, self.end, self.context)))
    def call(self, name, args) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be called', self.start, self.end, self.context)))
    def istrue(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be interpreted as {TYPES["boolean"]}', self.start, self.end, self.context)))
    def tostr(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be converted to {TYPES["string"]}', self.start, self.end, self.context)))
    def toint(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be converted to {TYPES["integer"]}', self.start, self.end, self.context)))
    def tofloat(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be converted to {TYPES["floatingpoint"]}', self.start, self.end, self.context)))

    def __clean__(self):
        return(self.__repr__())

    def __repr__(self):
        return(f'{self.value}')



class NullType(TypeObj):
    def __init__(self):
        super().__init__(None, type_=TYPES['nonetype'])

    def copy(self):
        copy = NullType()
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end)

        return(copy)

    def tostr(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((StringType(self.__clean__()).setcontext(self.context).setpos(self.start, self.end), None))

    def __repr__(self) -> str:
        return(f'Null')



class IntType(TypeObj):
    def __init__(self, value):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f'Internal Error: Non integer value receievd ({type(value).__name__})')
        super().__init__(value, type_=TYPES['integer'])


    def add(self, other: IntType) -> Tuple[Optional[IntType], Optional[Exc_OperationError]]:
        if isinstance(other, IntType):
            return((
                IntType(self.value + other.value)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            return((
                None,
                Exc_OperationError(
                    f'{other.type} can not be added to {self.type}',
                    self.start, other.end,
                    self.context
                )
            ))

    def subtract(self, other: IntType) -> Tuple[Optional[IntType], Optional[Exc_OperationError]]:
        if isinstance(other, IntType):
            return((
                IntType(self.value - other.value)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            return((
                None,
                Exc_OperationError(
                    f'{other.type} can not be subtracted from {self.type}',
                    self.start, other.end,
                    self.context
                )
            ))

    def multiply(self, other: IntType) -> Tuple[Optional[IntType], Optional[Exc_OperationError]]:
        if isinstance(other, IntType):
            return((
                IntType(self.value * other.value)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            return((
                None,
                Exc_OperationError(
                    f'{self.type} can not be multiplied by {other.type}',
                    self.start, other.end,
                    self.context
                )
            ))

    def divide(self, other: IntType) -> Tuple[Optional[IntType], Optional[Exc_OperationError]]:
        if isinstance(other, IntType):
            if other.value == 0:
                return((
                    None,
                    Exc_OperationError(
                        f'Division by zero',
                        other.start, other.end,
                        self.context
                    )
                ))

            return((
                IntType(int(self.value / other.value))
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            return((
                None,
                Exc_OperationError(
                    f'{self.type} can not be divided by {other.type}',
                    self.start, other.end,
                    self.context
                )
            ))

    def raised(self, other: IntType) -> Tuple[Optional[IntType], Optional[Exc_OperationError]]:
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
            return((
                None,
                Exc_OperationError(
                    f'{self.type} can not be raised to {other.type}',
                    self.start, other.end,
                    self.context
                )
            ))

    def lessthan(self, other: IntType) -> Tuple[Optional[BooleanType], Optional[Exc_OperationError]]:
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
            return((None, Exc_OperationError(f'{self.type} can not be compared with {other.type}', self.start, other.end, self.context)))

    def ltequals(self, other: IntType) -> Tuple[Optional[BooleanType], Optional[Exc_OperationError]]:
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
            return((None, Exc_OperationError(f'{self.type} can not be compared with {other.type}', self.start, other.end, self.context)))

    def greaterthan(self, other: IntType) -> Tuple[Optional[BooleanType], Optional[Exc_OperationError]]:
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
            return((None, Exc_OperationError(f'{self.type} can not be compared with {other.type}', self.start, other.end, self.context)))

    def gtequals(self, other: IntType) -> Tuple[Optional[BooleanType], Optional[Exc_OperationError]]:
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
            return((None, Exc_OperationError(f'{self.type} can not be compared with {other.type}', self.start, other.end, self.context)))

    def tostr(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((StringType(self.__clean__()).setcontext(self.context).setpos(self.start, self.end), None))

    def toint(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((self.copy(), None))

    def tofloat(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((FloatType(float(self.value)).setcontext(self.context).setpos(self.start, self.end), None))

    def copy(self):
        copy = IntType(self.value)
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end)

        return(copy)


class FloatType(TypeObj):
    def __init__(self, value):
        if not isinstance(value, float):
            raise TypeError(f'Internal Error: Non floating point value receievd ({type(value).__name__})')
        super().__init__(value, type_=TYPES['floatingpoint'])


    def add(self, other: FloatType) -> Tuple[Optional[FloatType], Optional[Exc_OperationError]]:
        if isinstance(other, FloatType):
            return((
                FloatType(self.value + other.value)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            return((
                None,
                Exc_OperationError(
                    f'{other.type} can not be added to {self.type}',
                    self.start, other.end,
                    self.context
                )
            ))

    def subtract(self, other: FloatType) -> Tuple[Optional[FloatType], Optional[Exc_OperationError]]:
        if isinstance(other, FloatType):
            return((
                FloatType(self.value - other.value)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            return((
                None,
                Exc_OperationError(
                    f'{other.type} can not be subtracted from {self.type}',
                    self.start, other.end,
                    self.context
                )
            ))

    def multiply(self, other: FloatType) -> Tuple[Optional[FloatType], Optional[Exc_OperationError]]:
        if isinstance(other, FloatType):
            return((
                FloatType(self.value * other.value)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            return((
                None,
                Exc_OperationError(
                    f'{self.type} can not be multiplied by {other.type}',
                    self.start, other.end,
                    self.context
                )
            ))

    def divide(self, other: FloatType) -> Tuple[Optional[FloatType], Optional[Exc_OperationError]]:
        if isinstance(other, FloatType):
            if other.value == 0:
                return((
                    None,
                    Exc_OperationError(
                        f'Division by zero',
                        self.start, other.end,
                        self.context
                    )
                ))

            return((
                FloatType(self.value / other.value)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            return((
                None,
                Exc_OperationError(
                    f'{self.type} can not be divided by {other.type}',
                    self.start, other.end,
                    self.context
                )
            ))

    def raised(self, other: FloatType) -> Tuple[Optional[FloatType], Optional[Exc_OperationError]]:
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
            return((
                None,
                Exc_OperationError(
                    f'{self.type} can not be raised to {other.type}',
                    self.start, other.end,
                    self.context
                )
            ))

    def lessthan(self, other: FloatType) -> Tuple[Optional[BooleanType], Optional[Exc_OperationError]]:
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
            return((
                None,
                Exc_OperationError(
                    f'{self.type} can not be compared with {other.type}',
                    self.start, other.end, 
                    self.context
                )
            ))

    def ltequals(self, other: FloatType) -> Tuple[Optional[BooleanType], Optional[Exc_OperationError]]:
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
            return((
                None,
                Exc_OperationError(
                    f'{self.type} can not be compared with {other.type}',
                    self.start, other.end,
                    self.context
                )
            ))

    def greaterthan(self, other: FloatType) -> Tuple[Optional[BooleanType], Optional[Exc_OperationError]]:
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
            return((
                None,
                Exc_OperationError(
                    f'{self.type} can not be compared with {other.type}',
                    self.start, other.end,
                    self.context
                )
            ))

    def gtequals(self, other: FloatType) -> Tuple[Optional[BooleanType], Optional[Exc_OperationError]]:
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
            return((
                None, 
                Exc_OperationError(
                    f'{self.type} can not be compared with {other.type}',
                    self.start, other.end,
                    self.context
                )
            ))

    def tostr(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((StringType(self.__clean__()).setcontext(self.context).setpos(self.start, self.end), None))

    def toint(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        if int(self.value) != self.value:
            return((None,
                    Exc_ValueError(
                        f'{self.__repr__()} ({self.type}) can not be converted to {TYPES["integer"]}',
                        self.start, self.end,
                        self.context
                    )
                ))
        return((IntType(int(self.value)).setcontext(self.context).setpos(self.start, self.end), None))

    def tofloat(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((self.copy(), None))

    def copy(self):
        copy = FloatType(self.value)
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end)

        return(copy)




class StringType(TypeObj):
    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError(f'Internal Error: Non string value receievd ({type(value).__name__})')
        super().__init__(value, type_=TYPES['string'])


    def add(self, other: StringType) -> Tuple[Optional[StringType], Optional[Exc_OperationError]]:
        if isinstance(other, StringType):
            return((
                StringType(self.value + other.value)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                None
            ))
        else:
            return((
                None,
                Exc_OperationError(
                    f'{other.type} can not be added to {self.type}',
                    self.start, other.end,
                    self.context
                )
            ))

    def tostr(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((StringType(self.__clean__()).setcontext(self.context).setpos(self.start, self.end), None))

    def toint(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        try:
            value = int(self.value)
        except:
            return((None,
                    Exc_ValueError(
                        f'{self.__repr__()} ({self.type}) can not be converted to {TYPES["integer"]}',
                        self.start, self.end,
                        self.context
                    )
                ))
        return((IntType(value).setcontext(self.context).setpos(self.start, self.end), None))

    def tofloat(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        try:
            value = float(self.value)
        except:
            return((None,
                    Exc_ValueError(
                        f'{self.__repr__()} ({self.type}) can not be converted to {TYPES["floatingpoint"]}',
                        self.start, self.end,
                        self.context
                    )
                ))
        return((FloatType(value).setcontext(self.context).setpos(self.start, self.end), None))

    def copy(self):
        copy = StringType(self.value)
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end)

        return(copy)

    def __clean__(self):
        return(f'{self.value}')

    def __repr__(self):
        return(f'\'{self.value}\'')




class BooleanType(TypeObj):
    def __init__(self, value):
        if not isinstance(value, bool):
            raise TypeError(f'Internal Error: Non boolean value receievd ({type(value).__name__})')
        super().__init__(value, type_=TYPES['boolean'])

    def and_(self, other: BooleanType) -> Tuple[Optional[BooleanType], Optional[Exc_OperationError]]:
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
            return((
                None, 
                Exc_OperationError(
                    f'{self.type} can not be combined with {other.type}',
                    self.start, other.end,
                    self.context
                )
            ))

    def or_(self, other: BooleanType) -> Tuple[Optional[BooleanType], Optional[Exc_OperationError]]:
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
            return((
                None, 
                Exc_OperationError(
                    f'{self.type} can not be combined with {other.type}',
                    self.start, other.end,
                    self.context
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
        return((StringType(self.__clean__()).setcontext(self.context).setpos(self.start, self.end), None))

    def toint(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((IntType(int(self.value)).setcontext(self.context).setpos(self.start, self.end), None))

    def tofloat(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((IntType(float(self.value)).setcontext(self.context).setpos(self.start, self.end), None))

    def copy(self):
        copy = BooleanType(self.value)
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end)

        return(copy)


class ArrayType(TypeObj):
    def __init__(self, elements):
        super().__init__(type_=TYPES['list'])
        self.elements = elements

    def copy(self):
        copy = ArrayType(self.elements.copy())
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end)

        return(copy)

    def tostr(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((StringType(self.__clean__()).setcontext(self.context).setpos(self.start, self.end), None))

    def __repr__(self):
        return(f'[{", ".join([str(i) for i in self.elements])}]')



class BaseFunction(TypeObj):
    def __init__(self, name=None, type_=TYPES['builtinfunc']):
        super().__init__(type_=type_)
        self.name = name or '<Anonymous>'

    def gencontext(self, display):
        self.display = display
        context = Context(
            display,
            SymbolTable(self.context.symbols),
            self.context,
            self.start
        )

        return(context)

    def checkargs(self, argnames, args):
        res = RTResult()

        if len(args) != len(argnames):
            end = self.end
            end.column -= 1
            return(
                res.failure(
                    Exc_ArgumentError(
                        f'\'{self.name}\' takes {len(argnames)} arguments, {len(args)} given',
                        self.start, end,
                        self.context
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
        return((StringType(self.__clean__()).setcontext(self.context).setpos(self.start, self.end), None))


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

            if res.shouldreturn():
                return(res)

        result = res.funcvalue or NullType()
        return(
            res.success(result)
        )

    def copy(self):
        copy = FunctionType(self.bodynodes, self.argnames, self.shouldreturn)
        copy.id = self.id
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end)

        return(copy)

    def tostr(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((StringType(self.__clean__()).setcontext(self.context).setpos(self.start, self.end), None))

    def __repr__(self):
        return(f'<{TYPES["function"]} {self.name} <{self.id}>>')


class BuiltInFunctionType(BaseFunction):
    def __init__(self, name):
        super().__init__(name, type_=TYPES['builtinfunc'])

    def call(self, name, args):
        res = RTResult()

        exec_context = self.gencontext(('Built-In Function', name))

        method = f'exec_{self.name}'
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
        return((StringType(self.__clean__()).setcontext(self.context).setpos(self.start, self.end), None))

    def copy(self):
        copy = BuiltInFunctionType(self.name)
        copy.id = self.id
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end)

        return(copy)

    def __repr__(self):
        return(f'<{TYPES["builtinfunc"]} {self.name}>')


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
                        exec_context
                    )
                )
            )

        if not isinstance(message, StringType):
            return(
                res.failure(
                    Exc_ArgumentTypeError(
                        f'\'message\' must be of type {TYPES["string"]}, {message.type} given',
                        message.start, message.end,
                        exec_context
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
            return(
                res.failure(
                    Exc_AssertionError(
                        f'{message}',
                        condition.start, condition.end,
                        exec_context
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
                        exec_context
                    )
                )
            )

        raise PeridotPanic(message)
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
                        exec_context
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
        copy.setpos(self.start, self.end)

        return(copy)

    def tostr(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((StringType(self.__clean__()).setcontext(self.context).setpos(self.start, self.end), None))

    def __repr__(self):
        return(f'<{self.exc}:{self.msg}, {self.line + 1}:{self.column + 1}>')


class IdType(TypeObj):
    def __init__(self, value):
        super().__init__(value, type_=TYPES['id'])

    def copy(self):
        copy = IdType(self.value)
        copy.id = self.id
        copy.setcontext(self.context)
        self.setpos(self.start, self.end)

        return(copy)

    def tostr(self):
        return((StringType(self.value).setcontext(self.context).setpos(self.start, self.end)), None)

    def toint(self):
        return((IntType(int(self.value, 16)).setcontext(self.context).setpos(self.start, self.end)), None)

    def __repr__(self):
        return(f'<Id {self.value}>')
