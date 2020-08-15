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
    'return'    : 'return',
    'handler'   : 'handler',
    'logicaland': 'and',
    'logicalor' : 'or',
    'logicalnot': 'not'
}

RESERVED = []