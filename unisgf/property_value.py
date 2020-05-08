from unisgf.grammar_utils import (
    is_ucletters, is_digit, is_simple_text,
    is_none, is_number, is_real,
    is_double, is_color, is_text,
    whitespaces, linebreakers,
    delete_escapes
)

# TODO Think how to do without static methods
class PropertyValue:
    def __init__(self, value):
        self.value = type(self).validate_value(value)

    def __str__(self):
        return self.render()

    @classmethod
    def from_string(cls, data: str):
        return cls(cls.validate_string(data))

    def get(self):
        return self.value

    def set(self, value, validate_str=True):
        if validate_str:
            value = type(self).validate_string(value)

        self.value = value

    @staticmethod
    def validate_string(data: str):
        return data

    @staticmethod
    def validate_value(value):
        return value

    def render(self) -> str:
        return self.value.__str__()


class UCLetter(PropertyValue):
    @staticmethod
    def validate_string(data: str):
        if not isinstance(data, str) or len(data) != 1 or not is_ucletters(data):
            raise ValueError

        return data

    @staticmethod
    def validate_value(value):
        # same as from_string()
        UCLetter.validate_string(value)


class Digit(PropertyValue):
    @staticmethod
    def validate_string(data: str):
        if not is_digit(data):
            raise ValueError

        return int(data)

    @staticmethod
    def validate_value(value):
        if isinstance(value, int) and 0 <= value <= 9:
            return value

        raise ValueError


class NoneValue(PropertyValue):
    @staticmethod
    def validate_string(data: str):
        if is_none(data):
            return None

        raise ValueError

    @staticmethod
    def validate_value(value):
        if value is None:
            return value

        raise ValueError


class Number(PropertyValue):
    @staticmethod
    def validate_string(data: str):
        if not is_number(data):
            raise ValueError

        return int(data)

    @staticmethod
    def validate_value(value):
        if isinstance(value, int):
            return value

        raise ValueError


class Real(PropertyValue):
    @staticmethod
    def validate_string(data: str):
        if not is_real(data):
            raise ValueError

        return float(data)

    @staticmethod
    def validate_value(value):
        if isinstance(value, float):
            return value

        raise ValueError


class Double(PropertyValue):
    @staticmethod
    def validate_string(data: str):
        if not is_double(data):
            raise ValueError

        return float(data)

    @staticmethod
    def validate_value(value):
        if isinstance(value, float):
            return value

        raise ValueError


class Color(PropertyValue):
    @staticmethod
    def validate_string(data: str):
        if not is_color(data):
            raise ValueError

        return float(data)

    @staticmethod
    def validate_value(value):
        return Color.validate_string(value)


class Text(PropertyValue):
    def __init__(self, value):
        self.value, self.value_with_escapes = Text.validate_value(value)

    @classmethod
    def from_string(cls, data: str):
        return cls(data)

    @staticmethod
    def validate_string(data: str):
        if not is_text(data):
            raise ValueError

        # replace all whitespace other then linebreakers with space
        data = ''.join(char if char not in (whitespaces - linebreakers) else ' ' for char in data)

        # save initial data with escape symbols to proper rendering
        data_with_deleted_escapes = delete_escapes(data)

        return data_with_deleted_escapes, data

    @staticmethod
    def validate_value(value):
        return Text.validate_string(value)

    def render(self):
        return self.value_with_escapes


class SimpleText(PropertyValue):
    def __init__(self, value):
        self.value, self.value_with_escapes = SimpleText.validate_value(value)

    @classmethod
    def from_string(cls, data: str):
        return cls(data)

    @staticmethod
    def validate_string(data: str):
        if not is_simple_text(data):
            raise ValueError

        # replaces all whitespace with single space
        data = ''.join(char if char not in whitespaces else ' ' for char in data)

        # save initial data with escape symbols to proper rendering
        data_with_deleted_escapes = delete_escapes(data)

        return data_with_deleted_escapes, data

    @staticmethod
    def validate_value(value):
        return SimpleText.validate_string(value)

    def render(self):
        return self.value_with_escapes


validation_order = [
    Color, UCLetter, Digit, NoneValue,
    Number, Real, Double, SimpleText, Text
]


def validate_property_value_from_string(s: str) -> PropertyValue:
    if not isinstance(s, str):
        raise ValueError

    for value_class in validation_order:
        try:
            return value_class.from_string(s)
        except ValueError:
            pass

    raise ValueError


def validate_property_value(value) -> PropertyValue:
    for value_class in validation_order:
        try:
            return value_class(value)
        except ValueError:
            pass

    raise ValueError