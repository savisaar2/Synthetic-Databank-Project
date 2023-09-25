from customtkinter import CTkFrame
from .base import BaseView

class AnalyseView(BaseView):
    def __init__(self, root, *args, **kwargs):
        """
        Initialise the Analyse view of the application.

        This class represents the AnalyseView page of the application.
        It renders the interactive widgets on the frontend of the application.

        Parameters
        ----------
        root : Root
            The applicaiton's root instance.
        """
        # Pass some base title and description to our BaseView class.
        super().__init__(root, "Analyse", "Descriptive Statistics and Visualisations.", *args, **kwargs)
        self._render_page()

    def _render_page(self):
        """Renders widgets on the AnalyseView page."""
        
        self._render_page()

    def _render_page(self): 
        """Render the widgets! 
        """
        self.parent_frame = CTkFrame(self, fg_color="gray20")
        self.parent_frame.pack(fill="both", pady=(0, 20), padx=20, expand=False)

        self.table_frame = CTkFrame(self, fg_color="gray20")
        self.table_frame.pack(fill="both", padx=20, pady=(0, 20), expand=True)

    def reconfig_widgets(self, option, option_set): 
        """Tottle (disable or enable) the appropriate button based on whether a valid option is selected.

        Args:
            option (str): selected item of an options menu
            option_set (str): the specific options menu
        """
        ...
