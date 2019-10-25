from pygammon.game import Game
from pygammon import players as p
import random
import time
import numpy as np




players = [p.randomPlayer(), p.aggressivePlayer]
for i, player in enumerate(players):
    player.id = i

score = [0, 0]

n = 100

start_time = time.time()
for i in range(n):
    random.shuffle(players)
    game = Game(players)
    winner = game.playFullGame()
    score[players[winner].id] += 1
    print('Game ', i, ' done')
duration = time.time() - start_time

print('win distribution:\n', players[0].name, score[players[0].id], "\n", players[1].name, score[players[1].id])
print('games per second:', n / duration)
