import pytest
from peridot.version.types import IntType,FloatType,BooleanType,NullType
from peridot.version.exceptions import *


class TestPeridotInt:
    def test_int(self):
        a = IntType(4)
        assert(isinstance(a, IntType))
        assert(a.value == 4)
        assert(a.type == "Int")

    def test_not_int(self):
        with pytest.raises(TypeError):
            a = IntType(4.2)
        with pytest.raises(TypeError):
            a = IntType("String")

    def test_int_add(self):
        a = IntType(4)
        b = IntType(2)
        c,err = a.add(b)
        assert(c.value == 6)
        assert(err == None)

    def test_int_subtract(self):
        a = IntType(100)
        b = IntType(42)
        c,err = a.subtract(b)
        assert(c.value == 58)
        assert(err == None)

    def test_int_multiply(self):
        a = IntType(10)
        b = IntType(42)
        c,err = a.multiply(b)
        assert(c.value == 420)
        assert(err == None)

    def test_int_divide(self):
        a = IntType(42)
        b = IntType(10)
        c,err = a.divide(b)
        assert(c.value == 4)
        assert(err == None)

    def test_int_raised(self):
        a = IntType(2)
        b = IntType(3)
        c, err = a.raised(b)
        assert(c.value == 8)
        assert(err == None)

    def test_int_raised(self):
        a = IntType(2)
        b = IntType(3)
        c, err = a.raised(b)
        assert(c.value == 8)
        assert(err == None)

    def test_int_lessthan(self):
        a = IntType(2)
        b = IntType(3)
        c, err = a.lessthan(b)
        d, err = b.lessthan(a)
        assert(isinstance(c, BooleanType))
        assert(isinstance(d, BooleanType))
        assert(c.value == True)
        assert(d.value == False)

    def test_int_ltequals(self):
        a = IntType(2)
        b = IntType(3)
        c = IntType(3)
        d, err = a.ltequals(b)
        e, err = b.ltequals(a)
        f, err = b.ltequals(c)
        assert(isinstance(d, BooleanType))
        assert(isinstance(e, BooleanType))
        assert(isinstance(f, BooleanType))
        assert(d.value == True)
        assert(e.value == False)
        assert(f.value == True)

    def test_int_greaterthan(self):
        a = IntType(2)
        b = IntType(3)
        c, err = a.greaterthan(b)
        d, err = b.greaterthan(a)
        assert(isinstance(c, BooleanType))
        assert(isinstance(d, BooleanType))
        assert(c.value == False)
        assert(d.value == True)

    def test_int_gtequals(self):
        a = IntType(2)
        b = IntType(3)
        c = IntType(3)
        d, err = a.gtequals(b)
        e, err = b.gtequals(a)
        f, err = b.gtequals(c)
        assert(isinstance(d, BooleanType))
        assert(isinstance(e, BooleanType))
        assert(isinstance(f, BooleanType))
        assert(d.value == False)
        assert(e.value == True)
        assert(f.value == True)

    def test_int_equals(self):
        a = IntType(2)
        b = IntType(3)
        c = IntType(3)
        d, err = a.equals(b)
        e, err = b.equals(a)
        f, err = b.equals(c)
        assert(isinstance(d, BooleanType))
        assert(isinstance(e, BooleanType))
        assert(isinstance(f, BooleanType))
        assert(d.value == False)
        assert(e.value == False)
        assert(f.value == True)

