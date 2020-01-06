from pygammon.game import Game
from pygammon import players as p
import random
import time
import numpy as np

playerTD = p.TD_gammon(num_hidden=40)
train_player = [playerTD, playerTD]
players = [playerTD, p.fastAggressivePlayer()]
players1 = [playerTD, p.randomPlayer()]
for i, player in enumerate(players):
    player.id = i

score = [0, 0]

n_train = 2000
for i in range(n_train):
    game = Game(train_player)
    winner = game.playFullGame()
    print('Train Game ', i, ' done')

n_test = 1000
playerTD.set_train(False)
#start_time = time.time()
for i in range(n_test):
    random.shuffle(players)
    game = Game(players)
    winner = game.playFullGame()
    score[players[winner].id] += 1
    #print('Game ', i, ' done')

#duration = time.time() - start_time

print('win distribution:\n', players[0].name, score[players[0].id], "\n", players[1].name, score[players[1].id])

for i, player in enumerate(players1):
    player.id = i
score = [0, 0]
for i in range(n_test):
    random.shuffle(players1)
    game = Game(players1)
    winner = game.playFullGame()
    score[players1[winner].id] += 1
    #print('Game ', i, ' done')

#duration = time.time() - start_time

print('win distribution:\n', players1[0].name, score[players1[0].id], "\n", players1[1].name, score[players1[1].id])
#print('games per second:', n / duration)
#print("avrg game length: ", duration/n)
