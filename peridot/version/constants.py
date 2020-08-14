##########################################
# DEPENDENCIES                           #
##########################################

import string
from   .types import NullType, BooleanType # type: ignore

##########################################
# CONSTANTS                              #
##########################################

DIGITS = '1234567890'
ALPHABET = string.ascii_letters
ALPHANUMERIC = ALPHABET + DIGITS

BUILTINS = {
    'Null'      : NullType(),
    'True'      : BooleanType(True),
    'False'     : BooleanType(False),
}

BUILTINFUNCS = {
}

KEYWORDS = {
    'varcreate' : 'var',
    'createfunc': 'func',
    'logicaland': 'and',
    'logicalor' : 'or',
    'logicalnot': 'not'
}