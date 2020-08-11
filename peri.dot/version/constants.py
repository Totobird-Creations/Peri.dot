##########################################
# CONSTANTS                              #
##########################################

import string

DIGITS = '1234567890'
ALPHABET = string.ascii_letters
ALPHANUMERIC = ALPHABET + DIGITS

KEYWORDS = {
    'varcreate'    : 'var'
}

TYPES = {
    'invalid'      : 'Invalid',
    'integer'      : 'Int',
    'floatingpoint': 'Float',
    'string'       : 'Str',
    'boolean'      : 'Bool'
}

RESERVED = [
    'True',
    'False'
]