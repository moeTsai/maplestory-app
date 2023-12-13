import io
import time
import numpy as np
from PIL import Image
import pydirectinput as p_in
from src.common import config, utils


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
def type_auth(code, auth_pos):
    """
    Type the authentication code.

    :param code: the code to type.
    :param auth_pos: the position of the authentication box.
    """
    p_in.PAUSE = 0.01
    auth_pos = list(auth_pos)
    x_bias, y_bias = 40, 80

    auth_pos[0] += x_bias
    auth_pos[1] += y_bias

    # click the auth box
    p_in.click(auth_pos[0], auth_pos[1])
    p_in.click(auth_pos[0], auth_pos[1])


    # p_in.write(code, interval=0.2)

    # Error Proofing
    """
    for _ in range(2):
        for c in code:
            p_in.press(c)

            # avoid chinese keyboard input
            p_in.press(',')
            p_in.press('backspace')
            time.sleep(0.2)
        p_in.press('shift')
    """
    # from pynput.keyboard import Key, Controller
    # keyboard = Controller()
    # keyboard.type(code)

    p_in.write(code, interval=0.2)



    p_in.press('enter')
    time.sleep(1)
    p_in.press('enter')



