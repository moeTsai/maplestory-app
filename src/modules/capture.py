
import time
import cv2
import threading
import ctypes
import mss
import mss.windows
import numpy as np
import user_var
from src.common import config, utils
from ctypes import wintypes

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

MAPLE_WINDOW_NAME = user_var.MAPLE_WINDOW_NAME

# The distance between the top of the minimap and the top of the screen
MINIMAP_TOP_BORDER = 0

# The thickness of the other three borders of the minimap
MINIMAP_BOTTOM_BORDER = 2

# Offset in pixels to adjust for windowed mode
WINDOWED_OFFSET_TOP = 10
WINDOWED_OFFSET_LEFT = 0

# The top-left and bottom-right corners of the minimap
MM_TL_TEMPLATE = cv2.imread('assets/minimap_tl_template.png', 0)
MM_BR_TEMPLATE = cv2.imread('assets/minimap_br_template.png', 0)

MMT_HEIGHT = max(MM_TL_TEMPLATE.shape[0], MM_BR_TEMPLATE.shape[0])
MMT_WIDTH = max(MM_TL_TEMPLATE.shape[1], MM_BR_TEMPLATE.shape[1])

LEVEL_TEMPLATE = cv2.imread('assets/level_template.png', 0)



# The player's symbol on the minimap
PLAYER_TEMPLATE = cv2.imread('assets/player_template.png', 0)
PT_HEIGHT, PT_WIDTH = PLAYER_TEMPLATE.shape


