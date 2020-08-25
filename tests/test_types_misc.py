import pytest
from peridot.version.types import NullType,IntType, StringType,ArrayType
from peridot.version.catch import InternalPeridotError


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

    def test_not_string(self):
        with pytest.raises(InternalPeridotError):
            a = StringType(5)

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
        i = IntType(1)
        j = IntType(2)
        k = IntType(3)
        a = ArrayType([i, j, k])
        assert(isinstance(a.value, list))
        print(a.value)
        assert(a.value == [i, j, k])
        assert(a.type == "Array")

    def test_array_type(self):
        with pytest.raises(InternalPeridotError):
            a = ArrayType([1, StringType("two"), IntType(3)])

    def test_array_copy(self):
        a = ArrayType([IntType(1), IntType(2), IntType(3)])
        b = a.copy()
        assert(a.id == b.id)
        assert(a.value == b.value)

    def test_array_tostr(self):
        a = ArrayType([IntType(1), IntType(2), IntType(3)])
        b = a.tostr()
        assert(isinstance(b, tuple))
        assert(isinstance(b[0], StringType))
        assert(b[1] is None)
        assert(b[0].value == "[1, 2, 3]")

    def test_array_repr(self):
        a = ArrayType([IntType(1), IntType(2), IntType(3)])
        b = a.__repr__()
        assert(isinstance(b, str))
        assert(b == "[1, 2, 3]")

