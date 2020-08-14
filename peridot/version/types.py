##########################################
# DEPENDENCIES                           #
##########################################

from __future__ import annotations
from typing import Any,Optional,Tuple, Type

from .context import Context, SymbolTable
from .exceptions import Exc_ArgumentError, Exc_OperationError, Exc_TypeError, Exc_OperationError # type: ignore


##########################################
# CONSTANTS                              #
##########################################

TYPES = {
    'invalid'      : 'Invalid',
    'nonetype'     : 'Null',
    'integer'      : 'Int',
    'floatingpoint': 'Float',
    'string'       : 'Str',
    'boolean'      : 'Bool'
}

##########################################
# RUNTIME RESULT                         #
##########################################

class RTResult():
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        self.error = res.error
        return(res.value)

    def success(self, value):
        self.value = value
        return(self)

    def failure(self, error):
        self.error = error
        return(self)

##########################################
# TYPES                                  #
##########################################

class TypeObj():
    def __init__(self, value, type_=TYPES['invalid']):
        self.value = value
        self.type  = type_

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
        return((None, Exc_OperationError(f'{self.type} can not be added to', self.start, other.end, self.context)))
    def subtract(self, other: Any) -> Tuple[Any, Optional[Exc_OperationError]]:
        return((None, Exc_OperationError(f'{self.type} can not be subtracted from', self.start, other.end, self.context)))
    def multiply(self, other: Any) -> Tuple[Any, Optional[Exc_OperationError]]:
        return((None, Exc_OperationError(f'{self.type} can not be multiplied', self.start, other.end, self.context)))
    def divide(self, other: Any) -> Tuple[Any, Optional[Exc_OperationError]]:
        return((None, Exc_OperationError(f'{self.type} can not be divided', self.start, other.end, self.context)))
    def raised(self, other: Any) -> Tuple[Any, Optional[Exc_OperationError]]:
        return((None, Exc_OperationError(f'{self.type} can not be raised', self.start, other.end, self.context)))
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
        return((None, Exc_OperationError(f'{self.type} can not be compared with \'<\'', self.start, other.end, self.context)))
    def ltequals(self, other: Any) -> Tuple[Any, Optional[Exc_OperationError]]:
        return((None, Exc_OperationError(f'{self.type} can not be compared with \'<=\'', self.start, other.end, self.context)))
    def greaterthan(self, other: Any) -> Tuple[Any, Optional[Exc_OperationError]]:
        return((None, Exc_OperationError(f'{self.type} can not be compared with \'>\'', self.start, other.end, self.context)))
    def gtequals(self, other: Any) -> Tuple[Any, Optional[Exc_OperationError]]:
        return((None, Exc_OperationError(f'{self.type} can not be compared with \'>=\'', self.start, other.end, self.context)))
    def and_(self, other: Any) -> Tuple[Any, Optional[Exc_OperationError]]:
        return((None, Exc_OperationError(f'{self.type} can not be combined with \'and\'', self.start, other.end, self.context)))
    def or_(self, other: Any) -> Tuple[Any, Optional[Exc_OperationError]]:
        return((None, Exc_OperationError(f'{self.type} can not be combined with \'or\'', self.start, other.end, self.context)))
    def not_(self) -> Tuple[Any, Optional[Exc_OperationError]]:
        return((None, Exc_OperationError(f'{self.type} can not be inverted', self.start, self.end, self.context)))
    def call(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be called', self.start, self.end, self.context)))
    def istrue(self) -> Tuple[Any, Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be interpreted as {TYPES["boolean"]}', self.start, self.end, self.context)))

    def __repr__(self):
        return(f'{self.value}')



class NullType(TypeObj):
    def __init__(self):
        super().__init__(None, type_=TYPES['nonetype'])

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
                        self.start, other.end,
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
