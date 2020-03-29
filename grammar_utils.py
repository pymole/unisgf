import string


uc_letters = set(string.ascii_uppercase)


def is_whitespace(char):
    return char in (' ', '\n', '\t')


def is_ucletter(letters):
    return all(letter in uc_letters for letter in letters)