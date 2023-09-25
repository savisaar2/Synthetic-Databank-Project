from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkOptionMenu, CTkEntry, CTkScrollbar
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

        # Visualisation options 
        self.v_frame = CTkFrame(self.parent_frame, fg_color="transparent")
        self.v_frame.pack(fill='x', pady=(20, 0), padx=20)
        self.graph_label = CTkLabel(self.v_frame, text="Graph Style:", anchor="w")
        self.graph_label.pack(side="left", padx=(8, 0))
        self.graphing_options = ["------", "Box", "Histogram", "Line", "Scatter", "Violin"]
        self.graph_option_menu = CTkOptionMenu(
            self.v_frame, fg_color="gray10", width=3, values=self.graphing_options, 
            command=lambda option: self.reconfig_widgets(option, "graph")
            )
        self.graph_option_menu.pack(side="left", padx=(8, 0))
        self.variable_a_label = CTkLabel(self.v_frame, text="Variable:", anchor="w")
        self.variable_a_label.pack(side="left", padx=(8, 0))
        self.variable_a_option_menu = CTkOptionMenu(
            self.v_frame, fg_color="gray10", width=3, state="disabled", values=("------",), 
            command=lambda option: self.reconfig_widgets(option, "var_a")
            )
        self.variable_a_option_menu.pack(side="left", padx=(8, 0))
        self.variable_b_label = CTkLabel(self.v_frame, text="Variable:", anchor="w")
        self.variable_b_option_menu = CTkOptionMenu(
            self.v_frame, fg_color="gray10", width=3, state="disabled", values=("------",), 
            command=lambda option: self.reconfig_widgets(option, "var_b")
            )
        self.plot_button = CTkButton(
            self.v_frame, text="Plot", corner_radius=5, border_spacing=5, anchor="center", state="disabled"
            )
        self.plot_button.pack(side="right", padx=(8, 8))

    def reconfig_widgets(self, option, option_set): 
        """Tottle (disable or enable) the appropriate button based on whether a valid option is selected.

        Args:
            option (str): selected item of an options menu
            option_set (str): the specific options menu
        """
        ...
