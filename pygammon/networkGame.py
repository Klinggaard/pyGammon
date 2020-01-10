from pygammon.game import Game
from pygammon import players as p
import random
import time
import numpy as np

lrs = [0.1, 0.3]
hiddens = [40, 60]
lams = [0.5, 0.7]
file = open("tuneParamV2.txt", "w")
file.close()
num_pos = len(lrs)*len(hiddens)*len(lams)
step = 0
for lr in lrs:
    for hidden in hiddens:
        for lam in lams:
            playerTD = p.TD_gammon(num_hidden=hidden, lr=lr, lam=lam)
            train_player = [playerTD, playerTD]
            players = [playerTD, p.randomPlayer()]
            for i, player in enumerate(players):
                player.id = i

            score = [0, 0]

            n_train = 10000
            for i in range(n_train):
                game = Game(train_player)
                winner = game.playFullGame()

            n_test = 1000
            playerTD.set_train(False)
            #start_time = time.time()
            for i in range(n_test):
                #random.shuffle(players)
                game = Game(players)
                winner = game.playFullGame()
                score[players[winner].id] += 1

            file = open("tuneParamV2.txt", "a")
            file.write("lr: " + str(lr) + " hidden: " + str(hidden) + " lam: " + str(lam))
            file.write("\n")
            file.write('win distribution: ' + str(score[players[0].id]/n_test))
            file.write("\n")
            file.close()
            step = step + 1
            print("Possibility " + str(step) + " out of " + str(num_pos) + ", Done")
            #duration = time.time() - start_time

            #print('win distribution:\n', players[0].name, score[players[0].id], "\n", players[1].name, score[players[1].id])
            #print('games per second:', n / duration)
            #print("avrg game length: ", duration/n)
