##########################################
# DEPENDENCIES                           #
##########################################

import string
from   .types import *

##########################################
# CONSTANTS                              #
##########################################

DIGITS = '1234567890'
ALPHABET = string.ascii_letters
ALPHANUMERIC = ALPHABET + DIGITS

BUILTINS = {
    'Null'      : NullType(),
    'True'      : BooleanType(True),
    'False'     : BooleanType(False)
}

KEYWORDS = {
    'varcreate' : 'var',
    'logicaland': 'and',
    'logicalor' : 'or',
    'logicalnot': 'not'
}