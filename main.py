"""The central program that ties all the modules together."""

import time
import customtkinter as ctk
from src.modules.bot import Bot
from src.modules.capture import Capture
from src.modules.listener import Listener
from src.modules.notifier import Notifier
from src.modules.gui import GUI

def main():
    bot = Bot()
    capture = Capture()
    listener = Listener()
    notifier = Notifier()
    print('\n[-] Successfully initialized Maple APP')

    capture.start()
    while not capture.ready:
        time.sleep(0.01)

    bot.start()
    while not bot.ready:
        time.sleep(0.01)

    listener.start()
    while not listener.ready:
        time.sleep(0.01)

    notifier.start()
    while not notifier.ready:
        time.sleep(0.01)
    

    gui = GUI()
    gui.start()

    pass

if __name__ == '__main__':
    main()
