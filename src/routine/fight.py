"""automatically kill daemon slime"""

import cv2
import time
from src.common import config, utils
from user_var import DEFAULT_CONFIG
from src.common.vkeys import press, click, key_down, key_up
from src.common.utils_game import reset_keys
import random

cap = config.capture
bot = config.bot

attact = DEFAULT_CONFIG['Attack']
heal = DEFAULT_CONFIG['Heal']

# import pydirectinput as p_in
# p_in.PAUSE = 0.01


threshold = 0.95
is_alt = False
alt_time = None
middle = config.player_pos[0]
print(middle)


def _main():
    num = random.randint(100,120)
    global alt_time
    global middle
    for _ in range(num):
        if config.locked:
            time.sleep(0.1)
            continue
        # if not alt_time or time.time() - alt_time > 59:
        #     alt_time = time.time()
        #     print(' -  active alt')
        #     alt_active()
        press(heal, 1)
        time.sleep(random.randint(10,30)/100)

    time.sleep(1.2)
    active_fight(middle)

def active_fight(x):
    delayyyy = 0.1
    if x > config.player_pos[0]:
        key_down('right')
        time.sleep(delayyyy)
        key_up('right')
    else:
        key_down('left')
        time.sleep(delayyyy)
        key_up('left')

def alt_active():
    switch_alt()
    press(attact, 2)
    time.sleep(0.1)
    press(attact, 2)
    switch_alt()

def switch_alt():
    global is_alt
    
    reset_keys(['left', 'right'])
    cap.switch_hwnd()
    time.sleep(0.1)

    while config.locked:
        time.sleep(0.1)

    left = cap.window['left']
    top = cap.window['top']
    if is_alt:
        is_alt = False
        click((left + 50, top + 40))
    else:
        is_alt = True
        click((left + 70, top + 766))

    time.sleep(0.1)


def walk_to(x):
    bias = 0.005
    while config.enabled:
        
        cur_pos = config.player_pos[0]
        # print(cur_pos)
        if x - bias < cur_pos < x + bias:
            reset_keys(['left', 'right'])
            break
        elif x < cur_pos:
            key_up('right')
            key_down('left')
        else:
            key_up('left')
            key_down('right')
        time.sleep(0.01)

    
    

def attact_slime(direction_dist):
    """Attack the slime considering direction_dist."""

    too_far = 300
    facing = config.real_player_facing
    press(DEFAULT_CONFIG['Pick up'], 1)
    if direction_dist > too_far:

        key_down('right')
        # time.sleep(0.1)
    elif direction_dist < -too_far:
        key_down('left')
        # time.sleep(0.1)
    elif direction_dist > 0:
        reset_keys(['left', 'right'])
        if facing and facing != 'left':
            key_down('right')
            time.sleep(0.3)
            key_up('right')
            facing = 'right'
        press(attact, 1)
    else:
        reset_keys(['left', 'right'])
        if facing and facing != 'right':
            key_down('left')
            time.sleep(0.3)
            key_up('left')
            facing = 'left'
        press(attact, 1)
    time.sleep(0.01)


def find_next_slime(slimes, player_pos):
    """Find the next slime to attack."""

    sweet_spot = 50

    px, _ = player_pos
    

    # retunr the closest slime's distance and direction to the player's +- sweet_spot
    closest_len = 9999
    closest_slime = None
    for slime in slimes:
        sx, _ = slime
        if min(abs(sx - (px + sweet_spot)), abs(sx - (px + sweet_spot))) < closest_len:
            closest_slime = slime
            closest_len = min(abs(sx - (px + sweet_spot)), abs(sx - (px + sweet_spot)))

    print(f' -  Closest slime at {closest_slime}')
    print(f' -  Player at {player_pos}')
    return closest_slime[0] - player_pos[0]
