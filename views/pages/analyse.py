from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkOptionMenu, CTkEntry, CTkScrollbar, CTkTabview
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
        self.tabview = CTkTabview(master=self, fg_color="gray14", width=744, height=563)
        self.tabview.add("Entire Dataset")
        self.tabview.add("Individual Columns")
        self.tabview.add("Visualise / Tabulate")
        self.tabview.pack()

        self.entire_dataset_parent_frame = CTkFrame(self.tabview.tab("Entire Dataset"), fg_color="gray14")
        self.entire_dataset_parent_frame.pack(fill="x", expand=True, pady=0, padx=0)

        self.individual_cols_parent_frame = CTkFrame(self.tabview.tab("Individual Columns"), fg_color="gray14")
        self.individual_cols_parent_frame.pack(fill="x", expand=True, pady=0, padx=0)

        self.plot_tabulate_parent_frame = CTkFrame(self.tabview.tab("Visualise / Tabulate"), fg_color="gray14")
        self.plot_tabulate_parent_frame.pack(fill="both", expand=True, padx=0, pady=(0, 0))

        # Descriptive Stats - Entire Dataset
        self.ds_frame = CTkFrame(self.entire_dataset_parent_frame, fg_color="transparent")
        self.ds_frame.pack(fill="x", pady=(0, 0), padx=0)
        self.desc_stats_label = CTkLabel(self.ds_frame, text="Descriptive", font=("Arial", 14, "bold"), anchor="w")
        self.desc_stats_label.pack(side="left", expand=False, padx=(8, 0))
        self.ds_table_frame = CTkFrame(self.entire_dataset_parent_frame, fg_color="transparent")   
        self.ds_table_frame.pack(fill="x", pady=(5, 0), padx=0)
        self.desc_stats_tree_view = self.build_table(
            self.ds_table_frame, ("#", "Column", "Non-Null Count", "Data Type"), height=5, width=10
            )
        self.desc_stats_y_scroll = CTkScrollbar(
            self.ds_table_frame, orientation="vertical", height=59, fg_color="gray14", 
            command=self.desc_stats_tree_view.yview
            )
        self.desc_stats_y_scroll.pack(side="right", fill="y")
        self.desc_stats_tree_view.configure(yscrollcommand=self.desc_stats_y_scroll.set)
        self.desc_stats_tree_view.pack(side="left", fill="x", expand=True)

        # Summary Statistics - Individual Columns
        self.ss_frame = CTkFrame(self.entire_dataset_parent_frame, fg_color="transparent")
        self.ss_frame.pack(fill="x", pady=(10, 0), padx=0, expand=True)
        self.summary_stats_label = CTkLabel(self.ss_frame, text="Summary", font=("Arial", 14, "bold"), anchor="w")
        self.summary_stats_label.pack(side="left", expand=False, padx=(8, 0))
        self.ss_table_frame = CTkFrame(self.entire_dataset_parent_frame, fg_color="transparent")   
        self.ss_table_frame.pack(fill="x", pady=(5, 0), padx=0)
        #self.summary_table_tree_view = ttk.Treeview(self.ss_table_frame) # stub
        self.summary_table_tree_view = self.build_table(
            self.ss_table_frame, ("#", "Column", "Non-Null Count", "Data Type"), height=5, width=10
            )
        self.summary_table_y_scroll = CTkScrollbar(
            self.ss_table_frame, orientation="vertical", height=59, fg_color="gray14", 
            command=self.summary_table_tree_view.yview
            )
        self.summary_table_y_scroll.pack(side="right", fill="y")
        self.summary_table_tree_view.configure(yscrollcommand=self.summary_table_y_scroll.set)
        
        self.summary_table_x_scroll = CTkScrollbar(
            self.ss_table_frame, orientation="horizontal", width=59, fg_color="gray14", 
            command=self.summary_table_tree_view.xview
            )
        self.summary_table_x_scroll.pack(side="bottom", fill="x")
        self.summary_table_tree_view.configure(xscrollcommand=self.summary_table_x_scroll.set)
        #self.summary_table_tree_view.pack()
        self.summary_table_tree_view.pack(side="left", fill="x", expand=True)

        # Correlation Analysis
        self.ca_frame = CTkFrame(self.entire_dataset_parent_frame, fg_color="transparent")
        self.ca_frame.pack(fill="x", pady=(10, 0), padx=0, expand=True)
        self.correlation_label = CTkLabel(
            self.ca_frame, text="Correlation Statistics", font=("Arial", 14, "bold"), anchor="w"
            )
        self.correlation_label.pack(side="left", expand=False, padx=(8, 0))
        self.ca_table_frame = CTkFrame(self.entire_dataset_parent_frame, fg_color="transparent")   
        self.ca_table_frame.pack(fill="x", pady=(5, 0), padx=0)
        #self.correlate_table_tree_view = ttk.Treeview(self.ca_frame) # stub
        #self.correlate_table_tree_view.pack()
        self.correlation_table_tree_view = self.build_table(
            self.ca_table_frame, ("#", "Column", "Non-Null Count", "Data Type"), height=5, width=10
            )
        self.correlation_table_y_scroll = CTkScrollbar(
            self.ca_table_frame, orientation="vertical", height=59, fg_color="gray14", 
            command=self.correlation_table_tree_view.yview
            )
        self.correlation_table_y_scroll.pack(side="right", fill="y")
        self.correlation_table_tree_view.configure(yscrollcommand=self.correlation_table_y_scroll.set)
        
        self.correlation_table_x_scroll = CTkScrollbar(
            self.ca_table_frame, orientation="horizontal", width=59, fg_color="gray14", 
            command=self.correlation_table_tree_view.xview
            )
        self.correlation_table_x_scroll.pack(side="bottom", fill="x")
        self.correlation_table_tree_view.configure(xscrollcommand=self.correlation_table_x_scroll.set)
        #self.summary_table_tree_view.pack()
        self.correlation_table_tree_view.pack(side="left", fill="x", expand=True)

        # Individual Columns
        # Summary options
        self.is_frame = CTkFrame(self.individual_cols_parent_frame, fg_color="transparent")
        self.is_frame.pack(fill="x", pady=(0, 0), padx=0)
        self.summarise_label = CTkLabel(
            self.is_frame, text="Basic Info", font=("Arial", 14, "bold"), anchor="w"
            )
        self.summarise_label.pack(side="left", expand=False, padx=(8, 0))
        self.is_options_frame = CTkFrame(self.individual_cols_parent_frame, fg_color="gray20")
        self.is_options_frame.pack(fill="x", pady=(5, 0), padx=0)
        self.select_column_label = CTkLabel(self.is_options_frame, text="Column:", anchor="w")
        self.select_column_label.pack(side="left", expand=False, pady=(0, 0), padx=(8, 0))        
        self.select_column_menu = CTkOptionMenu(
            self.is_options_frame, fg_color="gray10", width=3, values=("------",),
            command=lambda option: self.reconfig_widgets(option, "summarise")
            )
        self.select_column_menu.pack(side="left", padx=(8, 0))

        # Summary table
        self.st_frame = CTkFrame(self.individual_cols_parent_frame, fg_color="transparent")
        self.st_frame.pack(fill="x", pady=(5, 0), padx=0, expand=True)
        self.adv_summary_tree_view = self.build_table(
            self.st_frame, ("SD", "Variance", "IQR", "Outlier Count", "Skew", "Kurtosis"), height=1, width=10
            )
        self.adv_summary_tree_view.pack(side="bottom", fill="both", pady=(0, 5), expand=True)
        
        self.basic_summary_tree_view = self.build_table(
            self.st_frame, ("Min", "Max", "Mean", "Median", "Mode", "Null Count"), height=1, width=10
        )
        self.basic_summary_tree_view.pack(side="bottom", fill="both", pady=(0, 5), expand=True)

        # Pivot options
        self.piv_frame = CTkFrame(self.individual_cols_parent_frame, fg_color="transparent")
        self.piv_frame.pack(fill="x", pady=(5, 0), padx=0)
        self.pivot_table_label = CTkLabel(self.piv_frame, text="Pivot Table", font=("Arial", 14, "bold"), anchor="w")
        self.pivot_table_label.pack(side="left", expand=False, padx=(8, 0))
        self.piv_frame_col1_row1 = CTkFrame(self.individual_cols_parent_frame, fg_color="gray20")
        self.piv_frame_col1_row1.pack(side="top", fill="x", pady=(5, 5), padx=0)
        self.categories_label = CTkLabel(self.piv_frame_col1_row1, text="Categories:", anchor="w")
        self.categories_label.pack(side="left", expand=False, padx=(8, 0))        
        self.categories_option_menu = CTkOptionMenu(
            self.piv_frame_col1_row1, fg_color="gray10", width=3, values=("------",), 
            command=lambda option: self.reconfig_widgets(option, "categories")
            )
        self.categories_option_menu.pack(side="left", padx=(8, 0))
        self.values_label = CTkLabel(self.piv_frame_col1_row1, text="Values:", anchor="w")
        self.values_label.pack(side="left", expand=False, padx=(8, 0))        
        self.values_option_menu = CTkOptionMenu(
            self.piv_frame_col1_row1, fg_color="gray10", width=3, values=("------",), state="disabled", 
            command=lambda option: self.reconfig_widgets(option, "values")
            )
        self.values_option_menu.pack(side="left", padx=(8, 0))
        self.agg_func_list = [
            "------", "count", "min", "max", "mean", "median", "mode", "sum", "std", "var"
            ]
        self.aggregate_function_label = CTkLabel(self.piv_frame_col1_row1, text="Aggregate:", anchor="w")
        self.aggfunc_option_menu = CTkOptionMenu(
            self.piv_frame_col1_row1, fg_color="gray10", width=3, values=self.agg_func_list, state="disabled", 
            command=lambda option: self.reconfig_widgets(option, "aggfunc")
            )
        self.pivot_round_value_label = CTkLabel(self.piv_frame_col1_row1, text="Rounding:", anchor="w")
        self.pivot_round_value_input = CTkEntry(self.piv_frame_col1_row1, corner_radius=5, width=50)

        # Pivot table
        self.pt_frame = CTkFrame(self.individual_cols_parent_frame, fg_color="transparent")
        self.pt_frame.pack(side="top", fill="both", pady=(0, 0), padx=0, expand=True)
        self.pt_table_frame = CTkFrame(self.pt_frame, fg_color="gray20")
        self.pt_table_frame.pack(side="left", fill="both")
        self.pivot_table = self.build_table(self.pt_table_frame, ("Categories", "------"), height=6)
        
        self.pivot_table_y_scroll = CTkScrollbar(
            self.pt_table_frame, orientation="vertical", height=40, fg_color="gray14", command=self.pivot_table.yview
            )
        self.pivot_table_y_scroll.pack(side="right", fill="y")
        self.pivot_table.configure(yscrollcommand=self.pivot_table_y_scroll.set)
        
        self.pivot_table.pack(side="top", fill="x", expand=True)
        self.pt_button_frame = CTkFrame(self.pt_frame, fg_color="transparent")
        self.pt_button_frame.pack(side="right", fill="both")
        self.pivot_button = CTkButton(
            self.pt_button_frame, text="Pivot", corner_radius=5, border_spacing=5, anchor="center", state="disabled"
            )
        self.pivot_button.pack(side="right", anchor="s", padx=(8, 8))

        # Placeholder - padding - invisible 3rd row
        self.place_holder_frame = CTkFrame(self.individual_cols_parent_frame, fg_color="transparent")
        self.place_holder_frame.pack(side="bottom", fill="both", pady=(0, 0), padx=0, expand=True)

        # Visualisations options
        self.v_frame = CTkFrame(self.plot_tabulate_parent_frame, fg_color="transparent")
        self.v_frame.pack(fill='x', pady=(0, 0), padx=0)
        self.visualise_label = CTkLabel(self.v_frame, text="Visualise", font=("Arial", 14, "bold"), anchor="w")
        self.visualise_label.pack(side="left", expand=False, padx=(8, 0))
        self.v_options_frame = CTkFrame(self.plot_tabulate_parent_frame, fg_color="gray20")
        self.v_options_frame.pack(fill='x', pady=(5, 0), padx=0)
        self.graph_label = CTkLabel(self.v_options_frame, text="Graph Style:", anchor="w")
        self.graph_label.pack(side="left", padx=(8, 0))
        self.graphing_options = ["------", "Box", "Heat Map", "Histogram", "Line", "Scatter", "Violin"]
        self.graph_option_menu = CTkOptionMenu(
            self.v_options_frame, fg_color="gray10", width=3, values=self.graphing_options, 
            command=lambda option: self.reconfig_widgets(option, "graph")
            )
        self.graph_option_menu.pack(side="left", padx=(8, 0))
        self.variable_a_label = CTkLabel(self.v_options_frame, text="Variable:", anchor="w")
        self.variable_a_label.pack(side="left", padx=(8, 0))
        self.variable_a_option_menu = CTkOptionMenu(
            self.v_options_frame, fg_color="gray10", width=3, state="disabled", values=("------",), 
            command=lambda option: self.reconfig_widgets(option, "var_a")
            )
        self.variable_a_option_menu.pack(side="left", padx=(8, 0))
        self.variable_b_label = CTkLabel(self.v_options_frame, text="Variable:", anchor="w")
        self.variable_b_option_menu = CTkOptionMenu(
            self.v_options_frame, fg_color="gray10", width=3, state="disabled", values=("------",), 
            command=lambda option: self.reconfig_widgets(option, "var_b")
            )
        self.plot_button = CTkButton(
            self.v_options_frame, text="Plot", corner_radius=5, border_spacing=5, anchor="center", state="disabled"
            )
        self.plot_button.pack(side="right", padx=(8, 8))

        # Tabulate options
        self.to_frame = CTkFrame(self.plot_tabulate_parent_frame, fg_color="transparent")
        self.to_frame.pack(fill="x", pady=(10, 0), padx=0)
        self.tabulate_label = CTkLabel(self.to_frame, text="Tabulate", font=("Arial", 14, "bold"), anchor="w")
        self.tabulate_label.pack(side="left", expand=False, padx=(8, 0))
        self.t_options_frame = CTkFrame(self.plot_tabulate_parent_frame, fg_color="gray20")
        self.t_options_frame.pack(fill='x', pady=(5, 0), padx=0)
        self.row_count_label = CTkLabel(self.t_options_frame, text="Row Count:", anchor="w")
        self.row_count_label.pack(side="left", expand=False, padx=(8, 0))
        self.row_count_value_label = CTkLabel(self.t_options_frame, text="", anchor="w")
        self.row_count_value_label.pack(side="left", expand=False, padx=(8, 0))
        self.tabulate_button = CTkButton(
            self.t_options_frame, text="Tabulate", corner_radius=5, border_spacing=5, anchor="center"
            )
        self.tabulate_button.pack(side="right", padx=(8, 8))
        self.end_row_input = CTkEntry(self.t_options_frame, corner_radius=5, width=50)
        self.end_row_input.pack(side="right", padx=(5, 0))
        self.end_row_label = CTkLabel(self.t_options_frame, text="End Row:", anchor="w")
        self.end_row_label.pack(side="right", expand=False, padx=(8, 0))
        self.start_row_input = CTkEntry(self.t_options_frame, corner_radius=5, width=50)
        self.start_row_input.pack(side="right", padx=(5, 0))
        self.start_row_label = CTkLabel(self.t_options_frame, text="Start Row:", anchor="w")
        self.start_row_label.pack(side="right", expand=False, padx=(8, 0))

        # Tabulate table
        self.tt_frame = CTkFrame(self.plot_tabulate_parent_frame, fg_color="gray10", height=30)
        self.tt_frame.pack(side="top", fill="both", expand=True, padx=0, pady=(10, 0))
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
        self.select_column_menu.configure(values=column_headers) # summarise
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
    
    def clear_table(self, table):
        """Remove data values from table. 

        Args:
            table (ttk.Treeview): Table on which to perform action.
        """
        for item in table.get_children(): 
            table.delete(item)
    
    def populate_summary_tables(self, d): 
        """Populate the summary table with descriptive statistics. 

        Args:
            d (dict): dictionary of values returned from calculations of model and 
            passed through by controller.
        """
        self.clear_table(self.basic_summary_tree_view)
        self.clear_table(self.adv_summary_tree_view)
        self.basic_summary_tree_view.insert("", "end", values=(
            d["Min"], d["Max"], d["Mean"], d["Median"], d["Mode"], d["Null Count"]
            )
        )
        self.adv_summary_tree_view.insert("", "end", values=(
            d["SD"], d["Variance"], d["IQR"], d["Outlier Count"], d["Skew"], d["Kurtosis"]
            )
        )
        
    def populate_pivot_table(self, d): 
        """Populate the pivot table with appropriate information.

        Args:
            d (dict): dictionary of pivot related keys and values
        """
        self._change_table_heading( # Change name of aggregate function column header to selected
            table=self.pivot_table, target_header="#2", new_header=self.aggfunc_option_menu.get()
            )
        self.clear_table(self.pivot_table) # Clear
        
        for key, value in d.items():
            self.pivot_table.insert("", "end", values=(key, value))

    def create_and_populate_raw_table(self, container_frame, column_headers, rows): 
        """Populate tabulate section with raw table data from the loaded dataset. 
        
        Args:
            container_frame (CTkFrame): Frame that will hold this widget
            column_headers (list): List of strings which contain column headers
            rows (pandas DataFrame): Specific row range.
        """
        self._delete_child_widgets_refresh_container(parent=self.tt_frame) # Refresh

        # Create tabulate table
        self.raw_table = self.build_table(
            root=container_frame, tuple_of_col_names=column_headers, height=10, width=None
            )
        self.raw_table_x_scroll = CTkScrollbar(
            container_frame, orientation="horizontal", fg_color="gray14", command=self.raw_table.xview
            )
        self.raw_table_x_scroll.pack(side="bottom", fill="x")
        self.raw_table.configure(xscrollcommand=self.raw_table_x_scroll.set)
        self.raw_table_y_scroll = CTkScrollbar(
            container_frame, orientation="vertical", fg_color="gray14", command=self.raw_table.yview
            )
        self.raw_table_y_scroll.pack(side="right", fill="y")
        self.raw_table.configure(yscrollcommand=self.raw_table_y_scroll.set)
        self.raw_table.pack(side="top", fill="both", expand=True)

        # Populate table with rows
        for index, row in rows.iterrows():
            self.raw_table.insert('', 'end', values=row.tolist())

    def _delete_child_widgets_refresh_container(self, parent):
        """Used for purposes of clearing contents of an entire container object for re-rendering.

        Args:
            parent (CTkFrame): Parent frame (container) of which the child widgets need
            to be removed. 
        """
        for widget in parent.winfo_children():
            widget.destroy()
        
    def _change_table_heading(self, table, target_header, new_header): 
        """Change heading of table (specifically used for pivot feature. 
        
        Args:
            table (ttk.Treeview): Targeted table to change header for.
            target_header (str): Target_header a single value e.g. "#1", "#2" etc. 
            new_header (str): Name of new header i.e. used for aggregate functionality e.g. "Median".
        """
        table.heading(f"{target_header}", text=f"{new_header}")

    def reconfig_widgets(self, option, option_set): 
        """Toggle (disable or enable) the appropriate widget based on predefined conditions.

        Args:
            option (str): selected item of an options menu
            option_set (str): the specific options menu
        """
        def bulk_toggle(mode, list_of_widgets): 
            if mode == "off": 
                for w in list_of_widgets: 
                    w.configure(state="disabled")
            elif mode == "on": 
                for w in list_of_widgets: 
                    w.configure(state="normal")
            elif mode == "hide": 
                for w in list_of_widgets: 
                    w.pack_forget()
            elif mode == "show": 
                for w in list_of_widgets: 
                    w.pack(side="left", padx=(8, 0))
            elif mode == "reset_menu": 
                for w in list_of_widgets: 
                    w.set("------") 

        if option == "------":
            match option_set: 
                case "graph":
                    bulk_toggle("reset_menu", [
                        self.variable_a_option_menu, self.variable_b_option_menu]
                        )
                    bulk_toggle("off", [
                        self.variable_a_option_menu, self.variable_b_option_menu, 
                        self.plot_button
                        ])
                    bulk_toggle("hide", [
                        self.variable_b_label, self.variable_b_option_menu
                        ])
                case "var_a":
                    bulk_toggle("reset_menu", [
                        self.variable_b_option_menu
                        ])
                    bulk_toggle("off", [
                        self.plot_button
                    ])
                case "var_b": 
                    bulk_toggle("off", [
                        self.plot_button
                    ])
                case "categories":
                    bulk_toggle("reset_menu", [
                        self.values_option_menu, self.aggfunc_option_menu]
                        )
                    bulk_toggle("off", [
                        self.values_option_menu, self.aggfunc_option_menu, 
                        self.pivot_button
                        ])
                    bulk_toggle("hide", [
                        self.aggregate_function_label, self.aggfunc_option_menu, 
                        self.pivot_round_value_label, self.pivot_round_value_input
                        ])
                case "values":
                    bulk_toggle("reset_menu", [
                        self.aggfunc_option_menu]
                        )
                    bulk_toggle("off", [
                        self.aggfunc_option_menu, self.pivot_button
                        ])
                    bulk_toggle("hide", [
                        self.aggregate_function_label, self.aggfunc_option_menu, 
                        self.pivot_round_value_label, self.pivot_round_value_input
                        ])
                case "aggfunc":
                    bulk_toggle("off", [
                        self.pivot_button
                    ])
                    bulk_toggle("hide", [
                        self.pivot_round_value_label, self.pivot_round_value_input
                    ])
        else: # != "------"
            match option_set: 
                case "graph":
                    bulk_toggle("reset_menu", [ # Always reset variables
                        self.variable_a_option_menu, self.variable_b_option_menu]
                    )
                    bulk_toggle("off", [ # Always disable plot after reset
                        self.plot_button
                    ])
                    if self.graph_option_menu.get() == "Scatter":
                        bulk_toggle("on", [
                            self.variable_b_option_menu
                        ])
                        bulk_toggle("show", [
                           self.variable_b_label, self.variable_b_option_menu
                        ])
                        bulk_toggle("off", [
                            self.plot_button
                        ])
                    else: 
                        bulk_toggle("off", [
                            self.variable_b_option_menu
                        ])
                        bulk_toggle("hide", [
                            self.variable_b_label, self.variable_b_option_menu
                        ])
                    if self.graph_option_menu.get() == "Heat Map": 
                        bulk_toggle("off", [
                            self.variable_a_option_menu
                        ])
                        bulk_toggle("on", [
                            self.plot_button
                        ])
                    else: 
                        bulk_toggle("on", [
                            self.variable_a_option_menu
                            ])
                case "var_a":
                    if self.graph_option_menu.get() != "Scatter": 
                        bulk_toggle("on", [
                            self.plot_button
                            ])
                    else: 
                        if self.variable_b_option_menu.get() != "------": 
                            bulk_toggle("on", [
                                self.plot_button
                                ])
                case "var_b": 
                    if self.variable_a_option_menu.get() != "------": 
                        bulk_toggle("on", [
                            self.plot_button
                            ])
                case "categories":
                    bulk_toggle("on", [
                        self.values_option_menu
                        ])
                case "values":
                    bulk_toggle("on", [
                        self.aggfunc_option_menu
                    ])
                    bulk_toggle("show", [
                        self.aggregate_function_label, self.aggfunc_option_menu
                        ])
                case "aggfunc":
                    bulk_toggle("on", [
                        self.pivot_button
                    ])
                    bulk_toggle("show", [
                        self.pivot_round_value_label, self.pivot_round_value_input
                    ])
                    