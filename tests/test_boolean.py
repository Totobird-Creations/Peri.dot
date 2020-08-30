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
import peridot.version.run                as run
import peridot.version.tokens             as tokens
import peridot.version.types              as types
import perimod

default._defaultinit(MODULEVERSION, str(Path(__file__).parent), types, context)
exceptions._exceptionsinit(lang)
interpreter._interpreterinit(lang, tokens, context, default, constants, types, exceptions, run, perimod)
lexer._lexerinit(lang, constants, tokens, exceptions)
parser._parserinit(lang, tokens, exceptions, constants, nodes)
perimod._perimodinit(catch, types, interpreter, exceptions)
run._runinit(lexer, parser, context, interpreter)
types._typesinit(catch, exceptions, context, constants, tokens, nodes, interpreter)

InternalPeridotError = catch.InternalPeridotError

BooleanType          = types.BooleanType

class TestPeridotBoolean:
    def test_bool(self):
        a = BooleanType(True)
        assert(isinstance(a, BooleanType))
        assert(a.value == True)
        assert(a.type == "Bool")

    def test_not_bool(self):
        with pytest.raises(InternalPeridotError):
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
