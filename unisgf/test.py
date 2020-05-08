from unisgf.rendering import Renderer
from unisgf.game_tree import GameTree
from unisgf.collection import Collection
from unisgf.property import Property
from unisgf.property_value import PropertyValue
from unisgf import property_value
from string import ascii_letters



class DotsMove(PropertyValue):
    @staticmethod
    def validate_string(data: str):
        if len(data) != 2:
            raise ValueError

        x, y = data
        x = ascii_letters.find(x)
        if x == -1:
            return ValueError
        y = ascii_letters.find(y)
        if y == -1:
            return ValueError

        return x, y

    @staticmethod
    def validate_value(value):
        try:
            x, y = value
        except Exception:
            raise ValueError

        if not isinstance(x, int) or not isinstance(y, int) or x < 0 or y < 0:
            raise ValueError

        return value

    def render(self):
        return ascii_letters[self.value[0]] + ascii_letters[self.value[1]]


property_value.validation_order = [DotsMove] + property_value.validation_order

gt = GameTree()

n = gt.get_root()
n = n.create_child()
n['AA'] = [1, 2, 3, 4]
n['AV'] = [2, 4]

n1 = n.create_child()
n1['ASD'] = [2, 4]

n1 = n1.create_child()
n1['D'] = [2, 4]

n2 = n.create_child()
n2['A'] = [1, 2, 4]
n2['AD'] = ['aS']
n2['AD'].add_value('As')

collection = Collection()
collection.append(gt)

renderer = Renderer()
print(renderer.render_string(collection))
print(renderer.render_file('test.txt', collection))

from unisgf.parsing import Parser

data = """
(;AW[\[hh\t])
"""
p = Parser()
collection = p.parse_string(data)
print(collection[0].get_root().children)
print(renderer.render_string(collection))