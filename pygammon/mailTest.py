from game import Game
import players as pl
import random
import time
import numpy as np
import multiprocessing

import smtplib

threads = 2

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
    email_data("limit test", subject="limit test")




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


