import pytest
from peridot.version.types import NullType
from peridot.version.exceptions import *


class TestPeridotMiscTypes:
    def test_null(self):
        a = NullType()
        assert(isinstance(a, NullType))
        assert(a.value == None)
        assert(a.type == "Null")