"""A module for detecting and notifying the user of in-game events or authenticator."""

import time
import os
# import pygame
import cv2
import threading
import numpy as np
import keyboard as kb

from src.common import config, utils
# from src.common.utils_game import solve_auth, type_auth
from src.detection.detection import solve_auth, type_auth



# auth event template
AUTH_RANGES = (
    ((60,130,180), (80, 148, 199)),
)
AUTH_TEMPLATE = cv2.imread('assets/auth_template.png', 0)
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
                height, width, _ = frame.shape

                
                # auth_frame = frame[height // 4:3 * height // 4, width // 4:3 * width // 4]
                # auth = utils.multi_match(auth_frame, AUTH_TEMPLATE, threshold=0.8)

                auth = utils.multi_match(frame, AUTH_TEMPLATE, threshold=0.8)


                # save the auth
                # found the auth
                if auth:
                    print(" -  Auth event detected!")
                    cv2.imwrite('auth.png', frame)
                    self._solve_auth(frame, auth[0])
                    time.sleep(10)
            time.sleep(0.1)



    def _solve_auth(self, frame, auth_pos):
        """Solve the authentication event."""
        
        def filter_alphanumeric(text):
            return "".join(filter(lambda x: x.isalnum(), text))
        # pause the program
        config.locked = True

        auth_pos = list(auth_pos)
        x_bias, y_bias = 260, 250

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

        cropped = frame[tl[1]:br[1], tl[0]:br[0]]

        ## TODO : save all the cropped image
        # cv2.imwrite('cropped.png', cropped)
        
        
        code = solve_auth(cropped)
        print(f' -  Auth code: {code}')

        code = filter_alphanumeric(code)

        type_auth(code, tl)
        time.sleep(0.1)
            


        # resume the program
        config.locked = False
        




# save the image




