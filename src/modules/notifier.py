"""A module for detecting and notifying the user of in-game events or authenticator."""

import time
import os
# import pygame
import cv2
import threading
import numpy as np
import keyboard as kb
from datetime import datetime

from src.common import config, utils
from src.common.vkeys import click
from src.detection.detection import solve_auth, type_auth



# auth event template
# AUTH_RANGES = (
#     ((60,130,180), (80, 148, 199)),
# )
AUTH_TEMPLATE = cv2.imread('assets/auth_template.png', 0)
AUTH_ENTRY_TEMPLATE = cv2.imread('assets/auth_entry_template.png', 0)
GIFT_TEMPLATE = cv2.imread('assets/gift_template.png', 0)

# auth_filtered = utils.filter_color(cv2.imread('assets/auth_template.png'), AUTH_RANGES)
# AUTH_TEMPLATE = cv2.cvtColor(auth_filtered, cv2.COLOR_BGR2GRAY)

class Notifier:
    ALERTS_DIR = os.path.join('assets', 'alerts')

    def __init__(self):
        """initialize the notifier class."""

        self.ready = False
        self.thread = threading.Thread(target=self._main)
        self.thread.daemon = True

    def start(self):
        """Starts this Notifier's thread."""

        print('\n[-] Started notifier')
        self.thread.start()

    def _main(self):
        self.ready = True
        while True:
            if config.enabled:
                
                frame = config.capture.frame
                
                gift = utils.multi_match(frame, GIFT_TEMPLATE, threshold=0.8)
                if gift:
                    gift = gift[0]
                    # bias
                    gift_pos = (gift[0] + 115, gift[1] + 40)
                    self._click_gift(gift_pos)
                    cv2.imwrite('gift.png', frame)
                    time.sleep(1)

                auth = utils.multi_match(frame, AUTH_TEMPLATE, threshold=0.8)
                entry = utils.multi_match(frame, AUTH_ENTRY_TEMPLATE, threshold=0.8)

                # found the auth save the auth
                if auth and entry:
                    print(" -  Auth event detected!")
                    cv2.imwrite('auth.png', frame)
                    self._solve_auth(frame, auth[0], entry[0])
            time.sleep(0.1)

    def _click_gift(self, gift_pos):
        """Click the gift button."""
        # TODO
        
        print(" -  Gift event detected!")
        click(gift_pos)


    def _solve_auth(self, frame, auth_pos, entry_pos):
        """Solve the authentication event."""
        
        def filter_alphanumeric(text):
            return "".join(filter(lambda x: x.isalnum(), text))
        # pause the program
        config.locked = True
        time.sleep(2)

        auth_pos = list(auth_pos)
        x_bias, y_bias = -85, 50

        width, height = 194, 30

        print(f' -  auth pos  : {auth_pos}')

        tl = (
            auth_pos[0] + x_bias,
            auth_pos[1] + y_bias
        )
        br = (
            auth_pos[0] + x_bias + width,
            auth_pos[1] + y_bias + height
        )

        ## TODO : filter the image to raise the accuracy

        cropped = frame[tl[1]:br[1], tl[0]:br[0]]

        code = solve_auth(cropped)
        
        print(f' -  Auth code: {code}')
        code = filter_alphanumeric(code)

        original = 'auth_data/original'
        os.makedirs(original, exist_ok=True)
        
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        original_path = f'{original}/{current_time}__{code}.png'

        cv2.imwrite(original_path, cropped)

        type_auth(code, entry_pos)

        time.sleep(10)
        time.sleep(0.1)
        
        # resume the program
        config.locked = False
    
