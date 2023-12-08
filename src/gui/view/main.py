
import customtkinter as ctk
from src.gui.view.minimap import Minimap
from src.gui.interfaces import Tab

class View(Tab):
    """The main window of the application."""
    
    def __init__(self, parent, **kwargs):
        """Initialize the main window."""
        super().__init__(parent, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.minimap = Minimap(self)
        self.minimap.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
