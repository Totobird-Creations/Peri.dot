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
    'Null'     : NullType()
}

KEYWORDS = {
    'varcreate': 'var'
}