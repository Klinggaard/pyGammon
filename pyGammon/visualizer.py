import os
import pyglet
from pyglet.window import key
from pyGammon.config import VISUALIZER
from pyGammon.utils import playerColors
#TODO: Make a visualizer class which allows the game to be visualized whilst being played


class Visualizer(pyglet.window.Window):
    def __init__(self, state=None):
        super(Visualizer, self).__init__()

        # set scaling
        self.width, self.height = VISUALIZER["BORDER_SIZE"]
        self.load_img(VISUALIZER["BOARD"])
        self.scaling = VISUALIZER["POSITION_SCALE"]

        # load sprites
        self.backgroundSprite = self.load_sprite(VISUALIZER["BOARD"])
        self.playerSprites = [self.load_sprite(color + "Player.png") for color in playerColors]



    @staticmethod
    def load_img(local_path):
        assets_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
        return pyglet.image.load(os.path.join(assets_folder, local_path))

    def load_sprite(self, local_path):
        img = self.load_img(local_path)
        sprite = pyglet.sprite.Sprite(img)
        sprite.scale = self.scaling
        return sprite
