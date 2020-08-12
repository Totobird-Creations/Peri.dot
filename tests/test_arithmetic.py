import pytest
from peridot.version.types import IntType,FloatType,NullType
from peridot.version.exceptions import *
#import importlib.util
#import sys
#import os

#spec = importlib.util.spec_from_file_location("pdTypes", "peri.dot/version/types.py")
#module = importlib.util.module_from_spec(spec)
#sys.modules["pdTypes"] = module
#spec.loader.exec_module(module)


class TestPeridotInt:
    def test_totobird_int(self):
        a = IntType(4)
        assert(isinstance(a, IntType))
        assert(a.value == 4)

    def test_totobird_not_int(self):
        with pytest.raises(TypeError):
            a = IntType(4.2)
        with pytest.raises(TypeError):
            a = IntType("String")

    def test_totobird_int_add(self):
        a = IntType(4)
        b = IntType(2)
        c,err = a.add(b)
        assert(c.value == 6)
        assert(err == None)

    def test_totobird_int_subtract(self):
        a = IntType(100)
        b = IntType(42)
        c,err = a.subtract(b)
        assert(c.value == 58)
        assert(err == None)

    def test_totobird_int_multiply(self):
        a = IntType(10)
        b = IntType(42)
        c,err = a.multiply(b)
        assert(c.value == 420)
        assert(err == None)

    def test_totobird_int_divide(self):
        a = IntType(42)
        b = IntType(10)
        c,err = a.divide(b)
        assert(c.value == 4)
        assert(err == None)

class TestPeridotFloat:
    def test_totobird_float(test):
        a = FloatType(4.2)
        assert(isinstance(a, FloatType))
        assert(a.value == 4.2)

    def test_totobird_not_float(self):
        with pytest.raises(TypeError):
            a = FloatType(4)
        with pytest.raises(TypeError):
            a = FloatType("String")

class TestPeridotCrossTypes:
    def test_totobird_int_add_float(test):
        a = IntType(4)
        b = FloatType(2.3)
        c,err = a.add(b)
        assert(c == None)
        assert(isinstance(err, Exc_TypeError))
