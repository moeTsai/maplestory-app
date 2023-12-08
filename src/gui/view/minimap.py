

import cv2
import customtkinter as ctk
from PIL import ImageTk, Image
from src.gui.interfaces import LabelFrame
from src.common import config




class Minimap(LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.WIDTH = 400
        self.HEIGHT = 300
        self.image = None
        self.container = None
        
    def display_minimap(self):
        """update the minimap with current minimap."""
        
        minimap = config.capture.minimap
        if minimap:
            # path = minimap['path']

            img = cv2.cvtColor(minimap['minimap'], cv2.COLOR_BGR2RGB)
            height, width, _ = img.shape

            image = Image.fromarray(img.astype('uint8'))
            if self.container is None:
                self.image = ctk.CTkImage(light_image=image, size=(width, height))
                self.container = ctk.CTkLabel(config.gui.root, image=self.image, text='')
                self.container.place(x=10, y=20)
            else:
                self.image.configure(light_image=image)
            