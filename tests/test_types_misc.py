import pytest
from pathlib import Path

from peridot.__main__ import lang, MODULEVERSION
import peridot.version.catch as catch
import peridot.version.constants          as constants
import peridot.version.context            as context
import peridot.version.default            as default
import peridot.version.exceptions         as exceptions
import peridot.version.interpreter        as interpreter
import peridot.version.lexer              as lexer
import peridot.version.nodes              as nodes
import peridot.version.parser             as parser
import peridot.version.perimod            as perimod
import peridot.version.repl               as i_repl
import peridot.version.run                as run
import peridot.version.tokens             as tokens
import peridot.version.types              as types

default._defaultinit(MODULEVERSION, str(Path(__file__).parent), types, context)
exceptions._exceptionsinit(lang)
interpreter._interpreterinit(lang, tokens, context, default, constants, types, exceptions, run, perimod)
lexer._lexerinit(lang, constants, tokens, exceptions)
parser._parserinit(lang, tokens, exceptions, constants, nodes)
perimod._perimodinit(types, interpreter)
i_repl._replinit(default, context, run)
run._runinit(lexer, parser, context, interpreter)
types._typesinit(catch, exceptions, context, constants, tokens, nodes, interpreter)

InternalPeridotError = catch.InternalPeridotError

NullType             = types.NullType
StringType           = types.StringType
IntType              = types.IntType
ArrayType            = types.ArrayType


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

