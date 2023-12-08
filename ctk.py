import customtkinter
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("RL and RT")
        
        screen_width = self.winfo_screenwidth() # Get the width of the screen
        screen_height = self.winfo_screenheight() # Get the height of the screen
        taskbar_height = screen_height - self.winfo_rooty() # Get the height of the sidebar
        
        self.geometry("%dx%d+0+0" % (screen_width, 760))

        # create Sidebar
        #self.sidebar = SidebarSettings(self, self.simulation, self.quit_page) # Come back on it later !
        
        # EPL LOGO
        epl = customtkinter.CTkImage(light_image=Image.open("images/EPL.jpg"),
                                  dark_image=Image.open("images/EPL.jpg"),
                                  size=(150, 80))
        button_epl = customtkinter.CTkButton(self, text= '', 
                                                image=epl, fg_color='transparent')
        button_epl.place(relx=1, rely=1, anchor='se')


        # AUTHORS
        self.author_label = customtkinter.CTkLabel(self, text="Author: Florian Martin")
        self.author_label.place(relx=0.16, rely=.975, anchor='sw')
        
        self.supervisor_label = customtkinter.CTkLabel(self, text='Supervisors: Mélanie Ghislain, Manon Dausort, Damien Dasnoy-Sumell, Benoît Macq')
        self.supervisor_label.place(relx=0.16, rely=1.0, anchor='sw')


        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=550)
        self.tabview.place(relx= 0.17, rely=0.025, relwidth=0.82, relheight=0.8)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.tabview.add("Treatment")
        self.tabview.add("Nutrients")
        self.tabview.add("Cell cycle")
        self.tabview.add("Radiosensitivity")
        self.tabview.add("Classifier")
        self.tabview.tab("Treatment").grid_columnconfigure(0, weight=1)  
        self.tabview.tab("Nutrients").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Cell cycle").grid_columnconfigure(0, weight=1)


app = App()
app.mainloop()
