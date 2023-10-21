from customtkinter import CTkFrame, CTkLabel, CTkOptionMenu, CTkButton, CTkEntry, CTkCanvas, CTkScrollbar, CTkTextbox
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
        self.rows_of_operations = []
        self._render_page()

    def _render_page(self):
        """Renders widgets on the SampleView page."""
        self.parent_frame = CTkFrame(self, fg_color="gray14")
        self.parent_frame.pack(fill="both", pady=(0, 20), padx=20, expand=True)

        # Sampling options
        self.s_frame = CTkFrame(self.parent_frame, fg_color="gray14")
        self.s_frame.pack(side="top", fill='both', expand=True, pady=(0, 4), padx=0)
        self.s_frame_row_1 = CTkFrame(self.s_frame, fg_color="gray20")
        self.s_frame_row_1.pack(fill="x")
        
        self.advanced_algo_frame = CTkFrame(self.s_frame, fg_color="transparent") # rows of judgment & snowball 
        self.advanced_algo_frame.pack(side="top", fill="both", expand=True, pady=(5, 0))
        self.adv_algo_frame_scroll_y = CTkScrollbar(self.advanced_algo_frame, orientation="vertical")
        self.adv_algo_frame_scroll_y.pack(side="right", fill="y")
        self.canvas = CTkCanvas(self.advanced_algo_frame, height=50)
        self.canvas.configure(
            yscrollcommand=self.adv_algo_frame_scroll_y.set, bg="gray14", borderwidth=0, highlightthickness=0
            )
        self.canvas.pack(side="left", fill="both", anchor="n", expand=True)
        self.adv_algo_frame_scroll_y.configure(command=self.canvas.yview)
        self.scrollable_frame = CTkFrame(self.canvas, fg_color="gray14") # target
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.description_frame_row1 = CTkFrame(self.s_frame, fg_color="gray10")
        self.description_frame_row1.pack(fill="x", pady=(5, 0))

        self.description_frame_row2 = CTkFrame(self.s_frame, fg_color="gray10")
        self.description_frame_row2.pack(fill='x')
        
        self.algorithm_label = CTkLabel(self.s_frame_row_1, text="Algorithm:", anchor="w")
        self.algorithm_label.pack(side="left", padx=(8, 0))
        self.sampling_algo_options = [
            "------", "Simple Random", "Stratified", "Systematic", "Under", "Over", "Cluster", "Quota", "Judgment", 
            "Snowball"
            ]
        self.sampling_algo_menu = CTkOptionMenu(
            self.s_frame_row_1, fg_color="gray10", width=3, values=self.sampling_algo_options, 
            command=lambda option: self.reconfig_widgets(option)
            )
        self.sampling_algo_menu.pack(side="left", padx=(8, 0))
        
        self.generate = CTkButton( # Run (generate sample)!
            self.s_frame_row_1, text="Generate", corner_radius=5, border_spacing=5, anchor="center", state="disabled", 
            width=30 
            )
        self.generate.pack(side="right", padx=(8, 8))

        # Simple Random - sub widgets
        self.sample_size_label = CTkLabel(self.s_frame_row_1, text="Sample Size:", anchor="w")
        self.sample_size_entry = CTkEntry(self.s_frame_row_1, corner_radius=5, width=50, state="disabled")

        # Stratified - sub widgets
        self.num_of_splits_label = CTkLabel(self.s_frame_row_1, text="Number of Splits:", anchor="w")
        self.num_of_splits_entry = CTkEntry(self.s_frame_row_1, corner_radius=5, width=50, state="disabled")
        self.stratified_dependant_col_label = CTkLabel(self.s_frame_row_1, text="Dependent Column:", anchor="w")
        self.stratified_dependant_col_menu = CTkOptionMenu(
            self.s_frame_row_1, fg_color="gray10", width=3, values=("------",), 
            command=lambda option: self.reconfig_widgets(option)
        )
        # Systematic - sub widgets 
        self.sampling_interval_label = CTkLabel(self.s_frame_row_1, text="Sampling Interval:", anchor="w")
        self.sampling_interval_entry = CTkEntry(self.s_frame_row_1, corner_radius=5, width=50, state="disabled")

        # Under
        self.under_dependant_col_label = CTkLabel(self.s_frame_row_1, text="Dependent Column:", anchor="w")
        self.under_dependant_col_menu = CTkOptionMenu(
            self.s_frame_row_1, fg_color="gray10", width=3, values=("------",), 
            command=lambda option: self.reconfig_widgets(option)
        )
        # Over
        self.over_dependant_col_label = CTkLabel(self.s_frame_row_1, text="Dependent Column:", anchor="w")
        self.over_dependant_col_menu = CTkOptionMenu(
            self.s_frame_row_1, fg_color="gray10", width=3, values=("------",), 
            command=lambda option: self.reconfig_widgets(option)
        )
        # Cluster - sub widgets
        self.cluster_column_label = CTkLabel(self.s_frame_row_1, text="Cluster Column:", anchor="w")
        self.cluster_column_menu = CTkOptionMenu(
            self.s_frame_row_1, fg_color="gray10", width=3, values=("------",), 
            command=lambda option: self.reconfig_widgets(option)
        )
        self.num_of_clusters_label = CTkLabel(self.s_frame_row_1, text="Number of Clusters:", anchor="w")
        self.num_of_clusters_entry = CTkEntry(self.s_frame_row_1, corner_radius=5, width=50, state="disabled")

        # Quota - sub widgets
        self.column_to_build_quota_label = CTkLabel(self.s_frame_row_1, text="Column to Build Quota:", anchor="w")
        self.column_to_build_quota_menu = CTkOptionMenu(
            self.s_frame_row_1, fg_color="gray10", width=3, values=("------",), 
            command=lambda option: self.reconfig_widgets(option)
        )
        self.q_sample_size_label = CTkLabel(self.s_frame_row_1, text="Sample Size:", anchor="w")
        self.quota_sample_size_entry = CTkEntry(self.s_frame_row_1, corner_radius=5, width=50, state="disabled")

        # Judgment & Snowball - sub widgets
        self.add_row = CTkButton(
            self.s_frame_row_1, text="Add", corner_radius=5, border_spacing=5, anchor="center",state="normal", width=20,
            command=self.add_judgment_snowball_row
            )
        self.remove_row = CTkButton(
            self.s_frame_row_1, text="Remove", corner_radius=5, border_spacing=5, anchor="center",state="normal", width=20,
            command=self.remove_judgment_snowball_row
            )

        # Widget toggle groupings
        self.all_widgets = [
            self.sample_size_label, self.sample_size_entry, self.num_of_splits_label, self.num_of_splits_entry, 
            self.sampling_interval_label, self.under_dependant_col_label, self.under_dependant_col_menu, 
            self.stratified_dependant_col_label, self.stratified_dependant_col_menu, self.over_dependant_col_label,
            self.over_dependant_col_menu, self.cluster_column_label, self.cluster_column_menu, 
            self.num_of_clusters_label, self.num_of_clusters_entry, self.sampling_interval_entry, 
            self.column_to_build_quota_label, self.column_to_build_quota_menu, self.q_sample_size_label, 
            self.quota_sample_size_entry, self.add_row, self.remove_row
            ]
        
        self.simple_widgets = [
            self.sample_size_label, self.sample_size_entry
        ]

        self.stratified_widgets = [
            self.num_of_splits_label, self.num_of_splits_entry, self.stratified_dependant_col_label, 
            self.stratified_dependant_col_menu
        ]

        self.systematic_widgets = [
            self.sampling_interval_label, self.sampling_interval_entry
        ]

        self.under_widgets = [
            self.under_dependant_col_label, self.under_dependant_col_menu
        ]

        self.over_widgets = [
            self.over_dependant_col_label, self.over_dependant_col_menu
        ]

        self.cluster_widgets = [
            self.cluster_column_label, self.cluster_column_menu, self.num_of_clusters_label, self.num_of_clusters_entry
        ]

        self.quota_widgets = [
            self.column_to_build_quota_label, self.column_to_build_quota_menu, self.q_sample_size_label, 
            self.quota_sample_size_entry
        ]

        self.judgment_snowball_widgets = [
            self.add_row, self.remove_row
        ]

        self.algo_to_widget_set_mapping = {
            "Simple Random": self.simple_widgets, "Stratified": self.stratified_widgets, 
            "Systematic": self.systematic_widgets, "Under": self.under_widgets, "Over": self.over_widgets,
            "Cluster": self.cluster_widgets, "Quota": self.quota_widgets, "Judgment": self.judgment_snowball_widgets,
            "Snowball": self.judgment_snowball_widgets
        }

    class judgment_snowball_row: 
        """Instance of a row of widgets
        """
        def __init__(self, parent_frame): 
            self.row = CTkFrame(parent_frame, fg_color="gray20")
            self.row.pack(side="top", pady=(5, 5), fill="x")
            self.criteria_label = CTkLabel(self.row, text="Criteria:", anchor="w")
            self.criteria_label.pack(side="left", padx=(8, 0))
            self.criteria_menu = CTkOptionMenu(self.row, fg_color="gray10", width=3, values=("------",))
            self.criteria_menu.pack(side="left", padx=(8, 0))
            self.comparison_label = CTkLabel(self.row, text="IS", anchor="w")
            self.comparison_label.pack(side="left", padx=(8, 0))
            self.comparison_operators = [
                "------", "EQUAL", "LESS", "MORE", "NOT EQUAL"
                ]
            self.comparison_menu = CTkOptionMenu(self.row, fg_color="gray10", width=3, values=(self.comparison_operators))
            self.comparison_menu.pack(side="left", padx=(8, 0))
            self.condition_label = CTkLabel(self.row, text="Condition:", anchor="w")
            self.condition_label.pack(side="left", padx=(8, 0))
            self.condition_entry = CTkEntry(self.row, corner_radius=5, width=50)
            self.condition_entry.pack(side="left", padx=(8, 0))
            self.logical_operators = [
                "------", "AND", "OR", "NOT"
                ]
            self.logical_operator_menu = CTkOptionMenu(self.row, fg_color="gray10", width=3, values=(self.logical_operators))
            self.logical_operator_menu.pack(side="left", padx=(8, 0))

    def add_judgment_snowball_row(self): 
        """For use with "judgment" and "snowball" algorithms of sampling. Will add new rows of widgets 
        at user discretion based on last known logical operator selected. 

        Args: 
            container (frame or canvas widget): the container object in which to render rows of widgets.
        """
        new_row = self.judgment_snowball_row(self.scrollable_frame)
        self.rows_of_operations.append(new_row)
        self.refresh_canvas()

    def remove_judgment_snowball_row(self):
        if len(self.rows_of_operations) > 0: 
            last_row = self.rows_of_operations[-1]
            last_row.row.destroy() # mojo
            self.rows_of_operations.pop()
        self.refresh_canvas()            

    def refresh_canvas(self): 
        """_summary_
        """
        self.canvas.update_idletasks() # refresh canvas
        self.on_configure("x")

    def clear_child_widgets(self, mode, widget):
        """Remove child widgets from container widget, either table or frame

        Args:
            mode (str): "last", "all"
            widget (ttk.Frame): table or frame.
        """
        if mode == "last": 
            del widget.winfo_children()[-1]
        elif mode == "all":
            for item in widget.winfo_children():
                item.destroy()

    def on_configure(self, event): 
        """_summary_
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def refresh_sample_widgets(self, mode, column_headers):
        """Populate / update the values of the dropdown menus view with appropriate column headers 
        of the working dataset.

        Args:
            mode (str): "menus" or "rows", latter == Refresh criteria
                menus of judgment / snowball rows with column headers.
                former == standard menus outside of the rows. 
            column_headers (list): A list of column headers (str).
        """
        if mode == "menus": 
            self.stratified_dependant_col_menu.configure(values=column_headers)
            self.under_dependant_col_menu.configure(values=column_headers)
            self.over_dependant_col_menu.configure(values=column_headers)
            self.cluster_column_menu.configure(values=column_headers)
            self.column_to_build_quota_menu.configure(values=column_headers)
        elif mode == "rows": 
            if len(self.rows_of_operations) > 0: 
                for row in self.rows_of_operations: 
                    row.criteria_menu.configure(values=column_headers)

    def bulk_toggle(self, mode, list_of_widgets):
        """To be used with reconfig_widgets method.

        Args:
            mode (_type_): _description_
            list_of_widgets (_type_): _description_
        """
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

    def reconfig_widgets(self, option): 
        """Toggle (disable or enable) the appropriate widget based on predefined conditions.

        Args:
            option (str): selected item of an options menu
        """
        self.bulk_toggle("hide", [
            widget for widget in self.all_widgets
        ])
        self.bulk_toggle("off", [
            widget for widget in self.all_widgets
        ])

        self.rows_of_operations.clear() # clear first! 
        self.clear_child_widgets(mode="all", widget=self.scrollable_frame) # delete any child widgets! 
        
        self.bulk_toggle("show", self.algo_to_widget_set_mapping[option])
        self.bulk_toggle("on", self.algo_to_widget_set_mapping[option])
            
                        