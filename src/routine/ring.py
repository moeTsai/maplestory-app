"""automatic ring routine"""

import cv2
import time
from src.common import config, utils
from user_var import DEFAULT_CONFIG
from src.common.vkeys import press, click, key_down, key_up
from src.common.utils_game import reset_keys

attact = DEFAULT_CONFIG['Attack']
interact = DEFAULT_CONFIG['Interact']
buff2 = DEFAULT_CONFIG['Buff2']

npc = cv2.imread('assets/routine/ring/npc.png', 0)

threshold = 0.95




def _main():
    """
    automatic ring routine
    """

    frame = config.capture.frame
    if frame is None:
        print(' -  No frame captured')
        return
    
    entry()
    wait_for_request()
    fight()
    out()


def entry():

    npc_pos = utils.multi_match(config.capture.frame, npc, threshold=threshold)
    while len(npc_pos) == 0:
        print(' -  finding npc...')
        npc_pos = utils.multi_match(config.capture.frame, npc, threshold=threshold)
        time.sleep(0.1)
    
    print(f' -  npc detected at {npc_pos}')
    click(npc_pos[0], 1)
    time.sleep(0.5)
    press('down', 1)
    time.sleep(0.25)
    press(interact, 1)
    time.sleep(0.25)
    press('down', 1)
    time.sleep(0.25)
    press('down', 1)
    time.sleep(0.25)
    press('down', 1)
    time.sleep(0.25)
    press(interact, 1)
    
def wait_for_request():
    npc_pos = utils.multi_match(config.capture.frame, npc, threshold=threshold)
    while len(npc_pos) == 0:
        print(' -  finding request...')
        npc_pos = utils.multi_match(config.capture.frame, npc, threshold=threshold)
        time.sleep(0.5)
    
    press(interact, 1)
    time.sleep(0.5)
    press(buff2, 1)
    press(buff2, 1)
    time.sleep(10)

def fight():
    # TODO
    pass

def out():
    # TODO
    pass


