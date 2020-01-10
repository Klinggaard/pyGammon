import random
import numpy as np
import time
import math
from pygammon import config as cf
from pygammon.utils import StateTree
from pygammon.game import Game
from pygammon.game import GameState

statesTotal = 0
expTimes = 0
simTimes = 0


class randomPlayer:
    """ takes a random valid action """
    name = 'random'

    def play(self, state, dice_roll, next_states):
        '''
        :param state: Current state of the game
        :param dice_roll: Two values between 1 and 6 on a list
        :param next_states: A list of the next possible steps
        :return: The index of the chosen next state
        '''
        choice = random.randrange(next_states[:].size)
        # print(choice)
        return choice


class aggressivePlayer:
    """ Sends an opponent home if possible, otherwise chooses random valid action """
    name = 'aggressive'

    def play(self, state, dice_roll, next_states):
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

        # print(choice)
        return choice


class fastAggressivePlayer:
    """ Sends an opponent home if possible, otherwise chooses random valid action """
    name = 'fastAggressive'

    def play(self, state, dice_roll, next_states):
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

    def play(self, state, dice_roll, next_states):
        '''
        :param state: Current state of the game
        :param dice_roll: Two values between 1 and 6 on a list
        :param next_states: A list of the next possible steps
        :return: The index of the chosen next state
        '''
        newStateIdx = -1
        maxNumSafe = 0
        currentUnsafe = len(np.where(state[0] == 1)[0])
        for i in range(len(next_states)):
            nextUnsafe = len(np.where(next_states[i][0] == 1)[0])
            changeOfUnsafe = currentUnsafe - nextUnsafe
            if changeOfUnsafe > maxNumSafe:
                maxNumSafe = changeOfUnsafe
                newStateIdx = i
        if newStateIdx >= 0:
            choice = newStateIdx
        else:
            choice = random.randrange(len(next_states))

        # print(choice)
        return choice


class fastPlayer:
    name = 'fast'

    def play(self, state, dice_roll, next_states):
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
            choice = len(next_states) - 1

        # print(choice)
        return choice


class monteCarlo:
    """ Use Monte-Carlo tree search to choose the best action """
    name = 'monte-carlo'

    def __init__(self, max_depth=10):
        self.max_depth = max_depth

    @staticmethod
    def simGame(state):
        players = [fastPlayer(), fastPlayer()]
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

    def play(self, state, dice_roll, next_states):
        '''
        :param state: Current state of the game
        :param dice_roll: Two values between 1 and 6 on a list
        :param next_states: A list of the next possible steps
        :return: The index of the chosen next state
        '''
        global simTimes
        simTimes = 0
        nowTime = time.time()
        # Build the starting tree
        root = StateTree(state, [], True)
        root.leaf = True
        # Next follow the Monte carlo steps (First for the root where the next_states are known beforehand
        expandNode = monteCarlo.selection(root)
        next_states = Game.trimStates(next_states)  # TODO TRIM
        monteCarlo.expansion(expandNode, next_states)
        win, sim = monteCarlo.simulation(expandNode)
        monteCarlo.backpropagation(expandNode, win, sim)
        for x in range(0, self.max_depth - 1):
            expandNode = monteCarlo.selection(root)
            state = monteCarlo.moveOppOneStep(expandNode.state)
            dice_roll = [random.randint(1, 6), random.randint(1, 6)]
            next_states = Game.getRelativeStates(state, dice_roll)
            next_states = Game.trimStates(next_states)  # TODO TRIM
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


