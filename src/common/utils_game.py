"""A collection of functions and classes used within game process."""

import time
import math
import io
import queue
import cv2
import numpy as np
from PIL import Image
from src.common import config, settings

# from src.common.vkeys import press, click, key_down, key_up
from random import random
import pydirectinput as p_in


def reset_keys(keys):
    for key in keys:
        p_in.keyUp(key)


def climb_robe(robe_pos, stay=False):
    """
    Climb the robe in the game.
    """

    is_climbing = False
    kb_config = config.bot.DEFAULT_CONFIG
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
        
        # climb the robe


        time.sleep(0.1)
    




def solve_auth(image_np_array):
    """
    Solve the authentication image.

    :param image_np_array: the image to solve.
    return: the decoded string.
    """
    import ddddocr

    # path = 'C:/Users/a0955\OneDrive\文件\GitHub\maplestory-app/assets/auth_test/'

    ocr = ddddocr.DdddOcr()

    
    image = Image.fromarray(np.uint8(image_np_array))
    image.show()

    type(f'type : {image}')
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    image_bytes = buf.getvalue()

    res = ocr.classification(image_bytes)
    return res


if __name__ == '__main__':
    solve_auth(None)
    pass