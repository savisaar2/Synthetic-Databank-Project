from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkTextbox, CTkEntry

class ImportView(CTkFrame):
    def __init__(self, root, *args, **kwargs):
        """
        Initialise the Import overlay of the application.

        This class represents the ImportView overlay of the application.
        It renders the interactive widgets on the frontend of the application.

        Parameters
        ----------
        root : Root
            The applicaiton's root instance.
        """
        super().__init__(root, *args, **kwargs)
        self._setup_page()

    def _setup_page(self):
        """Renders the widgets on the ImportView."""
        self.overlay_frame = CTkFrame(self.master)
        self.overlay_frame.place(
            relx=0.5, rely=0.5, anchor="center",
            relwidth=1, relheight=1
        )
        self.overlay_frame.lower()

        self.content_frame = CTkFrame(self.overlay_frame, fg_color="transparent")
        self.content_frame.pack(expand=True, padx=20, pady=20)

        self.title_label = CTkLabel(self.content_frame, text="Import New Dataset", font=("Arial", 24), anchor="center")
        self.title_label.pack(pady=20)

        self.file_frame = CTkFrame(self.content_frame, fg_color="#333333")
        self.file_frame.pack(fill="x", padx=10, pady=(0, 20))

        self.add_file_button = CTkButton(self.file_frame, corner_radius=5, text="Add File", font=("Arial", 16), height=40)
        self.add_file_button.pack(fill="x")

        self.loaded_file_label = CTkLabel(self.file_frame, text="", font=("Arial", 12), anchor="center")
        self.loaded_file_label.pack(pady=10)
        
        self.desc_frame = CTkFrame(self.content_frame)
        self.desc_frame.pack()

        self.desc_label = CTkLabel(self.desc_frame, text="Description:", font=("Arial", 18))
        self.desc_label.pack(side="top", anchor="w")

        self.description_entry = CTkTextbox(self.desc_frame, border_width=2, border_color="#575b5e", fg_color="#343638", corner_radius=5, font=("Arial", 16), width=300)
        self.description_entry.pack(side="bottom")

        self.source_frame = CTkFrame(self.content_frame)
        self.source_frame.pack(pady=20)

        self.source_label = CTkLabel(self.source_frame, text="Source:", font=("Arial", 18))
        self.source_label.pack(side="top", anchor="w")

        self.source_entry = CTkEntry(self.source_frame, corner_radius=5, font=("Arial", 16), width=300, height=40)
        self.source_entry.pack(side="bottom")

        button_frame = CTkFrame(self.content_frame)
        button_frame.pack(pady=10)

        self.import_button = CTkButton(button_frame, corner_radius=5, text="Import", font=("Arial", 16), width=150,
                                        height=40)
        self.import_button.pack(side="left", padx=5)

        self.cancel_button = CTkButton(button_frame, corner_radius=5, text="Cancel", font=("Arial", 16), width=150,
                                        height=40)
        self.cancel_button.pack(side="left", padx=5)

    def show_view(self):
        """Shows the ImportView overlay."""
        self.overlay_frame.lift()

    def hide_view(self):
        """Hides the ImportView overlay."""
        self.overlay_frame.lower()