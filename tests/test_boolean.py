import pytest
from peridot.version.types import BooleanType,NullType
from peridot.version.exceptions import *

class TestPeridotBoolean:
    def test_bool(self):
        a = BooleanType(True)
        assert(isinstance(a, BooleanType))
        assert(a.value == True)
        assert(a.type == "Bool")

    def test_not_bool(self):
        with pytest.raises(TypeError):
            a = BooleanType(1)

    def test_bool_and(self):
        a = BooleanType(True)
        b = BooleanType(False)
        c, cErr = a.and_(b)
        d, dErr = a.and_(a)
        assert(isinstance(c, BooleanType))
        assert(isinstance(d, BooleanType))
        assert(c.value == False)
        assert(d.value == True)
        assert(cErr is None)
        assert(dErr is None)

    def test_bool_or(self):
        a = BooleanType(True)
        b = BooleanType(False)
        c, cErr = a.or_(b)
        d, dErr = a.or_(a)
        e, eErr = b.or_(b)
        assert(isinstance(c, BooleanType))
        assert(isinstance(d, BooleanType))
        assert(isinstance(e, BooleanType))
        assert(c.value == True)
        assert(d.value == True)
        assert(e.value == False)
        assert(cErr is None)
        assert(dErr is None)
        assert(eErr is None)

    def test_bool_not(self):
        a = BooleanType(True)
        b, bErr = a.not_()
        c, cErr = b.not_()
        assert(isinstance(b, BooleanType))
        assert(isinstance(c, BooleanType))
        assert(b.value == False)
        assert(c.value == True)
        assert(bErr is None)
        assert(cErr is None)
