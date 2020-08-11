##########################################
# CONSTANTS                              #
##########################################

import string

DIGITS = '1234567890'
ALPHABET = string.ascii_letters
ALPHANUMERIC = ALPHABET + DIGITS

KEYWORDS = {
    'bool-true':  'True',
    'bool-false': 'False'
}

TYPES = {
    'invalid'      : 'Invalid',
    'integer'      : 'Int',
    'floatingpoint': 'Float',
    'string'       : 'Str',
    'boolean'      : 'Bool'
}