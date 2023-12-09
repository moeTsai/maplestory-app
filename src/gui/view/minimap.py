

import cv2
import customtkinter as ctk
from PIL import ImageTk, Image
from src.gui.interfaces import LabelFrame
from src.common import config, utils



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
            player_pos = minimap['player_pos']
            img = cv2.cvtColor(minimap['minimap'], cv2.COLOR_BGR2RGB)
            height, width, _ = img.shape

            # print(round(player_pos[0], 3), round(player_pos[1], 3))


            
            # Resize minimap to fit the Canvas
            ratio = min(self.WIDTH / width, self.HEIGHT / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            if new_height * new_width > 0:
                img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)


            # Draw the player's position on top of everything
            if player_pos:
                cv2.circle(img, utils.convert_to_absolute(player_pos, img), 3, (0, 0, 255), -1)

            image = Image.fromarray(img.astype('uint8'))

            # Create a new image object with the updated image
            new_image = ctk.CTkImage(light_image=image, size=(new_width, new_height))

            if self.container is None:
                # If the container does not exist, create it
                self.image = new_image
                self.container = ctk.CTkLabel(config.gui.root, image=self.image, text='')
                self.container.place(x=10, y=20)
            else:
                # Update the existing image without causing flickering
                self.container.configure(image=new_image)
                self.container.image = new_image