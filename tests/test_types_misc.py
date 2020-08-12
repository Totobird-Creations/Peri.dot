import pytest
from peridot.version.types import NullType,StringType
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