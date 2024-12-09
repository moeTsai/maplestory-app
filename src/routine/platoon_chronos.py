"""automatically kill Platoon Chronos"""

import cv2
import time
from src.common import config, utils
from user_var import DEFAULT_CONFIG
from src.common.vkeys import press, click, key_down, key_up
from src.common.utils_game import reset_keys

attact = DEFAULT_CONFIG['Heal']

# import pydirectinput as p_in
# p_in.PAUSE = 0.01

MOSTER_TEMPLATE_LF = cv2.imread('assets/routine/platoon_chronos/platoon_chronos1.png', 0)
MOSTER_TEMPLATE_RT = cv2.imread('assets/routine/platoon_chronos/platoon_chronos2.png', 0)

REAL_PLAYER_TEMPLATE_LF = cv2.imread('assets/routine/platoon_chronos/real_player1.png', 0)
REAL_PLAYER_TEMPLATE_RT = cv2.imread('assets/routine/platoon_chronos/real_player2.png', 0)

threshold = 0.95

def _main():

    # random initial player pos
    # player_pos = (200, 200)
    player_pos = config.real_player_pos
    frame = config.capture.frame
    if frame is None:
        print(' -  No frame captured')
        return
    
    bias = 0

    player = utils.multi_match(frame, REAL_PLAYER_TEMPLATE_LF, threshold=threshold) or utils.multi_match(frame, REAL_PLAYER_TEMPLATE_RT, threshold=threshold) 
    if len(player) == 0:
        print(' -  player not detected')
        return
    
    # find monsters at same layer
    search_top = max(0, player[1] - 150)
    search_bottom = min(frame.shape[0], player[1] + 150)
    search_frame = frame[search_top:search_bottom, :]
    
    player_pos = player[0]
    print(f' -  Player detected at {player_pos}')

    moster_lf = utils.multi_match(search_frame, MOSTER_TEMPLATE_LF, threshold=threshold)
    for monster in moster_lf:
        monster = (monster[0] + bias, monster[1])
    moster_rt = utils.multi_match(search_frame, MOSTER_TEMPLATE_RT, threshold=threshold)
    for monster in moster_rt:
        monster = (monster[0] - bias, monster[1])
    monsters = moster_lf or moster_rt
    
    if len(monsters) == 0:
        print(' -  No monsters detected')
        return
    

    # print(f' -  Player detected at {player}')
    next_monster_dir = find_next_monster(monsters, player_pos)

    print(f' -  Next monster at player + {next_monster_dir}')


    attact_monster(next_monster_dir)


def attact_monster(direction_dist):
    """Attack the slime considering direction_dist."""

    too_far = 300
    facing = config.real_player_facing
    # press(DEFAULT_CONFIG['Pick up'], 1)
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
            time.sleep(0.5)
            key_up('right')
            facing = 'right'
        press(attact, 1)
    else:
        reset_keys(['left', 'right'])
        if facing and facing != 'right':
            key_down('left')
            time.sleep(0.5)
            key_up('left')
            facing = 'left'
        press(attact, 1)
    time.sleep(0.01)


def find_next_monster(monsters, player_pos):
    """Find the next slime to attack."""

    sweet_spot = 50

    px, _ = player_pos
    

    # retunr the closest slime's distance and direction to the player's +- sweet_spot
    closest_len = 9999
    closest_slime = None
    for slime in monsters:
        sx, _ = slime
        if min(abs(sx - (px + sweet_spot)), abs(sx - (px + sweet_spot))) < closest_len:
            closest_slime = slime
            closest_len = min(abs(sx - (px + sweet_spot)), abs(sx - (px + sweet_spot)))

    print(f' -  Closest slime at {closest_slime}')
    print(f' -  Player at {player_pos}')
    return closest_slime[0] - player_pos[0]

