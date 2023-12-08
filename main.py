"""The central program that ties all the modules together."""

import time
import customtkinter as ctk
from src.modules.capture import Capture
from src.modules.gui import GUI

def main():
    capture = Capture()
    print('\n[-] Successfully initialized Maple APP')

    capture.start()
    while not capture.ready:
        time.sleep(0.01)

    gui = GUI()
    gui.start()

    pass

if __name__ == '__main__':
    main()
