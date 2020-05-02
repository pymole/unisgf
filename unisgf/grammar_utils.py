import string
from itertools import islice


"""
UcLetter   -> str
Digit      -> int
None       -> None

Number     -> int
Real       -> float

Double     -> str
Color      -> str

SimpleText -> str
Text       -> str

Point      -> game-specific
Move       -> game-specific
Stone      -> game-specific

Compose    -> ValueType ":" ValueType
"""


uc_letters = set(string.ascii_uppercase)
linebreakers = set('\n\r')
whitespaces = set(' \t\r\n\v')


def is_whitespace(s: str) -> bool:
    return s in whitespaces


def is_ucletters(s: str) -> bool:
    return all(char in uc_letters for char in s)


def is_digit(s: str) -> bool:
    return s.isdecimal()


def is_none(s: str) -> bool:
    return s == ''


def is_number(s: str) -> bool:
    if s[0] in '+-':
        return s[1:].isdecimal()
    else:
        return s.isdecimal()


def is_real(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_double(s: str) -> bool:
    return s == '1' or s == '2'


def is_color(s: str) -> bool:
    return s == 'B' or s == 'W'


def is_text(s: str) -> bool:
    return bool(linebreakers & set(s))


def is_simple_text(s: str) -> bool:
    return not is_text(s)


def delete_escapes(s: str) -> str:
    # get escapes and delete all
    is_escaping = False
    escape_indexes = [-1]

    for index, char in enumerate(s):
        if is_escaping:
            is_escaping = False
        elif char == '\\':
            is_escaping = True
            escape_indexes.append(index)

    escape_indexes.append(len(s))

    data = ''.join(s[i1+1:i2] for i1, i2 in zip(
        islice(escape_indexes, 0, len(escape_indexes) - 1, 1), islice(escape_indexes, 1, len(escape_indexes), 1)
    ))

    return data
