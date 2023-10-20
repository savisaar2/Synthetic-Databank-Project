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
        self._render_page()

    def _render_page(self):
        """Renders widgets on the SampleView page."""
        self.parent_frame = CTkFrame(self, fg_color="gray20")
        self.parent_frame.pack(fill="both", pady=(0, 20), padx=20, expand=True)

        # Sampling options
        self.s_frame = CTkFrame(self.parent_frame, fg_color="transparent")
        self.s_frame.pack(fill='x', pady=(20, 0), padx=20)
        self.s_frame_row_1 = CTkFrame(self.s_frame, fg_color="gray15")
        self.s_frame_row_1.pack(fill="x", pady=(0, 20), padx=20)
        self.s_frame_row_2 = CTkFrame(self.s_frame, fg_color="gray15")
        self.s_frame_row_2.pack(fill="x", pady=(0, 20), padx=20)
        self.s_frame_row_3 = CTkFrame(self.s_frame, fg_color="gray15")
        self.s_frame_row_3.pack(fill="x", pady=(0, 20), padx=20)
        
        self.algorithm_label = CTkLabel(self.s_frame_row_1, text="Sampling Algorithm:", anchor="w")
        self.algorithm_label.pack(side="left", padx=(8, 0))
        self.sampling_algo_options = [
            "------", "Simple Random", "Stratified", "Systematic", "Under", "Over", "Cluster", "Quota", "Judgement", 
            "Snowball"
            ]
        self.sampling_algo_menu = CTkOptionMenu(
            self.s_frame_row_1, fg_color="gray10", width=3, values=self.sampling_algo_options, 
            command=lambda option: self.reconfig_widgets(option, "sampling")
            )
        self.sampling_algo_menu.pack(side="left", padx=(8, 0))
        
        self.run = CTkButton( # Run (generate sample)!
            self.s_frame_row_3, text="Run", corner_radius=5, border_spacing=5, anchor="center", state="disabled"
            )
        self.run.pack(side="right", padx=(8, 8))

        # Simple Random - sub widgets
        self.sample_size_label = CTkLabel(self.s_frame_row_2, text="Sample Size:", anchor="w")
        self.sample_size_entry = CTkEntry(self.s_frame_row_2, corner_radius=5, width=50, state="disabled")

        # Stratified - sub widgets
        self.num_of_splits_label = CTkLabel(self.s_frame_row_2, text="Number of Splits:", anchor="w")
        self.num_of_splits_entry = CTkEntry(self.s_frame_row_2, corner_radius=5, width=50, state="disabled")
        self.stratified_dependant_col_label = CTkLabel(self.s_frame_row_2, text="Dependent Column:", anchor="w")
        self.stratified_dependant_col_menu = CTkOptionMenu(
            self.s_frame_row_2, fg_color="gray10", width=3, values=("------",), 
            command=lambda option: self.reconfig_widgets(option, "sampling")
        )
        # Systematic - sub widgets 
        self.sampling_interval_label = CTkLabel(self.s_frame_row_2, text="Sampling Interval:", anchor="w")
        self.sampling_interval_entry = CTkEntry(self.s_frame_row_2, corner_radius=5, width=50, state="disabled")

        # Under
        self.under_dependant_col_label = CTkLabel(self.s_frame_row_2, text="Dependent Column:", anchor="w")
        self.under_dependant_col_menu = CTkOptionMenu(
            self.s_frame_row_2, fg_color="gray10", width=3, values=("------",), 
            command=lambda option: self.reconfig_widgets(option, "sampling")
        )
        # Over
        self.over_dependant_col_label = CTkLabel(self.s_frame_row_2, text="Dependent Column:", anchor="w")
        self.over_dependant_col_menu = CTkOptionMenu(
            self.s_frame_row_2, fg_color="gray10", width=3, values=("------",), 
            command=lambda option: self.reconfig_widgets(option, "sampling")
        )
        # Cluster - sub widgets
        self.cluster_column_label = CTkLabel(self.s_frame_row_2, text="Cluster Column:", anchor="w")
        self.cluster_column_menu = CTkOptionMenu(
            self.s_frame_row_2, fg_color="gray10", width=3, values=("------",), 
            command=lambda option: self.reconfig_widgets(option, "sampling")
        )
        self.num_of_clusters_label = CTkLabel(self.s_frame_row_2, text="Number of Clusters:", anchor="w")
        self.num_of_clusters_entry = CTkEntry(self.s_frame_row_2, corner_radius=5, width=50, state="disabled")

        # Quota - sub widgets
        self.column_to_build_quota_label = CTkLabel(self.s_frame_row_2, text="Column to Build Quota:", anchor="w")
        self.column_to_build_quota_menu = CTkOptionMenu(
            self.s_frame_row_2, fg_color="gray10", width=3, values=("------",), 
            command=lambda option: self.reconfig_widgets(option, "sampling")
        )
        self.q_sample_size_label = CTkLabel(self.s_frame_row_2, text="Sample Size:", anchor="w")
        self.quota_sample_size_entry = CTkEntry(self.s_frame_row_2, corner_radius=5, width=50, state="disabled")

        # Judgement - sub widgets
        self.define_criteria_label = CTkLabel(self.s_frame_row_2, text="Column to Define Criteria:", anchor="w")
        self.define_criteria_menu = CTkOptionMenu(
            self.s_frame_row_2, fg_color="gray10", width=3, values=("------",), 
            command=lambda option: self.reconfig_widgets(option, "sampling")
        )
        self.comparison_operators_label = CTkLabel(self.s_frame_row_2, text="Comparison Operator:", anchor="w")
        self.comparison_operator_menu = CTkOptionMenu(
            self.s_frame_row_2, fg_color="gray10", width=3, values=(["------", "EQUAL", "LESS", "MORE", "NOT EQUAL"]),
            command=lambda option: self.reconfig_widgets(option, "sampling")
        )
        self.condition_label = CTkLabel(self.s_frame_row_3, text="Condition:", anchor="w")
        self.condition_entry = CTkEntry(self.s_frame_row_3, corner_radius=5, width=50, state="disabled")
        self.logical_operator_label = CTkLabel(self.s_frame_row_3, text="Logical Operator:", anchor="w")
        self.logical_operator_menu = CTkOptionMenu(
            self.s_frame_row_3, fg_color="gray10", width=3, values=(["------", "AND", "OR", "NOT"]), 
            command=lambda option: self.reconfig_widgets(option, "sampling")
        )
        # Snowball - sub widgets - TODO need clarificaiton

        # Widget toggle groupings
        self.all_widgets = [
            self.sample_size_label, self.sample_size_entry, self.num_of_splits_label, self.num_of_splits_entry, 
            self.sampling_interval_label, self.under_dependant_col_label, self.under_dependant_col_menu, 
            self.stratified_dependant_col_label, self.stratified_dependant_col_menu, self.over_dependant_col_label, 
            self.over_dependant_col_menu, self.cluster_column_label, self.cluster_column_menu, 
            self.num_of_clusters_label, self.num_of_clusters_entry, self.sampling_interval_entry, 
            self.column_to_build_quota_label, self.logical_operator_menu, self.logical_operator_label, 
            self.column_to_build_quota_menu, self.q_sample_size_label, self.quota_sample_size_entry, 
            self.define_criteria_label, self.define_criteria_menu, self.comparison_operators_label, 
            self.comparison_operator_menu, self.condition_label, self.condition_entry, 
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

        self.judgement_widgets = [
            self.define_criteria_label, self.define_criteria_menu, self.comparison_operators_label, 
            self.comparison_operator_menu, self.condition_label, self.condition_entry,
            self.logical_operator_label, self.logical_operator_menu
        ]

        self.algo_to_widget_set_mapping = {
            "Simple Random": self.simple_widgets, "Stratified": self.stratified_widgets, 
            "Systematic": self.systematic_widgets, "Under": self.under_widgets, "Over": self.over_widgets,
            "Cluster": self.cluster_widgets, "Quota": self.quota_widgets, "Judgement": self.judgement_widgets
        }

    def refresh_sample_widgets(self, column_headers):
        """Populate / update the values of the dropdown menus view with appropriate column headers 
        of the working dataset.

        Args:
            column_headers (list): A list of column headers (str).
        """
        self.dependant_col_menu.configure(values=column_headers) 

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

        if option_set == "sampling": 
            bulk_toggle("hide", [
                widget for widget in self.all_widgets
            ])
            bulk_toggle("show", self.algo_to_widget_set_mapping[option])
            bulk_toggle("off", [
                widget for widget in self.all_widgets
            ])
            bulk_toggle("on", self.algo_to_widget_set_mapping[option])
            
                        