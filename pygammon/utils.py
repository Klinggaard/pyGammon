class StateTree:
    def __init__(self, state=None, children=[], root=False, parent=None):
        self.state = state
        self.children = children
        self.parent = parent
        self.leaf = len(self.children) == 0
        self.root = root
        self.nWins = 0
        self.nSims = 0

    def __str__(self):
        return str(self.node)

    def getWinRatio(self):
        return self.nWins/self.nSims
