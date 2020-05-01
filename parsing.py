from game_tree import GameTree
from collection import Collection
from grammar_utils import is_whitespace


class Parser:
    structure_rules = {
        '(': (None, ']', ';', ')'),
        ';': ('(', ';', ']'),
        '[': (';', ']'),
        ']': ('[',),
        ')': (']', ';', ')')
    }

    def parse_file(self, path) -> Collection:
        with open(path, 'r') as f:
            unparsed_string = f.read()

        collection = self.parse_string(unparsed_string)
        return collection

    def parse_string(self, string) -> Collection:
        collection = Collection()

        last_structure_element = None

        parentheses_balance = 0
        square_brackets_balance = 0

        is_escaping = False

        property_ident_search = False

        cur_game_tree = None
        cur_property = None
        cur_node = None
        depth_stack = []

        span_copier = SpanCopier()

        for index, char in enumerate(string):
            print(index, char)
            if is_escaping:
                is_escaping = False

            elif char == '\\':
                is_escaping = True

            elif is_whitespace(char):
                # if searching for new property start index should shift until
                # property identifier is reached
                if property_ident_search and not span_copier.is_ready():
                    # pass whitespace, move start
                    if span_copier.is_start_previous_to(index):
                        span_copier.set_start(index)

                    # Whitespace met after some chars other than whitespace.
                    else:
                        # Now: ' <start>propIdent<end> '
                        # Moving start at the beginning of propIdent and fix the end.
                        span_copier.set_start(span_copier.start + 1)
                        span_copier.set_end(index)

            elif char in self.structure_rules:
                if last_structure_element not in self.structure_rules[char]:
                    raise SyntaxError("'{}' can't not follow '{}'".format(char, last_structure_element))

                last_structure_element = char

                if char == '(':
                    parentheses_balance += 1

                    if parentheses_balance == 1:
                        cur_game_tree = GameTree()
                        cur_property = None
                        cur_node = None

                        depth_stack = []
                    else:
                        depth_stack.append(cur_node)

                    property_ident_search = False
                    span_copier.reset()

                # ending variation or game tree
                elif char == ')':
                    parentheses_balance -= 1

                    if parentheses_balance == -1:
                        raise SyntaxError("Unexpected ')' parenthesis at position " + str(index))

                    if parentheses_balance == 0:
                        collection.append(cur_game_tree)
                    else:
                        cur_node = depth_stack.pop()

                    property_ident_search = False
                    span_copier.reset()

                elif char == '[':
                    square_brackets_balance += 1

                    if square_brackets_balance == 2:
                        raise SyntaxError("Unexpected '[' square bracket at position " + str(index))

                    # property identifier found
                    if not span_copier.is_start_previous_to(index):
                        # no spaces after property identifier
                        if not span_copier.is_ready():
                            span_copier.set_end(index)

                        # create new property
                        span_copier.set_start(span_copier.start + 1)
                        property_identifier = span_copier.copy(string)
                        cur_property = cur_node.create_property(property_identifier)

                    property_ident_search = False

                    # search value of the property
                    span_copier.prepare(index)

                elif char == ']':
                    square_brackets_balance -= 1

                    if square_brackets_balance == -1:
                        raise SyntaxError("Unexpected ']' square bracket at position " + str(index))

                    # add value
                    span_copier.set_start(span_copier.start + 1)
                    span_copier.set_end(index)
                    property_value = span_copier.copy(string)
                    cur_property.add_value(property_value)

                    # search property identifier
                    span_copier.prepare(index)
                    property_ident_search = True

                elif char == ';':
                    # unexpected property identifier between ; and ; found
                    if span_copier.is_active() and not span_copier.is_start_previous_to(index):
                        raise SyntaxError('Unexpected property identifier at position ' + str(span_copier.start))

                    cur_property = None

                    if cur_node is None:
                        cur_node = cur_game_tree.get_root()
                    else:
                        cur_node = cur_node.create_child()

                    # search property identifier
                    span_copier.prepare(index)
                    property_ident_search = True

            # identifier already found and second identifier met
            elif property_ident_search and span_copier.is_ready():
                raise SyntaxError("Unexpected property identifier at " + str(index))

        if parentheses_balance != 0:
            raise SyntaxError('Not all parentheses are closed')

        if not collection:
            raise SyntaxError('Collection is empty')

        return collection


class SpanCopier:
    def __init__(self):
        self.start = None
        self.end = None

    def set_start(self, value: int):
        self.start = value

    def set_end(self, value: int):
        self.end = value

    def prepare(self, start: int):
        self.start = start
        self.end = None

    def reset(self):
        self.start = None
        self.end = None

    def is_ready(self) -> bool:
        return self.end is not None

    def is_active(self) -> bool:
        return self.start is not None

    def is_start_previous_to(self, index):
        return self.start + 1 == index

    def copy(self, string) -> str:
        return string[self.start: self.end]
