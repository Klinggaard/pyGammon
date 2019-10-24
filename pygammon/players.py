import random
import numpy as np
from pygammon import config as cf

class randomPlayer:
    """ takes a random valid action """
    name = 'random'

    @staticmethod
    def play(state, dice_roll, next_states):
        '''
        :param state: Current state of the game
        :param dice_roll: Two values between 1 and 6 on a list
        :param next_states: A list of the next possible steps
        :return: The index of the chosen next state
        '''
        choice = random.randrange(next_states[:].size)
        #print(choice)
        return choice


class aggressivePlayer:
    # TODO: Fix issue with random freezing
    """ Sends an opponent home if possible, otherwise chooses random valid action """
    name = 'aggressive'

    @staticmethod
    def play(state, dice_roll, next_states):
        '''
        :param state: Current state of the game
        :param dice_roll: Two values between 1 and 6 on a list
        :param next_states: A list of the next possible steps
        :return: The index of the chosen next state
        '''
        prison = []
        # print(len(prison))
        choice = None
        print("states", len(next_states))
        for i in range(len(next_states)):
            if next_states[i][1][cf.PRISON] > state[1][cf.PRISON]:
                prison.append(i)
        print("prison", len(prison))
        if len(prison):
            choice = random.choice(prison)
        else:
            choice = random.randrange(len(next_states))

        print(choice)
        return choice
