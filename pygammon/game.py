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
