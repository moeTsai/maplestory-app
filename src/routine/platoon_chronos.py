"""automatically kill Platoon Chronos"""

import cv2
import time
import random
from src.common import config, utils
from user_var import DEFAULT_CONFIG
from src.common.vkeys import press, click, key_down, key_up
from src.common.utils_game import reset_keys

attact = DEFAULT_CONFIG['Heal']
jump = DEFAULT_CONFIG['Jump']

# pos: layer
LAYER_POS = {
    0.12: 5, # layer
    0.21: 4,
    0.314: 3,
    0.40: 2,
    0.48: 1
}

LADDER_POS = {
    5: [0.207],
    4: [0.308],
    3: [0.207, 0.415],
    2: [0.305, 0.519]
}

# import pydirectinput as p_in
# p_in.PAUSE = 0.01

MOSTER_TEMPLATE_LF = cv2.imread('assets/routine/platoon_chronos/platoon_chronos1.png', 0)
MOSTER_TEMPLATE_RT = cv2.imread('assets/routine/platoon_chronos/platoon_chronos2.png', 0)

REAL_PLAYER_TEMPLATE_LF = cv2.imread('assets/routine/platoon_chronos/real_player1.png', 0)
REAL_PLAYER_TEMPLATE_RT = cv2.imread('assets/routine/platoon_chronos/real_player2.png', 0)
REAL_PLAYER_TEMPLATE_LF2 = cv2.imread('assets/routine/platoon_chronos/real_player3.png', 0)
REAL_PLAYER_TEMPLATE_RT2 = cv2.imread('assets/routine/platoon_chronos/real_player4.png', 0)


threshold = 0.85
no_monster_count = 0
bias = 0


def _main():
    global threshold, no_monster_count, bias

    
    player_pos = config.real_player_pos
    frame = config.capture.frame

    # random initial player pos
    # player_pos = (200, 200)
    if frame is None:
        print(' -  No frame captured')
        return
    
    player = (utils.multi_match(frame, REAL_PLAYER_TEMPLATE_LF, threshold=threshold) 
                or utils.multi_match(frame, REAL_PLAYER_TEMPLATE_RT, threshold=threshold)
                or utils.multi_match(frame, REAL_PLAYER_TEMPLATE_RT2, threshold=threshold)
                or utils.multi_match(frame, REAL_PLAYER_TEMPLATE_RT2, threshold=threshold))
    if len(player) == 0:
        print(' -  player not detected')
        return
    
    # find monsters at same layer
    print('player[1]:' + str(player[0]))
    
    player_pos = player[0]

    search_top = max(0, player_pos[1] - 150)
    search_bottom = min(frame.shape[0], player_pos[1] + 150)
    search_frame = frame[search_top:search_bottom, :]
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
        no_monster_count += 1
        print(no_monster_count)
        if no_monster_count >= 10:
            move_to_next_layer()
            no_monster_count = 0
        return

    # print(f' -  Player detected at {player}')
    next_monster_dir = find_next_monster(monsters, player_pos)

    print(f' -  Next monster at player + {next_monster_dir}')
    attact_monster(next_monster_dir)

    

def move_to_next_layer():
    """Move the player to the next layer in a back-and-forth order."""
    global move_direction
    
    current_layer = get_player_layer(config.player_pos)
    print('Current layer:', current_layer, '\tPosition:', config.player_pos)
    
    # Determine the next layer based on the current direction
    if current_layer == max(LAYER_POS.values()):
        move_direction = -1
    elif current_layer == min(LAYER_POS.values()):
        move_direction = 1
    
    next_layer = current_layer + move_direction
    
    # Move to the next layer
    if move_direction == 1:
        move_to_upper_layer(current_layer, next_layer, config.player_pos)
    else:
        move_to_lower_layer(current_layer, next_layer, config.player_pos)
    print('Moved to layer:', next_layer)


def get_player_layer(pos, tolerance = 0.03):
    """Determine the player's current layer based on Y position."""
    
    y_pos = pos[1]
    
    for layer_y_pos, layer in LAYER_POS.items():
        if abs(y_pos - layer_y_pos) <= tolerance:
            return layer
    return 0

def move_to_upper_layer(current_layer, target_layer, player_pos):
    """Move to the correct ladder and climb to the target layer."""
    
    if current_layer == target_layer:
        return

    # 找到最近的梯子
    ladder_positions = LADDER_POS[current_layer]
    closest_ladder = min(ladder_positions, key=lambda x: abs(x - player_pos[0]))

    # 移動到最近的梯子
    if player_pos[0] < closest_ladder:
        key_down('right')
        while player_pos[0] < closest_ladder:
            player_pos = config.real_player_pos
        key_up('right')
    else:
        key_down('left')
        while player_pos[0] > closest_ladder:
            player_pos = config.real_player_pos
        key_up('left')

    # 爬梯子
    key_down('up')
    time.sleep(1)  # 爬梯子的時間，根據需要調整
    key_up('up')

def move_to_lower_layer(current_layer, target_layer, player_pos):
    """Move to the next layer by avoiding ladders and performing a down jump."""
    
    if current_layer == target_layer:
        return

    # 隨機選擇下左跳或是下右跳
    direction = random.choice(['left', 'right'])
    key_down('down')
    key_down(direction)
    press(jump, 1) 
    time.sleep(0.5)
    key_up(direction)
    key_up('down')


def attact_monster(direction_dist):
    """Attack the slime considering direction_dist."""

    too_far = 250
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
        press(attact, 2)
    else:
        reset_keys(['left', 'right'])
        if facing and facing != 'right':
            key_down('left')
            time.sleep(0.5)
            key_up('left')
            facing = 'left'
        press(attact, 2)
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

