"""user friendly GUI to interact with Maple APP"""

import time
import threading
import customtkinter as ctk
from ttkbootstrap import ttk
from PIL import ImageTk
from src.common import config
from src.gui import View



class GUI:
    DISPLAY_FRAME_RATE = 30
    RESOLUTION = {
        'DEFAULT': (800, 600)
    }

    def __init__(self):
        """initialize the GUI class."""
        config.gui = self

        self.root = ctk.CTk()
        self.root.title("Maple APP")
        icon = ImageTk.PhotoImage(file="assets/icon.png")
        self.root.iconphoto(False, icon)
        # self.root.geometry(GUI.RESOLUTION['DEFAULT'])
        self.root.geometry(f"{GUI.RESOLUTION['DEFAULT'][0]}x{GUI.RESOLUTION['DEFAULT'][1]}")
        self.root.resizable(False, False)


        # # Build the GUI
        # self.navigation = ctk.CTkNotebook(self.root)\
        self.navigation = ttk.Notebook(self.root)
        self.view = View(self.root)

        self.navigation.pack(expand=True, fill="both")
        # self.navigation.bind("<<NotebookTabChanged>>", self.on_tab_change)
        self.root.focus()


    def start(self):
        """Start the GUI."""
        display_thread = threading.Thread(target=self._display_minimap)
        display_thread.daemon = True
        display_thread.start()

        self.root.mainloop()


    def _display_minimap(self):
        """Display the minimap."""
        delay = 1 / GUI.DISPLAY_FRAME_RATE
        while True:
            self.view.minimap.display_minimap()
            time.sleep(delay)



if __name__ == '__main__':
    gui = GUI()
    gui.start()
