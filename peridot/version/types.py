##########################################
# DEPENDENCIES                           #
##########################################

from __future__ import annotations
from typing import Any as _Any, Optional as _Optional, Tuple as _Tuple
from uuid import uuid4 as _uuid4
from decimal   import Decimal
from fractions import Fraction as _Fraction

def _typesinit(catch, exceptions, context, constants, tokens, nodes, interpreter):
    global InternalPeridotError
    InternalPeridotError = catch.InternalPeridotError
    global Exc_ArgumentError, Exc_AssertionError, Exc_AttributeError, Exc_IndexError, Exc_KeyError, Exc_OperationError, Exc_PanicError, Exc_ReturnError, Exc_ThrowError, Exc_TypeError, Exc_ValueError
    Exc_ArgumentError    = exceptions.Exc_ArgumentError
    Exc_AssertionError   = exceptions.Exc_AssertionError
    Exc_AttributeError   = exceptions.Exc_AttributeError
    Exc_IndexError       = exceptions.Exc_IndexError
    Exc_KeyError         = exceptions.Exc_KeyError
    Exc_OperationError   = exceptions.Exc_OperationError
    Exc_PanicError       = exceptions.Exc_PanicError
    Exc_ReturnError      = exceptions.Exc_ReturnError
    Exc_ThrowError       = exceptions.Exc_ThrowError
    Exc_TypeError        = exceptions.Exc_TypeError
    Exc_ValueError       = exceptions.Exc_ValueError
    global Context, SymbolTable
    Context              = context.Context
    SymbolTable          = context.SymbolTable
    global KEYWORDS, DIGITS
    KEYWORDS             = constants.KEYWORDS
    DIGITS               = constants.DIGITS
    global TT_EQEQUALS, TT_BANGEQUALS, TT_LESSTHAN, TT_LTEQUALS, TT_GREATERTHAN, TT_GTEQUALS, TT_KEYWORD
    TT_EQEQUALS          = tokens.TT_EQEQUALS
    TT_BANGEQUALS        = tokens.TT_BANGEQUALS
    TT_LESSTHAN          = tokens.TT_LESSTHAN
    TT_LTEQUALS          = tokens.TT_LTEQUALS
    TT_GREATERTHAN       = tokens.TT_GREATERTHAN
    TT_GTEQUALS          = tokens.TT_GTEQUALS
    TT_KEYWORD           = tokens.TT_KEYWORD
    global VarAssignNode, VarCreateNode, VarNullNode, VarAccessNode, FuncCallNode, IndicieNode, AttributeNode, BinaryOpNode, UnaryOpNode
    VarAssignNode        = nodes.VarAssignNode
    VarCreateNode        = nodes.VarCreateNode
    VarNullNode          = nodes.VarNullNode
    VarAccessNode        = nodes.VarAccessNode
    FuncCallNode         = nodes.FuncCallNode
    IndicieNode          = nodes.IndicieNode
    AttributeNode        = nodes.AttributeNode
    BinaryOpNode         = nodes.BinaryOpNode
    UnaryOpNode          = nodes.UnaryOpNode

    global _RTResult, Interpreter
    _RTResult            = interpreter.RTResult
    Interpreter          = interpreter.Interpreter

##########################################
# CONSTANTS                              #
##########################################

TYPES = {
    'invalid'      : 'Invalid',
    'type'         : 'Type',
    'nonetype'     : 'Null',
    'integer'      : 'Int',
    'floatingpoint': 'Float',
    'string'       : 'Str',
    'list'         : 'Array',
    'tuple'        : 'Tuple',
    'dictionary'   : 'Dict',
    'boolean'      : 'Bool',
    'function'     : 'Function',
    'builtinfunc'  : 'Built-In Function',
    'exception'    : 'Exception',
    'id'           : 'Id',
    'namespace'    : 'Namespace'
}

def _uuid():
    u = '00000000000000000000000000000000'
    while u == '00000000000000000000000000000000':
        u = str(_uuid4()).replace('-', '')

    return(u)

class PeriSpace(): pass
class PyriObj(): pass

def toperidot(value, start, end, context):
    if value == None:
        return(
            NullType()
                .setpos(start, end)
                .setcontext(context)
        )

    elif type(value) == int:
        return(
            IntType(value)
                .setpos(start, end)
                .setcontext(context)
        )

    elif type(value) == float:
        return(
            FloatType(value)
                .setpos(start, end)
                .setcontext(context)
        )

    elif type(value) == str:
        return(
            StringType(value)
                .setpos(start, end)
                .setcontext(context)
        )

    elif type(value) == bool:
        return(
            BooleanType(value)
                .setpos(start, end)
                .setcontext(context)
        )

    elif type(value) == list:
        v = []
        for i in value:
            v.append(
                toperidot(i, start, end, context)
            )
        return(
            ArrayType(v)
                .setpos(start, end)
                .setcontext(context)
        )

    elif type(value) == dict:
        v = {}
        for i in value.keys():
            key = toperidot(i, start, end, context)
            v[i] = toperidot(value[i], start, end, context)
        return(
            DictionaryType(v)
                .setpos(start, end)
                .setcontext(context)
        )

    elif type(value) == tuple:
        v = []
        for i in value:
            v.append(
                toperidot(i, start, end, context)
            )
        return(
            TupleType(tuple(v))
                .setpos(start, end)
                .setcontext(context)
        )

    elif isinstance(value, TypeObj):
        return(value)

    else:
        raise TypeError(f'{value} is not a valid peridot type')

##########################################
# TYPES                                  #
##########################################

