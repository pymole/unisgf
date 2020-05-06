from unisgf.grammar_utils import (
    is_ucletters, is_digit, is_simple_text,
    is_none, is_number, is_real,
    is_double, is_color, is_text,
    whitespaces, linebreakers,
    delete_escapes
)


class PropertyValue:
    def __init__(self, value):
        value = value.__str__()
        self.__value = self.validate(value)

    def __str__(self):
        return self.render()

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, v):
        self.__value = self.validate(v)

    def validate(self, data: str):
        return data

    def render(self) -> str:
        return self.__value.__str__()


class UCLetter(PropertyValue):
    def validate(self, data: str):
        if len(data) != 1 or not is_ucletters(data):
            raise ValueError

        return data


class Digit(PropertyValue):
    def validate(self, data: str):
        if not is_digit(data):
            raise ValueError

        return int(data)


class NoneValue(PropertyValue):
    def validate(self, data: str):
        if is_none(data):
            return None

        raise ValueError


class Number(PropertyValue):
    def validate(self, data: str):
        if not is_number(data):
            raise ValueError

        return int(data)


class Real(PropertyValue):
    def validate(self, data: str):
        if not is_real(data):
            raise ValueError

        return float(data)


class Double(PropertyValue):
    def validate(self, data: str):
        if not is_double(data):
            raise ValueError

        return data


class Color(PropertyValue):
    def validate(self, data: str):
        if not is_color(data):
            raise ValueError

        return data


class Text(PropertyValue):
    def validate(self, data: str):
        if not is_text(data):
            raise ValueError

        # replace all whitespace other then linebreakers with space
        data = ''.join(char if char not in (whitespaces - linebreakers) else ' ' for char in data)

        # save initial data with escape symbols to proper rendering
        self.__value_with_escape_symbols = data

        data = delete_escapes(data)
        return data

    def render(self):
        return self.__value_with_escape_symbols


class SimpleText(PropertyValue):
    def validate(self, data: str):
        if not is_simple_text(data):
            raise ValueError

        # replaces all whitespace with single space
        data = ''.join(char if char not in whitespaces else ' ' for char in data)

        # save initial data with escape symbols to proper rendering
        self.__value_with_escape_symbols = data

        data = delete_escapes(data)
        return data

    def render(self):
        return self.__value_with_escape_symbols


validation_order = [
    Color, UCLetter, Digit, NoneValue,
    Number, Real, Double, SimpleText, Text
]


def validate_property_value(s: str) -> PropertyValue:
    for value_class in validation_order:
        try:
            return value_class(s)
        except ValueError:
            pass

    raise ValueError


print(type(validate_property_value('W')))