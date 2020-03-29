class Collection:
    def __init__(self, game_trees=None):
        if game_trees is None:
            game_trees = []

        self.game_trees = game_trees

    def __iter__(self):
        return iter(self.game_trees)

    def add_game_tree(self, game_tree):
        self.game_trees.append(game_tree)

    def is_empty(self):
        return len(self.game_trees) == 0
