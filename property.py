from grammar_utils import is_ucletter



class Property:
    def __init__(self, identifier, values=None):
        if not is_ucletter(identifier):
            raise SyntaxError(f"'{identifier}' is not uppercase")

        self.identifier = identifier

        if values is None:
            values = []

        self.values = values

    def __str__(self):
        return self.identifier

    def add_value(self, value):
        self.values.append(value)
