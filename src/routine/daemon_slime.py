"""automatically kill daemon slime"""

import cv2
import time
from src.common import config, utils
from user_var import DEFAULT_CONFIG
from src.common.vkeys import press, click, key_down, key_up
from src.common.utils_game import reset_keys

attact = DEFAULT_CONFIG['Attack']

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

    # random initial player pos
    # player_pos = (200, 200)
    player_pos = config.real_player_pos
    frame = config.capture.frame
    if frame is None:
        print(' -  No frame captured')
        return
    

    bias = 20
    slime_lf = utils.multi_match(frame, SLIME_TEMPLATE_LF, threshold=threshold)
    for slime in slime_lf:
        slime = (slime[0] + bias, slime[1])
    slime_rt = utils.multi_match(frame, SLIME_TEMPLATE_RT, threshold=threshold)
    for slime in slime_rt:
        slime = (slime[0] - bias, slime[1])
    slimes = slime_lf or slime_rt
    player = utils.multi_match(frame, REAL_PLAYER_TEMPLATE, threshold=threshold)
    if len(player) > 0:
        player_pos = player[0]
        print(f' -  Player detected at {player_pos}')
    if len(slimes) == 0:
        print(' -  No slimes detected')
        return
    if len(player) == 0:
        print(' -  player not detected')
        return

    # print(f' -  Player detected at {player}')
    next_slime_dir = find_next_slime(slimes, player_pos)

    print(f' -  Next slime at player + {next_slime_dir}')


    attact_slime(next_slime_dir)


def attact_slime(direction_dist):
    """Attack the slime considering direction_dist."""

    too_far = 300
    facing = config.real_player_facing
    if direction_dist > too_far:
        key_down('right')
        # time.sleep(0.1)
    elif direction_dist < -too_far:
        key_down('left')
        # time.sleep(0.1)
    elif direction_dist > 0:
        reset_keys(['left', 'right'])
        if facing and facing != 'left':
            press('right', 1)
            facing = 'right'
            press('right', 1)
        press(attact, 1)
    else:
        reset_keys(['left', 'right'])
        if facing and facing != 'right':
            press('left', 1)
            facing = 'left'
            press('left', 1)
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

