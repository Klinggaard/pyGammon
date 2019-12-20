import random
import logging
import numpy as np
import time
from pygammon import config as cf


class GameState:
    def __init__(self, state=None, empty=False):
        if state is not None:
            self.state = state
        else:
            self.state = np.empty((2, 26), dtype=np.int)  # 2 players, 15 tokens per player
            if not empty:
                # Setup game
                # Last positions are goal and prison in that order
                self.state[0] = [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, 0, 0, 0]
                self.state[1] = [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0]

    def copy(self):
        return GameState(self.state.copy())

    def __getitem__(self, item):
        return self.state[item]

    def __setitem__(self, key, value):
        self.state[key] = value

    def __iter__(self):
        return self.state.__iter__()

    def __eq__(self, other):
        """Overrides the default implementation"""
        return np.array_equal(self.state, other.state)

    def toString(self):
        return str(self[:])

    def getStateRelativeToPlayer(self, relativePlayerID):
        '''
        :param relativePlayerID: Player id
        :return:
        '''
        if relativePlayerID == 0:
            return GameState(self.state.copy())

        rel = GameState(empty=True)
        newPlayerIDs = 1
        rel0 = np.flip(self.state[1][0:24:1])
        rel[0] = np.append(rel0, self.state[1][24:26:1])
        rel1 = np.flip(self.state[0][0:24:1])
        rel[1] = np.append(rel1, self.state[0][24:26:1])
        return rel

    @staticmethod
    def _move(state, tokenIdx, die):
        return

    def moveFourToken(self, diceRolls):
        '''
        :param diceRolls: Two values between 1 and 6 on a list
        :return:
        '''
        # diceRolls is a list of the two dice rolls
        possibleStates = []
        indices = np.where(self[0] > 0)[0]
        prison = self[0][cf.PRISON]
        opponents = self[1]
        if prison > 0 and (opponents[diceRolls[0] - 1] > 1 and opponents[diceRolls[1] - 1] > 1):
            return np.asarray(possibleStates)
        for x in indices:
            newState = self.copy()
            player = newState[0]
            prison = self[0][cf.PRISON]
            opponents = newState[1]
            if prison > 0 and x != cf.PRISON:
                continue
            for y in indices:
                newState = self.copy()
                player = newState[0]
                prison = self[0][cf.PRISON]
                opponents = newState[1]

                if prison > 1 and (x != cf.PRISON or y != cf.PRISON):
                    continue
                for z in indices:
                    newState = self.copy()
                    player = newState[0]
                    prison = self[0][cf.PRISON]
                    opponents = newState[1]
                    if prison > 2 and (x != cf.PRISON or y != cf.PRISON or z != cf.PRISON):
                        continue
                    for w in indices:
                        newState = self.copy()
                        player = newState[0]
                        prison = self[0][cf.PRISON]
                        opponents = newState[1]
                        if x == cf.GOAL or y == cf.GOAL or z == cf.GOAL or w == cf.GOAL:
                            continue
                        # TODO: create for prison
                        # if four or more is in prison
                        if prison > 0:
                            if prison > 3:
                                if not (x == cf.PRISON and y == cf.PRISON and z == cf.PRISON and w == cf.PRISON):
                                    continue
                                if opponents[diceRolls[0] -1] == 1:
                                    opponents[diceRolls[0] -1] -= 1
                                    opponents[cf.PRISON] += 1
                                player[diceRolls[0] -1] += 1
                                player[x] -= 1
                                player[diceRolls[0] -1] += 1
                                player[y] -= 1
                                player[diceRolls[0] -1] += 1
                                player[z] -= 1
                                player[diceRolls[0] -1] += 1
                                player[w] -= 1
                                possibleStates.append(newState)
                            # if tree tokens is in prison
                            elif prison == 3:
                                #Move a token that are moved out of prison
                                if w == cf.PRISON and opponents[diceRolls[0] -1] < 2 and opponents[diceRolls[0] + diceRolls[0] -1] < 1:
                                    if opponents[diceRolls[0] -1] == 1:
                                        opponents[diceRolls[0] -1] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[diceRolls[0] + diceRolls[0] -1 == 1]:
                                        opponents[diceRolls[0] + diceRolls[0] -1] -= 1
                                        opponents[cf.PRISON] += 1
                                    player[x] -= 1
                                    player[diceRolls[0] -1] += 1
                                    player[y] -= 1
                                    player[diceRolls[0] -1] += 1
                                    player[z] -= 1
                                    player[diceRolls[0] + diceRolls[0] -1] += 1
                                    possibleStates.append(newState)
                                #move a different token than a token moved from prison
                                elif w != cf.PRISON and w + diceRolls[0] < 24 and opponents[w + diceRolls[0]] < 2:
                                    if opponents[diceRolls[0] -1] == 1:
                                        opponents[diceRolls[0]  -1] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[w + diceRolls[0] == 1]:
                                        opponents[w + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    player[diceRolls[0] -1] += 1
                                    player[x] -= 1
                                    player[diceRolls[0] -1] += 1
                                    player[y] -= 1
                                    player[diceRolls[0] -1] += 1
                                    player[z] -= 1
                                    player[w + diceRolls[0]] += 1
                                    player[w] -= 1
                                    possibleStates.append(newState)
                            # if two tokens in prison
                            elif prison == 2:
                                newState = self.copy()
                                player = newState[0]
                                prison = self[0][cf.PRISON]
                                opponents = newState[1]
                                #TODO: move the tokens twice or three times from prison
                                if z == w and z != x:
                                    # move two tokens from one position
                                    if player[z] > 1 and w + diceRolls[0] < 24 and z + diceRolls[0] < 24 and opponents[z + diceRolls[0]] < 2 and opponents[w + diceRolls[0]] < 2:
                                        if opponents[diceRolls[0] -1] == 1:
                                            opponents[diceRolls[0] -1] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[z + diceRolls[0]] == 1:
                                            opponents[z + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        player[diceRolls[0] -1] += 1
                                        player[x] -= 1
                                        player[diceRolls[0] -1] += 1
                                        player[y] -= 1
                                        player[z + diceRolls[0]] += 1
                                        player[z] -= 1
                                        player[w + diceRolls[0]] += 1
                                        player[w] -= 1
                                        possibleStates.append(newState)
                                    # move the same token twice
                                    newState = self.copy()
                                    player = newState[0]
                                    prison = self[0][cf.PRISON]
                                    opponents = newState[1]
                                    if z + diceRolls[0] + diceRolls[0] < 24 and opponents[z + diceRolls[0]] < 2 and opponents[z + diceRolls[0] + diceRolls[0]] < 2:
                                        if opponents[diceRolls[0] -1] == 1:
                                            opponents[diceRolls[0] -1] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[z + diceRolls[0]] == 1:
                                            opponents[z + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[z + diceRolls[0] + diceRolls[0]] == 1:
                                            opponents[z + diceRolls[0] + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        player[diceRolls[0] -1] += 1
                                        player[x] -= 1
                                        player[diceRolls[0] -1] += 1
                                        player[y] -= 1
                                        player[z + diceRolls[0] + diceRolls[0]] += 1
                                        player[z] -= 1
                                        possibleStates.append(newState)
                                # move tokens from two different positions
                                elif x != z and z != w and x != w and z + diceRolls[0] < 24 and w + diceRolls[0] < 24 and opponents[z + diceRolls[0]] < 2 and opponents[w + diceRolls[0]] < 2:
                                    if opponents[diceRolls[0] -1] == 1:
                                        opponents[diceRolls[0] -1] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[z + diceRolls[0]] == 1:
                                        opponents[z + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[w + diceRolls[0]] == 1:
                                        opponents[w + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    player[diceRolls[0] -1] += 1
                                    player[x] -= 1
                                    player[diceRolls[0] -1] += 1
                                    player[y] -= 1
                                    player[z + diceRolls[0]] += 1
                                    player[z] -= 1
                                    player[w + diceRolls[0]] += 1
                                    player[w] -= 1
                                    possibleStates.append(newState)
                                #move token that are moved out of prison and another token
                                elif x == z and x != w and w + diceRolls[0] < 24 and opponents[w + diceRolls[0]] < 2 and opponents[diceRolls[0] + diceRolls[0] -1] < 2:
                                    if opponents[diceRolls[0] -1] == 1:
                                        opponents[diceRolls[0] -1] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[diceRolls[0] + diceRolls[0] -1] == 1:
                                        opponents[diceRolls[0] + diceRolls[0] -1] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[w + diceRolls[0]] == 1:
                                        opponents[w + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    player[diceRolls[0] + diceRolls[0] -1] += 1
                                    player[x] -= 1
                                    player[diceRolls[0] - 1] += 1
                                    player[y] -= 1
                                    player[w + diceRolls[0]] += 1
                                    player[w] -= 1
                                    possibleStates.append(newState)
                                #move tokens that are moved out of prison
                                elif x == z and w == x:
                                    if opponents[diceRolls[0] + diceRolls[0] -1] < 2:
                                        if opponents[diceRolls[0] + diceRolls[0] - 1] == 1:
                                            opponents[diceRolls[0] + diceRolls[0] - 1] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[diceRolls[0] -1] == 1:
                                            opponents[diceRolls[0] -1] -= 1
                                            opponents[cf.PRISON] += 1
                                        player[diceRolls[0] + diceRolls[0] - 1] += 1
                                        player[x] -= 1
                                        player[diceRolls[0] + diceRolls[0] - 1] += 1
                                        player[y] -= 1
                                        possibleStates.append(newState)
                                    newState = self.copy()
                                    player = newState[0]
                                    prison = self[0][cf.PRISON]
                                    opponents = newState[1]
                                    if opponents[diceRolls[0] + diceRolls[0] + diceRolls[0] -1] < 2 and opponents[diceRolls[0] + diceRolls[0] -1] < 2:
                                        if opponents[diceRolls[0] -1] == 1:
                                            opponents[diceRolls[0] -1] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[diceRolls[0] + diceRolls[0] - 1] == 1:
                                            opponents[diceRolls[0] + diceRolls[0] - 1] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[diceRolls[0] + diceRolls[0] + diceRolls[0] - 1] == 1:
                                            opponents[diceRolls[0] + diceRolls[0] + diceRolls[0] - 1] -= 1
                                            opponents[cf.PRISON] += 1
                                        player[x] -= 1
                                        player[y] -= 1
                                        player[diceRolls[0] + diceRolls[0] + diceRolls[0] - 1] += 1
                                        player[diceRolls[0] -1] += 1
                                        possibleStates.append(newState)

                            elif prison == 1:
                                #TODO:
                                #move one token three times or three tokens from same pos that are not prison pos
                                if x != y and y == z and y == w:
                                    newState = self.copy()
                                    player = newState[0]
                                    prison = self[0][cf.PRISON]
                                    opponents = newState[1]
                                    if y + diceRolls[0] + diceRolls[0] + diceRolls[0] < 24 and opponents[y + diceRolls[0]] < 2 and opponents[y + diceRolls[0] + diceRolls[0]] < 2 and opponents[y + diceRolls[0] + diceRolls[0] + diceRolls[0]] < 2:
                                        if opponents[diceRolls[0] -1] == 1:
                                            opponents[diceRolls[0] -1] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[y + diceRolls[0]] == 1:
                                            opponents[y + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[y + diceRolls[0] + diceRolls[0]] == 1:
                                            opponents[y + diceRolls[0] + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[y + diceRolls[0] + diceRolls[0] + diceRolls[0]] == 1:
                                            opponents[y + diceRolls[0] + diceRolls[0] + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        player[diceRolls[0] -1] += 1
                                        player[x] -= 1
                                        player[y + diceRolls[0] + diceRolls[0] + diceRolls[0]] += 1
                                        player[y] -= 1
                                        possibleStates.append(newState)
                                    newState = self.copy()
                                    player = newState[0]
                                    prison = self[0][cf.PRISON]
                                    opponents = newState[1]
                                    if player[y] > 2 and y + diceRolls[0] < 24 and opponents[y + diceRolls[0]] < 2:
                                        if opponents[diceRolls[0] -1] == 1:
                                            opponents[diceRolls[0] -1] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[y + diceRolls[0]] == 1:
                                            opponents[y + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        player[x] -= 1
                                        player[diceRolls[0] -1] += 1
                                        player[y] -= 1
                                        player[y + diceRolls[0]] += 1
                                        player[z] -= 1
                                        player[z + diceRolls[0]] += 1
                                        player[w] -= 1
                                        player[w + diceRolls[0]] += 1
                                        possibleStates.append(newState)
                                #move the token in prison four times
                                newState = self.copy()
                                player = newState[0]
                                prison = self[0][cf.PRISON]
                                opponents = newState[1]
                                if x == y and y == z and y == w and opponents[diceRolls[0] -1] < 2 and opponents[diceRolls[0] + diceRolls[0] -1] < 2 and opponents[diceRolls[0] + diceRolls[0] + diceRolls[0] -1] < 2 and opponents[diceRolls[0] + diceRolls[0] + diceRolls[0] + diceRolls[0] -1] < 2:
                                    if opponents[diceRolls[0] - 1] == 1:
                                        opponents[diceRolls[0] - 1] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[diceRolls[0] + diceRolls[0] - 1] == 1:
                                        opponents[diceRolls[0] + diceRolls[0] - 1] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[diceRolls[0] + diceRolls[0] + diceRolls[0] - 1] == 1:
                                        opponents[diceRolls[0] + diceRolls[0] + diceRolls[0] - 1] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[diceRolls[0] + diceRolls[0] + diceRolls[0] + diceRolls[0] - 1] == 1:
                                        opponents[diceRolls[0] + diceRolls[0] + diceRolls[0] + diceRolls[0] - 1] -= 1
                                        opponents[cf.PRISON] += 1
                                    player[x] -= 1
                                    player[diceRolls[0] + diceRolls[0] + diceRolls[0] + diceRolls[0] -1] += 1
                                    possibleStates.append(newState)

                                #move one token two times or two tokens from same placement that are not prison token
                                if x != y and y == z and y != w and x != w:
                                    newState = self.copy()
                                    player = newState[0]
                                    prison = self[0][cf.PRISON]
                                    opponents = newState[1]
                                    if player[y] > 1 and w + diceRolls[0] < 24 and y + diceRolls[0] < 24 and opponents[y + diceRolls[0]] < 2 and opponents[w + diceRolls[0]] < 2:
                                        if opponents[diceRolls[0] - 1] == 1:
                                            opponents[diceRolls[0] - 1] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[y + diceRolls[0]] == 1:
                                            opponents[y + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[w + diceRolls[0]] == 1:
                                            opponents[w + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        player[x] -= 1
                                        player[diceRolls[0] -1] += 1
                                        player[y] -= 1
                                        player[y + diceRolls[0]] += 1
                                        player[z] -= 1
                                        player[z + diceRolls[0]] += 1
                                        player[w] -= 1
                                        player[w + diceRolls[0]] += 1
                                        possibleStates.append(newState)
                                    newState = self.copy()
                                    player = newState[0]
                                    prison = self[0][cf.PRISON]
                                    opponents = newState[1]
                                    if w + diceRolls[0] < 24 and y + diceRolls[0] + diceRolls[0] < 24 and opponents[y + diceRolls[0]] < 2 and opponents[y + diceRolls[0] + diceRolls[0]] < 2 and opponents[w + diceRolls[0]] < 2:
                                        if opponents[diceRolls[0] - 1] == 1:
                                            opponents[diceRolls[0] - 1] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[y + diceRolls[0]] == 1:
                                            opponents[y + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[y + diceRolls[0] + diceRolls[0]] == 1:
                                            opponents[y + diceRolls[0] + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[w + diceRolls[0]] == 1:
                                            opponents[w + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        player[x] -= 1
                                        player[diceRolls[0] - 1] += 1
                                        player[y] -= 1
                                        player[y + diceRolls[0] + diceRolls[0]] += 1
                                        player[w] -= 1
                                        player[w + diceRolls[0]] += 1
                                        possibleStates.append(newState)

                                # move three different tokens that are not of prison
                                newState = self.copy()
                                player = newState[0]
                                prison = self[0][cf.PRISON]
                                opponents = newState[1]
                                if x != y and x != z and x != w and y != z and y != w and z != w and y + diceRolls[0] < 24 and z + diceRolls[0] < 24 and w + diceRolls[0] < 24 and opponents[y + diceRolls[0]] < 2 and opponents[z + diceRolls[0]] < 2 and opponents[w + diceRolls[0]] < 2:
                                    if opponents[diceRolls[0] -1] == 1:
                                        opponents[diceRolls[0] -1] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[y + diceRolls[0]] == 1:
                                        opponents[y + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[z + diceRolls[0]] == 1:
                                        opponents[z + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[w + diceRolls[0]] == 1:
                                        opponents[w + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    player[diceRolls[0] -1] += 1
                                    player[x] -= 1
                                    player[y + diceRolls[0]] += 1
                                    player[y] -= 1
                                    player[z + diceRolls[0]] += 1
                                    player[z] -= 1
                                    player[w + diceRolls[0]] += 1
                                    player[w] -= 1
                                    possibleStates.append(newState)

                                #move the token that are moved out of prison:
                                    #move prison token twice and two other different tokens
                                newState = self.copy()
                                player = newState[0]
                                prison = self[0][cf.PRISON]
                                opponents = newState[1]
                                if x == y and x != z and x != w and z != w and w + diceRolls[0] < 24 and z + diceRolls[0] < 24 and opponents[diceRolls[0] + diceRolls[0] -1] < 2 and opponents[z + diceRolls[0]] < 2 and opponents[w + diceRolls[0]] < 2:
                                    if opponents[diceRolls[0] -1] == 1:
                                        opponents[diceRolls[0] -1] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[diceRolls[0] + diceRolls[0] -1] == 1:
                                        opponents[diceRolls[0] + diceRolls[0] -1] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[z + diceRolls[0]] == 1:
                                        opponents[z + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[w + diceRolls[0]] == 1:
                                        opponents[w + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    player[diceRolls[0] + diceRolls[0] -1] += 1
                                    player[x] -= 1
                                    player[z + diceRolls[0]] += 1
                                    player[z] -= 1
                                    player[w + diceRolls[0]] += 1
                                    player[w] -= 1
                                    possibleStates.append(newState)
                                if x == y and x != z and z == w:
                                    newState = self.copy()
                                    player = newState[0]
                                    prison = self[0][cf.PRISON]
                                    opponents = newState[1]
                                    # move prison token twice and one other different tokens from same position twice
                                    if opponents[diceRolls[0] + diceRolls[0] -1] < 2 and z + diceRolls[0] + diceRolls[0] < 24 and opponents[z + diceRolls[0]] < 2 and opponents[z + diceRolls[0] + diceRolls[0]] < 2:
                                        if opponents[diceRolls[0] -1] == 1:
                                            opponents[diceRolls[0] -1] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[diceRolls[0] + diceRolls[0] -1] == 1:
                                            opponents[diceRolls[0] + diceRolls[0] -1] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[z + diceRolls[0]] == 1:
                                            opponents[z + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[w + diceRolls[0] + diceRolls[0]] == 1:
                                            opponents[w + diceRolls[0] + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1

                                        possibleStates.append(newState)
                                    newState = self.copy()
                                    player = newState[0]
                                    prison = self[0][cf.PRISON]
                                    opponents = newState[1]
                                    # move prison token twice and two other different tokens from same position
                                    if z + diceRolls[0] < 24 and player[z] > 1 and opponents[diceRolls[0] + diceRolls[0] -1] < 2 and opponents[z + diceRolls[0]] < 2:
                                        if opponents[diceRolls[0] -1] == 1:
                                            opponents[diceRolls[0] -1] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[diceRolls[0] + diceRolls[0] -1] == 1:
                                            opponents[diceRolls[0] + diceRolls[0] -1] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[z + diceRolls[0]] == 1:
                                            opponents[z + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        player[diceRolls[0] + diceRolls[0] - 1] += 1
                                        player[x] -= 1
                                        player[z + diceRolls[0]] += 1
                                        player[z] -= 1
                                        player[w + diceRolls[0]] += 1
                                        player[w] -= 1
                                #move the token in prison twice and (two other different from eachother) (two other from same position) (two times from one posisition)
                                #move the token in prison three times and another
                                if x == y and x == z and x != w:
                                    newState = self.copy()
                                    player = newState[0]
                                    prison = self[0][cf.PRISON]
                                    opponents = newState[1]
                                    if w + diceRolls[0] < 24 and opponents[diceRolls[0] + diceRolls[0] -1] < 2 and opponents[diceRolls[0] + diceRolls[0] + diceRolls[0] -1] < 2 and opponents[w + diceRolls[0]] < 2:
                                        if opponents[diceRolls[0] -1] == 1:
                                            opponents[diceRolls[0] -1] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[diceRolls[0] + diceRolls[0] -1] == 1:
                                            opponents[diceRolls[0] + diceRolls[0] -1] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[diceRolls[0] + diceRolls[0] + diceRolls[0] -1] == 1:
                                            opponents[diceRolls[0] + diceRolls[0] + diceRolls[0] -1] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[w + diceRolls[0]] == 1:
                                            opponents[w + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        player[diceRolls[0] + diceRolls[0] + diceRolls[0] - 1] += 1
                                        player[x] -= 1
                                        player[w + diceRolls[0]] += 1
                                        player[w] -= 1

                        else:
                            # TODO: move (two token from same pos or move token twice) and two other tokens
                            newState = self.copy()
                            player = newState[0]
                            opponents = newState[1]
                            if x == y and x != z and x != w and z != w:
                                if player[x] > 1 and x + diceRolls[0] < 24 and z + diceRolls[0] < 24 and w + diceRolls[0] < 24 and opponents[x + diceRolls[0]] < 2 and opponents[z + diceRolls[0]] < 2 and opponents[w + diceRolls[0]] < 2:
                                    if opponents[x + diceRolls[0]] == 1:
                                        opponents[x + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[z + diceRolls[0]] == 1:
                                        opponents[z + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[w + diceRolls[0]] == 1:
                                        opponents[w + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    player[x + diceRolls[0]] += 1
                                    player[x] -= 1
                                    player[y + diceRolls[0]] += 1
                                    player[y] -= 1
                                    player[z + diceRolls[0]] += 1
                                    player[z] -= 1
                                    player[w + diceRolls[0]] += 1
                                    player[w] -= 1
                                    possibleStates.append(newState)
                                newState = self.copy()
                                player = newState[0]
                                opponents = newState[1]
                                if z + diceRolls[0] < 24 and x + diceRolls[0] + diceRolls[0] < 24 and w + diceRolls[0] < 24 and opponents[x + diceRolls[0]] < 2 and opponents[x + diceRolls[0] + diceRolls[0]] < 2 and opponents[z + diceRolls[0]] < 2 and opponents[w + diceRolls[0]] < 2:
                                    if opponents[x + diceRolls[0]] == 1:
                                        opponents[x + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[x + diceRolls[0] + diceRolls[0]] == 1:
                                        opponents[x + diceRolls[0] + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[z + diceRolls[0]] == 1:
                                        opponents[z + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[w + diceRolls[0]] == 1:
                                        opponents[w + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    player[x + diceRolls[0] + diceRolls[0]] += 1
                                    player[x] -= 1
                                    player[z + diceRolls[0]] += 1
                                    player[z] -= 1
                                    player[w + diceRolls[0]] += 1
                                    player[w] -= 1
                                    possibleStates.append(newState)

                            # TODO: move two tokens in pairs or all tokens from same pos or one token four times from one pos
                            if x == y and z == w:
                                newState = self.copy()
                                player = newState[0]
                                opponents = newState[1]
                                if x != z:
                                    if player[x] > 1 and z + diceRolls[0] < 24 and player[z] > 1 and x + diceRolls[0] < 24 and opponents[x + diceRolls[0]] < 2 and opponents[z + diceRolls[0]] < 2:
                                        if opponents[x + diceRolls[0]] == 1:
                                            opponents[x + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[z + diceRolls[0]] == 1:
                                            opponents[z + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        player[x + diceRolls[0]] += 1
                                        player[x] -= 1
                                        player[y + diceRolls[0]] += 1
                                        player[y] -= 1
                                        player[z + diceRolls[0]] += 1
                                        player[z] -= 1
                                        player[w + diceRolls[0]] += 1
                                        player[w] -= 1
                                        possibleStates.append(newState)
                                    newState = self.copy()
                                    player = newState[0]
                                    opponents = newState[1]
                                    if z + diceRolls[0] + diceRolls[0] < 24 and x + diceRolls[0] + diceRolls[0] < 24 and opponents[x + diceRolls[0]] < 2 and opponents[x + diceRolls[0] + diceRolls[0]] < 2 and opponents[z + diceRolls[0]] < 2 and opponents[z + diceRolls[0] + diceRolls[0]] < 2:
                                        if opponents[x + diceRolls[0]] == 1:
                                            opponents[x + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[x + diceRolls[0] + diceRolls[0]] == 1:
                                            opponents[x + diceRolls[0] + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[z + diceRolls[0]] == 1:
                                            opponents[z + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[z + diceRolls[0] + diceRolls[0]] == 1:
                                            opponents[z + diceRolls[0] + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        player[x + diceRolls[0] + diceRolls[0]] += 1
                                        player[x] -= 1
                                        player[z + diceRolls[0] + diceRolls[0]] += 1
                                        player[z] -= 1
                                        possibleStates.append(newState)
                                elif x == z:
                                    if player[x] > 3 and x + diceRolls[0] < 24 and z + diceRolls[0] < 24 and opponents[x + diceRolls[0]] < 2 and opponents[z + diceRolls[0]] < 2:
                                        if opponents[x + diceRolls[0]] == 1:
                                            opponents[x + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        player[x + diceRolls[0]] += 1
                                        player[x] -= 1
                                        player[y + diceRolls[0]] += 1
                                        player[y] -= 1
                                        player[z + diceRolls[0]] += 1
                                        player[z] -= 1
                                        player[w + diceRolls[0]] += 1
                                        player[w] -= 1
                                        possibleStates.append(newState)
                                    newState = self.copy()
                                    player = newState[0]
                                    opponents = newState[1]
                                    if x == z and x + diceRolls[0] + diceRolls[0] + diceRolls[0] + diceRolls[0] < 24 and opponents[x + diceRolls[0]] < 2 and opponents[x + diceRolls[0] + diceRolls[0]] < 2 and opponents[x + diceRolls[0] + diceRolls[0] + diceRolls[0]] < 2 and opponents[x + diceRolls[0] + diceRolls[0] + diceRolls[0] + diceRolls[0]] < 2:
                                        if opponents[x + diceRolls[0]] == 1:
                                            opponents[x + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[x + diceRolls[0] + diceRolls[0]] == 1:
                                            opponents[x + diceRolls[0] + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[x + diceRolls[0] + diceRolls[0] + diceRolls[0]] == 1:
                                            opponents[x + diceRolls[0] + diceRolls[0] + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        if opponents[x + diceRolls[0] + diceRolls[0] + diceRolls[0] + diceRolls[0]] == 1:
                                            opponents[x + diceRolls[0] + diceRolls[0] + diceRolls[0] + diceRolls[0]] -= 1
                                            opponents[cf.PRISON] += 1
                                        player[x] -= 1
                                        player[x + diceRolls[0] + diceRolls[0] + diceRolls[0] + diceRolls[0]] += 1
                                        possibleStates.append(newState)

                            # TODO: move token from the same pos three times and one other pos
                            if x == y and x == z and x != w:
                                newState = self.copy()
                                player = newState[0]
                                opponents = newState[1]
                                if player[x] > 2 and x + diceRolls[0] < 24 and w + diceRolls[0] < 24 and opponents[x + diceRolls[0]] < 2 and opponents[w + diceRolls[0]] < 2:
                                    if opponents[x + diceRolls[0]] == 1:
                                        opponents[x + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[w + diceRolls[0]] == 1:
                                        opponents[w + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    player[x + diceRolls[0]] += 1
                                    player[x] -= 1
                                    player[y + diceRolls[0]] += 1
                                    player[y] -= 1
                                    player[z + diceRolls[0]] += 1
                                    player[z] -= 1
                                    player[w + diceRolls[0]] += 1
                                    player[w] -= 1
                                    possibleStates.append(newState)
                                newState = self.copy()
                                player = newState[0]
                                opponents = newState[1]
                                if x + diceRolls[0] + diceRolls[0] + diceRolls[0] < 24 and w + diceRolls[0] < 24 and opponents[x + diceRolls[0]] < 2 and opponents[x + diceRolls[0] + diceRolls[0]] < 2 and opponents[x + diceRolls[0] + diceRolls[0]] + diceRolls[0] < 2 and opponents[w + diceRolls[0]] < 2:
                                    if opponents[x + diceRolls[0]] == 1:
                                        opponents[x + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[x + diceRolls[0] + diceRolls[0]] == 1:
                                        opponents[x + diceRolls[0] + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[x + diceRolls[0] + diceRolls[0] + diceRolls[0]] == 1:
                                        opponents[x + diceRolls[0] + diceRolls[0] + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[w + diceRolls[0]] == 1:
                                        opponents[w + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    player[x + diceRolls[0] + diceRolls[0] + diceRolls[0]] += 1
                                    player[x] -= 1
                                    player[w + diceRolls[0]] += 1
                                    player[w] -= 1
                                    possibleStates.append(newState)
                                newState = self.copy()
                                player = newState[0]
                                opponents = newState[1]
                                if player[x] > 1 and x + diceRolls[0] + diceRolls[0] < 24 and z + diceRolls[0] < 24 and w + diceRolls[0] < 24 and opponents[x + diceRolls[0]] < 2 and opponents[x + diceRolls[0] + diceRolls[0]] < 2 and opponents[w + diceRolls[0]] < 2:
                                    if opponents[x + diceRolls[0]] == 1:
                                        opponents[x + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[x + diceRolls[0] + diceRolls[0]] == 1:
                                        opponents[x + diceRolls[0] + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    if opponents[w + diceRolls[0]] == 1:
                                        opponents[w + diceRolls[0]] -= 1
                                        opponents[cf.PRISON] += 1
                                    player[x + diceRolls[0] + diceRolls[0]] += 1
                                    player[x] -= 1
                                    player[z + diceRolls[0]] += 1
                                    player[z] -= 1
                                    player[w + diceRolls[0]] += 1
                                    player[w] -= 1
                                    possibleStates.append(newState)
                            # Move four different tokens
                            newState = self.copy()
                            player = newState[0]
                            opponents = newState[1]
                            if x != y and x != z and x != w and y != z and y != w and z != w and x + diceRolls[0] < 24 and opponents[x + diceRolls[0]] < 2 \
                                    and y + diceRolls[0] < 24 and opponents[y + diceRolls[0]] < 2 \
                                    and z + diceRolls[0] < 24 and opponents[z + diceRolls[0]] < 2 \
                                    and w + diceRolls[0] < 24 and opponents[w + diceRolls[0]] < 2:
                                if opponents[x + diceRolls[0]] == 1:
                                    opponents[x + diceRolls[0]] -= 1
                                    opponents[cf.PRISON] += 1
                                if opponents[y + diceRolls[0]] == 1:
                                    opponents[y + diceRolls[0]] -= 1
                                    opponents[cf.PRISON] += 1
                                if opponents[z + diceRolls[0]] == 1:
                                    opponents[z + diceRolls[0]] -= 1
                                    opponents[cf.PRISON] += 1
                                if opponents[w + diceRolls[0]] == 1:
                                    opponents[w + diceRolls[0]] -= 1
                                    opponents[cf.PRISON] += 1
                                player[x + diceRolls[0]] += 1
                                player[x] -= 1
                                player[y + diceRolls[0]] += 1
                                player[y] -= 1
                                player[z + diceRolls[0]] += 1
                                player[z] -= 1
                                player[w + diceRolls[0]] += 1
                                player[w] -= 1
                                possibleStates.append(newState)
                            # TODO move same token serveral time
                            # two, three, four time.
                            # at two times more two different to eachother tokens
                            # TODO move two different tokens two times
        return np.asarray(possibleStates)

    def moveToken(self, diceRolls):
        '''
        :param diceRolls: Two values between 1 and 6 on a list
        :return:
        '''
        # diceRolls is a list of the two dice rolls
        possibleStates = []
        indices = np.where(self[0] > 0)[0]
        prison = self[0][cf.PRISON]
        opponents = self[1]
        if prison > 0 and (opponents[diceRolls[0] - 1] > 1 and opponents[diceRolls[1] - 1] > 1):
            return np.asarray(possibleStates)
        for x in indices:
            for y in indices:
                newState = self.copy()
                player = newState[0]
                opponents = newState[1]

                firstTargetPos = x + diceRolls[0]
                secondTargetPos = y + diceRolls[1]

                if x == cf.GOAL or y == cf.GOAL:
                    continue

                prison = self[0][cf.PRISON]
                # If more than one of the tokens are in "prison"
                if prison > 1:
                    # If it is not both of the tokens, no move possible
                    if not (x == cf.PRISON and y == cf.PRISON):
                        continue
                    else:
                        if opponents[diceRolls[0] - 1] > 1 or opponents[diceRolls[1] - 1] > 1:
                            continue
                        if opponents[diceRolls[0] - 1] == 1:
                            opponents[diceRolls[0] - 1] -= 1
                            opponents[cf.PRISON] += 1
                        if opponents[diceRolls[1] - 1] == 1:
                            opponents[diceRolls[1] - 1] -= 1
                            opponents[cf.PRISON] += 1
                        player[diceRolls[0] - 1] += 1
                        player[cf.PRISON] -= 1
                        player[diceRolls[1] - 1] += 1
                        player[cf.PRISON] -= 1
                        possibleStates.append(newState)

                # If only one of the tokens are in "prison"
                elif prison == 1:
                    # If it is not one of the tokens, no move possible
                    if not (x == cf.PRISON or y == cf.PRISON):
                        continue
                    elif x == y:
                        if opponents[diceRolls[0] - 1] < 2 and opponents[diceRolls[0] - 1 + diceRolls[1]] < 2:
                            if opponents[diceRolls[0] - 1] == 1:
                                opponents[diceRolls[0] - 1] -= 1
                                opponents[cf.PRISON] += 1
                            if opponents[diceRolls[0] - 1 + diceRolls[1]] == 1:
                                opponents[diceRolls[0] - 1 + diceRolls[1]] -= 1
                                opponents[cf.PRISON] += 1
                            player[diceRolls[0] - 1 + diceRolls[1]] += 1
                            player[cf.PRISON] -= 1
                            possibleStates.append(newState)
                        newState = self.copy()
                        player = newState[0]
                        opponents = newState[1]
                        if opponents[diceRolls[1] - 1] < 2 and opponents[diceRolls[1] - 1 + diceRolls[0]] < 2:
                            if opponents[diceRolls[1] - 1] == 1:
                                opponents[diceRolls[1] - 1] -= 1
                                opponents[cf.PRISON] += 1
                            if opponents[diceRolls[1] - 1 + diceRolls[0]] == 1:
                                opponents[diceRolls[1] - 1 + diceRolls[0]] -= 1
                                opponents[cf.PRISON] += 1
                            player[diceRolls[1] - 1 + diceRolls[0]] += 1
                            player[cf.PRISON] -= 1
                            possibleStates.append(newState)
                    else:
                        if x == cf.PRISON:
                            if secondTargetPos > 23:
                                continue
                            if opponents[diceRolls[0] - 1] > 1 or opponents[secondTargetPos] > 1:
                                continue
                            if opponents[diceRolls[0] - 1] == 1:
                                opponents[diceRolls[0] - 1] -= 1
                                opponents[cf.PRISON] += 1
                            if opponents[secondTargetPos] == 1:
                                opponents[secondTargetPos] -= 1
                                opponents[cf.PRISON] += 1

                            player[diceRolls[0] - 1] += 1
                            player[cf.PRISON] -= 1
                            player[secondTargetPos] += 1
                            player[y] -= 1
                            possibleStates.append(newState)
                        else:
                            if firstTargetPos > 23:
                                continue
                            if opponents[firstTargetPos] > 1 or opponents[diceRolls[1] - 1] > 1:
                                continue
                            if opponents[firstTargetPos] == 1:
                                opponents[firstTargetPos] -= 1
                                opponents[cf.PRISON] += 1
                            if opponents[diceRolls[1] - 1] == 1:
                                opponents[diceRolls[1] - 1] -= 1
                                opponents[cf.PRISON] += 1
                            player[firstTargetPos] += 1
                            player[x] -= 1
                            player[diceRolls[1] - 1] += 1
                            player[cf.PRISON] -= 1
                            possibleStates.append(newState)
                else:
                    if x == y:
                        if firstTargetPos < 24 and opponents[firstTargetPos] < 2 \
                                and firstTargetPos + diceRolls[1] < 24 and opponents[firstTargetPos + diceRolls[1]] < 2:
                            if opponents[firstTargetPos] == 1:
                                opponents[firstTargetPos] -= 1
                                opponents[cf.PRISON] += 1
                            if opponents[firstTargetPos + diceRolls[1]] == 1:
                                opponents[firstTargetPos + diceRolls[1]] -= 1
                                opponents[cf.PRISON] += 1
                            player[firstTargetPos + diceRolls[1]] += 1
                            player[x] -= 1
                            possibleStates.append(newState)
                        newState = self.copy()
                        player = newState[0]
                        opponents = newState[1]
                        if secondTargetPos < 24 and opponents[secondTargetPos] < 2 \
                                and secondTargetPos + diceRolls[0] < 24 and opponents[
                            secondTargetPos + diceRolls[0]] < 2:
                            if opponents[secondTargetPos] == 1:
                                opponents[secondTargetPos] -= 1
                                opponents[cf.PRISON] += 1
                            if opponents[secondTargetPos + diceRolls[0]] == 1:
                                opponents[secondTargetPos + diceRolls[0]] -= 1
                                opponents[cf.PRISON] += 1
                            player[secondTargetPos + diceRolls[0]] += 1
                            player[x] -= 1
                            possibleStates.append(newState)
                    newState = self.copy()
                    player = newState[0]
                    opponents = newState[1]
                    if firstTargetPos > 23 or opponents[firstTargetPos] > 1 or secondTargetPos > 23 or opponents[
                        secondTargetPos] > 1:
                        continue
                    if x == y and player[x] < 2:
                        continue
                    # Check for opponent occupied by spaces
                    if opponents[firstTargetPos] == 1:
                        opponents[firstTargetPos] -= 1
                        opponents[cf.PRISON] += 1
                    if opponents[secondTargetPos] == 1:
                        opponents[secondTargetPos] -= 1
                        opponents[cf.PRISON] += 1
                    player[firstTargetPos] += 1
                    player[x] -= 1
                    player[secondTargetPos] += 1
                    player[y] -= 1
                    possibleStates.append(newState)

        return np.asarray(possibleStates)

    def moveTokenHome(self, diceRolls):
        '''
        :param diceRolls: Two values between 1 and 6 on a list
        :return:
        '''
        # diceRolls is a list of the two dice rolls
        possibleStates = []
        indices = np.where(self[0] > 0)[0]
        minPos = np.min(indices)
        for x in indices:
            for y in indices:
                firstTargetPos = x + diceRolls[0]
                secondTargetPos = y + diceRolls[1]
                if x == cf.GOAL or y == cf.GOAL:
                    continue
                newState = self.copy()
                player = newState[0]
                opponents = newState[1]

                if x == y:
                    # MOVE THEN HOME x2

                    if (firstTargetPos < 24 and opponents[firstTargetPos] < 2) \
                            and ((12 - (firstTargetPos - 12)) == diceRolls[1]
                                 or (firstTargetPos == minPos and firstTargetPos +
                                     diceRolls[1] > 23)):
                        if opponents[firstTargetPos] == 1:
                            opponents[firstTargetPos] -= 1
                            opponents[cf.PRISON] += 1
                        player[cf.GOAL] += 1
                        player[x] -= 1
                        possibleStates.append(newState)

                    newState = self.copy()
                    player = newState[0]
                    opponents = newState[1]
                    if (secondTargetPos < 24 and opponents[secondTargetPos] < 2) \
                            and ((12 - (secondTargetPos - 12)) == diceRolls[0]
                                 or (firstTargetPos + diceRolls[0] == minPos and firstTargetPos +
                                     diceRolls[0] > 23)):
                        if opponents[secondTargetPos] == 1:
                            opponents[secondTargetPos] -= 1
                            opponents[cf.PRISON] += 1
                        player[cf.GOAL] += 1
                        player[y] -= 1
                        possibleStates.append(newState)

                    newState = self.copy()
                    player = newState[0]
                    opponents = newState[1]

                    # MOVE TWICE x2
                    if firstTargetPos < 24 and opponents[firstTargetPos] < 2 \
                            and firstTargetPos + diceRolls[1] < 24 and opponents[firstTargetPos + diceRolls[1]] < 2:
                        if opponents[firstTargetPos] == 1:
                            opponents[firstTargetPos] -= 1
                            opponents[cf.PRISON] += 1
                        if opponents[firstTargetPos + diceRolls[1]] == 1:
                            opponents[firstTargetPos + diceRolls[1]] -= 1
                            opponents[cf.PRISON] += 1
                        player[firstTargetPos + diceRolls[1]] += 1
                        player[x] -= 1
                        possibleStates.append(newState)
                    newState = self.copy()
                    player = newState[0]
                    opponents = newState[1]
                    if secondTargetPos < 24 and opponents[secondTargetPos] < 2 \
                            and secondTargetPos + diceRolls[0] < 24 and opponents[secondTargetPos + diceRolls[0]] < 2:
                        if opponents[secondTargetPos] == 1:
                            opponents[secondTargetPos] -= 1
                            opponents[cf.PRISON] += 1
                        if opponents[secondTargetPos + diceRolls[0]] == 1:
                            opponents[secondTargetPos + diceRolls[0]] -= 1
                            opponents[cf.PRISON] += 1
                        player[secondTargetPos + diceRolls[0]] += 1
                        player[x] -= 1
                        possibleStates.append(newState)

                newState = self.copy()
                player = newState[0]
                opponents = newState[1]

                if x == y and player[x] < 2:  # If there is less than 2 players
                    continue

                if ((12 - (x - 12)) == diceRolls[0]) or (x == minPos and x + diceRolls[0] > 23):
                    player[x] -= 1
                    player[cf.GOAL] += 1
                    if ((12 - (y - 12)) == diceRolls[1]) or (y == minPos and y + diceRolls[1] > 23):
                        player[y] -= 1
                        player[cf.GOAL] += 1
                        possibleStates.append(newState)

                    newState = self.copy()
                    player = newState[0]
                    opponents = newState[1]

                    player[x] -= 1
                    player[cf.GOAL] += 1
                    if secondTargetPos < 24 and opponents[secondTargetPos] < 2:
                        if opponents[secondTargetPos] == 1:
                            opponents[secondTargetPos] -= 1
                            opponents[cf.PRISON] += 1
                        player[secondTargetPos] += 1
                        player[y] -= 1
                        possibleStates.append(newState)

                newState = self.copy()
                player = newState[0]
                opponents = newState[1]

                if firstTargetPos < 24 and opponents[firstTargetPos] < 2:
                    if opponents[firstTargetPos] == 1:
                        opponents[firstTargetPos] -= 1
                        opponents[cf.PRISON] += 1
                    player[firstTargetPos] += 1
                    player[x] -= 1
                    if ((12 - (y - 12)) == diceRolls[1]) or (y == minPos and y + diceRolls[1] > 23):
                        player[y] -= 1
                        player[cf.GOAL] += 1
                        possibleStates.append(newState)

                    newState = self.copy()
                    player = newState[0]
                    opponents = newState[1]
                    if opponents[firstTargetPos] == 1:
                        opponents[firstTargetPos] -= 1
                        opponents[cf.PRISON] += 1
                    player[firstTargetPos] += 1
                    player[x] -= 1

                    if secondTargetPos < 24 and opponents[secondTargetPos] < 2:
                        if opponents[secondTargetPos] == 1:
                            opponents[secondTargetPos] -= 1
                            opponents[cf.PRISON] += 1
                        player[secondTargetPos] += 1
                        player[y] -= 1
                        possibleStates.append(newState)
        return np.asarray(possibleStates)

    def moveOneToken(self, diceRolls):
        possibleStates = []
        indices = np.where(self[0] > 0)[0]
        for x in indices:
            newState = self.copy()
            player = newState[0]
            opponents = newState[1]
            if x == cf.GOAL:
                continue
            if player[cf.PRISON] > 0 and x == cf.PRISON:
                if opponents[diceRolls[0] - 1] > 1:
                    continue
                if opponents[diceRolls[0] - 1] == 1:
                    opponents[diceRolls[0] - 1] -= 1
                    opponents[cf.PRISON] += 1
                player[diceRolls[0] - 1] += 1
                player[cf.PRISON] -= 1
                possibleStates.append(newState)
            elif player[cf.PRISON] == 0:
                targetPos = x + diceRolls[0]
                if targetPos < 24 and opponents[targetPos] < 2:
                    if opponents[targetPos] == 1:
                        opponents[targetPos] -= 1
                        opponents[cf.PRISON] += 1
                    player[targetPos] += 1
                    player[x] -= 1
                    possibleStates.append(newState)

        for y in indices:
            newState = self.copy()
            player = newState[0]
            opponents = newState[1]
            if y == cf.GOAL:
                continue
            if player[cf.PRISON] > 0 and y == cf.PRISON:
                if opponents[diceRolls[1] - 1] > 1:
                    continue
                if opponents[diceRolls[1] - 1] == 1:
                    opponents[diceRolls[1] - 1] -= 1
                    opponents[cf.PRISON] += 1
                player[diceRolls[1] - 1] += 1
                player[cf.PRISON] -= 1
                possibleStates.append(newState)
            elif player[cf.PRISON] == 0:
                targetPos = y + diceRolls[1]
                if targetPos < 24 and opponents[targetPos] < 2:
                    if opponents[targetPos] == 1:
                        opponents[targetPos] -= 1
                        opponents[cf.PRISON] += 1
                    player[targetPos] += 1
                    player[y] -= 1
                    possibleStates.append(newState)

        return np.asarray(possibleStates)

    def moveOneTokenHome(self, diceRolls):
        '''
        :param diceRolls: Two values between 1 and 6 on a list
        :return:
        '''
        possibleStates = []
        indices = np.where(self[0] > 0)[0]
        minPos = np.min(indices)
        for x in indices:
            if x == cf.GOAL:
                continue
            newState = self.copy()
            player = newState[0]
            opponents = newState[1]
            targetPos = x + diceRolls[0]

            if ((12 - (x - 12)) == diceRolls[0]) or (x == minPos and x + diceRolls[0] > 23):
                player[x] -= 1
                player[cf.GOAL] += 1
                possibleStates.append(newState)

            newState = self.copy()
            player = newState[0]
            opponents = newState[1]

            if targetPos < 24 and opponents[targetPos] < 2:
                if opponents[targetPos] == 1:
                    opponents[targetPos] -= 1
                    opponents[cf.PRISON] += 1
                player[targetPos] += 1
                player[x] -= 1
                possibleStates.append(newState)

        for y in indices:
            if y == cf.GOAL:
                continue
            newState = self.copy()
            player = newState[0]
            opponents = newState[1]

            targetPos = y + diceRolls[1]

            if ((12 - (y - 12)) == diceRolls[1]) or (y == minPos and y + diceRolls[1] > 23):
                player[y] -= 1
                player[cf.GOAL] += 1
                possibleStates.append(newState)

            newState = self.copy()
            player = newState[0]
            opponents = newState[1]

            if targetPos < 24 and opponents[targetPos] < 2:
                if opponents[targetPos] == 1:
                    opponents[targetPos] -= 1
                    opponents[cf.PRISON] += 1
                player[targetPos] += 1
                player[y] -= 1
                possibleStates.append(newState)
        return np.asarray(possibleStates)

    def getWinner(self):
        '''
        :return: Winner of the game
        '''
        for player_id in range(2):
            if self[player_id][cf.GOAL] == 15:
                return player_id
        return -1


class Game:
    def __init__(self, players, state=None):
        assert len(players) == 2, "There must be 2 players in the game"
        self.players = players
        self.currentPlayerId = -1
        self.state = GameState() if state is None else state
        self.stepCount = 0

    @staticmethod
    def trimStates(possibleStates):
        # TODO Optimize the code if possible
        # nowTime = time.time()
        if len(possibleStates) == 0:
            return possibleStates
        states = []
        for x in range(len(possibleStates)):
            if not possibleStates[x] in states:
                states.append(possibleStates[x])
        # print("TimeList:", (time.time() - nowTime))
        # print("DIFF:", len(possibleStates)-len(states))
        return np.asarray(states)

    @staticmethod
    def getRelativeStates(currentState, diceRolls):
        relativeNextStates = []
        if not sum(currentState[0][0:26:1]) == 15:
            print(sum(currentState[0][0:26:1]))
        if sum(currentState[0][18:25:1]) == 15:
            relativeNextStates = currentState.moveTokenHome(diceRolls)

            if not len(relativeNextStates):
                relativeNextStates = currentState.moveOneTokenHome(diceRolls)
        else:
            if diceRolls[0] == diceRolls[1]:
                relativeNextStates = currentState.moveFourToken(diceRolls)

            if not len(relativeNextStates) or diceRolls[0] != diceRolls[1]:
                relativeNextStates = currentState.moveToken(diceRolls)

            if not len(relativeNextStates):
                relativeNextStates = currentState.moveOneToken(diceRolls)
        return relativeNextStates

    def step(self, debug=False):
        state = self.state
        self.currentPlayerId = (self.currentPlayerId + 1) % 2
        player = self.players[self.currentPlayerId]
        diceRolls = [random.randint(1, 6), random.randint(1, 6)]
        #TODO inserted that allwasys double hit
        diceRolls[1] = diceRolls[0]
        if debug:
            playerName = "red" if self.currentPlayerId == 1 else "blue"
            print("Player: ", playerName)
            print("Dice Rolls", diceRolls)
        relativeState = state.getStateRelativeToPlayer(self.currentPlayerId)
        # print(player.name, relativeState.state)

        relativeNextStates = Game.getRelativeStates(relativeState, diceRolls)
        if relativeNextStates.size > 0:
            nextStateID = player.play(relativeState, diceRolls, relativeNextStates)
            if not nextStateID > - 1:
                return
            if nextStateID > relativeNextStates.size - 1:
                logging.warning("Player chose invalid move. Choosing first valid move.")
                nextStateID = relativeNextStates[0]
            self.state = relativeNextStates[nextStateID].getStateRelativeToPlayer((-self.currentPlayerId) % 2)
            print("Player 1",  " State: ", self.state[0])
            print("Player 2", " State: ", self.state[1])

    def playFullGame(self):
        while self.state.getWinner() == -1:
            print("Player 1", " State: ", self.state[0])
            print("Player 2", " State: ", self.state[1])
            self.step()
            self.stepCount += 1
        if (self.players[0].name == "monte-carlo" or self.players[1].name == "monte-carlo"):
            print(self.stepCount)

        return self.state.getWinner()
