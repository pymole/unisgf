from node import RootNode


class GameTree:
    def __init__(self):
        self.root = RootNode()

    def __iter__(self):
        return GameTreeBaseIterator(self)

    def get_root(self):
        return self.root


class GameTreeBaseIterator:
    def __init__(self, game_tree):
        self.cur_node = game_tree.get_root()

    def __iter__(self):
        return self

    def __next__(self):
        if not self.cur_node.children:
            raise StopIteration

        return self.cur_node.children[0]


