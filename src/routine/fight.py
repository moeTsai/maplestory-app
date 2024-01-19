"""automatically kill daemon slime"""

import cv2
import time
from src.common import config, utils
from user_var import DEFAULT_CONFIG
from src.common.vkeys import press, click, key_down, key_up
from src.common.utils_game import reset_keys
import random

attact = DEFAULT_CONFIG['Attack']
heal = DEFAULT_CONFIG['Heal']

# import pydirectinput as p_in
# p_in.PAUSE = 0.01

SLIME_TEMPLATE_LF = cv2.imread('assets/routine/daemon_slime/daemon_left.png', 0)
SLIME_TEMPLATE_RT = cv2.imread('assets/routine/daemon_slime/daemon_right.png', 0)

REAL_PLAYER_TEMPLATE = cv2.imread('assets/routine/daemon_slime/real_player.png', 0)

if SLIME_TEMPLATE_LF is None:
    print(' -  Failed to load daemon_left.png')
if SLIME_TEMPLATE_RT is None:
    print(' -  Failed to load daemon_right.png')

threshold = 0.95


def _main():
    num = random.randint(100,150)
    for i in range(num):
        press(heal, 1)
        time.sleep(random.randint(10,30)/100)

    time.sleep(1.2)
    active_fight(0.72)

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

