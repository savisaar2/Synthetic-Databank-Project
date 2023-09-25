from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkImage, CTkFont
from PIL import Image

class MenuView(CTkFrame):
    def __init__(self, root, *args, **kwargs):
        """
        Initialise the Menu view of the application.

        This class represents the MenuView section of the application.
        It renders the interactive widgets on the frontend of the application.

        Parameters
        ----------
        root : Root
            The applicaiton's root instance.
        """
        # Pass some base parameters to our CTkFrame class.
        super().__init__(root.menu_frame, *args, **kwargs)
        self.pack(fill="both", expand=True) # Pack the base frame.

        # Displays menu items.
        self._render_menu()

    def _render_menu(self):
        """Renders widgets on the Menu section."""
        
        # Create a container for widgets.
        self.content_frame = CTkFrame(self)
        self.content_frame.pack(fill="both", expand=True)

        # Render logo with application title.
        self.logo_label = self._create_logo_label(img="views/static/images/unisa_logo.png", text="Synthetic Databank")

        # Render relevant navigational buttons for application pages.
        self.library_button = self._create_button(text="Library", side="top")
        self.analyse_button = self._create_button(text="Analyse", side="top")
        self.manipulate_button =self._create_button(text="Manipulate", side="top")
        self.sample_button = self._create_button(text="Sample", side="top")
        self.save_button = self._create_button(text="Save & Export", side="top")

        # Bottom pushed buttons.
        self.end_button = self._create_button(text="Quit", side="bottom")
        self.accounts_button = self._create_button(text="Accounts", side="bottom")

    def _create_button(self, text="Text Here", side="top"):
        """
        Renders a button widget with corrisponding text.

        Parameters
        ----------
        text : str
            Text to appear on the button.
        side : str
            Defines top|bottom positioning.
        """
        button = CTkButton(self.content_frame, corner_radius=0, height=40, image="", border_spacing=10, text=text, anchor="w")
        button.pack(side=side, fill="x")
        return button
    
    def _create_logo_label(self, img, text="Text Here"):
        """
        Renders a label widget with corrisponding text.

        Parameters
        ----------
        img : str
            Path to image file to be displayed with label.
        text : str
            Text to appear on the label.
        """
        image = CTkImage(Image.open(img), size=(150, 150))
        label = CTkLabel(self.content_frame, text="Synthetic Databank", image=image, compound="top", font=CTkFont(size=18, weight="bold"))
        label.pack(side="top", padx=20, pady=(0, 20), anchor="w")
        return label