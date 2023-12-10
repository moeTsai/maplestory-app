""""""

import threading
import time
import cv2
import inspect
import importlib
import traceback
from os.path import splitext, basename
from src.common import config, utils, utils_game
# from src.common.vkeys import press, click, key_down, key_up
from src.common.interfaces import Configurable


ROPES = [
    (0.756, 0.577),
    (0.513, 0.609),
    (0.416, 0.796),
]

class Bot():

    DEFAULT_CONFIG = {
        'Interact': 'y',
        'Feed pet': '9',
        'Jump': 'space',
    }

    def __init__(self):
        """initialize the bot class."""
        config.bot = self

        self.ready = False

        self.config = config.bot
        self.thread = threading.Thread(target=self._main)
        self.thread.daemon = True

    def start(self):
        """Start the bot."""

        print('\n[-] Started main bot loop')
        self.thread.start()

    def _get_player_pos(self):
        """Get the player's position in the world."""
        player_pos = config.capture.minimap['player_pos']
        px, py = player_pos
        return round(px, 3), round(py, 3)

    def _main(self):
        """The main bot loop."""

        # TODO setups

        
        # finish setup
        self.ready = True

        while True:
            # not enabled, sleep
            if not config.enabled:
                time.sleep(0.1)
                continue
            self._custom_f()

            time.sleep(5)


            # player_pos = self._get_player_pos()
            # print(player_pos[0], player_pos[1])
            
        


    def _custom_f(self):
        """Custom function to be executed by the bot."""
        utils_game.climb_robe(ROPES[0])
 
        time.sleep(0.1)

        pass