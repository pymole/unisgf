from rendering import Renderer
from game_tree import GameTree
from collection import Collection
from property import Property


gt = GameTree()

n = gt.get_root()
n = n.create_child()
n.create_property('AA', [1, 2, 3, 4])
n.create_property('AV', [2, 4])

n1 = n.create_child()
n1.create_property('ASD', [2, 4])

n1 = n1.create_child()
n1.create_property('D', [2, 4])

n2 = n.create_child()
n2.create_property('A', [1, 2, 4])

collection = Collection()
collection.add_game_tree(gt)

renderer = Renderer()
print(renderer.render_string(collection))
print(renderer.render_file('test.txt', collection))

from parsing import Parser

data = """
(;;A[1][2][3][4]AS[2][4](;AA[2][4];DD[2][4])(;SS[1][2][4]))
(;;A[1][2][3][4]S[2][4](;V[2][4];ASD[2][4])(;ASFAFS[1][2][4]))
"""
p = Parser()
collection = p.parse_string(data)


from rendering import Renderer

r = Renderer()
print(r.render_string(collection))

