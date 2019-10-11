from pygammon.game import Game
import random
import time
import numpy as np

class randomPlayer:
    """ takes a random valid action """
    name = 'random'

    @staticmethod
    def play(state, dice_roll, next_states):
        if all(item==False for item in next_states):
            return False
        return random.choice(np.argwhere(next_states != False))


players = [randomPlayer(), randomPlayer()]
for i, player in enumerate(players):
    player.id = i

score = [0, 0]

n = 10

start_time = time.time()
for i in range(n):
    random.shuffle(players)
    game = Game(players)
    winner = game.playFullGame()
    score[players[winner].id] += 1
    print('Game ', i, ' done')
duration = time.time() - start_time

print('win distribution:', score)
print('games per second:', n / duration)