class Capture:
    """
    This class is responsible for capturing in-game events and updating the GUI.
    """

    def __init__(self):
        """initialize the capture class."""
        config.capture = self
        self.frame = None
        self.sct = None
        self.hwnds = []
        self.window = {
            'left': 0,
            'top': 0,
            'width': 1920,
            'height': 1080
        }
        self.ready = False
        self.calibrated = False
        self.thread = threading.Thread(target=self._main)
        self.thread.daemon = True

    def start(self):
        """Starts this Capture's thread."""
        global MAPLE_WINDOW_NAME

        print('\n[-] Get hwnd of all the windows')
        self.hwnds = self.get_hwnds()

        print('\n[-] Started video capture')
        self.thread.start()

    def _main(self):
        """
        This method captures in-game events and updates the GUI.
        """
        while True:
            # Calibrate screen capture

            # handle = user32.FindWindowW(None, MAPLE_WINDOW_NAME)
            # self.switch_hwnd()
            handle = self.hwnds[0]

            rect = wintypes.RECT()
            
            user32.GetWindowRect(handle, ctypes.pointer(rect))
            
            rect = (rect.left, rect.top, rect.right, rect.bottom)
            

            self.window['left'] = rect[0]
            self.window['top'] = rect[1]
            self.window['width'] = max(rect[2] - rect[0], MMT_WIDTH)
            self.window['height'] = max(rect[3] - rect[1], MMT_HEIGHT)

            # Calibrate by finding the top-left and bottom-right corners of the minimap
            with mss.mss() as self.sct:
                self.frame = self.screenshot()
            
            if self.frame is None:
                continue
            cv2.imwrite('map.png', self.frame)
            tl, _ = utils.single_match(self.frame, MM_TL_TEMPLATE, (0, 0, 200, 150))
            _, br = utils.single_match(self.frame, MM_BR_TEMPLATE, (tl[0], tl[1], 500, 500))
            # get the location of the hp bar and mp bar
            self.get_hp_bar()
            self.get_mp_bar()

            br = (br[0], br[1])

            mm_tl = (
                tl[0] + MINIMAP_BOTTOM_BORDER,
                tl[1] + MINIMAP_TOP_BORDER
            )
            mm_br = (
                max(mm_tl[0] + PT_WIDTH, br[0] - MINIMAP_BOTTOM_BORDER),
                max(mm_tl[1] + PT_HEIGHT, br[1] - MINIMAP_BOTTOM_BORDER)
            )
            self.minimap_ratio = (mm_br[0] - mm_tl[0]) / (mm_br[1] - mm_tl[1])
            self.minimap_sample = self.frame[mm_tl[1]:mm_br[1], mm_tl[0]:mm_br[0]]
            self.calibrated = True

            with mss.mss() as self.sct:
                while True:
                    if not self.calibrated:
                        break

                    # screenshot
                    self.frame = self.screenshot()
                    if self.frame is None:
                        continue
                    
                    minimap = self.frame[mm_tl[1]:mm_br[1], mm_tl[0]:mm_br[0]]
                    # Crop the minimap

                     # Determine the player's position
                    player = utils.multi_match(minimap, PLAYER_TEMPLATE, threshold=0.8)
                    if player:
                        config.player_pos = utils.convert_to_relative(player[0], minimap)

                    self.minimap = {
                        'minimap': minimap,
                        'player_pos': config.player_pos,
                    }

                    if not self.ready:
                        self.ready = True
                    time.sleep(0.01)

    def get_hp_bar(self):
        _, level = utils.single_match(self.frame, LEVEL_TEMPLATE)

        from src.common import config

        config.HP0_LOCATION = (level[0] + 200, level[1] - 5)
        config.HP100_LOCATION = (level[0] + 280, level[1] - 5)
        hp0_location = config.HP0_LOCATION
        hp100_location = config.HP100_LOCATION
        config.HPs_X = {
            0  : (hp0_location[0]),
            10 : (hp0_location[0] * 9 + hp100_location[0]    )//10,
            20 : (hp0_location[0] * 8 + hp100_location[0] * 2)//10,
            30 : (hp0_location[0] * 7 + hp100_location[0] * 3)//10,
            40 : (hp0_location[0] * 6 + hp100_location[0] * 4)//10,
            50 : (hp0_location[0] * 5 + hp100_location[0] * 5)//10,
            60 : (hp0_location[0] * 4 + hp100_location[0] * 6)//10,
            70 : (hp0_location[0] * 3 + hp100_location[0] * 7)//10,
            80 : (hp0_location[0] * 2 + hp100_location[0] * 8)//10,
            90 : (hp0_location[0]     + hp100_location[0] * 9)//10,
            100: (hp100_location[0])
        }
        config.HPs_Y = hp0_location[1]
    
    def get_mp_bar(self):
        _, level = utils.single_match(self.frame, LEVEL_TEMPLATE)

        from src.common import config

        config.MP0_LOCATION = (level[0] + 300, level[1] - 5)
        config.MP100_LOCATION = (level[0] + 380, level[1] - 5)
        mp0_location = config.MP0_LOCATION
        mp100_location = config.MP100_LOCATION
        config.MPs_X = {
            0  : (mp0_location[0]),
            10 : (mp0_location[0] * 9 + mp100_location[0]    )//10,
            20 : (mp0_location[0] * 8 + mp100_location[0] * 2)//10,
            30 : (mp0_location[0] * 7 + mp100_location[0] * 3)//10,
            40 : (mp0_location[0] * 6 + mp100_location[0] * 4)//10,
            50 : (mp0_location[0] * 5 + mp100_location[0] * 5)//10,
            60 : (mp0_location[0] * 4 + mp100_location[0] * 6)//10,
            70 : (mp0_location[0] * 3 + mp100_location[0] * 7)//10,
            80 : (mp0_location[0] * 2 + mp100_location[0] * 8)//10,
            90 : (mp0_location[0]     + mp100_location[0] * 9)//10,
            100: (mp100_location[0])
        }
        config.MPs_Y = mp0_location[1]

    def screenshot(self, delay=1):
        """Take a screenshot of the game window."""
        try:
            return np.array(self.sct.grab(self.window))
        except mss.exception.ScreenShotError:
            print(f'\n[!] Error while taking screenshot, retrying in {delay} second'
                  + ('s' if delay != 1 else ''))
            time.sleep(delay)

    def get_hwnds(self):
        """Get the hwnd of all the windows."""
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, ctypes.c_int)
        def enum_windows_proc(hwnd, lParam):
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)

            if buff.value == MAPLE_WINDOW_NAME:
                self.hwnds.append(hwnd)
                print(f"hwnd: {hwnd}, name: {buff.value}")

            return True
        ctypes.windll.user32.EnumWindows(EnumWindowsProc(enum_windows_proc), 0)
        return self.hwnds

    def switch_hwnd(self):
        self.hwnds.append(self.hwnds.pop(0))        
        self.calibrated = False
        print(f'switched: {self.hwnds}')
        return self.hwnds[0]
