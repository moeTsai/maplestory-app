"""user friendly GUI to interact with Maple APP"""

import time
import threading
import tkinter as tk
import customtkinter as ctk
from ttkbootstrap import ttk
from PIL import ImageTk
from src.common import config
from src.gui import View



class GUI:
    DISPLAY_FRAME_RATE = 20
    RESOLUTION = {
        'DEFAULT': (800, 600)
    }

    def __init__(self):
        """initialize the GUI class."""
        config.gui = self
        #  "dark-blue", "sweetkind"
        # ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')

        self.root = ctk.CTk()
        self.root.title("Maple APP")
        self.root.wm_iconbitmap()
        icon = ImageTk.PhotoImage(file="assets/icon.png")
        self.root.iconphoto(False, icon)
        self.root.geometry(f"{GUI.RESOLUTION['DEFAULT'][0]}x{GUI.RESOLUTION['DEFAULT'][1]}")
        self.root.resizable(False, False)

        # configure grid layout (4x4)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure((2, 3), weight=0)
        self.root.grid_rowconfigure((0, 1, 2), weight=1)



        # Build the GUI
        self.view = View(self.root)

        
        # change appearance mode
        self.root.sidebar_frame = ctk.CTkFrame(self.root, width=140, corner_radius=0)
        self.root.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.root.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Create appearance_mode_label and set it to the bottom left
        self.root.appearance_mode_label = ctk.CTkLabel(self.root.sidebar_frame, text="", anchor="w")
        self.root.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.root.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.root.sidebar_frame, values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event)
        self.root.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

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

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)



if __name__ == '__main__':
    gui = GUI()
    gui.start()
