from pygammon.game import Game
from pygammon import players as p
import csv
import time

playerTD = p.TD_gammon(num_hidden=60, lr=0.1, lam=0.5)
train_player = [playerTD, p.fastPlayer()]
players = [playerTD, p.randomPlayer()]
for i, player in enumerate(players):
    player.id = i

with open('trainTD.txt', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["NR Train", "Win Number"])

n_train = 1000
n_test = 100

start_time = time.time()
for k in range(10):
    score = [0, 0]
    playerTD.set_train(True)
    playerTD.reset_step()
    for i in range(n_train):
        game = Game(train_player)
        winner = game.playFullGame()
        #print('Game ', i, ' done')
    playerTD.save_weights(str(k * 3000 + 3000))

    playerTD.set_train(False)
    for i in range(n_test):
        game = Game(players)
        winner = game.playFullGame()
        score[players[winner].id] += 1

    with open('trainTD.txt', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([str(k*1000+1000), str(score[players[0].id])])

    print(str(k+1) + " out of 25, Done")
