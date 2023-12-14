import io
import time
import numpy as np
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
def type_auth(code, auth_pos):
    """
    Type the authentication code.

    :param code: the code to type.
    :param auth_pos: the position of the authentication box.
    """
    p_in.PAUSE = 0.01
    auth_pos = list(auth_pos)
    x_bias, y_bias = 50, 85

    auth_pos[0] += x_bias
    auth_pos[1] += y_bias

    # click the auth box
    p_in.click(auth_pos[0], auth_pos[1])
    p_in.click(auth_pos[0], auth_pos[1])

    # # type the code
    for c in code:
        press(c, 1)
        time.sleep(0.3)

    # p_in.write(code, interval=0.5)


    if BOT_TOKEN and CHAT_ID:
        flag = True

        # take a screenshot
        frame = config.capture.screenshot()

        # send telegram message
        send_message_in_thread(f'Auth Code: {code}')
        send_photo_in_thread(frame)

    p_in.press('enter')
    time.sleep(1)
    p_in.press('enter')




