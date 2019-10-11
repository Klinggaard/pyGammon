import random
import logging
import numpy as np
from pygammon.utils import playerColors


# noinspection PyPep8Naming
class GameState:
    def __init__(self, state=None, empty=False):
        if state is not None:
            self.state = state
        else:
            self.state = np.empty((2, 15), dtype=np.int)  # 2 players, 15 tokens per player
            if not empty:
                # Setup game
                self.state[0] = [18, 18, 18, 18, 18, 16, 16, 16, 11, 11, 11, 11, 11, 0, 0]
                self.state[1] = [5, 5, 5, 5, 5, 7, 7, 7, 12, 12, 12, 12, 12, 23, 23]


    def copy(self):
        return GameState(self.state.copy())

    def __getitem__(self, item):
        return self.state[item]

    def __setitem__(self, key, value):
        self.state[key] = value

    def __iter__(self):
        return self.state.__iter__()

    @staticmethod
    def getTokensRelativeToPlayer(tokens, playerID):
        if playerID is 0:
            return tokens
        relTokens = []
        for tokenID, tokenPos in enumerate(tokens):
            #print(tokenID, tokenPos)
            if tokenPos == -1 or tokenPos == 99:  # center and end pos are independent of player id
                relTokens.append(tokenPos)
            else:
                relTokens.append(11 - (tokenPos - 12))  # flips the list values, so 23 becomes 0
        return relTokens

    def getStateRelativeToPlayer(self, relativePlayerID):
        if relativePlayerID == 0:
            return GameState(self.state.copy())

        rel = GameState(empty=True)
        newPlayerIDs = [(x - relativePlayerID) % 2 for x in range(2)]
        for playerID, playerTokens in enumerate(self):
            newPlayerID = newPlayerIDs[playerID]
            rel[newPlayerID] = self.getTokensRelativeToPlayer(playerTokens, relativePlayerID)
        return rel

    def moveToken(self, firstTokenID, secondTokenID, diceRolls):
        # diceRolls is a list of the two dice rolls
        newState = self.copy()
        player = newState[0]
        opponents = newState[1]

        firstCurPos = self[0][firstTokenID]
        secondCurPos = self[0][secondTokenID]
        firstTargetPos = firstCurPos + diceRolls[0]
        secondTargetPos = secondCurPos + diceRolls[1]
        firstSpaceOccupants = opponents == firstTargetPos
        secondSpaceOccupants = opponents == secondTargetPos
        firstDieOccupants = opponents == diceRolls[0]-1  # Die Roll of one equal space 0
        secondDieOccupants = opponents == diceRolls[1]-1


        if np.sum(firstSpaceOccupants) > 1 or np.sum(secondSpaceOccupants) > 1:
            return False

        # One of the tokens in goal
        if firstCurPos == 99 or secondCurPos == 99:
            return False
        # One of the tokens in move past goal
        if firstTargetPos > 23 or secondTargetPos > 23:
            return False

        prison = sum(i == -1 for i in self[0])
        # TODO: Implement moving the same token twice
        if firstTokenID == secondTokenID:
            return False
        else:
            # If more than one of the tokens are in "prison"
            if prison > 1:
                # If it is not both of the tokens, no move possible
                if not self[0][firstTokenID] == -1 and self[0][secondTokenID] == -1:
                    return False
                else:
                    if np.sum(firstDieOccupants) > 1 or np.sum(secondDieOccupants) > 1:
                        return False
                    if np.sum(firstDieOccupants) == 1:
                        opponents[firstDieOccupants] = -1
                    if np.sum(secondDieOccupants) == 1:
                        opponents[secondDieOccupants] = -1
                    player[firstTokenID] = diceRolls[0]-1
                    player[secondTokenID] = diceRolls[1]-1

            # If only one of the tokens are in "prison"
            elif prison == 1:
                # If it is not one of the tokens, no move possible
                if not self[0][firstTokenID] == -1 or self[0][secondTokenID] == -1:
                    return False
                else:
                    if self[0][firstTokenID] == -1:
                        if np.sum(firstDieOccupants) > 1 or np.sum(secondSpaceOccupants) > 1:
                            return False
                        if np.sum(firstDieOccupants) == 1:
                            opponents[firstDieOccupants] = -1
                        if np.sum(secondSpaceOccupants) == 1:
                            opponents[secondSpaceOccupants] = -1

                        player[firstTokenID] = diceRolls[0] - 1
                        player[secondTokenID] = secondTargetPos
                    else:
                        if np.sum(firstSpaceOccupants) > 1 or np.sum(secondDieOccupants) > 1:
                            return False
                        if np.sum(firstSpaceOccupants) == 1:
                            opponents[firstSpaceOccupants] = -1
                        if np.sum(secondDieOccupants) == 1:
                            opponents[secondDieOccupants] = -1

                        player[firstTokenID] = firstTargetPos
                        player[secondTokenID] = diceRolls[1]-1
            else:
                # Check for opponent occupied by spaces
                if np.sum(firstSpaceOccupants) == 1:
                    opponents[firstSpaceOccupants] = -1
                if np.sum(secondSpaceOccupants) == 1:
                    opponents[secondSpaceOccupants] = -1
                player[firstTokenID] = firstTargetPos
                player[secondTokenID] = secondTargetPos

        return newState

    def moveTokenHome(self, firstTokenID, secondTokenID, diceRolls):
        # TODO: Implement the move tokens Home
        # diceRolls is a list of the two dice rolls
        firstCurPos = self[0][firstTokenID]
        secondCurPos = self[0][secondTokenID]
        if firstCurPos == 99 or secondCurPos == 99:
            return False
        newState = self.copy()
        player = newState[0]
        opponents = newState[1]
        player[firstTokenID] = 99
        player[secondTokenID] = 99

        return newState

    def getWinner(self):
        for player_id in range(2):
            if np.all(self[player_id] == 99):
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

        #TODO: Needs to handle if only one token can move
        if all(item >= 18 for item in relativeState[0]):
            relativeNextStates = np.array([
                relativeState.moveTokenHome(firstTokenID, secondTokenID, diceRolls) for firstTokenID in range(15) for
                secondTokenID in range(15)]
            )
        else:
            relativeNextStates = np.array([
                relativeState.moveToken(firstTokenID, secondTokenID, diceRolls) for firstTokenID in range(15) for secondTokenID in range(15)]
            )
        if np.any(relativeNextStates is not False):
            tokenID = player.play(relativeState, diceRolls, relativeNextStates)
            if not tokenID:
                return
            elif isinstance(tokenID, np.ndarray):
                tokenID = tokenID[0]
            elif relativeNextStates[tokenID] is False:
                logging.warning("Player chose invalid move. Choosing first valid move.")
                tokenID = np.argwhere(relativeNextStates is not False)[0][0]
            self.state = relativeNextStates[tokenID].getStateRelativeToPlayer((-self.currentPlayerId) % 2)
            #print("Player 1",  " State: ", self.state[0])
            #print("Player 2", " State: ", self.state[1])

    def playFullGame(self):
        while self.state.getWinner() == -1:
            print("Player 1", " State: ", self.state[0])
            print("Player 2", " State: ", self.state[1])
            self.step()
        return self.state.getWinner()


