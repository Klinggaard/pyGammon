from pygammon.game import Game
from pygammon import players as pl
import random
import time
import numpy as np
import multiprocessing

import smtplib

retList = []


def email_data(body, to='oliver.klinggaard@gmail.com', subject='pygammon - data'):
    gmail_user = 'pygammonmail@gmail.com'
    gmail_password = 'rPqNERsweh3mRvi'
    _to = [to]
    sent_from = gmail_user

    # Sending data

    email_text = 'Subject: {}\n\n{}'.format(subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, _to, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')


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
    body = str(str(players[0].name) + ":" + str(score[players[0].id]) + ";" + str(players[1].name) + ":" + str(
        score[players[1].id]))
    email_data(body=body)
    return (players[0].name, score[players[0].id]), (players[1].name, score[players[1].id])


def multiprocessing_func():
    # time.sleep(2)
    print(basic_func())


if __name__ == '__main__':
    starttime = time.time()
    processes = []
    for i in range(0, 1):
        p = multiprocessing.Process(target=multiprocessing_func)
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    print('That took {} seconds'.format(time.time() - starttime))
    print(retList)
