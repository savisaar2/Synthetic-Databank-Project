from customtkinter import CTkFrame
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
        
        row_1 = self._create_frame(parent_frame=content_frame)
        row_2 = self._create_frame(parent_frame=content_frame)
        row_3 = self._create_frame(parent_frame=content_frame)
        row_4 = self._create_frame(parent_frame=content_frame)

    def _create_frame(self, parent_frame, padx=0, pady=0):
        frame = CTkFrame(parent_frame)
        frame.pack(fill="x", padx=padx, pady=pady)
        return frame