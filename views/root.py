from customtkinter import CTk, CTkFrame, set_appearance_mode, set_default_color_theme

class Root(CTk):
    def __init__(self):
        super().__init__()

        width = 1000
        height = 700

        self.geometry(f"{width}x{height}")
        self.minsize(width=width, height=height)
        self.maxsize(width=width, height=height)

        set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
        set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

        # set program title
        self.title("Synthetic DataBank - UniSA")

        #self.login_frame = CTkFrame(self, width=width, height=height)
        #self.login_frame.place(in_=self)

        self.menu_frame = CTkFrame(self, width=500)
        self.menu_frame.pack(side="left", fill="y")

        self.view_frame = CTkFrame(self, width=100, fg_color="transparent")
        self.view_frame.pack(side="left", fill="both", expand=True)