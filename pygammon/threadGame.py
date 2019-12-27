from game import Game
import players as pl
import random
import time
import numpy as np
import multiprocessing

import smtplib

retList = []

depth = [10,30,50]

threads = 80
n_games = 1000

if n_games < threads:
    threads = n_games


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
    body = ""

    # TODO for loop
    for d in depth:
        players = [pl.monteCarlo(), pl.randomPlayer()]
        for j, player in enumerate(players):
            player.id = j

        score = [0, 0]

        n = int(n_games/threads)

        # start_time = time.time()
        for j in range(n):
            random.shuffle(players)
            game = Game(players)
            winner = game.playFullGame()
            score[players[winner].id] += 1
            #print('Game ', j, ' done')
        # duration = time.time() - start_time


        body += str(str(d)+","+str(players[0].name) + ":" + str(score[players[0].id]) + "," + str(players[1].name) + ":" + str(
            score[players[1].id])+"\n")


    email_data(body=body)
    return body


def multiprocessing_func():
    # time.sleep(2)
    print(basic_func())


if __name__ == '__main__':
    starttime = time.time()
    processes = []
    for i in range(0, threads):
        p = multiprocessing.Process(target=multiprocessing_func)
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    print('That took {} seconds'.format(time.time() - starttime))
    print(retList)
