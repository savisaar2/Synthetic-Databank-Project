from customtkinter import CTkFrame
from .base import BaseView

class SaveView(BaseView):
    def __init__(self, root, *args, **kwargs):
        """
        Initialise the Save view of the application.

        This class represents the SaveView page of the application.
        It renders the interactive widgets on the frontend of the application.

        Parameters
        ----------
        root : Root
            The applicaiton's root instance.
        """
        # Pass some base title and description to our BaseView class.
        super().__init__(root, "Save & Export", "Save your Dataset for later.", *args, **kwargs)
        self._render_page()

    def _render_page(self):
        """Renders widgets on the SaveView page."""
        pass