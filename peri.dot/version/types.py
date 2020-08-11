##########################################
# DEPENDENCIES                           #
##########################################

from .constants  import *
from .exceptions import *

##########################################
# TYPES                                  #
##########################################

class TypeObj():
    def __init__(self, value, type_=TYPES['invalid']):
        self.value = value
        self.type  = type_
        self.setpos()

    def setpos(self, start=None, end=None):
        self.start = start
        self.end   = end

        return(self)

    def add(self, other):
        return((None, Exc_TypeError(f'{self.type} can not be added to', self.start, self.end)))
    def subtract(self, other):
        return((None, Exc_TypeError(f'{self.type} can not be subtracted from', self.start, self.end)))
    def multiply(self, other):
        return((None, Exc_TypeError(f'{self.type} can not be multiplied', self.start, self.end)))
    def divide(self, other):
        return((None, Exc_TypeError(f'{self.type} can not be divided', self.start, self.end)))
    def raised(self, other):
        return((None, Exc_TypeError(f'{self.type} can not be raised', self.start, self.end)))

    def __repr__(self):
        return(f'<{self.type}:{self.value}>')



class IntType(TypeObj):
    def __init__(self, value):
        super().__init__(value, type_=TYPES['integer'])


    def add(self, other):
        if isinstance(other, IntType):
            return((
                IntType(self.value + other.value),
                None
            ))
        else:
            return((None, Exc_TypeError(f'{other.type} can not be added to {self.type}', other.start, other.end)))

    def subtract(self, other):
        if isinstance(other, IntType):
            return((
                IntType(self.value - other.value),
                None
            ))
        else:
            return((None, Exc_TypeError(f'{other.type} can not be subtracted from {self.type}', other.start, other.end)))

    def multiply(self, other):
        if isinstance(other, IntType):
            return((
                IntType(self.value * other.value),
                None
            ))
        else:
            return((None, Exc_TypeError(f'{self.type} can not be multiplied by {other.type}', other.start, other.end)))

    def divide(self, other):
        if isinstance(other, IntType):
            if other.value == 0:
                return((
                    None,
                    Exc_ValueError(f'Division by zero', other.start, other.end)
                ))

            return((
                IntType(int(self.value / other.value)),
                None
            ))
        else:
            return((None, Exc_TypeError(f'{self.type} can not be divided by {other.type}', other.start, other.end)))

    def raised(self, other):
        if isinstance(other, IntType):
            return((
                IntType(self.value ^ other.value),
                None
            ))
        else:
            return((None, Exc_TypeError(f'{self.type} can not be raised to {other.type}', other.start, other.end)))



class FloatType(TypeObj):
    def __init__(self, value):
        super().__init__(value, type_=TYPES['floatingpoint'])


    def add(self, other):
        if isinstance(other, FloatType):
            return((
                FloatType(self.value + other.value),
                None
            ))
        else:
            return((None, Exc_TypeError(f'{other.type} can not be added to {self.type}', other.start, other.end)))

    def subtract(self, other):
        if isinstance(other, FloatType):
            return((
                FloatType(self.value - other.value),
                None
            ))
        else:
            return((None, Exc_TypeError(f'{other.type} can not be subtracted from {self.type}', other.start, other.end)))

    def multiply(self, other):
        if isinstance(other, FloatType):
            return((
                FloatType(self.value * other.value),
                None
            ))
        else:
            return((None, Exc_TypeError(f'{self.type} can not be multiplied by {other.type}', other.start, other.end)))

    def divide(self, other):
        if isinstance(other, FloatType):
            if other.value == 0:
                return((
                    None,
                    Exc_ValueError(f'Division by zero', other.start, other.end)
                ))

            return((
                FloatType(self.value / other.value),
                None
            ))
        else:
            return((None, Exc_TypeError(f'{self.type} can not be divided by {other.type}', other.start, other.end)))

    def raised(self, other):
        if isinstance(other, FloatType):
            return((
                FloatType(self.value ^ other.value),
                None
            ))
        else:
            return((None, Exc_TypeError(f'{self.type} can not be raised to {other.type}', other.start, other.end)))
