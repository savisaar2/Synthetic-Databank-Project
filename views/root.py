from customtkinter import CTk, CTkFrame, set_appearance_mode, set_default_color_theme

class Root(CTk):
    def __init__(self):
        """
        Initialize the application's main gui window.

        This class represents the main application gui window. It defines size and appearance,
        it defines the window's title and creates sectional frames for the menu and view master frames.
        """
        super().__init__()

        # Define window size.
        width = 1000
        height = 700
        self.geometry(f"{width}x{height}")
        self.minsize(width=width, height=height)
        self.maxsize(width=width, height=height)

        set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
        set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

        # set program title
        self.title("Synthetic DataBank - UniSA")

        # Define menu master frame.
        self.menu_frame = CTkFrame(self, width=250)
        self.menu_frame.pack(side="left", fill="y")

        # Define view master frame (for pages).
        self.view_frame = CTkFrame(self, width=100, fg_color="transparent")
        self.view_frame.pack(side="left", fill="both", expand=True)