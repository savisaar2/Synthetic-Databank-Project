from customtkinter import CTkFrame, CTkFont, CTkLabel, CTkEntry, CTkButton
from .base import BaseView

class LibraryView(BaseView):
    def __init__(self, root, *args, **kwargs):
        """
        Initialise the Library view of the application.

        This class represents the LibraryView page of the application.
        It renders the interactive widgets on the frontend of the application.

        Parameters
        ----------
        root : Root
            The applicaiton's root instance.
        """
        # Pass some base title and description to our BaseView class.
        super().__init__(root, "Choose", "Pick or Import an Existing Dataset.", *args, **kwargs)
        self._render_page()

    def _render_page(self):
        """Renders widgets on the LibraryView page."""
        content_frame = self._create_frame(parent_frame=self, padx=20, pady=(0, 20))
        
        row_1 = self._create_frame(parent_frame=content_frame, pady=20)
        row_2 = self._create_frame(parent_frame=content_frame)
        row_3 = self._create_frame(parent_frame=content_frame)
        row_4 = self._create_frame(parent_frame=content_frame)

        self.search_label = self._create_label(row_1, str.upper("search"), "left")
        self.search_input = self._create_entry(row_1, "left")

        self.import_button = self._create_button(row_1, "Import", "left")
        self.new_button = self._create_button(row_1, "New", "left")

    def _create_frame(self, parent_frame, padx=0, pady=0):
        frame = CTkFrame(parent_frame)
        frame.pack(fill="x", padx=padx, pady=pady)
        return frame
    
    def _create_label(self, frame, text="Text Here", side=None):
        label = CTkLabel(frame, text=text, font=CTkFont(size=18, weight="normal"))
        label.pack(padx=20, anchor="w", side=side)
        return label
    
    def _create_entry(self, frame, side):
        entry = CTkEntry(frame, height=45)
        entry.pack(side=side, expand=True, fill="x", padx=10)
        return entry
    
    def _create_button(self, frame, text="Text Here", side="top"):
        button = CTkButton(frame, corner_radius=5, height=40, image="", border_spacing=10, text=text, anchor="n")
        button.pack(side=side, fill="x", padx=5)
        return button