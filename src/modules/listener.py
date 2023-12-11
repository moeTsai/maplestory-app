"""A keyboard listener to track user inputs."""

import time
import threading
import winsound
import keyboard as kb
from src.common.interfaces import Configurable
from src.common import config, utils
from datetime import datetime


class Listener(Configurable):
    DEFAULT_CONFIG = {
        'Start/stop': 'f10',
        'Reload routine': 'f6',
        'Record position': 'f7'
    }

    def __init__(self):
        """Initializes this Listener object's main thread."""
        super().__init__('controls')
        config.listener = self
        

        self.enabled = False
        self.ready = False

        self.thread = threading.Thread(target=self._main)
        self.thread.daemon = True


    def start(self):
        """Start listening to user inputs."""

        print('\n[-] Started keyboard listener')
        self.thread.start()

    def _main(self):
        """The main listener loop."""

        # finish setup
        self.ready = True

        while True:
            # not enabled, sleep
            """
            if not self.enabled:
                time.sleep(0.1)
                continue
            """
            # print('[-] Listening to keyboard inputs')

            if kb.is_pressed(self.config['Start/stop']):
                Listener.toggle_enabled()
            elif self.restricted_pressed('Record position'):
                Listener.record_position()
                time.sleep(0.5)
            
            time.sleep(0.01)

    def restricted_pressed(self, action):
        """Returns whether the key bound to ACTION is pressed only if the bot is disabled."""

        if kb.is_pressed(self.config[action]):
            if not config.enabled:
                return True
            now = time.time()
            if now - self.block_time > Listener.BLOCK_DELAY:
                print(f"\n[!] Cannot use '{action}' while Auto Maple is enabled")
                self.block_time = now
        return False

    @staticmethod
    def toggle_enabled():
        """Resumes or pauses the current routine. Plays a sound to notify the user."""

        
        if not config.enabled:
            Listener.recalibrate_minimap()      # Recalibrate only when being enabled.
        

        config.enabled = not config.enabled
        utils.print_state()

        if config.enabled:
            winsound.Beep(784, 333)     # G5
        else:
            winsound.Beep(523, 333)     # C5
        time.sleep(0.3)

    @staticmethod
    def recalibrate_minimap():
        config.capture.calibrated = False
        while not config.capture.calibrated:
            time.sleep(0.01)

    @staticmethod
    def record_position():
        pos = tuple('{:.3f}'.format(round(i, 3)) for i in config.player_pos)
        now = datetime.now().strftime('%I:%M:%S %p')
        # config.gui.edit.record.add_entry(now, pos)
        print(f'\n[~] Recorded position ({pos[0]}, {pos[1]}) at {now}')
        time.sleep(0.6)

