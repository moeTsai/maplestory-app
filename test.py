"""user friendly GUI to interact with Maple APP"""

import time
import threading
import customtkinter as ctk
from ttkbootstrap import ttk
from PIL import ImageTk, Image
from src.common import config
from src.gui import View
import os
import ctypes
import numpy as np
import mss
import cv2

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

def screenshot(delay=1):
    """Take a screenshot of the game window."""
    try:
        window = (0, 0, 1366, 768)
        return np.array(sct.grab(window))
    except mss.exception.ScreenShotError:
        print(f'\n[!] Error while taking screenshot, retrying in {delay} second'
                + ('s' if delay != 1 else ''))
        time.sleep(delay)

# set dark mode and blue theme
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

# create window
root = ctk.CTk()

# set window size
root.geometry('800x600')

# add image to the root window
frame = None
with mss.mss() as sct:
    frame = screenshot()

frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
image = Image.fromarray(frame.astype('uint8'))

print(type(image))

image = ctk.CTkImage(light_image=image, size=(1366, 768))
image_label = ctk.CTkLabel(root, image=image, text='')
image_label.place(x=10, y=20)

# start mainloop
root.mainloop()