class TypeObj():
    def __init__(self, value=None, type_=TYPES['invalid']):
        self.value = value
        self.type  = type_
        self.id = _uuid()
        self.name = '<Anonymous>'

        self.reserved = False

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


    def add(self, other: _Any) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be added to', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def subtract(self, other: _Any) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be subtracted from', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def multiply(self, other: _Any) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be multiplied', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def divide(self, other: _Any) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be divided', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def raised(self, other: _Any) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be raised', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def eqequals(self: _Any, other: _Any) -> _Tuple[BooleanType, None]:
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
    def bangequals(self, other: _Any) -> _Tuple[BooleanType, None]:
        eqequals, error = self.eqequals(other)
        if error:
            return((None, error))
        eqequals.value = not eqequals.value

        return((eqequals, None))
        
    def lessthan(self, other: _Any) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be compared with \'<\'', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def ltequals(self, other: _Any) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be compared with \'<=\'', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def greaterthan(self, other: _Any) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be compared with \'>\'', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def gtequals(self, other: _Any) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be compared with \'>=\'', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def and_(self, other: _Any) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be combined with \'and\'', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def or_(self, other: _Any) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be combined with \'or\'', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def not_(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be inverted', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def call(self, name, args, opts, rawargs) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        res = _RTResult()
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
    def istrue(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be interpreted as {TYPES["boolean"]}', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def totype(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be converted to {TYPES["type"]}', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def tostr(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be converted to {TYPES["string"]}', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def toint(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be converted to {TYPES["integer"]}', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def tofloat(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be converted to {TYPES["floatingpoint"]}', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def tobool(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be converted to {TYPES["boolean"]}', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def toarray(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be converted to {TYPES["list"]}', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))
    def totuple(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be converted to {TYPES["tuple"]}', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))

    def indicie(self, indicie) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((None, Exc_TypeError(f'{self.type} can not be indexed', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))

    def attribute(self, attribute) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((None, Exc_AttributeError(f'\'{self.name}\' has no attribute \'{attribute.value}\'', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))

    def __clean__(self):
        return(self.__repr__())

    def __repr__(self):
        return(f'{self.value}')



class NullType(TypeObj):
    def __init__(self):
        super().__init__(type_=TYPES['nonetype'])

    def eqequals(self: _Any, other: _Any) -> _Tuple[BooleanType, None]:
        if type(self) == type(other):
            return((
                BooleanType(True)
                    .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)
                    .setcontext(self.context),
                None
            ))
        else:
            return((
                BooleanType(False)
                    .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)
                    .setcontext(self.context),
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
NullType.type = TYPES['nonetype']



class IntType(TypeObj):
    def __init__(self, value):
        if isinstance(value, bool) or not isinstance(value, int):
            raise InternalPeridotError(f'Non int value receievd ({type(value).__name__})')
        super().__init__(value, type_=TYPES['integer'])


    def add(self, other: _Any) -> _Tuple[_Optional[IntType], _Optional[Exc_TypeError]]:
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

    def subtract(self, other: _Any) -> _Tuple[_Optional[IntType], _Optional[Exc_TypeError]]:
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

    def multiply(self, other: _Any) -> _Tuple[_Optional[IntType], _Optional[Exc_TypeError]]:
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

    def divide(self, other: _Any) -> _Tuple[_Optional[IntType], _Any]:
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

    def raised(self, other: _Any) -> _Tuple[_Optional[IntType], _Optional[Exc_TypeError]]:
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

    def lessthan(self, other: _Any) -> _Tuple[_Optional[BooleanType], _Optional[Exc_TypeError]]:
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

    def ltequals(self, other: _Any) -> _Tuple[_Optional[BooleanType], _Optional[Exc_TypeError]]:
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

    def greaterthan(self, other: _Any) -> _Tuple[_Optional[BooleanType], _Optional[Exc_TypeError]]:
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

    def gtequals(self, other: _Any) -> _Tuple[_Optional[BooleanType], _Optional[Exc_TypeError]]:
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

    def totype(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            BuiltInFunctionType('int', type_=TYPES['type'], returntype=TYPES['integer'])
                .setcontext(self.context)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay),
            None
        ))

    def tostr(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def tofloat(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            FloatType(float(self.value))
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def attribute(self, attribute) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        if attribute.value == 'as_ratio':
            f = BuiltInFunctionType('as_ratio').setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        else:
            return((None, Exc_TypeError(f'\'{self.name}\' has no attribute \'{attribute.value}\'', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))

    def copy(self):
        copy = IntType(self.value)
        copy.setcontext(self.context)
        copy.setpos(
            self.start, self.end,
            self.originstart, self.originend, self.origindisplay
        )
        copy.id = self.id

        return(copy)
IntType.type = TYPES['integer']


class FloatType(TypeObj):
    def __init__(self, value):
        if not isinstance(value, float):
            raise InternalPeridotError(f'Non float value receievd ({type(value).__name__})')
        super().__init__(value, type_=TYPES['floatingpoint'])


    def add(self, other: _Any) -> _Tuple[_Optional[FloatType], _Optional[Exc_TypeError]]:
        if isinstance(other, FloatType):
            return((
                FloatType(float(Decimal(str(self.value)) + Decimal(str(other.value))))
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

    def subtract(self, other: _Any) -> _Tuple[_Optional[FloatType], _Optional[Exc_TypeError]]:
        if isinstance(other, FloatType):
            return((
                FloatType(float(Decimal(str(self.value)) - Decimal(str(other.value))))
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

    def multiply(self, other: _Any) -> _Tuple[_Optional[FloatType], _Optional[Exc_TypeError]]:
        if isinstance(other, FloatType):
            return((
                FloatType(float(Decimal(str(self.value)) * Decimal(str(other.value))))
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

    def divide(self, other: _Any) -> _Tuple[_Optional[FloatType], _Any]:
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
                FloatType(float(Decimal(str(self.value)) / Decimal(str(other.value))))
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

    def raised(self, other: _Any) -> _Tuple[_Optional[FloatType], _Optional[Exc_TypeError]]:
        if isinstance(other, FloatType):
            return((
                FloatType(
                    float(Decimal(str(self.value)) ** Decimal(str(other.value)))
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

    def lessthan(self, other: _Any) -> _Tuple[_Optional[BooleanType], _Optional[Exc_TypeError]]:
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

    def ltequals(self, other: _Any) -> _Tuple[_Optional[BooleanType], _Optional[Exc_TypeError]]:
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

    def greaterthan(self, other: _Any) -> _Tuple[_Optional[BooleanType], _Optional[Exc_TypeError]]:
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

    def gtequals(self, other: _Any) -> _Tuple[_Optional[BooleanType], _Optional[Exc_TypeError]]:
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

    def totype(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            BuiltInFunctionType('float', type_=TYPES['type'], returntype=TYPES['floatingpoint'])
                .setcontext(self.context)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay),
            None
        ))

    def tostr(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def toint(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
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

    def attribute(self, attribute) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        if attribute.value == 'as_ratio':
            f = BuiltInFunctionType('as_ratio').setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        else:
            return((None, Exc_AttributeError(f'\'{self.name}\' has no attribute \'{attribute.value}\'', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))

    def copy(self):
        copy = FloatType(self.value)
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)
        copy.id = self.id

        return(copy)
FloatType.type = TYPES['floatingpoint']




class StringType(TypeObj):
    def __init__(self, value):
        if not isinstance(value, str):
            raise InternalPeridotError(f'Non str value receievd ({type(value).__name__})')
        super().__init__(value, type_=TYPES['string'])


    def add(self, other: _Any) -> _Tuple[_Optional[StringType], _Optional[Exc_TypeError]]:
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

    def totype(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            BuiltInFunctionType('str', type_=TYPES['type'], returntype=TYPES['string'])
                .setcontext(self.context)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay),
            None
        ))

    def toint(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
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

    def tofloat(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        try:
            num = ''
            dots = 0
            index = 0
            char = self.value[index]

            if char == '.':
                raise(ValueError)

            while index < len(self.value):
                char = self.value[index]
                if char == '.':
                    if dots >= 1:
                        raise(ValueError())
                    dots += 1
                    num += '.'
                else:
                    num += char

                index += 1

            index -= 1
            char = self.value[index]
            if char == '.' or dots == 0:
                raise(ValueError())

            value = float(num)
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

    def toarray(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            ArrayType([StringType(i) for i in list(self.value)])
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def totuple(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            TupleType(tuple([StringType(i) for i in list(self.value)]))
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

    def attribute(self, attribute) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        if attribute.value == 'lalign':
            f = BuiltInFunctionType('lalign').setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        elif attribute.value == 'calign':
            f = BuiltInFunctionType('calign').setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        elif attribute.value == 'ralign':
            f = BuiltInFunctionType('ralign').setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        elif attribute.value == 'length':
            f = IntType(len(self.value)).setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        elif attribute.value == 'to_lower':
            f = BuiltInFunctionType('to_lower').setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        elif attribute.value == 'repeat':
            f = BuiltInFunctionType('repeat').setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        elif attribute.value == 'replace':
            f = BuiltInFunctionType('replace').setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        elif attribute.value == 'slice':
            f = BuiltInFunctionType('slice').setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        elif attribute.value == 'split':
            f = BuiltInFunctionType('split').setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        elif attribute.value == 'startswith':
            f = BuiltInFunctionType('startswith').setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        elif attribute.value == 'endswith':
            f = BuiltInFunctionType('endswith').setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        else:
            return((None, Exc_AttributeError(f'\'{self.name}\' has no attribute \'{attribute.value}\'', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))

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
StringType.type = TYPES['string']




class BooleanType(TypeObj):
    def __init__(self, value):
        if not isinstance(value, bool):
            raise InternalPeridotError(f'Non bool value receievd ({type(value).__name__})')
        super().__init__(value, type_=TYPES['boolean'])

    def and_(self, other: _Any) -> _Tuple[_Optional[BooleanType], _Optional[Exc_TypeError]]:
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

    def or_(self, other: _Any) -> _Tuple[_Optional[BooleanType], _Optional[Exc_TypeError]]:
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

    def not_(self) -> _Tuple[BooleanType, None]:
        return((
            BooleanType(
                not self.value
            )
                .setpos(self.start, self.end)
                .setcontext(self.context),
            None
        ))

    def istrue(self) -> _Tuple[BooleanType, None]:
        return((
            self.value,
            None
        ))

    def totype(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            BuiltInFunctionType('bool', type_=TYPES['type'], returntype=TYPES['boolean'])
                .setcontext(self.context)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay),
            None
        ))

    def tostr(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            StringType(self.__clean__())
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
BooleanType.type = TYPES['boolean']


class ArrayType(TypeObj):
    def __init__(self, elements):
        if not isinstance(elements, list):
            raise InternalPeridotError(f'Non list value received')
        if len(elements):
            self.elmtype = type(elements[0])
            if not all(type(x) == self.elmtype for x in elements):
                raise InternalPeridotError(f'Array element recieved non {self.elmtype.__name__} value')

        super().__init__(elements, type_=TYPES['list'])

    def add(self: _Any, other: _Any) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        if type(self) == type(other):
            return((
                ArrayType(self.value + other.value)
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

    def eqequals(self: _Any, other: _Any) -> _Tuple[BooleanType, None]:
        equals = True
        if type(self) == type(other):
            if len(self.value) == len(other.value):
                for i in range(len(self.value)):
                    if not self.value[i].eqequals(other.value[i])[0].value:
                        equals = False
                        break
            else:
                equals = False
        else:
            equals = False
        return((
            BooleanType(equals)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)
                .setcontext(self.context),
            None
        ))

    def totype(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            BuiltInFunctionType('array', type_=TYPES['type'], returntype=TYPES['list'])
                .setcontext(self.context)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay),
            None
        ))

    def tostr(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def totuple(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            TupleType(tuple(self.value))
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

    def attribute(self, attribute):
        if attribute.value == 'join':
            f = BuiltInFunctionType('join').setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        elif attribute.value == 'slice':
            f = BuiltInFunctionType('slice').setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        elif attribute.value == 'length':
            f = IntType(len(self.value)).setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        else:
            return((None, Exc_AttributeError(f'\'{self.name}\' has no attribute \'{attribute.value}\'', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))

    def copy(self):
        copy = ArrayType(self.value.copy())
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)
        copy.id = self.id

        return(copy)

    def __repr__(self):
        return(f'[{", ".join([i.__repr__() for i in self.value])}]')
ArrayType.type = TYPES['list']


class DictionaryType(TypeObj):
    def __init__(self, elements):
        if not isinstance(elements, dict):
            raise InternalPeridotError(f'Non dict value received')
        keys = list(elements.keys())
        if len(keys):
            self.keytype = type(keys[0])
            self.keytypename = keys[0].type
            self.valuetype = type(elements[keys[0]])
            self.valuetypename = elements[keys[0]].type
            if not all(type(x) == self.keytype for x in keys):
                raise InternalPeridotError(f'Dictionary element key recieved non {self.keytype.__name__} value')
            if not all(type(elements[x]) == self.valuetype for x in keys):
                raise InternalPeridotError(f'Dictionary element recieved non {self.valuetype.__name__} value')

        super().__init__(elements, type_=TYPES['dictionary'])

    def add(self: _Any, other: _Any) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        if type(self) == type(other):
            return((
                DictionaryType(dict(list(self.value.items()) + list(other.value.items())))
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

    def eqequals(self: _Any, other: _Any) -> _Tuple[BooleanType, None]:
        equals = True
        if type(self) == type(other):
            selfkeys = list(self.value.keys())
            otherkeys = list(other.value.keys())
            if len(selfkeys) == len(otherkeys):
                for i in range(len(selfkeys)):
                    if not selfkeys[i].eqequals(otherkeys[i])[0].value:
                        equals = False
                        break
                    if not self.value[selfkeys[i]].eqequals(other.value[otherkeys[i]])[0].value:
                        equals = False
                        break
            else:
                equals = False
        else:
            equals = False
        return((
            BooleanType(equals)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)
                .setcontext(self.context),
            None
        ))

    def totype(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            BuiltInFunctionType('dictionary', type_=TYPES['type'], returntype=TYPES['dictionary'])
                .setcontext(self.context)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay),
            None
        ))

    def tostr(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def indicie(self, indicie):
        if not isinstance(indicie, self.keytype):
            return((
                None,
                Exc_TypeError(
                    f'{self.type} key must be of type {self.keytypename}',
                    indicie.start, indicie.end,
                    self.context,
                    indicie.originstart, indicie.originend, indicie.origindisplay
                )
            ))
        
        value = None
        keys = list(self.value.keys())
        for i in range(len(keys)):
            eqequals, error = keys[i].eqequals(indicie)
            if error:
                return((
                    None,
                    error
                ))
            if eqequals.value:
                value = self.value[keys[i]]
                break

        if not value:
            return((
                None,
                Exc_KeyError(
                    f'{self.type} key, {indicie} does not exist',
                    indicie.start, indicie.end,
                    self.context,
                    indicie.originstart, indicie.originend, indicie.origindisplay
                )
            ))

        value = value.setpos(self.start, self.end).setcontext(self.context)

        return((
            value,
            None
        ))

    def attribute(self, attribute) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        if attribute.value == 'keys':
            f = TupleType(tuple(
                self.value.keys()
            ))
            f.setcontext(self.context).setpos(attribute.start, attribute.end)
            return((
                f,
                None
            ))
        elif attribute.value == 'values':
            f = TupleType(tuple(
                self.value.values()
            ))
            f.setcontext(self.context).setpos(attribute.start, attribute.end)
            return((
                f,
                None
            ))
        else:
            return((None, Exc_AttributeError(f'\'{self.name}\' has no attribute \'{attribute.value}\'', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))

    def copy(self):
        copy = DictionaryType(self.value.copy())
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)
        copy.id = self.id

        return(copy)

    def __repr__(self):
        result = ''
        first = True
        keys = list(self.value.keys())
        values = self.value
        for i in range(len(keys)):
            if not first:
                result += ', '
            result += f'{keys[i]}: {values[keys[i]]}'
            first = False
        return(f'{{{result}}}')
DictionaryType.type = TYPES['dictionary']


class TupleType(TypeObj):
    def __init__(self, elements):
        if not isinstance(elements, tuple):
            raise InternalPeridotError(f'Non tuple value received')

        super().__init__(elements, type_=TYPES['tuple'])

    def eqequals(self: _Any, other: _Any) -> _Tuple[BooleanType, None]:
        equals = True
        if type(self) == type(other):
            if len(self.value) == len(other.value):
                for i in range(len(self.value)):
                    if not self.value[i].eqequals(other.value[i])[0].value:
                        equals = False
                        break
            else:
                equals = False
        else:
            equals = False
        return((
            BooleanType(equals)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)
                .setcontext(self.context),
            None
        ))

    def totype(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            BuiltInFunctionType('tuple', type_=TYPES['type'], returntype=TYPES['tuple'])
                .setcontext(self.context)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay),
            None
        ))

    def tostr(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def toarray(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        if len(self.value):
            self.elmtype = type(self.value[0])
            for i in self.value:
                if type(i) != self.elmtype:
                    return((
                        None,
                        Exc_ValueError(
                            f'{TYPES["list"]} of type {self.elmtype.type} can not include {i.type}',
                            self.start, self.end,
                            self.context,
                            self.originstart, self.originend, self.origindisplay
                        )
                    ))

        return((
            ArrayType(list(self.value))
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

    def attribute(self, attribute):
        if attribute.value == 'length':
            f = IntType(len(self.value)).setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        else:
            return((None, Exc_AttributeError(f'\'{self.name}\' has no attribute \'{attribute.value}\'', self.start, self.end, self.context, self.originstart, self.originend, self.origindisplay)))

    def copy(self):
        copy = TupleType(self.value)
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)
        copy.id = self.id

        return(copy)

    def __repr__(self):
        return(f'({", ".join([str(i) for i in self.value])})')
TupleType.type = TYPES['tuple']



class BaseFunction(TypeObj):
    def __init__(self, name=None, type_=TYPES['builtinfunc']):
        if not isinstance(name, str) and name:
            raise InternalPeridotError(f'Non str value receievd ({type(name).__name__})')

        super().__init__(type_=type_)
        if name:
            self.name = name

    def gencontext(self, display):
        self.display = display
        exec_context = Context(
            display,
            SymbolTable(self.context.symbols),
            self.context,
            [self.start, self.end, [self.originstart], [self.originend], [self.origindisplay]]
        )
        exec_context.caughterrors = self.context.caughterrors

        return(exec_context)

    def checkargs(self, arguments, options, args, opts):
        res = _RTResult()

        if len(args) != len(list(arguments.keys())):
            try:
                self.originstart = self.originstart[0]
                self.originend = self.originend[0]
                self.origindisplay = self.origindisplay[0]
            except IndexError:
                pass

            return(
                res.failure(
                    Exc_ArgumentError(
                        f'\'{self.name}\' takes {len(list(arguments.keys()))} arguments, {len(args)} given',
                        self.start, self.end,
                        self.context,
                        self.originstart, self.originend, self.origindisplay
                    )
                )
            )

        for i in range(len(list(arguments.keys()))):
            argtypekey = list(arguments.keys())[i]
            argumenttype = arguments[list(arguments.keys())[i]]
            argument = args[i]

            if argumenttype != NullType:
                try:
                    if not isinstance(argument, argumenttype):
                        return(
                            res.failure(
                                Exc_TypeError(
                                    f'\'{argtypekey}\' must be of type {argumenttype.type}, {argument.type} given',
                                    argument.start, argument.end,
                                    self.context,
                                    argument.originstart, argument.originend, argument.origindisplay
                                )
                            )
                        )
                except TypeError:
                    if argument.type != argumenttype:
                        return(
                            res.failure(
                                Exc_TypeError(
                                    f'\'{argtypekey}\' must be of type {argumenttype}, {argument.type} given',
                                    argument.start, argument.end,
                                    self.context,
                                    argument.originstart, argument.originend, argument.origindisplay
                                )
                            )
                        )

        for i in range(len(list(opts.keys()))):
            optkey = list(opts.keys())[i]
            try:
                optiondef = options[optkey]
            except KeyError:
                return(
                    res.failure(
                        Exc_ArgumentError(
                            f'\'{self.name}\' has no option \'{optkey}\'',
                            opts[optkey].start, opts[optkey].end,
                            self.context,
                            opts[optkey].originstart, opts[optkey].originend, opts[optkey].origindisplay
                        )
                    )
                )

            if opts[optkey]:
                option = opts[optkey]
            else:
                option = optiondef

            if not isinstance(optiondef, NullType):
                if optiondef.type != option.type:
                    return(
                        res.failure(
                            Exc_TypeError(
                                f'\'{optkey}\' must be of type {optiondef.type}, {option.type} given',
                                option.start, option.end,
                                self.context,
                                option.originstart, option.originend, option.origindisplay
                            )
                        )
                    )

        return(
            res.success(None)
        )

    def topython(self, value):
        if isinstance(value, tuple):
            value = value[0]

        if isinstance(value, str):
            v = value

        elif isinstance(value, NullType):
            v = None

        elif isinstance(value, ArrayType):
            v = []
            for i in value.value:
                v.append(
                    self.topython(i)
                )

        elif isinstance(value, DictionaryType):
            v = {}
            for i in value.value.keys():
                v[self.topython(i)] = self.topython(value.value[i])

        elif isinstance(value, TupleType):
            v = []
            for i in value.value:
                v.append(
                    self.topython(i)
                )
            v = tuple(v)

        elif isinstance(value, BaseFunction):
            return(value.call)

        elif isinstance(value, ExceptionType):
            exec(f'class PeriExc_{value.exc}(BaseException): pass')
            v = eval(f'PeriExc_{value.exc}')

        elif isinstance(value, NamespaceType):
            v = PeriSpace()
            for i in value.symbols.symbols.keys():
                try:
                    exec(f'v.{i} = value.symbols.symbols[i]')
                except: pass

        else:
            v = value.value

        ret = PyriObj()
        ret.value = v
        ret.start = value.start
        ret.end   = value.end
        ret.originstart   = value.originstart
        ret.originend     = value.originend
        ret.origindisplay = value.origindisplay
        return(ret)

    def popargs(self, arguments, options, args, opts, rawargs, exec_context):
        keys = list(arguments.keys())
        returnargs = {}
        for i in range(len(keys)):
            argname = keys[i]
            argvalue = args[i]
            argvalue.setcontext(exec_context)
            if rawargs:
                argvalue = (args[i], rawargs[i])

            exec_context.symbols.assign(argname, argvalue)
            returnargs[argname] = self.topython(argvalue)

        returnopts = {}
        keys = list(options.keys())
        for i in range(len(keys)):
            optname = keys[i]
            try:
                optvalue = opts[keys[i]]
            except KeyError:
                optvalue = options[keys[i]]
            optvalue.setcontext(exec_context)

            exec_context.symbols.assign(optname, optvalue)
            returnopts[optname] = self.topython(optvalue)

        return((returnargs, returnopts))

        

    def checkpopargs(self, arguments, options, args, opts, rawargs, exec_context):
        res = _RTResult()

        res.register(
            self.checkargs(
                arguments,
                options,
                args,
                opts
            )
        )

        if res.shouldreturn():
            return(res)

        ret = self.popargs(arguments, options, args, opts, rawargs, exec_context)

        return(
            res.success(ret)
        )

    def tostr(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay),
            None
        ))
BaseFunction.type = TYPES['builtinfunc']


class FunctionType(BaseFunction):
    def __init__(self, bodynodes, arguments, options, returntype, shouldreturn):
        super().__init__(type_=TYPES['function'])
        self.bodynodes = bodynodes
        self.arguments = arguments
        self.options = options
        self.returntype = returntype
        self.shouldreturn = shouldreturn

    def eqequals(self: _Any, other: _Any) -> _Tuple[BooleanType, None]:
        if type(self) == type(other):
            return((
                BooleanType(
                    self.id == other.id
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

    def call(self, name, args, opts, rawargs):
        res = _RTResult()
        interpreter = Interpreter()

        exec_context = self.gencontext((name or self.name, self.id))
        res.register(
            self.checkpopargs(
                self.arguments, self.options, args, opts, None,
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

        if not result:
            return(
                res.failure(
                    Exc_ReturnError(
                        f'\'{self.name}\' did not return a value',
                        self.start, self.end,
                        self.context,
                        self.originstart, self.originend, self.origindisplay
                    )
                )
            )

        if not self.returntype == NullType:
            if self.returntype.returntype.type != result.type:
                return(
                    res.failure(
                        Exc_TypeError(
                            f'Return value of \'{self.name}\' must be of type {self.returntype.returntype.type}, {result.type} returned',
                            result.start, result.end,
                            exec_context,
                            result.originstart, result.originend, result.origindisplay
                        )
                    )
                )

        if result:
            return(
                res.success(result)
            )

        try:
            self.originstart = self.originstart[0]
            self.originend = self.originend[0]
            self.origindisplay = self.origindisplay[0]
        except IndexError: pass

    def copy(self):
        copy = FunctionType(self.bodynodes, self.arguments, self.options, self.returntype, self.shouldreturn)
        copy.id = self.id
        copy.name = self.name
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)

        return(copy)

    def tostr(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay),
            None
        ))

    def __repr__(self):
        return(f'<{TYPES["function"]} {self.name} <{self.id}>>')
FunctionType.type = TYPES['function']


class BuiltInFunctionType(BaseFunction):
    def __init__(self, name, value=None, type_=TYPES['builtinfunc'], returntype=TYPES['type']):
        super().__init__(name, type_=type_)
        self.returntype = returntype
        if value:
            self.value = value
        else:
            self.value = name

    def eqequals(self: _Any, other: _Any) -> _Tuple[BooleanType, None]:
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

    def call(self, name, args, opts, rawargs):
        res = _RTResult()

        #exec_context = self.gencontext(('Built-In Function', name))
        exec_context = self.context.copy()

        method = f'exec_{self.value}'
        passself = False
        try:
            method = getattr(self, method)
        except AttributeError:
            passself = True
            method = f'{self.value}'
            method = BuiltInFunctionType.modules[method]

        try:
            argnames = method.argnames
        except AttributeError:
            argnames = {}
        try:
            optnames = method.optnames
        except AttributeError:
            optnames = {}

        ret = res.register(
            self.checkpopargs(
                argnames, optnames, args, opts, rawargs,
                exec_context
            )
        )

        if res.shouldreturn():
            return(res)

        args, opts = ret

        if passself:
            result = res.register(
                method(self, exec_context, args, opts)
            )
            if res.shouldreturn():
                return(res)
            result = toperidot(
                result,
                self.start, self.end,
                self.context
            )
        else:
            result = res.register(
                method(exec_context)
            )

        if res.shouldreturn():
            return(res)

        return(
            res.success(result)
        )

    def tostr(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay),
            None
        ))

    def copy(self):
        copy = BuiltInFunctionType(self.name, self.value, type_=self.type, returntype=self.returntype)
        copy.id = self.id
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)

        try:
            copy.editvalue = self.editvalue
        except AttributeError: pass

        return(copy)

    def __repr__(self):
        if self.type == TYPES['type']:
            return(f'<{self.type} {self.returntype}>')
        else:
            return(f'<{self.type} {self.name}>')


    def exec_throw(self, exec_context):
        res = _RTResult()

        exc = exec_context.symbols.access('exception')[0]
        
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
    exec_throw.argnames = {'exception': TYPES['exception']}
    exec_throw.optnames = {}


    def exec_assert(self, exec_context):
        res = _RTResult()

        condition = exec_context.symbols.access('condition')[0]
        conditiontype = exec_context.symbols.access('condition')[1]

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

            message = exec_context.symbols.access('msg')

            if len(message.value):
                message = message.value
            else:
                if isinstance(conditiontype, VarAssignNode) or isinstance(conditiontype, VarCreateNode) or isinstance(conditiontype, VarNullNode):
                    message = f'{conditiontype.valnode} is not True'

                elif isinstance(conditiontype, VarAccessNode) or isinstance(conditiontype, FuncCallNode) or isinstance(conditiontype, IndicieNode) or isinstance(conditiontype, AttributeNode):
                    message = f'{conditiontype} is not True'

                elif isinstance(conditiontype, BinaryOpNode):
                    if conditiontype.optoken.type == TT_EQEQUALS:
                        message = f'{conditiontype.lnode} is not equal to {conditiontype.rnode}'
                    elif conditiontype.optoken.type == TT_BANGEQUALS:
                        message = f'{conditiontype.lnode} is equal to {conditiontype.rnode}'
                    elif conditiontype.optoken.type == TT_LESSTHAN:
                        message = f'{conditiontype.lnode} is not less than {conditiontype.rnode}'
                    elif conditiontype.optoken.type == TT_LTEQUALS:
                        message = f'{conditiontype.lnode} is not less than or equal to {conditiontype.rnode}'
                    elif conditiontype.optoken.type == TT_GREATERTHAN:
                        message = f'{conditiontype.lnode} is not greater than {conditiontype.rnode}'
                    elif conditiontype.optoken.type == TT_GTEQUALS:
                        message = f'{conditiontype.lnode} is not greater than or equal to {conditiontype.rnode}'
                    elif conditiontype.optoken.matches(TT_KEYWORD, KEYWORDS['logicaland']):
                        message = f'Both {conditiontype.lnode} and {conditiontype.rnode} are not True'
                    elif conditiontype.optoken.matches(TT_KEYWORD, KEYWORDS['logicalor']):
                        message = f'Neither {conditiontype.lnode} or {conditiontype.rnode} are True'

                elif isinstance(conditiontype, UnaryOpNode):
                    if conditiontype.optoken.matches(TT_KEYWORD, KEYWORDS['logicalnot']):
                        message = f'{conditiontype.node} inverted is not True'


            return(
                res.failure(
                    Exc_AssertionError(
                        f'{message}',
                        condition.start, condition.end,
                        exec_context,
                        #condition.originstart, condition.originend, condition.origindisplay
                    )
                )
            )
    exec_assert.argnames = {'condition': TYPES['boolean']}
    exec_assert.optnames = {'msg': StringType('')}


    def exec_panic(self, exec_context):
        res = _RTResult()

        message = exec_context.symbols.access('message')[0]

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
    exec_panic.argnames = {'message': TYPES['string']}
    exec_panic.optnames = {}


    def exec_print(self, exec_context):
        res = _RTResult()

        message = exec_context.symbols.access('message')[0]
        prefix = exec_context.symbols.access('prefix')
        suffix = exec_context.symbols.access('suffix')

        print(f'{prefix.__clean__()}{message.__clean__()}{suffix.__clean__()}', end='')

        return(
            _RTResult().success(
                NullType()
            )
        )
    exec_print.argnames = {'message': TYPES['string']}
    exec_print.optnames = {'prefix': StringType(''), 'suffix': StringType('\n')}


    def exec_range(self, exec_context):
        res = _RTResult()

        stop = exec_context.symbols.access('stop')[0]
        start = exec_context.symbols.access('start')
        step = exec_context.symbols.access('step')

        returnlist = []

        i = start.value

        while i < stop.value:
            returnlist.append(
                IntType(i)
            )

            i += step.value



        return(
            _RTResult().success(
                ArrayType(returnlist)
            )
        )
    exec_range.argnames = {'stop': TYPES['integer']}
    exec_range.optnames = {'start': IntType(0), 'step': IntType(1)}


    def exec_type(self, exec_context):
        res = _RTResult()

        value = exec_context.symbols.access('obj')[0]
        result, error = value.totype()

        if error:
            return(
                _RTResult().failure(
                    error
                )
            )

        return(
            _RTResult().success(
                result
            )
        )
    exec_type.argnames = {'obj': NullType}
    exec_type.optnames = {}


    def exec_str(self, exec_context):
        res = _RTResult()

        value = exec_context.symbols.access('obj')[0]
        result, error = value.tostr()

        if error:
            return(
                _RTResult().failure(
                    error
                )
            )

        return(
            _RTResult().success(
                result
            )
        )
    exec_str.argnames = {'obj': NullType}
    exec_str.optnames = {}


    def exec_int(self, exec_context):
        res = _RTResult()

        value = exec_context.symbols.access('obj')[0]
        result, error = value.toint()

        if error:
            return(
                _RTResult().failure(
                    error
                )
            )

        return(
            _RTResult().success(
                result
            )
        )
    exec_int.argnames = {'obj': NullType}
    exec_int.optnames = {}


    def exec_float(self, exec_context):
        res = _RTResult()

        value = exec_context.symbols.access('obj')[0]
        result, error = value.tofloat()

        if error:
            return(
                _RTResult().failure(
                    error
                )
            )

        return(
            _RTResult().success(
                result
            )
        )
    exec_float.argnames = {'obj': NullType}
    exec_float.optnames = {}


    def exec_bool(self, exec_context):
        res = _RTResult()

        value = exec_context.symbols.access('obj')[0]
        result, error = value.tobool()

        if error:
            return(
                _RTResult().failure(
                    error
                )
            )

        return(
            _RTResult().success(
                result
            )
        )
    exec_bool.argnames = {'obj': NullType}
    exec_bool.optnames = {}


    def exec_array(self, exec_context):
        res = _RTResult()

        value = exec_context.symbols.access('obj')[0]
        result, error = value.toarray()

        if error:
            return(
                _RTResult().failure(
                    error
                )
            )

        return(
            _RTResult().success(
                result
            )
        )
    exec_array.argnames = {'obj': NullType}
    exec_array.optnames = {}


    def exec_tuple(self, exec_context):
        res = _RTResult()

        value = exec_context.symbols.access('obj')[0]
        result, error = value.totuple()

        if error:
            return(
                _RTResult().failure(
                    error
                )
            )

        return(
            _RTResult().success(
                result
            )
        )
    exec_tuple.argnames = {'obj': NullType}
    exec_tuple.optnames = {}


    def exec_id(self, exec_context):
        res = _RTResult()

        obj = exec_context.symbols.access('obj')[0]
        return(
            _RTResult().success(
                IdType(obj.id)
            )
        )
    exec_id.argnames = {'obj': NullType}
    exec_id.optnames = {}



    def exec_as_ratio(self, exec_context):
        res = _RTResult()

        fraction = _Fraction(str(
            self.editvalue.value
        ))

        return(
            _RTResult().success(
                TupleType((
                    IntType(fraction.numerator)
                        .setcontext(exec_context)
                        .setpos(self.editvalue.start, self.editvalue.end)
                        .setorigin(self.editvalue.originstart, self.editvalue.originend, self.editvalue.origindisplay),
                    IntType(fraction.denominator)
                        .setcontext(exec_context)
                        .setpos(self.editvalue.start, self.editvalue.end)
                        .setorigin(self.editvalue.originstart, self.editvalue.originend, self.editvalue.origindisplay)
                ))
                    .setcontext(exec_context)
                    .setpos(self.editvalue.start, self.editvalue.end)
                    .setorigin(self.editvalue.originstart, self.editvalue.originend, self.editvalue.origindisplay)
            )
        )



    def exec_to_lower(self, exec_context):
        res = _RTResult()

        return(
            _RTResult().success(
                StringType(
                    self.editvalue.value.casefold()
                )
                    .setcontext(exec_context)
                    .setpos(self.editvalue.start, self.editvalue.end)
                    .setorigin(self.editvalue.originstart, self.editvalue.originend, self.editvalue.origindisplay)
            )
        )

    def exec_lalign(self, exec_context):
        res = _RTResult()

        minwidth = exec_context.symbols.access('minwidth')[0]
        fillchar = exec_context.symbols.access('fillchar')

        if minwidth.value < 0:
            return(
                res.failure(
                    Exc_ValueError(
                        f'\'minwidth\' must be more than 0',
                        minwidth.start, minwidth.end,
                        exec_context,
                        minwidth.originstart, minwidth.originend, minwidth.origindisplay
                    )
                )
            )

        if len(fillchar.value) != 1:
            return(
                res.failure(
                    Exc_ValueError(
                        f'\'fillchar\' must be of length 1',
                        fillchar.start, fillchar.end,
                        exec_context,
                        fillchar.originstart, fillchar.originend, fillchar.origindisplay
                    )
                )
            )

        return(
            _RTResult().success(
                StringType(
                    self.editvalue.value.ljust(
                        minwidth.value, fillchar.value
                    )
                )
                    .setcontext(exec_context)
                    .setpos(self.editvalue.start, self.editvalue.end)
                    .setorigin(self.editvalue.originstart, self.editvalue.originend, self.editvalue.origindisplay)
            )
        )
    exec_lalign.argnames = {'minwidth': TYPES['integer']}
    exec_lalign.optnames = {'fillchar': StringType(' ')}

    def exec_calign(self, exec_context):
        res = _RTResult()

        minwidth = exec_context.symbols.access('minwidth')[0]
        fillchar = exec_context.symbols.access('fillchar')

        if minwidth.value < 0:
            return(
                res.failure(
                    Exc_ValueError(
                        f'\'minwidth\' must be more than 0',
                        minwidth.start, minwidth.end,
                        exec_context,
                        minwidth.originstart, minwidth.originend, minwidth.origindisplay
                    )
                )
            )

        if len(fillchar.value) != 1:
            return(
                res.failure(
                    Exc_ValueError(
                        f'\'fillchar\' must be of length 1',
                        fillchar.start, fillchar.end,
                        exec_context,
                        fillchar.originstart, fillchar.originend, fillchar.origindisplay
                    )
                )
            )

        return(
            _RTResult().success(
                StringType(
                    self.editvalue.value.center(
                        minwidth.value, fillchar.value
                    )
                )
                    .setcontext(exec_context)
                    .setpos(self.editvalue.start, self.editvalue.end)
                    .setorigin(self.editvalue.originstart, self.editvalue.originend, self.editvalue.origindisplay)
            )
        )
    exec_calign.argnames = {'minwidth': TYPES['integer']}
    exec_calign.optnames = {'fillchar': StringType(' ')}

    def exec_ralign(self, exec_context):
        res = _RTResult()

        minwidth = exec_context.symbols.access('minwidth')[0]
        fillchar = exec_context.symbols.access('fillchar')

        if minwidth.value < 0:
            return(
                res.failure(
                    Exc_ValueError(
                        f'\'minwidth\' must be more than 0',
                        minwidth.start, minwidth.end,
                        exec_context,
                        minwidth.originstart, minwidth.originend, minwidth.origindisplay
                    )
                )
            )

        if len(fillchar.value) != 1:
            return(
                res.failure(
                    Exc_ValueError(
                        f'\'fillchar\' must be of length 1',
                        fillchar.start, fillchar.end,
                        exec_context,
                        fillchar.originstart, fillchar.originend, fillchar.origindisplay
                    )
                )
            )

        return(
            _RTResult().success(
                StringType(
                    self.editvalue.value.rjust(
                        minwidth.value, fillchar.value
                    )
                )
                    .setcontext(exec_context)
                    .setpos(self.editvalue.start, self.editvalue.end)
                    .setorigin(self.editvalue.originstart, self.editvalue.originend, self.editvalue.origindisplay)
            )
        )
    exec_ralign.argnames = {'minwidth': TYPES['integer']}
    exec_ralign.optnames = {'fillchar': StringType(' ')}

    def exec_repeat(self, exec_context):
        res = _RTResult()

        count = exec_context.symbols.access('count')[0]
        if count.value < 0:
            return(
                res.failure(
                    Exc_ValueError(
                        f'\'count\' must be greater than or equal to 0',
                        count.start, count.end,
                        exec_context,
                        count.originstart, count.originend, count.origindisplay
                    )
                )
            )
        return(
            _RTResult().success(
                StringType(self.editvalue.value * count.value)
            )
        )
    exec_repeat.argnames = {'count': TYPES['integer']}
    exec_repeat.optnames = {}


    def exec_split(self, exec_context):
        res = _RTResult()

        separator = exec_context.symbols.access('separator')[0]
        if len(separator.value) <= 0:
            return(
                _RTResult().success(
                    ArrayType(list(self.editvalue.value))
                        .setpos(self.start, self.end)
                        .setcontext(exec_context)
                )
            )
        else:
            return(
                _RTResult().success(
                    ArrayType([StringType(i) for i in self.editvalue.value.split(separator.value)])
                )
            )
    exec_split.argnames = {'separator': TYPES['string']}
    exec_split.optnames = {}


    def exec_startswith(self, exec_context):
        res = _RTResult()

        text = exec_context.symbols.access('text')[0]
        if len(text.value) <= 0:
            return(
                res.failure(
                    Exc_ValueError(
                        f'\'text\' must be at least 1 character in length',
                        text.start, text.end,
                        exec_context,
                        text.originstart, text.originend, text.origindisplay
                    )
                )
            )
        else:
            return(
                _RTResult().success(
                    BooleanType(self.editvalue.value.startswith(text.value))
                        .setpos(self.start, self.end)
                        .setcontext(exec_context)
                )
            )
    exec_startswith.argnames = {'text': TYPES['string']}
    exec_startswith.optnames = {}


    def exec_endswith(self, exec_context):
        res = _RTResult()

        text = exec_context.symbols.access('text')[0]
        if len(text.value) <= 0:
            return(
                res.failure(
                    Exc_ValueError(
                        f'\'text\' must be at least 1 character in length',
                        text.start, text.end,
                        exec_context,
                        text.originstart, text.originend, text.origindisplay
                    )
                )
            )
        else:
            return(
                _RTResult().success(
                    BooleanType(self.editvalue.value.endswith(text.value))
                        .setpos(self.start, self.end)
                        .setcontext(exec_context)
                )
            )
    exec_endswith.argnames = {'text': TYPES['string']}
    exec_endswith.optnames = {}


    def exec_join(self, exec_context):
        res = _RTResult()

        combiner = exec_context.symbols.access('combiner')[0]
        if not all(i.type == TYPES['string'] for i in self.editvalue.value):
            return(
                res.failure(
                    Exc_ValueError(
                        f'All objects in \'combiner\' must be of type {TYPES["string"]}',
                        combiner.start, combiner.end,
                        exec_context,
                        combiner.originstart, combiner.originend, combiner.origindisplay
                    )
                )
            )
        return(
            _RTResult().success(
                StringType(combiner.value.join(i.value for i in self.editvalue.value))
            )
        )
    exec_join.argnames = {'combiner': TYPES['string']}
    exec_join.optnames = {}


    def exec_replace(self, exec_context):
        res = _RTResult()

        separator = exec_context.symbols.access('separator')[0]
        combiner = exec_context.symbols.access('combiner')[0]
        return(
            _RTResult().success(
                StringType(self.editvalue.value.replace(separator.value, combiner.value))
            )
        )
    exec_replace.argnames = {'separator': TYPES['string'], 'combiner': TYPES['string']}
    exec_replace.optnames = {}


    def exec_slice(self, exec_context):
        res = _RTResult()

        start = exec_context.symbols.access('start')[0]
        stop = exec_context.symbols.access('stop')[0]
        step = exec_context.symbols.access('step')[0]

        if not isinstance(start, IntType) and not isinstance(start, NullType):
            return(
                res.failure(
                    Exc_TypeError(
                        f'\'start\' must be of type {TYPES["integer"]} or {TYPES["nonetype"]}',
                        start.start, start.end,
                        exec_context,
                        start.originstart, start.originend, start.origindisplay
                    )
                )
            )

        if not isinstance(stop, IntType) and not isinstance(stop, NullType):
            return(
                res.failure(
                    Exc_TypeError(
                        f'\'stop\' must be of type {TYPES["integer"]} or {TYPES["nonetype"]}',
                        stop.start, stop.end,
                        exec_context,
                        stop.originstart, stop.originend, stop.origindisplay
                    )
                )
            )

        if not isinstance(step, IntType) and not isinstance(step, NullType):
            return(
                res.failure(
                    Exc_TypeError(
                        f'\'step\' must be of type {TYPES["integer"]} or {TYPES["nonetype"]}',
                        step.start, step.end,
                        exec_context,
                        step.originstart, step.originend, step.origindisplay
                    )
                )
            )

        if step.value == 0:
            return(
                res.failure(
                    Exc_ValueError(
                        f'\'step\' must not be equal to 0',
                        step.start, step.end,
                        exec_context,
                        step.originstart, step.originend, step.origindisplay
                    )
                )
            )

        return(
            _RTResult().success(
                type(self.editvalue)(self.editvalue.value[start.value:stop.value:step.value])
            )
        )
    exec_slice.argnames = {'start': NullType, 'stop': NullType, 'step': NullType}
    exec_slice.optnames = {}
BuiltInFunctionType.type = TYPES['builtinfunc']
BuiltInFunctionType.modules = {}


class ExceptionType(TypeObj):
    def __init__(self, exc, msg, start, end, context):
        super().__init__(type_=TYPES['exception'])
        self.exc = exc
        self.msg = msg
        self.exc_start = start
        self.file = self.exc_start.file
        self.exc_context = context
        self.loc = context.display
        if isinstance(self.loc, tuple):
            self.loc = self.loc[0]
        self.line = self.exc_start.line
        self.column = self.exc_start.column
        self.exc_end = end
        lines = self.exc_start.ftext.split('\n')
        self.text = ' '.join(lines[self.line::-(len(lines) - self.exc_end.column)])

    def eqequals(self: _Any, other: _Any) -> _Tuple[BooleanType, None]:
        if type(self) == type(other):
            return((
                BooleanType(
                    self.exc == other.exc and self.msg == other.msg and self.exc_start == other.exc_start and self.line == other.line and self.column == other.column
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

    def attribute(self, attribute):
        if attribute.value == 'name':
            f = StringType(self.exc).setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        elif attribute.value == 'msg':
            f = StringType(self.msg).setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        elif attribute.value == 'file':
            f = StringType(self.file).setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        elif attribute.value == 'loc':
            f = StringType(self.loc).setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        elif attribute.value == 'line':
            f = IntType(self.line + 1).setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        elif attribute.value == 'column':
            f = IntType(self.column + 1).setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        elif attribute.value == 'text':
            f = StringType(self.text).setcontext(self.context).setpos(attribute.start, attribute.end)
            f.editvalue = self.copy()
            return((
                f,
                None
            ))
        else:
            return((None, Exc_AttributeError(f'\'{self.name}\' has no attribute \'{attribute.value}\'', attribute.start, attribute.end, self.context, self.originstart, self.originend, self.origindisplay)))

    def copy(self):
        copy = ExceptionType(self.exc, self.msg, self.exc_start, self.exc_end, self.exc_context)
        copy.id = self.id
        copy.setcontext(self.context)
        copy.setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)

        return(copy)

    def tostr(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def totuple(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            TupleType((
                StringType(self.exc)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                StringType(self.msg)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                IntType(self.line + 1)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
                IntType(self.column + 1)
                    .setpos(self.start, self.end)
                    .setcontext(self.context),
            ))
        ), None)

    def __repr__(self):
        return(f'<{self.exc}:{self.msg}, {self.line + 1}:{self.column + 1}>')
ExceptionType.type = TYPES['exception']


class IdType(TypeObj):
    def __init__(self, value):
        super().__init__(value, type_=TYPES['id'])

    def eqequals(self: _Any, other: _Any) -> _Tuple[BooleanType, None]:
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

    def totype(self) -> _Tuple[_Any, _Optional[Exc_TypeError]]:
        return((
            BuiltInFunctionType('id', type_=TYPES['type'], returntype=TYPES['id'])
                .setcontext(self.context)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay),
            None
        ))

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
IdType.type = TYPES['id']


class NamespaceType(TypeObj):
    def __init__(self, symbols):
        self.symbols = symbols
        super().__init__(type_=TYPES['namespace'])

    def eqequals(self: _Any, other: _Any) -> _Tuple[BooleanType, None]:
        equals = True
        if type(self) == type(other):
            selfkeys = list(self.symbols.symbols.keys())
            otherkeys = list(other.symbols.symbols.keys())
            if len(selfkeys) == len(otherkeys):
                for i in range(len(selfkeys)):
                    if selfkeys[i] != otherkeys[i]:
                        equals = False
                        break
                    if not self.symbols.symbols[selfkeys[i]].eqequals(other.symbols.symbols[otherkeys[i]])[0].value:
                        equals = False
                        break
            else:
                equals = False
        else:
            equals = False
        return((
            BooleanType(equals)
                .setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)
                .setcontext(self.context),
            None
        ))

    def tostr(self):
        return((
            StringType(self.__clean__())
                .setcontext(self.context)
                .setpos(self.start, self.end),
            None
        ))

    def attribute(self, attribute):
        value = self.symbols.access(attribute.value)

        if value:
            return((
                value,
                None
            ))

        else:
            return((
                None,
                Exc_AttributeError(
                    f'\'{self.name}\' has no attribute \'{attribute.value}\'',
                    attribute.start, attribute.end,
                    self.context
                )
            ))

    def copy(self):
        copy = NamespaceType(self.symbols)
        copy.id = self.id
        copy.setcontext(self.context)
        self.setpos(self.start, self.end, self.originstart, self.originend, self.origindisplay)

        return(copy)

    def __repr__(self):
        return(f'<Namespace: {len(list(self.symbols.symbols.keys()))} objects>')
NamespaceType.type = TYPES['namespace']