class TD_gammon:
    """ An implementation of TD-Gammon """
    name = 'TD-gammon'

    def __init__(self, num_hidden=50, lr=0.1, lam=0.7, w_i = None, w_o = None):
        self.step = 1
        self.train = True
        self.lam = lam
        self.lr = lr
        self.x_h = None
        self.y_old_1 = np.ones((1, 2))
        self.y_old_2 = np.ones((1, 2))

        self.input = np.zeros((198, 1))

        self.num_hidden = num_hidden
        self.weights_input = np.random.rand(198, self.num_hidden)
        self.weights_output = np.random.rand(self.num_hidden, 2)
        if w_i is not None:
            self.weights_input = w_i
        if w_o is not None:
            self.weights_output = w_o
        #self.weights_input = np.full((198, self.num_hidden), 0.5)
        #self.weights_output = np.full((self.num_hidden, 2), 0.5)

        self.eli_input = np.zeros((198, self.num_hidden, 2))
        self.eli_output = np.zeros((self.num_hidden, 2))

    def reset_step(self):
        self.step = 1
        self.eli_input = np.zeros((198, self.num_hidden, 2))
        self.eli_output = np.zeros((self.num_hidden, 2))

    def save_weights(self, trainNr):
        np.savetxt('weightsV3/w_i' + trainNr + '.txt', self.weights_input, fmt='%10.5f')
        np.savetxt('weightsV3/w_o' + trainNr + '.txt', self.weights_output, fmt='%10.5f')

    def set_train(self, train):
        self.train = train

    def convert_state(self, state):
        for pos in range(24):
            players = (state[0][pos], state[1][pos])
            for i, p in enumerate(players):
                if p == 0:
                    self.input[(pos * 8) + i * 4] = 0
                    self.input[(pos * 8) + i * 4 + 1] = 0
                    self.input[(pos * 8) + i * 4 + 2] = 0
                    self.input[(pos * 8) + i * 4 + 3] = 0
                elif p == 1:
                    self.input[(pos * 8) + i * 4] = 1
                    self.input[(pos * 8) + i * 4 + 1] = 0
                    self.input[(pos * 8) + i * 4 + 2] = 0
                    self.input[(pos * 8) + i * 4 + 3] = 0
                elif p == 2:
                    self.input[(pos * 8) + i * 4] = 1
                    self.input[(pos * 8) + i * 4 + 1] = 1
                    self.input[(pos * 8) + i * 4 + 2] = 0
                    self.input[(pos * 8) + i * 4 + 3] = 0
                elif p == 3:
                    self.input[(pos * 8) + i * 4] = 1
                    self.input[(pos * 8) + i * 4 + 1] = 1
                    self.input[(pos * 8) + i * 4 + 2] = 1
                    self.input[(pos * 8) + i * 4 + 3] = 0
                else:
                    self.input[(pos * 8) + i * 4] = 1
                    self.input[(pos * 8) + i * 4 + 1] = 1
                    self.input[(pos * 8) + i * 4 + 2] = 1
                    self.input[(pos * 8) + i * 4 + 3] = (p - 2) / 3
        self.input[192] = state[0][cf.PRISON] / 2
        self.input[193] = state[1][cf.PRISON] / 2
        self.input[194] = state[0][cf.GOAL] / 15
        self.input[195] = state[1][cf.GOAL] / 15
        self.input[196] = 1
        self.input[197] = 0

    def forward(self):
        x_h = np.dot(np.transpose(self.input), self.weights_input)
        self.x_h = np.transpose(1.0/(1. + np.exp(-x_h)))
        #self.x_h = np.clip(self.x_h, -1000, 1000)
        y = np.dot(x_h, self.weights_output)
        y = 1.0/(1. + np.exp(-y))
        #max_y = max(y[0,0], y[0,1])
        #y[0, 0] = y[0, 0] / (50*self.num_hidden)
        #y[0, 1] = y[0, 1] / (50*self.num_hidden)
        #y = np.clip(y, -1000, 1000)
        return y

    def backward(self, error):
        self.weights_output = self.weights_output + self.lr * error * self.eli_output
        self.weights_output = np.clip(self.weights_output, -1000, 1000)
        for i in range(2):
            self.weights_input = self.weights_input + self.lr * error[0, i] * self.eli_input[:,:,i]
        self.weights_input = np.clip(self.weights_input, -1000, 1000)

    def update_elig(self, y):
        self.eli_output = self.lam * self.eli_output + (y*(1.-y)*self.x_h)
        self.eli_output = np.clip(self.eli_output, -1000, 1000)
        for i in range(198):
            self.eli_input[i] = self.lam * self.eli_input[i] + (y * (1. - y) * self.weights_output * self.x_h * (1. - self.x_h) * self.input[i])
        self.eli_input = np.clip(self.eli_input, -1000, 1000)

    def play(self, state, dice_roll, next_states):
        '''
        :param state: Current state of the game
        :param dice_roll: Two values between 1 and 6 on a list
        :param next_states: A list of the next possible steps
        :return: The index of the chosen next state
        '''

        if self.train and self.step > 1.:
            self.convert_state(state=state)
            forward = self.forward()
            error = forward - self.y_old_1
            self.update_elig(forward)
            self.backward(error)

        max_val = -float('Inf')
        max_idx = 0
        max_y = np.random.rand(1, 2)
        for x, pos_state in enumerate(next_states):
            self.convert_state(state=pos_state)
            y = self.forward()
            if y[0, 0] > max_val:
                max_idx = x
                max_y = y
                max_val = y[0, 0]

        self.y_old_1 = max_y
        self.step = self.step+1
        return max_idx
