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
        #print("states", len(next_states))
        newStateIdx = -1
        maxNumPris = 0
        for i in range(len(next_states)):
            newPrisoners = next_states[i][1][cf.PRISON] - state[1][cf.PRISON]
            if newPrisoners > maxNumPris:
                maxNumPris = newPrisoners
                newStateIdx = i
        #print("prison", len(prison))
        if newStateIdx >= 0:
            choice = newStateIdx
        else:
            choice = random.randrange(len(next_states))

        #print(choice)
        return choice

class fastAggressivePlayer:
    """ Sends an opponent home if possible, otherwise chooses random valid action """
    name = 'fastAggressive'

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
        # print("states", len(next_states))
        newStateIdx = -1
        maxNumPris = 0
        for i in range(len(next_states)):
            newPrisoners = next_states[i][1][cf.PRISON] - state[1][cf.PRISON]
            if newPrisoners > maxNumPris:
                newStateIdx = i
        # print("prison", len(prison))
        if newStateIdx >= 0:
            choice = newStateIdx
        else:
            choice = random.randrange(len(next_states))

        # print(choice)
        return choice


class simpleDefensivePlayer:
    name = 'simpleDefensive'

    @staticmethod
    def play(state, dice_roll, next_states):
        '''
        :param state: Current state of the game
        :param dice_roll: Two values between 1 and 6 on a list
        :param next_states: A list of the next possible steps
        :return: The index of the chosen next state
        '''
        prison = []
        choice = None
        newStateIdx = -1
        maxNumSafe = 0
        currentUnsafe = len(np.where(state[0] == 1)[0])
        for i in range(len(next_states)):
            nextUnsafe = len(np.where(next_states[i][0] == 1)[0])
            changeOfUnsafe = currentUnsafe - nextUnsafe
            if changeOfUnsafe > maxNumSafe:
                maxNumSafe = changeOfUnsafe
                newStateIdx = i
        #print("prison", len(prison))
        if newStateIdx >= 0:
            choice = newStateIdx
        else:
            choice = random.randrange(len(next_states))

        #print(choice)
        return choice

class fastPlayer:
    name = 'fast'

    @staticmethod
    def play(state, dice_roll, next_states):
        '''
        :param state: Current state of the game
        :param dice_roll: Two values between 1 and 6 on a list
        :param next_states: A list of the next possible steps
        :return: The index of the chosen next state
        '''
        choice = None
        newStateIdx = -1
        newStateGoalIdx = -1
        maxNumGoal = 0
        maxNumGoalReg = 0
        currentGoal = state[0][cf.GOAL]

        for i in range(len(next_states)):
            nextGoal = next_states[i][0][cf.GOAL]
            changeOfGoal = nextGoal - currentGoal
            changeInGoalRegion = sum(next_states[i][0][18:25:1]) - sum(state[0][18:25:1])
            if changeInGoalRegion > maxNumGoalReg:
                maxNumGoalReg = changeInGoalRegion
                newStateIdx = i
            if changeOfGoal > maxNumGoal:
                maxNumGoal = changeOfGoal
                newStateGoalIdx = i

        if newStateIdx >= 0:
            choice = newStateIdx
        elif newStateGoalIdx >= 0:
            choice = newStateGoalIdx
        else:
            choice = len(next_states)-1

        #print(choice)
        return choice

