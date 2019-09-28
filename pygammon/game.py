import random
import numpy as np
from pygammon.utils import playerColors

class GameState:
    def __init__(self, state=None, empty=False):
        if state is not None:
            self.state = state
        else:
            # Setup game
            self.state = np.empty((2, 15), dtype=np.int)  # 2 players, 15 tokens per player
        if not empty:
            self.state.fill(-1)

    def copy(self):
        return GameState(self.state.copy())

    def __getitem__(self, item):
        return self.state[item]

    def __setitem__(self, key, value):
        self.state[key] = value

    def __iter__(self):
        return self.state.__iter__()

