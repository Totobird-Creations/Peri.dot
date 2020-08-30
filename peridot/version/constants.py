##########################################
# DEPENDENCIES                           #
##########################################

import string as _string

##########################################
# CONSTANTS                              #
##########################################

DIGITS = '1234567890'
ALPHABET = _string.ascii_letters
ALPHANUMERIC = ALPHABET + DIGITS

KEYWORDS = {
    'varcreate'   : 'var',
    'funccreate'  : 'func',
    'lambdacreate': 'lambda',
    'logicaland'  : 'and',
    'logicalor'   : 'or',
    'logicalnot'  : 'not',
    'return'      : 'return',
    'if'          : 'if',
    'elif'        : 'elif',
    'else'        : 'else',
    'case'        : 'switch',
    'as'          : 'as',
    'when'        : 'when',
    'forloop'     : 'for',
    'in'          : 'in',
    'whileloop'   : 'while',
    'continue'    : 'continue',
    'break'       : 'break',
    'handler'     : 'handler',
    'import'      : 'include'
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
    'float',
    'bool',
    'array',
    'tuple'
]
