import os
import pyglet
from pyglet.window import key
from pygammon.config import VISUALIZER, playerColors, GOAL, PRISON
from pygammon.game import GameState


class Visualizer(pyglet.window.Window):
    def __init__(self, state=None):
        super(Visualizer, self).__init__()

        self.state = GameState() if state is None else state
        self.set_maximum_size(664, 454)
        self.set_minimum_size(664, 454)
        self.width, self.height = 664, 454 #VISUALIZER["CANVAS_SIZE"]
        bg_img = self.load_img(VISUALIZER["BOARD"])

        self.scaling = min(bg_img.height, self.height) / max(bg_img.height, self.height)

        # load sprites
        self.backgroundSprite = self.load_sprite(VISUALIZER["BOARD"])
        self.playerSprites = [self.load_sprite(color + "Player.png") for color in playerColors]

        self.switch_to()
        self.dispatch_event("on_draw")
        self.dispatch_events()
        self.flip()

    def index_to_pixels(self, index, numTokens, player):
        x = 0
        y = 0
        if index < 6:
            x = 663
            x -= index * 50 + 52
            y = 7 + (numTokens*10)
        elif index < 12:
            x = 663
            x -= index * 50 + 102
            y = 7 + (numTokens*10)
        elif index < 18:
            y = 454
            x = (index-12) * 50 + 12
            y -= 47 + (numTokens*10)
        elif index < 24:
            y = 454
            x = (index-12) * 50 + 62
            y -= 47 + (numTokens*10)
        elif index == PRISON:
            x = int(663 / 2) - 20
            if player == 0:
                y = 453 - 7 - 40 - (numTokens*10)
            else:
                y = 7 + (numTokens*10)

        return x, y

    def on_draw(self):
        self.clear()
        self.backgroundSprite.draw()
        for i in range(2):
            sprite = self.playerSprites[i]
            for j in range(26):
                if j == GOAL:
                    continue
                if self.state[i][j] > 0:
                    for k in range(self.state[i][j]):
                        sprite.position = self.index_to_pixels(j, k, i)
                        sprite.draw()

    @staticmethod
    def load_img(local_path):
        assets_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
        dirname = os.path.dirname(__file__)
        return pyglet.image.load(os.path.join(assets_folder, local_path))

    def load_sprite(self, local_path):
        img = self.load_img(local_path)
        sprite = pyglet.sprite.Sprite(img)
        #sprite.scale = self.scaling
        return sprite

class VisualizerStep(Visualizer):
    def __init__(self, game):
        super(VisualizerStep, self).__init__()
        self.game = game
        self.states = [game.state]
        self.state_index = 0

    def on_key_press(self, symbol, _):
        if symbol == key.LEFT:
            self.state_index = max(0, self.state_index - 1)
        if symbol == key.RIGHT:
            self.state_index += 1
            while self.state_index >= len(self.states):
                self.game.step(True)
                self.states.append(self.game.state)
        self.state = self.states[self.state_index]