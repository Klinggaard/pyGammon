playerColors = ['blue', 'red']


class StateTree:
    def __init__(self, state=None, children=[], root=False, parent=None):
        self.state = state
        self.children = children
        self.parent
        self.leaf = len(self.children) == 0
        self.root = root
        self.nWins = 0
        self.nSim = 0

    def __str__(self):
        return str(self.node)
