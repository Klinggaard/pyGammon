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
            # Setup game
            self.state = np.empty((2, 15), dtype=np.int)  # 2 players, 15 tokens per player
        if not empty:
            self.state.fill(-1)

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
            #TODO: add different states the tokens can be in
            print(tokenID, tokenPos)


    def getStateRelativeToPlayer(self, relativePlayerID):
        if relativePlayerID == 0:
            return self.copy()

        rel = GameState(empty=True)
        newPlayerIDs = [(x - relativePlayerID) % 2 for x in range(4)]
        for playerID, playerTokens in enumerate(self):
            newPlayerID = newPlayerIDs[playerID]
            rel[newPlayerID] = self.getTokensRelativeToPlayer(playerTokens, relativePlayerID)
        return rel

    def moveToken(self, tokenID, diceRolls):
        # diceRolls is a list of the two dice rolls
        # TODO: Implement moving system
        print("move")


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
        relativeNextStates = np.array([[
            relativeState.moveToken(tokenID, diceRolls) for tokenID in range(15)]]
        )
        if np.any(relativeNextStates is not False):
            tokenID = player.play(relativeState, diceRolls, relativeNextStates) # TODO: player.play()
            if isinstance(tokenID, np.ndarray):
                tokenID = tokenID[0]
            if relativeNextStates[tokenID] is False:
                logging.warning("Player chose invalid move. Choosing first valid move.")
                tokenID = np.argwhere(relativeNextStates is not False)[0][0]
            self.state = relativeNextStates[tokenID].getStateRelativeToPlayer((-self.currentPlayerId) % 2)

    # TODO: Implement playFullGame


