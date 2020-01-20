from pygammon.game import Game
from pygammon import players as pl
import random
import time
import numpy as np

import csv

weights_i = np.loadtxt("weightsV2/w_i288000.txt")
weights_o = np.loadtxt("weightsV2/w_o288000.txt")
playerTD = pl.TD_gammon(num_hidden=60, lr=0.1, lam=0.5, w_i=weights_i,w_o=weights_o)
playerTD.set_train(False)

player_collection = [pl.randomPlayer(), pl.fastPlayer(), pl.aggressivePlayer(), pl.fastAggressivePlayer(),
                     pl.simpleDefensivePlayer(), playerTD]

n_games = 5000

'''
DATA TO EXTRACT
win rate
avg time per game
avg number of turns per game
'''

with open("result.csv", 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(["player 1","player 2","player 1 wins","player 2 wins","avg steps / game","avg duration / game"])

for p1, player_1 in enumerate(player_collection):
    for p2, player_2 in enumerate(player_collection):
        if p2 < p1:
            continue
        if player_1.name == player_2.name:
            continue

        players = [player_1, player_2]
        for j, player in enumerate(players):
            player.id = j

        score = [0, 0]
        steps = 0

        start_time = time.time()
        for j in range(n_games):
            random.shuffle(players)
            game = Game(players)
            winner, game_steps = game.playFullGame(get_step=True)

            steps+=game_steps
            score[players[winner].id] += 1
            #print('Game ', j, ' done')
        duration = time.time() - start_time
        avg_duration = duration/n_games
        avg_steps = steps / n_games

        if players[0].id != 0:
            players = np.flip(players)
            print("DO A FLIP!")
        print(player_1.name,"vs",player_2.name,"\n",avg_duration,avg_steps,"\n",score[players[0].id],score[players[1].id])

        results =[player_1.name, player_2.name, score[players[0].id], score[players[1].id], avg_steps, avg_duration]
        with open("result.csv", 'a', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_NONNUMERIC)
            wr.writerow(results)
