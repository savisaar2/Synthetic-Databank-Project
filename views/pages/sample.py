from customtkinter import CTkFrame, CTkLabel, CTkOptionMenu, CTkButton, CTkEntry, CTkCanvas, CTkScrollbar, CTkTextbox, CTkFont
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

        self.description_frame = CTkFrame(self.s_frame, fg_color="gray10")
        self.description_frame.pack(side="bottom", fill="both", pady=(5, 0))

        self.status_frame = CTkFrame(self.s_frame, fg_color="gray20")
        self.status_frame.pack(side="top", fill='both', pady=(10, 10), expand=True)
        self.sample_status_label = CTkLabel(
           master=self.status_frame, text="No Sample Yet Generated", text_color="yellow"
           )
        self.sample_status_label.pack(expand=True)

        self.algorithm_label = CTkLabel(self.s_frame_row_1, text="Algorithm:", anchor="w")
        self.algorithm_label.pack(side="left", padx=(8, 0))
        self.sampling_algo_options = [
            "------", "Simple Random", "Stratified", "Systematic", "Under", "Over", "Cluster", "Quota", "Judgment", 
            "Snowball"
            ]
        self.sampling_algo_menu = CTkOptionMenu(
            self.s_frame_row_1, fg_color="gray10", width=3, values=self.sampling_algo_options, 
            command=lambda option: self.reconfig_widgets(level="main", option=option)
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
        self.strat_sample_size_label = CTkLabel(self.s_frame_row_1, text="Sample Size:", anchor="w")
        self.strat_sample_size_entry = CTkEntry(self.s_frame_row_1, corner_radius=5, width=50, state="disabled")
        self.stratified_dependant_col_label = CTkLabel(self.s_frame_row_1, text="Dependent Column:", anchor="w")
        self.stratified_dependant_col_menu = CTkOptionMenu(
            self.s_frame_row_1, fg_color="gray10", width=3, values=("------",), 
            command=lambda option: self.reconfig_widgets(level="sub", option=option)
        )
        # Systematic - sub widgets 
        self.systematic_interval_label = CTkLabel(self.s_frame_row_1, text="Sampling Interval:", anchor="w")
        self.systematic_interval_entry = CTkEntry(self.s_frame_row_1, corner_radius=5, width=50, state="disabled")

        # Under
        self.under_dependant_col_label = CTkLabel(self.s_frame_row_1, text="Dependent Column:", anchor="w")
        self.under_target_col_menu = CTkOptionMenu(
            self.s_frame_row_1, fg_color="gray10", width=3, values=("------",), 
            command=lambda option: self.reconfig_widgets(level="sub", option=option)
        )
        # Over
        self.over_dependant_col_label = CTkLabel(self.s_frame_row_1, text="Dependent Column:", anchor="w")
        self.over_target_col_menu = CTkOptionMenu(
            self.s_frame_row_1, fg_color="gray10", width=3, values=("------",), 
            command=lambda option: self.reconfig_widgets(level="sub", option=option)
        )
        # Cluster - sub widgets
        self.cluster_sample_size_label = CTkLabel(self.s_frame_row_1, text="Sample Size:", anchor="w")
        self.cluster_sample_size_entry = CTkEntry(self.s_frame_row_1, corner_radius=5, width=50, state="disabled")
        self.cluster_column_label = CTkLabel(self.s_frame_row_1, text="Cluster Column:", anchor="w")
        self.cluster_column_menu = CTkOptionMenu(
            self.s_frame_row_1, fg_color="gray10", width=3, values=("------",), 
            command=lambda option: self.reconfig_widgets(level="sub", option=option)
        )

        # Quota - sub widgets
        self.column_to_build_quota_label = CTkLabel(self.s_frame_row_1, text="Column to Build Quota:", anchor="w")
        self.column_to_build_quota_menu = CTkOptionMenu(
            self.s_frame_row_1, fg_color="gray10", width=3, values=("------",), 
            command=lambda option: self.reconfig_widgets(level="sub", option=option)
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

        # Widget toggle groupings - used for both toggling and input validation
        self.all_widgets = [
            self.sample_size_label, self.sample_size_entry, self.strat_sample_size_label, self.strat_sample_size_entry, 
            self.systematic_interval_label, self.under_dependant_col_label, self.under_target_col_menu, 
            self.stratified_dependant_col_label, self.stratified_dependant_col_menu, self.over_dependant_col_label,
            self.over_target_col_menu, self.cluster_column_label, self.cluster_column_menu, 
            self.cluster_sample_size_label, self.cluster_sample_size_entry, self.systematic_interval_entry, 
            self.column_to_build_quota_label, self.column_to_build_quota_menu, self.q_sample_size_label, 
            self.quota_sample_size_entry, self.add_row, self.remove_row
            ]
        
        self.simple_widgets = [
            self.sample_size_label, self.sample_size_entry
        ]

        self.stratified_widgets = [
            self.strat_sample_size_label, self.strat_sample_size_entry, self.stratified_dependant_col_label, 
            self.stratified_dependant_col_menu
        ]

        self.systematic_widgets = [
            self.systematic_interval_label, self.systematic_interval_entry
        ]

        self.under_widgets = [
            self.under_dependant_col_label, self.under_target_col_menu
        ]

        self.over_widgets = [
            self.over_dependant_col_label, self.over_target_col_menu
        ]

        self.cluster_widgets = [
            self.cluster_sample_size_label, self.cluster_sample_size_entry, self.cluster_column_label, 
            self.cluster_column_menu
        ]

        self.quota_widgets = [
            self.q_sample_size_label, self.quota_sample_size_entry, self.column_to_build_quota_label, 
            self.column_to_build_quota_menu, 
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

        self.all_menu_option_widgets = { # hack to reset upon algo selection - needed to toggle "generate" button
            self.stratified_dependant_col_menu, self.under_target_col_menu, self.over_target_col_menu, 
            self.cluster_column_menu, self.column_to_build_quota_menu, 
        }

    class judgment_snowball_row: 
        """Instance of a row of widgets
        """
        def __init__(self, parent_frame, row_object_validation, rows): 
            self.row_object_validation = row_object_validation # outside method
            self.rows = rows # outside collection of rows
            self.row = CTkFrame(parent_frame, fg_color="gray20")
            self.row.pack(side="top", pady=(5, 5), fill="x")
            self.criteria_label = CTkLabel(self.row, text="Criteria:", anchor="w")
            self.criteria_label.pack(side="left", padx=(8, 0))
            self.criteria_menu = CTkOptionMenu(
                self.row, fg_color="gray10", width=3, values=("------",), command=lambda x: self.validate(self.rows)
                )
            self.criteria_menu.pack(side="left", padx=(8, 0))
            self.comparison_label = CTkLabel(self.row, text="IS", anchor="w")
            self.comparison_label.pack(side="left", padx=(8, 0))
            self.comparison_operators = [
                "------", "EQUAL", "LESS", "MORE", "NOT EQUAL"
                ]
            self.comparison_menu = CTkOptionMenu(
                self.row, fg_color="gray10", width=3, values=(self.comparison_operators), 
                command=lambda x: self.validate(self.rows)
                )
            self.comparison_menu.pack(side="left", padx=(8, 0))
            self.condition_label = CTkLabel(self.row, text="Condition:", anchor="w")
            self.condition_label.pack(side="left", padx=(8, 0))
            self.condition_entry = CTkEntry(self.row, corner_radius=5, width=50)
            self.condition_entry.pack(side="left", padx=(8, 0))
            self.logical_operators = [
                "------", "AND", "OR", "NOT"
                ]
            self.logical_operator_menu = CTkOptionMenu(
                self.row, fg_color="gray10", width=3, values=(self.logical_operators), 
                command=lambda x: self.validate(self.rows)
                )
            self.logical_operator_menu.pack(side="left", padx=(8, 0))
            self.validate_all_menus()
        
        def validate_all_menus(self): 
            """Returns increment value of validations, each integer increment signifying the option menu validated.
            """
            three_turn = []
            if self.criteria_menu.get() != "------":
                three_turn.append(True)
            else:
                three_turn.append(False)
            if self.comparison_menu.get() != "------": 
                three_turn.append(True)
            else: 
                three_turn.append(False)
            if self.logical_operator_menu.get() != "------": 
                three_turn.append(True)
            else:
                three_turn.append(False)

            return three_turn
        
        def get_criteria(self): 
            return self.criteria_menu.get()
        
        def get_comparison_operator(self): 
            return self.comparison_menu.get()
        
        def get_condition_entry(self): 
            return self.condition_entry.get()
        
        def get_logical_operator(self): 
            return self.logical_operator_menu.get()
        
        def validate(self, rows): 
            """Initiate outer method call for cipher lock.

            Args:
                rows (list): list of instantiated judgment_snowball_row objects
            """
            self.row_object_validation(rows=rows)

        def convert_condition_entry_to_float(self): 
            value = float(self.get_condition_entry())
            return value
    
    def get_generate_button_state(self):
        """Get the state of the generate button.

        Returns:
            str: state of button i.e., disabled or normal
        """
        return self.generate.cget("state")

    def _create_textbox(self, frame, text, height):
        """Create a text box for the purposes of displaying sample algorithm description / examples. 

        Args:
            frame (tkinter frame widget): parent frame
            text (str): text to add to textbox
            height (int): height of the text box

        Returns:
            tkinter textbox widget: non self referenced widget for display!
        """
        text_block = CTkTextbox(frame, wrap="word", fg_color="gray10", height=height)
        text_block.insert("1.0", text)
        text_block.configure(state="disabled")
        text_block.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        return text_block

    def add_judgment_snowball_row(self): 
        """For use with "judgment" and "snowball" algorithms of sampling. Will add new rows of widgets 
        at user discretion based on last known logical operator selected. 

        Args: 
            container (frame or canvas widget): the container object in which to render rows of widgets.
        """
        new_row = self.judgment_snowball_row( # instantiate!
            self.scrollable_frame, row_object_validation=self.row_object_validation, 
            rows = self.rows_of_operations
            ) 
        self.rows_of_operations.append(new_row)
        self.refresh_canvas()
        self.row_object_validation(rows=self.rows_of_operations) # ABV - always be validating, AIDA! 

    def remove_judgment_snowball_row(self):
        if len(self.rows_of_operations) > 0: 
            last_row = self.rows_of_operations[-1]
            last_row.row.destroy() # mojo
            self.rows_of_operations.pop()
        self.refresh_canvas()
        self.row_object_validation(rows=self.rows_of_operations) 

    def refresh_canvas(self): 
        """Refresh canvas object.
        """
        self.canvas.update_idletasks() # refresh canvas
        self.on_configure("x")

    def update_sample_status(self, text, colour): 
        """Update the sample status with new text e.g. sample generated

        Args:
            text (str): update label text with arg text
            colour (str): colour value in hex or name e.g. "green"
        """
        self.sample_status_label.configure(text=text, text_color=colour)

    def clear_child_widgets(self, mode, widget):
        """Remove child widgets from container widget, either table or frame.

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
        """Re-render scroll region.
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
            self.under_target_col_menu.configure(values=column_headers)
            self.over_target_col_menu.configure(values=column_headers)
            self.cluster_column_menu.configure(values=column_headers)
            self.column_to_build_quota_menu.configure(values=column_headers)
        elif mode == "rows": 
            if len(self.rows_of_operations) > 0: 
                for row in self.rows_of_operations: 
                    row.criteria_menu.configure(values=column_headers)

    def update_algorithm_description_info(self, text):
        """Display examples and information for the selected algorithm.

        Args:
            text (str): description information of particular algorithm.
        """
        for widget in self.description_frame.winfo_children(): 
            widget.destroy()

        self._create_textbox(frame=self.description_frame, text=text, height=190)

    def get_reference_to_rows_of_operations(self): 
        """ref to self.rows_of_operations
        """
        return self.rows_of_operations

    def get_sample_algo_menu_selection(self): 
        """Get the name of the selected item.
        """
        return self.sampling_algo_menu.get()
    
    def get_sample_size_entry(self): 
        """Simple Random entry prop
        """
        return self.sample_size_entry.get()
    
    def get_strat_sample_size_entry(self): 
        """Stratified entry prop
        """
        return self.strat_sample_size_entry.get()
    
    def get_stratified_dependant_col_menu(self): 
        """Stratified dependant col menu prop
        """
        return self.stratified_dependant_col_menu.get()
    
    def get_systematic_interval_entry(self): 
        """Systematic entry prop
        """
        return self.systematic_interval_entry.get()
    
    def get_under_target_col_menu(self): 
        """Under target col menu prop
        """
        return self.under_target_col_menu.get()
    
    def get_over_target_col_menu(self): 
        """Over target col menu prop
        """
        return self.over_target_col_menu.get()
    
    def get_cluster_sample_size_entry(self): 
        """Cluster num of clusters entry prop
        """
        self.cluster_sample_size_entry.get()
    
    def get_cluster_column_menu(self): 
        """Cluster column menu prop
        """
        return self.cluster_column_menu.get()
    
    def get_quota_sample_size_entry(self):
        """Quota sample size entry prop
        """ 
        self.quota_sample_size_entry.get()

    def get_column_to_build_quota_menu(self): 
        """Quota column to build quota menu prop
        """
        self.column_to_build_quota_menu.get()
    
    def row_object_validation(self, rows): 
        """Reconfigure generate state based on selection of widgets in judgment_snowball_row objects.

        Args:
            rows (list): list of row instance objects
        """
        def check_last_row(rows, cipher_lock): 
            """Validate last row.
            """
            if rows[-1].validate_all_menus() == [True, True, False]:
                cipher_lock.append(True)
            else: 
                cipher_lock.append(False)

        cipher_lock = [] # a series of Truthy values will unlock generate

        match len(rows): 
            case 1: 
                check_last_row(rows=rows, cipher_lock=cipher_lock)
            case length if length >= 2: 
                for row in range(len(rows) - 1): 
                    if rows[row].validate_all_menus() == [True, True, True]: 
                        cipher_lock.append(True)
                    else: 
                        cipher_lock.append(False)
                check_last_row(rows=rows, cipher_lock=cipher_lock)
        
        if len(cipher_lock) != 0 and all(cipher_lock): 
            self.generate.configure(state="normal")
        else: 
            self.generate.configure(state="disabled")

    def reset_algo_menu(self): 
        """Used post successful sampling algorithm.
        """
        self.sampling_algo_menu.set("------")

    def bulk_toggle(self, mode, list_of_widgets):
        """To be used with reconfig_widgets method.

        Args:
            mode (_type_): _description_
            list_of_widgets (_type_): _description_
        """
        if mode == "off": 
            for widget in list_of_widgets: 
                widget.configure(state="disabled")
        elif mode == "on": 
            for widget in list_of_widgets: 
                widget.configure(state="normal")
        elif mode == "hide": 
            for widget in list_of_widgets: 
                widget.pack_forget()
        elif mode == "show": 
            for widget in list_of_widgets: 
                widget.pack(side="left", padx=(8, 0))
        elif mode == "reset": 
            for widget in list_of_widgets:
                if isinstance(widget, CTkEntry): 
                    widget.delete(0, "end")
                elif isinstance(widget, CTkOptionMenu): 
                    widget.set("------")

    def reconfig_widgets(self, level, option):
        """Toggle (disable or enable) the appropriate widget based on predefined conditions.

        Args:
            level (str): "main" - primary algo selection or "sub" - sub menu selection of selected main algo
            option (str): selected item of an options menu
        """
        if level == "main": 
            self.rows_of_operations.clear()
            self.bulk_toggle("hide", [
                widget for widget in self.all_widgets
            ])
            self.bulk_toggle("off", [
                widget for widget in self.all_widgets
            ])
            self.clear_child_widgets(mode="all", widget=self.scrollable_frame) # delete any child widgets! 

            if option != "------": 
                self.bulk_toggle("show", self.algo_to_widget_set_mapping[option])
                self.bulk_toggle("on", self.algo_to_widget_set_mapping[option])

                if option in ["Simple Random", "Systematic"]: 
                    self.generate.configure(state="normal")
                else: 
                    self.generate.configure(state="disabled")
            else: 
                self.generate.configure(state="disabled")
        elif level == "sub": 
            if option == "------":
                self.generate.configure(state="disabled")
            else: 
                self.generate.configure(state="normal")
        