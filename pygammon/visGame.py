from pygammon.game import Game
from pygammon.game import GameState
from pygammon import players as p
from pygammon.visualizer import VisualizerStep
import pyglet
import numpy as np

players = [p.fastPlayer, p.monteCarlo]

state = np.empty((2, 26), dtype=np.int)  # 2 players, 15 tokens per player
state[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, 0, 0, 2]
state[1] = [5, 5, 0, 5, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0]

gameState = GameState(state)

game = Game(players)
window = VisualizerStep(game)
print('use left and right arrow to progress game')
pyglet.app.run()
