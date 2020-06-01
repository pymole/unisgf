from unisgf.grammar_utils import is_ucletters
from unisgf.property_value import (
    validate_property_value,
    validate_property_value_from_string,
    PropertyValue
)
from typing import Iterable, Any, Optional


class Property:
    def __init__(self, identifier, values: Optional[Iterable[PropertyValue]] = None):
        if not is_ucletters(identifier):
            raise SyntaxError(f"'{identifier}' is not uppercase")

        self.identifier = identifier
        self.values = []

        if values is not None:
            for value in values:
                self.add_value(value)

    def __getitem__(self, item):
        return self.values[item]

    def __contains__(self, item):
        return item in self.values

    def add_value(self, value: Any):
        if isinstance(value, str):
            value = validate_property_value_from_string(value)
        elif not isinstance(value, PropertyValue):
            value = validate_property_value(value)

        self.values.append(value)

