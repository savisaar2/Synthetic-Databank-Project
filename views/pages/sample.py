from customtkinter import CTkFrame
from .base import BaseView

class SampleView(BaseView):
    def __init__(self, root, *args, **kwargs):
        """
        Initialise the Sample view of the application.

        This class represents the SampleView page of the application.
        It renders the interactive widgets on the frontend of the application.

        Parameters
        ----------
        root : Root
            The applicaiton's root instance.
        """
        # Pass some base title and description to our BaseView class.
        super().__init__(root, "Sample", "Create a Sample of your Dataset.", *args, **kwargs)
        self._render_page()

    def _render_page(self):
        """Renders widgets on the SampleView page."""
        pass