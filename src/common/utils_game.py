"""A collection of functions and classes used within game process."""

import time
import user_var
from src.common import config, utils
from src.common.vkeys import press, click, key_down, key_up
import pydirectinput as p_in

def reset_keys(keys):
    for key in keys:
        # p_in.keyUp(key)
        key_up(key)

def get_hp_location(percentage):
    dozens = percentage//10 * 10
    return config.HPs_X[dozens], config.HPs_Y

def get_mp_location(percentage):
    dozens = percentage//10 * 10
    return config.MPs_X[dozens], config.MPs_Y    

def hp_record():
    """
    check the hp color and record it.
    """

    color_temp = {}
    for i in range(0, 101, 10):
        color_L = get_hp_location(i)
        click((color_L[0], color_L[1]))
        color = config.capture.frame[color_L[1], color_L[0]]
        color_temp[i] = color
        # print(f' -  HP {i} color: {color}')
        time.sleep(0.3)
    
    config.HP_COLOR = color_temp
    config.locked = False
    print(' -  HP color recorded')

def mp_record():
    """
    check the mp color and record it.
    """

    color_temp = {}
    for i in range(0, 101, 10):
        color_L = get_mp_location(i)
        click((color_L[0], color_L[1]))
        color = config.capture.frame[color_L[1], color_L[0]]
        color_temp[i] = color
        # print(f' -  MP {i} color: {color}')
        time.sleep(0.3)
    
    config.MP_COLOR = color_temp
    config.locked = False
    print(' -  MP color recorded')


def hp_fill(percentage):
    """
    Fill the hp if below the given percentage.
    
    :param percentage: The percentage of hp to fill.
    """
    # hp_color = config.HP_COLOR
    # if hp_color is None:
    #     print('hp color not recorded yet')
    #     config.locked = True
    #     return
    
    hp_filler = user_var.DEFAULT_CONFIG['Hp potion']
    
    color_L = get_hp_location(percentage)
    # print(f' -  HP {percentage} color: {config.capture.frame[color_L[1], color_L[0]]}')
    # click((color_L[0], color_L[1]))
    # print(f' -  HP {percentage} color: {hp_color[percentage]}')
    
    if all(config.capture.frame[color_L[1], color_L[0]] == [177, 177, 177, 255]):
        print(f' -  Filling HP from {percentage}%')
        press(hp_filler, 1)

def mp_fill(percentage):
    """
    Fill the mp if below the given percentage.
    
    :param percentage: The percentage of mp to fill.
    """
    mp_filler = user_var.DEFAULT_CONFIG['Mp potion']
    
    color_L = get_mp_location(percentage)
    # print(f' -  MP {percentage} color: {config.capture.frame[color_L[1], color_L[0]]}')
    # click((color_L[0], color_L[1]))
    # print(f' -  MP {percentage} color: {mp_color[percentage]}')
    if all(config.capture.frame[color_L[1], color_L[0]] == [177, 177, 177, 255]):
        print(f' -  Filling MP from {percentage}%')
        press(mp_filler, 1)

@utils.run_if_enabled
def climb_robe(robe_pos, stay=False):
    """
    Climb the robe in the game.

    :param robe_pos: The position of the robe in the minimap.
    """

    is_climbing = False
    kb_config = user_var.DEFAULT_CONFIG
    jump = kb_config['Jump']


    def get_direction(player_pos, robe_pos):
        """
        Get the direction to the robe.
        """

        # Get the direction to the robe
        x_dir = player_pos[0] - robe_pos[0]
        y_dir = player_pos[1] - robe_pos[1]

        return round(x_dir, 3), round(y_dir, 3)

    print(" -  Climbing robe...")
    player_pos = config.player_pos
    if player_pos is None:
        print("\n[!] Player position not found\n")
        return

    
    # Get the position of the robe
    while True:
        # not enabled, sleep
        _, y_dir = get_direction(config.player_pos, robe_pos)
        if not config.enabled or y_dir > 0.1:
            # reset_keys(['up'])
            time.sleep(0.1)
            break
        # # direction to robe
        # x_dir, y_dir = get_direction(config.player_pos, robe_pos)


        x_dir, y_dir = get_direction(config.player_pos, robe_pos)
        print(f' -  Direction to robe: ({x_dir}, {y_dir})')

        
        if x_dir == 0 and y_dir > 0:
            p_in.press(jump)
            p_in.keyDown('up')
        elif x_dir > 0 and y_dir > 0:
            p_in.keyDown('up')
            p_in.keyUp('right')
            p_in.keyDown('left')
            if abs(x_dir) < 0.1:
                p_in.press(jump)
        elif x_dir < 0 and y_dir > 0:
            p_in.keyDown('up')
            p_in.keyUp('left')
            p_in.keyDown('right')
            if abs(x_dir) < 0.1:
                p_in.press(jump)
        else:
            p_in.keyUp('up')
        
        if x_dir == 0 and y_dir == 0:
            reset_keys(['up', 'left', 'right'])
            break

        # 10 = 1 second
        confirm_time_mm = 10
        for i in range(confirm_time_mm):
            
            # check if the player is at the robe
            x_dir, y_dir = get_direction(config.player_pos, robe_pos)
            if x_dir != 0 or y_dir > 0:
                break
            if i == confirm_time_mm - 1:
                reset_keys(['up', 'left', 'right'])
                is_climbing = True
                print(" -  Player is at the robe")

            time.sleep(0.1)

        # if not at the rope, reclimb
        if not is_climbing:
            continue

        if stay:
            reset_keys(['up', 'left', 'right'])
            break
        

        time.sleep(0.1)
    

