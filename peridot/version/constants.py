##########################################
# DEPENDENCIES                           #
##########################################

import string

##########################################
# CONSTANTS                              #
##########################################

DIGITS = '1234567890'
ALPHABET = string.ascii_letters
ALPHANUMERIC = ALPHABET + DIGITS

KEYWORDS = {
    'varcreate' : 'var',
    'funccreate': 'func',
    'logicaland': 'and',
    'logicalor' : 'or',
    'logicalnot': 'not',
    'return'    : 'return',
    'if'        : 'if',
    'elif'      : 'elif',
    'else'      : 'else',
    'handler'   : 'handler'
}

RESERVED = [
    'True',
    'False',
    'Null',
    'throw',
    'assert',
    'panic',
    'print',
    'id',
    'str',
    'int',
    'float'
]