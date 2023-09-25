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
            self.v_frame, fg_color="gray10", width=3, state="normal", values=("------",), 
            command=lambda option: self.reconfig_widgets(option, "var_a")
            )
        self.variable_a_option_menu.pack(side="left", padx=(8, 0))
        self.variable_b_label = CTkLabel(self.v_frame, text="Variable:", anchor="w")
        self.variable_b_option_menu = CTkOptionMenu(
            self.v_frame, fg_color="gray10", width=3, state="normal", values=("------",), 
            command=lambda option: self.reconfig_widgets(option, "var_b")
            )
        self.plot_button = CTkButton(
            self.v_frame, text="Plot", corner_radius=5, border_spacing=5, anchor="center", state="normal"
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
        self.summary_round_value_input = CTkEntry(self.so_frame, corner_radius=5, width=50, state="normal")
        self.summary_round_value_input.pack(side="left", padx=(5, 0))
        self.null_value_label = CTkLabel(self.so_frame, text="Null Value:", anchor="w")
        self.null_value_label.pack(side="left", expand=False, padx=(8, 0))        
        self.null_value_input = CTkEntry(self.so_frame, corner_radius=5, width=50, state="normal")
        self.null_value_input.pack(side="left", padx=(5, 0))
        self.summarise_button = CTkButton(
            self.so_frame, text="Summarise", corner_radius=5, border_spacing=5, anchor="center", state="normal"
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
            self.po_frame_col1_row1, fg_color="gray10", width=3, values=("------",), state="normal", 
            command=lambda option: self.reconfig_widgets(option, "values")
            )
        self.values_option_menu.pack(side="left", padx=(8, 0))
        self.agg_func_list = [
            "------", "count", "min", "max", "mean", "median", "mode", "sum", "std", "var"
            ]
        self.aggregate_function_label = CTkLabel(self.po_frame_col1_row1, text="Aggregate:", anchor="w")
        self.aggfunc_option_menu = CTkOptionMenu(
            self.po_frame_col1_row1, fg_color="gray10", width=3, values=self.agg_func_list, state="normal", 
            command=lambda option: self.reconfig_widgets(option, "aggfunc")
            )
        self.aggregate_function_label.pack(side="left", padx=(8, 8))
        self.aggfunc_option_menu.pack(side="left", padx=(8, 0))

        self.pivot_round_value_label = CTkLabel(self.po_frame_col1_row1, text="Rounding:", anchor="w")
        self.pivot_round_value_label.pack(side="left", padx=(8, 0))
        self.pivot_round_value_input = CTkEntry(self.po_frame_col1_row1, corner_radius=5, width=50)
        self.pivot_round_value_input.pack(side="left", padx=(8, 0))

        # Pivot table
        self.pt_frame = CTkFrame(self.parent_frame, fg_color="transparent", height=55)
        self.pt_frame.pack(side="top", fill="both", pady=(0, 0), padx=20, expand=True)
        self.pt_table_frame = CTkFrame(self.pt_frame)
        self.pt_table_frame.pack(side="left", fill="both")
        self.pivot_table = self.build_table(self.pt_table_frame, ("Categories", "------"), 1)
        
        self.pivot_table_y_scroll = CTkScrollbar(
            self.pt_table_frame, orientation="vertical", height=59, fg_color="gray30", command=self.pivot_table.yview
            )
        self.pivot_table_y_scroll.pack(side="right")
        self.pivot_table.configure(yscrollcommand=self.pivot_table_y_scroll.set)
        
        self.pivot_table.pack(side="top", fill="x", expand=True)
        self.pt_button_frame = CTkFrame(self.pt_frame, fg_color="transparent")
        self.pt_button_frame.pack(side="right", fill="both")
        self.pivot_button = CTkButton(
            self.pt_button_frame, text="Pivot", corner_radius=5, border_spacing=5, anchor="center", state="normal"
            )
        self.pivot_button.pack(side="right", padx=(8, 8))

        # Tabulate options
        self.to_frame = CTkFrame(self.table_frame, fg_color="transparent")
        self.to_frame.pack(fill="x", pady=(20, 10), padx=20)
        self.row_count_label = CTkLabel(self.to_frame, text="Row Count:", anchor="w")
        self.row_count_label.pack(side="left", expand=False, padx=(8, 0))
        self.row_count_value_label = CTkLabel(self.to_frame, text="", anchor="w")
        self.row_count_value_label.pack(side="left", expand=False, padx=(8, 0))
        self.tabulate_button = CTkButton(
            self.to_frame, text="Tabulate", corner_radius=5, border_spacing=5, anchor="center"
            )
        self.tabulate_button.pack(side="right", padx=(8, 8))
        self.end_row_input = CTkEntry(self.to_frame, corner_radius=5, width=50)
        self.end_row_input.pack(side="right", padx=(5, 0))
        self.end_row_label = CTkLabel(self.to_frame, text="End Row:", anchor="w")
        self.end_row_label.pack(side="right", expand=False, padx=(8, 0))
        self.start_row_input = CTkEntry(self.to_frame, corner_radius=5, width=50)
        self.start_row_input.pack(side="right", padx=(5, 0))
        self.start_row_label = CTkLabel(self.to_frame, text="Start Row:", anchor="w")
        self.start_row_label.pack(side="right", expand=False, padx=(8, 0))

        # Tabulate table
        self.tt_frame = CTkFrame(self.table_frame, fg_color="gray10", height=30)
        self.tt_frame.pack(side="top", fill="both", expand=True, padx=20, pady=(0, 20))
        self.raw_table = ttk.Treeview(self.tt_frame) # stub

    def refresh_analyse_widgets(self, dataset_attributes):
        """Refresh, update or populate the values of various widgets on Analyse view with appropriate
        information pulled from the loaded dataset e.g. column headers for option menues, row count etc. 

        Args:
            dataset_attributes (tuple): A tuple consisting of row count and list of column headers (str).
        """
        row_count, column_headers = dataset_attributes
        self.row_count_value_label.configure(text=row_count) # row count
        self.variable_a_option_menu.configure(values=column_headers) # visualisations var_a
        self.variable_b_option_menu.configure(values=column_headers) # visualisations var_b
        self.summary_option_menu.configure(values=column_headers) # summarise
        self.categories_option_menu.configure(values=column_headers) # pivot category
        self.values_option_menu.configure(values=column_headers) # pivot value

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
    
    def clear_table(self):
        ...
    
    def populate_summary_tables(self): 
        ...

    def populate_pivot_table(self): 
        ...

    def create_and_populate_raw_table(self): 
        ...

    def change_table_heading(self): 
        ...

    def reconfig_widgets(self, option, option_set): 
        """Toggle (disable or enable) the appropriate widget based on predefined conditions.

        Args:
            option (str): selected item of an options menu
            option_set (str): the specific options menu
        """
        ...