import io
import os
import cv2
import time
import numpy as np
from datetime import datetime
from PIL import Image
import pydirectinput as p_in
from src.common import config, utils
from src.common.vkeys import press
from src.common.message import send_message_in_thread, send_photo_in_thread
from user_var import BOT_TOKEN, CHAT_ID



@utils.run_if_enabled
def solve_auth(image_np_array):
    """
    Solve the authentication image.

    :param image_np_array: the image to solve.
    return: the decoded string.
    """
    import ddddocr


    ocr = ddddocr.DdddOcr(show_ad=False)

    
    image = Image.fromarray(np.uint8(image_np_array))
    # image.show()

    # type(f'type : {image}')
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    image_bytes = buf.getvalue()

    res = ocr.classification(image_bytes)
    return res



@utils.run_if_enabled
def type_auth(code, entry_pos):
    """
    Type the authentication code.

    :param code: the code to type.
    :param auth_pos: the position of the authentication box.
    """
    p_in.PAUSE = 0.01
    entry_pos = list(entry_pos)
    x_bias, y_bias = 90, 30

    entry_pos[0] += x_bias
    entry_pos[1] += y_bias

    # click the auth box
    p_in.click(entry_pos[0], entry_pos[1])
    p_in.click(entry_pos[0], entry_pos[1])

    # # type the code
    for c in code:
        press(c, 1)
        time.sleep(0.3)

    # p_in.write(code, interval=0.5)


    if BOT_TOKEN and CHAT_ID:

        # take a screenshot
        frame = config.capture.screenshot()

        check = 'auth_data/check'
        os.makedirs(check, exist_ok=True)
        
        # save the image to the given directory
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        check_path = f'{check}/{current_time}__{code}.png'
        cv2.imwrite(check_path, frame)

        # send telegram message
        send_message_in_thread(f'Auth Code: {code}')
        send_photo_in_thread(frame)

    p_in.press('enter')
    time.sleep(1)
    p_in.press('enter')
