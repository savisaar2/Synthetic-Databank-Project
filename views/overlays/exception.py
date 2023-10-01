from tkinter import ttk, Entry
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkImage, CTkFont, CTkCanvas, CTkEntry
from PIL import Image

class ExceptionView(CTkFrame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, fg_color="transparent", *args, **kwargs)

        self.error_frame = CTkFrame(self.master)
        self.error_frame.place(
            relx=0.5, rely=0.5, anchor="center",
            relwidth=1, relheight=1
        )

        self.info_frame = CTkFrame(self.master)
        self.info_frame.place(
            relx=0.5, rely=0.5, anchor="center",
            relwidth=1, relheight=1
        )

        self._load_error()
        self._load_info()

    def _load_error(self):
        """Render the unchanging aspects of exception UI.
        """
        self.exception_frame = CTkFrame(self.error_frame, fg_color="transparent")
        self.exception_frame.pack(expand=True, padx=20, pady=20)

        self.error_image = CTkImage(Image.open("views/static/images/error.png"), size=(150, 150))

        self.error_image_label = CTkLabel(self.exception_frame, text="", image=self.error_image)
        self.error_image_label.pack(padx=20)

        self.error_type = CTkLabel(self.exception_frame, text="ERROR", font=("Arial", 28, "bold"))
        self.error_type.pack(pady=25)

        self.error_msg = CTkLabel(self.exception_frame, font=("Arial", 18))
        self.error_msg.pack()

        self.error_button = CTkButton(self.exception_frame, corner_radius=5, text="TRY AGAIN", font=("Arial", 21), width=250, height=40, fg_color="#e6534e")
        self.error_button.pack(pady=(50, 0))

        self.hide_error_view()

    def _load_info(self):
        """Render specific exception passed through from calling object.
        """
        self.info_content_frame = CTkFrame(self.info_frame, fg_color="transparent")
        self.info_content_frame.pack(expand=True, padx=20, pady=20)

        self.info_image = CTkImage(Image.open("views/static/images/error.png"), size=(150, 150))

        self.info_image_label = CTkLabel(self.info_content_frame, text="", image=self.error_image)
        self.info_image_label.pack(padx=20)

        self.info_type = CTkLabel(self.info_content_frame, text="INFO", font=("Arial", 28, "bold"))
        self.info_type.pack(pady=25)

        self.info_msg = CTkLabel(self.info_content_frame, font=("Arial", 18))
        self.info_msg.pack()

        self.info_button = CTkButton(self.info_content_frame, corner_radius=5, text="CONFIRM", font=("Arial", 21), width=250, height=40, fg_color="green")
        self.info_button.pack(pady=(50, 0))

        self.hide_info_view()

    def display_error(self, error):
        """Display a custom error from caller. 

        Args:
            error (str): String to describe the type of error. 
        """
        self.error_msg.configure(text=error)
        self.error_frame.lift()

    def hide_error_view(self):
        """Hide frame for error.
        """
        self.error_frame.lower()

    def display_info(self, info):
        """Display a custom info from caller.

        Args:
            info (str): String to describe the info. 
        """
        self.info_msg.configure(text=info)
        self.info_frame.lift()

    def hide_info_view(self):
        """Hide frame for info.
        """
        self.info_frame.lower()