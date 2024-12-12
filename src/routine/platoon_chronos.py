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
POS_LAYER = {
    0.140: 5, # layer
    0.224: 4,
    0.316: 3,
    0.404: 2,
    0.500: 1
}

LAYER_POS = {
    5: 0.140, # layer
    4: 0.224,
    3: 0.316,
    2: 0.404,
    1: 0.500
}



LADDER_POS = {
    5: [0.209],
    4: [0.311],
    3: [0.212, 0.418],
    2: [0.308, 0.520]
}

# import pydirectinput as p_in
# p_in.PAUSE = 0.01

MOSTER_TEMPLATE_LF = cv2.imread('assets/routine/platoon_chronos/platoon_chronos1.png', 0)
MOSTER_TEMPLATE_RT = cv2.imread('assets/routine/platoon_chronos/platoon_chronos2.png', 0)
MOSTER_TEMPLATES = utils.load_templates_from_folder('assets/routine/platoon_chronos/platoon_chronos/')

# REAL_PLAYER_TEMPLATE_LF = cv2.imread('assets/routine/platoon_chronos/real_player1.png', 0)
# REAL_PLAYER_TEMPLATE_RT = cv2.imread('assets/routine/platoon_chronos/real_player2.png', 0)
# REAL_PLAYER_TEMPLATE_LF2 = cv2.imread('assets/routine/platoon_chronos/real_player3.png', 0)
# REAL_PLAYER_TEMPLATE_RT2 = cv2.imread('assets/routine/platoon_chronos/real_player4.png', 0)

REAL_PLAYER_TEMPLATES = utils.load_templates_from_folder('assets/routine/platoon_chronos/real_player/')




threshold = 0.90
no_monster_count = 0
bias = 0
move_direction = 1


def _main():
    global threshold, no_monster_count, bias
    
    frame = config.capture.frame
    
    # random initial player pos
    # player_pos = (200, 200)
    if frame is None:
        print(' -  No frame captured')
        return
    
    player = utils.multi_match_templates(frame, REAL_PLAYER_TEMPLATES, find_first=True, threshold=0.95)
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

    # mosters = utils.multi_match(search_frame, )

    
    monsters = utils.multi_match_templates(search_frame, MOSTER_TEMPLATES, find_first=False, threshold=threshold)

    # moster_lf = utils.multi_match(search_frame, MOSTER_TEMPLATE_LF, threshold=threshold)
    # for monster in moster_lf:
    #     monster = (monster[0] + bias, monster[1])
    # moster_rt = utils.multi_match(search_frame, MOSTER_TEMPLATE_RT, threshold=threshold)
    # for monster in moster_rt:
    #     monster = (monster[0] - bias, monster[1])
    # monsters = moster_lf or moster_rt
    
    
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
    print('Current layer:', str(current_layer), '\tPosition:', str(config.player_pos))
    
    # Determine the next layer based on the current direction
    if current_layer == max(POS_LAYER.values()):
        move_direction = -1
    elif current_layer == min(POS_LAYER.values()):
        move_direction = 1
    
    next_layer = current_layer + move_direction
    
    # Move to the next layer
    if move_direction == 1:
        move_to_upper_layer(current_layer, next_layer, config.player_pos)
    else:
        move_to_lower_layer(current_layer, next_layer, config.player_pos)
    print('Moved to layer:', next_layer)


def get_player_layer(pos, tolerance = 0.05):
    """Determine the player's current layer based on Y position."""
    
    y_pos = pos[1]
    x_pos = pos[0]
    
    for layer_y_pos, layer in POS_LAYER.items():
        if abs(y_pos - layer_y_pos) <= tolerance:
            return layer
    
    # 檢查玩家是否在繩子上
    for layer, ladder_positions in LADDER_POS.items():
        for ladder_x_pos in ladder_positions:
            if abs(x_pos - ladder_x_pos) < 0.01:
                return (layer + layer + 1) / 2

    return 0

def move_to_upper_layer(current_layer, target_layer, player_pos):
    """Move to the correct ladder and climb to the target layer."""

    if current_layer == target_layer:
        print(f"Error: No ladder positions found for layer {target_layer}")
        return

    if target_layer not in LADDER_POS:
        print(f"Error: No ladder positions found for layer {target_layer}")
        return

    # 找到最近的梯子
    ladder_positions = LADDER_POS[target_layer]
    closest_ladder = min(ladder_positions, key=lambda x: abs(x - player_pos[0]))

    jump_tolarance = 0.02

    # 移動到最近的梯子
    while not (abs(player_pos[0] - closest_ladder) < 0.01 and isinstance(get_player_layer(config.player_pos), int)):
        if abs(player_pos[0] - closest_ladder) < jump_tolarance:
            # 跳躍並在空中按下方向鍵"上"
            if player_pos[0] < closest_ladder:
                key_down('right')
                press(jump, 1)
                key_down('up')
                time.sleep(0.5)  # 跳躍時間，根據需要調整
                key_up('up')
                key_up('right')
            else:
                key_down('left')
                press(jump, 1)
                key_down('up')
                time.sleep(0.5)  # 跳躍時間，根據需要調整
                key_up('up')
                key_up('left')
        else:
            if player_pos[0] < closest_ladder:
                key_down('right')
                while player_pos[0] < closest_ladder - jump_tolarance:
                    player_pos = config.player_pos if config.player_pos else player_pos
                    time.sleep(0.01)
                key_up('right')
            else:
                key_down('left')
                # print(player_pos, closest_ladder)
                while player_pos[0] > closest_ladder + jump_tolarance:
                    player_pos = config.player_pos if config.player_pos else player_pos
                    time.sleep(0.01)
                key_up('left')

        player_pos = config.player_pos

    # 爬梯子
    target_y_pos = LAYER_POS[target_layer]
    key_down('up')
    print('position target:', config.player_pos[1], target_y_pos)
    for i in range(50):
        if config.player_pos[1] < target_y_pos:
            break
        print(config.player_pos)
        time.sleep(0.1)
    time.sleep(0.5)
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

