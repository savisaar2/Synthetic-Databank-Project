from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkOptionMenu, CTkEntry, CTkScrollbar
from tkinter import ttk
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
        """Renders widgets on the AnalyseView page.
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

        # Summary options
        self.so_frame = CTkFrame(self.parent_frame, fg_color="transparent")
        self.so_frame.pack(fill="x", pady=(20, 20), padx=20)
        self.summary_label = CTkLabel(self.so_frame, text="Summarise:", anchor="w")
        self.summary_label.pack(side="left", expand=False, padx=(8, 0))        
        self.summary_option_menu = CTkOptionMenu(
            self.so_frame, fg_color="gray10", width=3, values=("------",),
            command=lambda option: self.reconfig_widgets(option, "summarise")
            )
        self.summary_option_menu.pack(side="left", padx=(8, 0))
        self.summary_round_value_label = CTkLabel(self.so_frame, text="Rounding:", anchor="w")
        self.summary_round_value_label.pack(side="left", expand=False, padx=(8, 0))
        self.summary_round_value_input = CTkEntry(self.so_frame, corner_radius=5, width=50, state="disabled")
        self.summary_round_value_input.pack(side="left", padx=(5, 0))
        self.null_value_label = CTkLabel(self.so_frame, text="Null Value:", anchor="w")
        self.null_value_label.pack(side="left", expand=False, padx=(8, 0))        
        self.null_value_input = CTkEntry(self.so_frame, corner_radius=5, width=50, state="disabled")
        self.null_value_input.pack(side="left", padx=(5, 0))
        self.summarise_button = CTkButton(
            self.so_frame, text="Summarise", corner_radius=5, border_spacing=5, anchor="center", state="disabled"
            )
        self.summarise_button.pack(side="right", padx=(8, 8))

        # Summary table
        self.st_frame = CTkFrame(self.parent_frame, fg_color="transparent")
        self.st_frame.pack(fill="x", pady=(0, 20), padx=20, expand=True)
        self.adv_summary_tree_view = self.build_table(
            self.st_frame, ("SD", "Variance", "IQR", "Outlier Count", "Skew", "Kurtosis"), 1, 10
            )
        self.adv_summary_tree_view.pack(side="bottom", fill="both", expand=True)
        
        self.basic_summary_tree_view = self.build_table(
            self.st_frame, ("Min", "Max", "Mean", "Median", "Mode", "Null Count"), 1, 10
        )
        self.basic_summary_tree_view.pack(side="bottom", fill="both", pady=(0, 10), expand=True)

        # Pivot options
        self.po_frame_col1_row1 = CTkFrame(self.parent_frame, fg_color="transparent")
        self.po_frame_col1_row1.pack(side="top", fill="x", pady=(0, 20), padx=20)
        self.categories_label = CTkLabel(self.po_frame_col1_row1, text="Categories:", anchor="w")
        self.categories_label.pack(side="left", expand=False, padx=(8, 0))        
        self.categories_option_menu = CTkOptionMenu(
            self.po_frame_col1_row1, fg_color="gray10", width=3, values=("------",), 
            command=lambda option: self.reconfig_widgets(option, "categories")
            )
        self.categories_option_menu.pack(side="left", padx=(8, 0))
        self.values_label = CTkLabel(self.po_frame_col1_row1, text="Values:", anchor="w")
        self.values_label.pack(side="left", expand=False, padx=(8, 0))        
        self.values_option_menu = CTkOptionMenu(
            self.po_frame_col1_row1, fg_color="gray10", width=3, values=("------",), state="disabled", 
            command=lambda option: self.reconfig_widgets(option, "values")
            )
        self.values_option_menu.pack(side="left", padx=(8, 0))
        self.agg_func_list = [
            "------", "count", "min", "max", "mean", "median", "mode", "sum", "std", "var"
            ]
        self.aggregate_function_label = CTkLabel(self.po_frame_col1_row1, text="Aggregate:", anchor="w")
        self.aggfunc_option_menu = CTkOptionMenu(
            self.po_frame_col1_row1, fg_color="gray10", width=3, values=self.agg_func_list, state="disabled", 
            command=lambda option: self.reconfig_widgets(option, "aggfunc")
            )
        self.pivot_round_value_label = CTkLabel(self.po_frame_col1_row1, text="Rounding:", anchor="w")
        self.pivot_round_value_input = CTkEntry(self.po_frame_col1_row1, corner_radius=5, width=50)

    def build_table(self, root, tuple_of_col_names, height, width=None): 
        """Build a table of data for either pivot summary or for raw data view. 
        To be used specificially for treeview widget with horizontal and or vertical scrollbar. 
        Returns unpacked treeview widget.

        Args:
            root (CTkFrame): Parent frame in which the table will be embedded in.
            tuple_of_col_names (tuple): Tuple of strings to be used as column headers. 
            height (int): Height of the table.
            width (int, optional): Width of the table.

        Returns:
            ttk.Treeview: Returns the Treeview widget! Objects objects everywhere, first class objects FTW!
        """
        table = ttk.Treeview(root, columns=tuple_of_col_names, show="headings", selectmode="browse", height=height)
        
        for column in tuple_of_col_names: # Build headers
            table.heading(column, text=column)
            if width != None: 
                table.column(column, width=width, stretch=True)
            else: 
                table.column(column, stretch=True)
        
        return table

    def reconfig_widgets(self, option, option_set): 
        """Toggle (disable or enable) the appropriate widget based on predefined conditions.

        Args:
            option (str): selected item of an options menu
            option_set (str): the specific options menu
        """
        ...