class TestPeridotFloat:
    def test_float(test):
        a = FloatType(4.2)
        assert(isinstance(a, FloatType))
        assert(a.value == 4.2)
        assert(a.type == "Float")

    def test_not_float(self):
        with pytest.raises(TypeError):
            a = FloatType(4)
        with pytest.raises(TypeError):
            a = FloatType("String")

    def test_float_add(self):
        a = FloatType(4.7)
        b = FloatType(2.3)
        c,err = a.add(b)
        assert(c.value == 7.0)
        assert(err == None)

    def test_float_subtract(self):
        a = FloatType(30.6)
        b = FloatType(2.0)
        c,err = a.subtract(b)
        assert(c.value == 28.6)
        assert(err == None)

    def test_float_multiply(self):
        a = FloatType(2.2)
        b = FloatType(3.4)
        c,err = a.multiply(b)
        assert(c.value == 7.48)
        assert(err == None)

    def test_float_divide(self):
        a = FloatType(30.6)
        b = FloatType(2.0)
        c,err = a.divide(b)
        assert(c.value == 15.3)
        assert(err == None)
    
    def test_float_raised(self):
        a = FloatType(2.1)
        b = FloatType(3.0)
        c, err = a.raised(b)
        assert(c.value == 9.261)
        assert(err == None)

    def test_float_lessthan(self):
        a = FloatType(2.1)
        b = FloatType(3.0)
        c, err = a.lessthan(b)
        d, err = b.lessthan(a)
        assert(isinstance(c, BooleanType))
        assert(isinstance(d, BooleanType))
        assert(c.value == True)
        assert(d.value == False)

    def test_float_ltequals(self):
        a = FloatType(2.1)
        b = FloatType(3.4)
        c = FloatType(3.4)
        d, err = a.ltequals(b)
        e, err = b.ltequals(a)
        f, err = b.ltequals(c)
        assert(isinstance(d, BooleanType))
        assert(isinstance(e, BooleanType))
        assert(isinstance(f, BooleanType))
        assert(d.value == True)
        assert(e.value == False)
        assert(f.value == True)

    def test_float_greaterthan(self):
        a = FloatType(2.1)
        b = FloatType(3.4)
        c, err = a.greaterthan(b)
        d, err = b.greaterthan(a)
        assert(isinstance(c, BooleanType))
        assert(isinstance(d, BooleanType))
        assert(c.value == False)
        assert(d.value == True)

    def test_float_gtequals(self):
        a = FloatType(2.1)
        b = FloatType(3.4)
        c = FloatType(3.4)
        d, err = a.gtequals(b)
        e, err = b.gtequals(a)
        f, err = b.gtequals(c)
        assert(isinstance(d, BooleanType))
        assert(isinstance(e, BooleanType))
        assert(isinstance(f, BooleanType))
        assert(d.value == False)
        assert(e.value == True)
        assert(f.value == True)

    def test_float_equals(self):
        a = FloatType(2.1)
        b = FloatType(3.4)
        c = FloatType(3.4)
        d, err = a.equals(b)
        e, err = b.equals(a)
        f, err = b.equals(c)
        assert(isinstance(d, BooleanType))
        assert(isinstance(e, BooleanType))
        assert(isinstance(f, BooleanType))
        assert(d.value == False)
        assert(e.value == False)
        assert(f.value == True)

class TestPeridotCrossTypes:
    def test_int_add_float(self):
        a = IntType(4)
        b = FloatType(2.3)
        c,err = a.add(b)
        assert(c == None)
        assert(isinstance(err, Exc_TypeError))

    def test_int_mult_float(self):
        a = IntType(4)
        b = FloatType(2.3)
        c, err = a.multiply(b)
        assert(c == None)
        assert(isinstance(err, Exc_TypeError))

    def test_float_mult_int(self):
        b = IntType(4)
        a = FloatType(2.3)
        c, err = a.multiply(b)
        assert(c == None)
        assert(isinstance(err, Exc_TypeError))

    def test_float_lessthan_int(self):
        a = IntType(2)
        b = FloatType(3.0)
        c, err = b.lessthan(a)
        assert(c == None)
        assert(isinstance(err, Exc_TypeError))

    def test_int_lessthan_float(self):
        a = IntType(2)
        b = FloatType(3.0)
        c, err = a.lessthan(b)
        assert(c == None)
        assert(isinstance(err, Exc_TypeError))

    def test_int_equals_float(self):
        a = IntType(2)
        b = FloatType(2.0)
        c, err = a.equals(b)
        assert(c == None)
        assert(isinstance(err, Exc_TypeError))

    def test_int_equals_float(self):
        a = IntType(2.0)
        b = FloatType(2)
        c, err = a.equals(b)
        assert(c == None)
        assert(isinstance(err, Exc_TypeError))