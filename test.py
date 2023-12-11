"""A module for detecting and notifying the user of in-game events or authenticator."""

import time
import os
# import pygame
import mss
import cv2
import threading
import numpy as np
import keyboard as kb
from PIL import Image

from src.common import config, utils
from src.common.utils_game import solve_auth
import ctypes
from ctypes import wintypes
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()


def screenshot(delay=1):
    try:
        return np.array(sct.grab(window))
    except mss.exception.ScreenShotError:
        print(f'\n[!] Error while taking screenshot, retrying in {delay} second'
                + ('s' if delay != 1 else ''))
        time.sleep(delay)

sct = None
rect = wintypes.RECT()
handle = user32.FindWindowW(None, '[防爆模式] 楓葉幻境')
user32.GetWindowRect(handle, ctypes.pointer(rect))
rect = (rect.left, rect.top, rect.right, rect.bottom)
window = {
            'left': 0,
            'top': 0,
            'width': 1366,
            'height': 768
        }
window['left'] = rect[0]
window['top'] = rect[1]
window['width'] = max(rect[2] - rect[0], 30)
window['height'] = max(rect[3] - rect[1], 30)

# handle = user32.FindWindowW(None, '[防爆模式] 楓葉幻境')

# rect = wintypes.RECT()
# user32.GetWindowRect(handle, ctypes.pointer(rect))
# rect = (rect.left, rect.top, rect.right, rect.bottom)
# rect = tuple(max(0, x) for x in rect)

# auth event template
AUTH_TEMPLATE = cv2.imread('assets/auth_template.png')
with mss.mss() as sct:
    frame = screenshot()
    print(frame.shape)


tl, _ = utils.single_match(frame, AUTH_TEMPLATE)
print(tl)




# save the image
cv2.imwrite('/assets/auth_test/test.png', AUTH_TEMPLATE)




# show the image
img = cv2.imread('assets/auth_template.png')
image_path = 'assets/auth_template.png'
img = Image.open(image_path)

img.show()
