from unisgf.game_tree import GameTree


class Collection(list):
    def append(self, game_tree: GameTree):
        if not isinstance(game_tree, GameTree):
            raise TypeError("Collection must consist of game trees")

        super().append(game_tree)