import random
import logging
import numpy as np
from pygammon import config as cf

# noinspection PyPep8Naming
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

    def getStateRelativeToPlayer(self, relativePlayerID):
        if relativePlayerID == 0:
            return GameState(self.state.copy())

        rel = GameState(empty=True)
        newPlayerIDs = 1
        rel0 = np.flip(self.state[1][0:24:1])
        rel[0] = np.append(rel0, self.state[1][24:26:1])
        rel1 = np.flip(self.state[0][0:24:1])
        rel[1] = np.append(rel1, self.state[0][24:26:1])
        return rel

    def moveToken(self, diceRolls):
        # TODO: Implement moving the same token twice
        # diceRolls is a list of the two dice rolls
        possibleStates = []
        indices = np.where(self[0] > 0)[0]
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
                        if opponents[diceRolls[0]-1] > 1 or opponents[diceRolls[1]-1] > 1:
                            continue
                        if opponents[diceRolls[0]-1] == 1:
                            opponents[diceRolls[0]-1] -= 1
                            opponents[cf.PRISON] += 1
                        if opponents[diceRolls[1]-1] == 1:
                            opponents[diceRolls[1] - 1] -= 1
                            opponents[cf.PRISON] += 1
                        player[diceRolls[0]-1] += 1
                        player[cf.PRISON] -= 1
                        player[diceRolls[1]-1] += 1
                        player[cf.PRISON] -= 1
                        possibleStates.append(newState)

                # If only one of the tokens are in "prison"
                elif prison == 1:
                    # If it is not one of the tokens, no move possible
                    if not (x == cf.PRISON or y == cf.PRISON):
                        continue
                    else:
                        if x == cf.PRISON:
                            if secondTargetPos > 23:
                                continue
                            if opponents[diceRolls[0]-1] > 1 or opponents[secondTargetPos] > 1:
                                continue
                            if opponents[diceRolls[0]-1] == 1:
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
                            if opponents[firstTargetPos] > 1 or opponents[diceRolls[1]-1] > 1:
                                continue
                            if opponents[firstTargetPos] == 1:
                                opponents[firstTargetPos] -= 1
                                opponents[cf.PRISON] += 1
                            if opponents[diceRolls[1]-1] == 1:
                                opponents[diceRolls[1] - 1] -= 1
                                opponents[cf.PRISON] += 1
                            player[firstTargetPos] += 1
                            player[x] -= 1
                            player[diceRolls[1] - 1] += 1
                            player[cf.PRISON] -= 1
                            possibleStates.append(newState)
                else:
                    if firstTargetPos > 23 or secondTargetPos > 23:
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
        # TODO: Return two states when tokenIds are the same
        # TODO: Can bear off the last relative to the goal with higher number.
        # diceRolls is a list of the two dice rolls
        possibleStates = []
        indices = np.where(self[0] > 0)[0]
        for x in indices:
            for y in indices:
                if x == cf.GOAL or y == cf.GOAL:
                    continue
                newState = self.copy()
                player = newState[0]
                opponents = newState[1]
                if x == y and player[x] < 2:
                    continue
                firstTargetPos = x + diceRolls[0]
                secondTargetPos = y + diceRolls[1]
                if firstTargetPos < 24:
                    opponents[firstTargetPos] = opponents[firstTargetPos]
                if secondTargetPos < 24:
                    opponents[secondTargetPos] = opponents[secondTargetPos]
                if (12 - (x-12)) == diceRolls[0]:
                    player[x] -= 1
                    player[cf.GOAL] += 1
                elif firstTargetPos < 24 and opponents[firstTargetPos] < 2:
                    if opponents[firstTargetPos] == 1:
                        opponents[firstTargetPos] -= 1
                        opponents[cf.PRISON] += 1
                    player[firstTargetPos] += 1
                    player[x] -= 1
                else:
                    continue

                if (12 - (y - 12)) == diceRolls[1]:
                    player[y] -= 1
                    player[cf.GOAL] += 1
                elif secondTargetPos < 24 and opponents[secondTargetPos] < 2:
                    if opponents[secondTargetPos] == 1:
                        opponents[secondTargetPos] -= 1
                        opponents[cf.PRISON] += 1
                    player[secondTargetPos] += 1
                    player[y] -= 1
                else:
                    continue
                possibleStates.append(newState)
        return np.asarray(possibleStates)

    def moveOneToken(self, diceRolls):
        # TODO: Implement this function
        newState = self.copy()
        player = newState[0]
        opponents = newState[1]
        for tokenID in range(15):
            curPos = self[0][tokenID]
            firstTargetPos = curPos + diceRolls[0]
            secondTargetPos = curPos + diceRolls[1]
            opponents[firstTargetPos] = opponents == firstTargetPos
            opponents[secondTargetPos] = opponents == secondTargetPos

    def moveOneTokenHome(self, diceRolls):
        # TODO: Implement this function
        newState = self.copy()
        player = newState[0]
        opponents = newState[1]
        for tokenID in range(15):
            curPos = self[0][tokenID]
            firstTargetPos = curPos + diceRolls[0]
            secondTargetPos = curPos + diceRolls[1]
            opponents[firstTargetPos] = opponents == firstTargetPos
            opponents[secondTargetPos] = opponents == secondTargetPos

    def getWinner(self):
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

    def step(self):
        state = self.state
        self.currentPlayerId = (self.currentPlayerId + 1) % 2
        player = self.players[self.currentPlayerId]

        diceRolls = [random.randint(1, 6), random.randint(1, 6)]
        relativeState = state.getStateRelativeToPlayer(self.currentPlayerId)

        if sum(relativeState[0][18:25:1]) == 15:
            relativeNextStates = relativeState.moveTokenHome(diceRolls)
            #if np.all(relativeNextStates is False):
            #    relativeNextStates = np.array(
            #        relativeState.moveOneTokenHome(diceRolls)
            #    )
        else:
            relativeNextStates = relativeState.moveToken(diceRolls)

            #if np.all(relativeNextStates is False):
            #    relativeNextStates = np.array(
            #        relativeState.moveOneToken(diceRolls)
            #    )

        if relativeNextStates.size > 0:
            nextStateID = player.play(relativeState, diceRolls, relativeNextStates)
            if not nextStateID > - 1:
                return
            if nextStateID > relativeNextStates.size - 1:
                logging.warning("Player chose invalid move. Choosing first valid move.")
                nextStateID = relativeNextStates[0]
            self.state = relativeNextStates[nextStateID].getStateRelativeToPlayer((-self.currentPlayerId) % 2)
            # print("Player 1",  " State: ", self.state[0])
            # print("Player 2", " State: ", self.state[1])

    def playFullGame(self):
        while self.state.getWinner() == -1:
            print("Player 1", " State: ", self.state[0])
            print("Player 2", " State: ", self.state[1])
            self.step()
        return self.state.getWinner()


