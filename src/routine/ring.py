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
fight_req = cv2.imread('assets/routine/ring/fight_request.png', 0)
tp = cv2.imread('assets/routine/ring/tp.png', 0)

threshold = 0.95



@utils.run_if_enabled
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
    time.sleep(10)

def entry():

    npc_pos = utils.multi_match(config.capture.frame, npc, threshold=threshold)
    while len(npc_pos) == 0 and config.enabled:
        print(' -  finding npc...')
        npc_pos = utils.multi_match(config.capture.frame, npc, threshold=threshold)
        time.sleep(0.1)
    
    if not config.enabled:
        return

    print(f' -  npc detected at {npc_pos}')
    click(npc_pos[0])
    time.sleep(2)
    press('down', 1)
    time.sleep(0.25)
    press('down', 1)
    time.sleep(0.25)
    press('down', 1)
    time.sleep(0.25)
    press(interact, 1)
    time.sleep(0.25)
    press('down', 1)
    time.sleep(0.25)

def wait_for_request():
    fight_req_pos = utils.multi_match(config.capture.frame, fight_req, threshold=threshold)
    while len(fight_req_pos) == 0 and config.enabled:
        print(' -  finding request...')
        fight_req_pos = utils.multi_match(config.capture.frame, fight_req, threshold=threshold)
        time.sleep(0.5)
    
    if not config.enabled:
        return
    
    press(interact, 1)
    time.sleep(0.5)
    press(buff2, 1)
    press(buff2, 1)
    time.sleep(10)

def fight():
    # TODO
    entry_time = time.time()
    summon_time = time.time()
    while time.time() - entry_time < 605:
        if not config.enabled:
            time.sleep(0.1)
            continue
        print(' -  fighting...')
        if time.time() - summon_time > 30:
            summon()
        press(attact, 1)
    pass

def summon():
    # TODO
    pass

def out():
    npc_pos = utils.multi_match(config.capture.frame, npc, threshold=threshold)
    while len(npc_pos) == 0 and config.enabled:
        print(' -  finding npc...(out)')
        npc_pos = utils.multi_match(config.capture.frame, npc, threshold=threshold)
        time.sleep(0.1)
    
    if not config.enabled:
        return

    print(f' -  npc detected at {npc_pos}')
    click(npc_pos[0])
    time.sleep(2)
    press(interact, 1)
    time.sleep(2)
    
    pass


