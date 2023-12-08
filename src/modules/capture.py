
import time
import cv2
import threading
import ctypes
import mss
import mss.windows
import numpy as np
from src.common import config
from ctypes import wintypes
from PIL import Image

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()


class Capture:
    """
    This class is responsible for capturing in-game events and updating the GUI.
    """

    def __init__(self):
        """initialize the capture class."""
        config.capture = self
        self.frame = None
        self.sct = None
        self.window = {
            'left': 0,
            'top': 0,
            'width': 1366,
            'height': 768
        }
        self.ready = False
        self.thread = threading.Thread(target=self._main)
        self.thread.daemon = True

    def start(self):
        """Starts this Capture's thread."""

        print('\n[~] Started video capture')
        self.thread.start()


    def _main(self):
        """
        This method captures in-game events and updates the GUI.
        """
        while True:
            # Calibrate screen capture
            # handle = user32.FindWindowW(None, 'MapleStory')
            handle = user32.FindWindowW(None, '[防爆模式] 楓葉幻境')

            rect = wintypes.RECT()
            user32.GetWindowRect(handle, ctypes.pointer(rect))
            rect = (rect.left, rect.top, rect.right, rect.bottom)
            

            self.window['left'] = rect[0]
            self.window['top'] = rect[1]
            self.window['width'] = rect[2] - rect[0]
            self.window['height'] = rect[3] - rect[1]

            # Calibrate by finding the top-left and bottom-right corners of the minimap
            with mss.mss() as self.sct:
                self.frame = self.screenshot()
            
            if self.frame is None:
                continue
            cv2.imwrite('map.png', self.frame)

            mm_tl = (
                0,
                0
            )
            mm_br = (
                300,
                200
            )

            with mss.mss() as self.sct:
                while True:
                    # screenshot
                    self.frame = self.screenshot()
                    if self.frame is None:
                        continue
                    
                    minimap = self.frame[mm_tl[1]:mm_br[1], mm_tl[0]:mm_br[0]]
                    # Crop the minimap

                    self.minimap = {
                        'minimap': minimap,
                    }

                    if not self.ready:
                        self.ready = True
                    time.sleep(0.001)


    def screenshot(self, delay=1):
        """Take a screenshot of the game window."""
        try:
            return np.array(self.sct.grab(self.window))
        except mss.exception.ScreenShotError:
            print(f'\n[!] Error while taking screenshot, retrying in {delay} second'
                  + ('s' if delay != 1 else ''))
            time.sleep(delay)