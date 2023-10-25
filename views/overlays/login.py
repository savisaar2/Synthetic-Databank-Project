from customtkinter import CTkFrame, CTkLabel, CTkImage, CTkEntry, CTkButton
from PIL import Image

class LoginView(CTkFrame):
    def __init__(self, root, *args, **kwargs):
        """
        Initialise the Login overlay of the application.

        This class represents the LoginView overlay of the application.
        It renders the interactive widgets on the frontend of the application.

        Parameters
        ----------
        root : Root
            The applicaiton's root instance.
        """
        super().__init__(root, *args, **kwargs)
        self._setup_page()

    def _setup_page(self):
        """Renders the widgets on the LoginView."""
        self.overlay_frame = CTkFrame(self.master)
        self.overlay_frame.place(
            relx=0.5, rely=0.5, anchor="center",
            relwidth=1, relheight=1
        )
        # Comment below to show authentication page (production).
        # self.overlay_frame.lower()

        # Primary frame to house login widgets.
        self.login_frame = CTkFrame(self.overlay_frame)
        self.login_frame.place(rely=0.5, relx=0.5, anchor="c")

        # Feature image.
        self.logo_image = CTkImage(Image.open("views/static/images/unisa2.png"), size=(300, 300))
        self.logo_label = CTkLabel(self.login_frame, text="", image=self.logo_image)
        self.logo_label.pack(padx=100,pady=10)

        # Add the username_entry and center it horizontally
        self.username_entry = CTkEntry(self.login_frame, corner_radius=5, placeholder_text="username", justify="center", font=("Arial", 16), width=250, height=40, border_width=1)
        self.username_entry.pack(padx=20, pady=5)

        # Add the password_entry and center it horizontally
        self.password_entry = CTkEntry(self.login_frame, corner_radius=5, placeholder_text="password", justify="center", show="*", font=("Arial", 16), width=250, height=40, border_width=1)
        self.password_entry.pack(pady=5)

        # Add the login_button and center it horizontally
        self.login_button = CTkButton(self.login_frame, corner_radius=5, text="Login", font=("Arial", 16), width=250, height=40)
        self.login_button.pack(pady=10)

        # Authentication status message (on failure).
        self.msg_label = CTkLabel(self.login_frame, text="")
        self.msg_label.pack(pady=(0, 50))

    def get_login_info(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        return username, password

    def show_view(self):
        """Shows the LoginView overlay."""
        self.overlay_frame.lift()

    def hide_view(self):
        """Hides the LoginView overlay."""
        self.overlay_frame.lower()
