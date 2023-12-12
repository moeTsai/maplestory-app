""""""

import threading
import time
import cv2
import inspect
import importlib
import traceback
import importlib
from os.path import splitext, basename
from src.common import config
import user_var
from src.common.vkeys import press, click, key_down, key_up
from src.common.interfaces import Configurable


ROPES = [
    (0.756, 0.577),
    (0.513, 0.609),
    (0.416, 0.796),
]



class Bot():


    def __init__(self):
        """initialize the bot class."""
        config.bot = self

        self.ready = False

        self.repetative = user_var.repetative
        self.repeat_times = user_var.repeat_times
        self.hp_percent_to_fill = user_var.hp_percent_to_fill
        
        self.config = config.bot
        self.thread = threading.Thread(target=self._main)
        self.thread.daemon = True
        self.buff_time = 0

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
        config.listener.enabled = True

        repeat_times = self.repeat_times

        while True:
            # not enabled, sleep
            if config.enabled and not config.locked:
                repeat_times -= 1
                
                now = time.time()
                if self.buff_time == 0 or now - self.buff_time > 120:
                    press(user_var.DEFAULT_CONFIG['Buff'], 1)
                    time.sleep(0.1)
                    press(user_var.DEFAULT_CONFIG['Pets'], 1)
                    self.buff_time = now

                self.custom_function()
                
                # exit if not repetative or repeat_times == 0
                if not self.repetative or repeat_times == 0:
                    break

            time.sleep(0.01)


            # player_pos = self._get_player_pos()
            # print(player_pos[0], player_pos[1])
            
        

    
    def custom_function(self):
        """Custom function to be executed by the bot."""

        from src.routine import daemon_slime
        from src.common.utils_game import hp_fill
        
        hp_fill(self.hp_percent_to_fill)

        daemon_slime._main()

        # load the routine        
        # routine = importlib.import_module(user_var.routine)

        # routine._main()
 
        time.sleep(0.01)

        pass