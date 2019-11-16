from pygammon.game import Game
from pygammon import players as pl
import random
import time
import numpy as np
import multiprocessing

retList = []


def basic_func():
    players = [pl.monteCarlo(), pl.randomPlayer()]
    for j, player in enumerate(players):
        player.id = j

    score = [0, 0]

    n = 100

    start_time = time.time()
    for j in range(n):
        random.shuffle(players)
        game = Game(players)
        winner = game.playFullGame()
        score[players[winner].id] += 1
        print('Game ', j, ' done')
    duration = time.time() - start_time

    return ((players[0].name, score[players[0].id]), (players[1].name, score[players[1].id]))


def multiprocessing_func():
    # time.sleep(2)
    print(basic_func())


if __name__ == '__main__':
    starttime = time.time()
    processes = []
    for i in range(0, 10):
        p = multiprocessing.Process(target=multiprocessing_func)
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    print('That took {} seconds'.format(time.time() - starttime))
    print(retList)


