
# import os
# import sys
# # Add the parent' parent directory to the Python path
# cur_path = os.path.dirname(os.path.abspath(__file__))
# for _ in range(2):
#     cur_path = os.path.dirname(cur_path)
# sys.path.append(cur_path)

import io
import telebot
import threading
import telebot
import numpy as np
from PIL import Image
from user_var import BOT_TOKEN, CHAT_ID

bot = telebot.TeleBot(BOT_TOKEN)


def send_message_in_thread(message):
    thread = threading.Thread(target=send_message, args=(message,))
    thread.start()

def send_photo_in_thread(np_array):
    thread = threading.Thread(target=send_photo, args=(np_array,))
    thread.start()

def send_message(message):
    """
    Send a message to the user.

    :param message: the message to send.
    """
    bot.send_message(CHAT_ID, message)

def send_photo(np_array_img):
    """
    Send a photo to the user.

    :param np_array_img: the image to send.
    """
    # Convert the NumPy array to a PIL Image
    image = Image.fromarray(np_array_img.astype('uint8'))

    # Save the image to an in-memory file
    with io.BytesIO() as image_io:
        image.save(image_io, format='PNG')
        image_io.seek(0)

        # Send the photo
        bot.send_photo(CHAT_ID, image_io)


if __name__ == '__main__':
    
    send_photo()
    send_message('123')