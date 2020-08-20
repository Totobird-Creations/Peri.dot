import pytest
from peridot.version.types import NullType,StringType,ArrayType
from peridot.version.exceptions import *


class TestPeridotMiscTypes:
    def test_null(self):
        a = NullType()
        assert(a.value == None)
        assert(a.type == "Null")

class TestPeridotString:
    def test_string(self):
        a = StringType("totobird")
        assert(isinstance(a.value, str))
        assert(a.value == "totobird")
        assert(a.type == "Str")

    def test_string_add(self):
        a = StringType("totobird")
        b = StringType(" made this")
        c,err = a.add(b)
        assert(isinstance(c.value, str))
        assert(c.value == "totobird made this")
        assert(c.type == "Str")
        assert(err is None)


class TestPeridotArray:
    def test_array(self):
        a = ArrayType([1, 2, 3])
        assert(isinstance(a.value, list))
        assert(a.value == [1, 2, 3])
        assert(a.type == "Array")

    def test_array_copy(self):
        a = ArrayType([1, 2, 3])
        b = a.copy()
        assert(a.id == b.id)
        assert(a.value == b.value)
