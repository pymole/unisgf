

class NodeAlreadyHasAProperty(Exception):
    def __init__(self, property_name):
        super().__init__('Node already has a property with name: ' + str(property_name))


class ParenthesesSyntaxError(Exception):
    def __init__(self, position):
        super().__init__('Parentheses syntax error at position: ' + str(position))


class ValidationError(Exception):
    pass