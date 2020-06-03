from unisgf.game_tree import GameTree


class Collection(list):
    def append(self, game_tree: GameTree):
        if not isinstance(game_tree, GameTree):
            raise TypeError("Collection must consist of game trees")

        super().append(game_tree)

    def __add__(self, other: 'Collection'):
        if not isinstance(other, Collection):
            raise TypeError("'Operator '+' is not allowed between Collection and " + str(type(other)))

        return Collection(list.__add__(self, other))

    def __iadd__(self, other: 'Collection'):
        if not isinstance(other, Collection):
            raise TypeError("'Operator '+' is not allowed between Collection and " + str(type(other)))

        return list.__iadd__(self, other)
