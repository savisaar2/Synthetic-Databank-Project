from customtkinter import CTkLabel, CTkButton
from PIL import Image, ImageTk

class ErrorView:
    def __init__(self, root, *args, **kwargs):
        """
        Initalize the Error Warning overlay of the application

        Parameters
        ----------
        root : Root
            The applicaiton's root instance.
        """
        super().__init__(root, *args, **kwargs)
        self._setup_page()

    def _setup_page(self, error_message):

        self.root.attributes("-fullscreen", True)

        # Image
        image = Image.open("views/static/images/error.png")
        image = image.resize((300, 300))
        photo = ImageTk.PhotoImage(image=image)
        self.image_label = CTkLabel(image=photo)
        self.image_label.image = photo
        self.image_label.pack(pady=20)

        # Labels
        self.error_label = CTkLabel(text="Error!", font=16)
        self.error_label.pack(pady=20)

        self.error_label = CTkLabel(text="An error has occurred:")
        self.error_label.pack(pady=20)

        self.error_message_label = CTkLabel(text=error_message)
        self.error_message_label.pack(pady=20)

        #Button
        self.back_button = CTkButton(text="Go Back")
        self.back_button.pack(pady=20)

