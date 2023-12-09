import customtkinter as ctk


class Frame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

class Tab(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        # parent.add(self, text=self.__class__.__name__)

class LabelFrame(ctk.CTkLabel):
    def __init__(self, parent, **kwargs):
        kwargs["text"] = self.__class__.__name__
        super().__init__(parent, **kwargs)
        self.parent = parent
