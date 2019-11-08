import random
import numpy as np
import time
from pygammon import config as cf
from pygammon.utils import StateTree
from pygammon.game import Game

statesTotal = 0
expTimes = 0
simTimes = 0
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
        choice = None
        newStateIdx = -1
        maxNumPris = 0
        for i in range(len(next_states)):
            newPrisoners = next_states[i][1][cf.PRISON] - state[1][cf.PRISON]
            if newPrisoners > maxNumPris:
                maxNumPris = newPrisoners
                newStateIdx = i
        if newStateIdx >= 0:
            choice = newStateIdx
        else:
            choice = random.randrange(next_states[:].size)

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


class monteCarlo:
    """ Use Monte-Carlo tree search to choose the best action """
    name = 'monte-carlo'

    @staticmethod
    def simGame(state):
        players = [fastPlayer, fastPlayer]
        game = Game(players, state)
        winner = game.playFullGame()
        return winner

    @staticmethod
    def selection(node, c_param=1.4):
        '''
        :param node: A StateTree object
        :param c_param: A parameter to weight exploration or exploitation
        :return: Recursively return a StateTree object
        '''
        if not node.leaf:
            weights = [
                (c.nWins / c.nSims) + c_param * np.sqrt((2 * np.log(node.nSims) / c.nSims))
                for c in node.children
            ]
            return monteCarlo.selection(node.children[np.argmax(weights)], c_param=c_param)
        return node

    @staticmethod
    def expansion(node, nextStates):
        '''
        :param node: A StateTree object
        :param nextStates: A list of the next possible states from the current state (node.state)
        '''

        global statesTotal
        global expTimes
        statesTotal += len(nextStates)
        expTimes += 1
        children = [StateTree() for i in range(len(nextStates))]
        for i in range(len(children)):
            children[i].state = nextStates[i]
            children[i].parent = node
        node.children = children
        if len(children):
            node.leaf = False

    @staticmethod
    def simulation(node):
        '''
        :param node: A StateTree object
        :return: number of wins and sims
        '''
        state = node.state
        wins = 0
        sims = 0
        global simTimes
        for c in node.children:
            simTimes += 1
            winner = monteCarlo.simGame(c.state)
            if winner == 0:
                c.nWins += 1
                wins += 1
            c.nSims += 1
            sims += 1
        return wins, sims

    @staticmethod
    def backpropagation(node, wins, sims):
        '''
        :param node: A StateTree object
        :param wins: number of wins
        :param sims: number of sims
        '''
        node.nWins += wins
        node.nSims += sims
        if not node.root:
            monteCarlo.backpropagation(node.parent, wins, sims)

    @staticmethod
    def moveOppOneStep(state):
        diceRolls = [random.randint(1, 6), random.randint(1, 6)]
        oppState = state.getStateRelativeToPlayer(1)
        next_states = Game.getRelativeStates(oppState, diceRolls)
        if next_states.size > 0:
            choice = random.randrange(next_states[:].size)
            nextOppState = next_states[choice]
            nextOppState = nextOppState.getStateRelativeToPlayer(1)
            state[1] = nextOppState[1]
        return state

    @staticmethod
    def play(state, dice_roll, next_states):
        '''
        :param state: Current state of the game
        :param dice_roll: Two values between 1 and 6 on a list
        :param next_states: A list of the next possible steps
        :return: The index of the chosen next state
        '''
        global simTimes
        simTimes = 0
        nowTime = time.time()
        numTimesRun = 10
        # Build the starting tree
        root = StateTree(state, [], True)
        root.leaf = True
        # Next follow the Monte carlo steps (First for the root where the next_states are known beforehand
        expandNode = monteCarlo.selection(root)
        monteCarlo.expansion(expandNode, next_states)
        win, sim = monteCarlo.simulation(expandNode)
        monteCarlo.backpropagation(expandNode, win, sim)
        for x in range(0, numTimesRun-1):
            expandNode = monteCarlo.selection(root)
            state = monteCarlo.moveOppOneStep(expandNode.state)
            dice_roll = [random.randint(1, 6), random.randint(1, 6)]
            next_states = Game.getRelativeStates(state, dice_roll)
            monteCarlo.expansion(expandNode, next_states)
            win, sim = monteCarlo.simulation(expandNode)
            monteCarlo.backpropagation(expandNode, win, sim)

        possilbeStates = root.children
        winRatio = [
            n.getWinRatio()
            for n in possilbeStates
        ]
        choice = np.argmax(winRatio)
        # print("AVGR:", statesTotal / expTimes)
        # print("Number of sims:", simTimes)
        # print("Step Time:", time.time()-nowTime)
        return choice
