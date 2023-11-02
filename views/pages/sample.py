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
        self._rows_of_operations = []
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
            "------", "Simple Random", "Stratified", "Systematic", "Under", "Over", "Cluster", "Judgment", 
            "Snowball"
            ]
        self.sampling_algo_menu = CTkOptionMenu(
            self.s_frame_row_1, fg_color="gray10", width=3, values=self.sampling_algo_options, 
            command=lambda option: self.reconfig_widgets(level="main", option=option)
            )
        self.sampling_algo_menu.pack(side="left", padx=(8, 0))
        
        self.generate_button = CTkButton( # Run (generate sample)!
            self.s_frame_row_1, text="Generate", corner_radius=5, border_spacing=5, anchor="center", state="disabled", 
            width=30 
            )
        self.generate_button.pack(side="right", padx=(8, 8))

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

        # Judgment & Snowball - sub widgets
        self.js_sample_size_label = CTkLabel(self.s_frame_row_1, text="Sample Size:", anchor="w")
        self.js_sample_size_entry = CTkEntry(self.s_frame_row_1, corner_radius=5, width=50, state="disabled")
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
            self.js_sample_size_label, self.js_sample_size_entry, self.add_row, self.remove_row
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

        self.judgment_widgets = [
            self.add_row, self.remove_row
        ]

        self.snowball_widgets = [
            self.js_sample_size_label, self.js_sample_size_entry, self.add_row, self.remove_row
        ]

        self.algo_to_widget_set_mapping = {
            "Simple Random": self.simple_widgets, "Stratified": self.stratified_widgets, 
            "Systematic": self.systematic_widgets, "Under": self.under_widgets, "Over": self.over_widgets,
            "Cluster": self.cluster_widgets, "Judgment": self.judgment_widgets,
            "Snowball": self.snowball_widgets
        }

        self.all_menu_option_widgets = { # hack to reset upon algo selection - needed to toggle generate button
            self.stratified_dependant_col_menu, self.under_target_col_menu, self.over_target_col_menu, 
            self.cluster_column_menu
        }

    class judgment_snowball_row: 
        """Instance of a row of widgets
        """
        def __init__(self, parent_frame, row_object_validation, rows): 
            self._col_dtypes = dict() # used to store column headers to pandas types - used for refreshing on instantiation
            self._pandas_datatype_groups = {
            "numeric": (
                "int64", "int32", "int16", "int8", "float64", "float32", "complex", "UInt8", "UInt16",
                "UInt32", "UInt64", "int64Dtype", "float64Dtype"
                ), 
            "categorical": (
                "category", "object", "string", "StringDtype"
                ), 
            "boolean": (
                "bool",
                ), 
            "date_time": (
                "datetime64", "timedelta64", "period"
                )
            }
            self._row_object_validation = row_object_validation # outside method
            self._rows = rows # outside collection of rows
            self._row = CTkFrame(parent_frame, fg_color="gray20")
            self._row.pack(side="top", pady=(5, 5), fill="x")
            self._criteria_label = CTkLabel(self._row, text="Criteria:", anchor="w")
            self._criteria_label.pack(side="left", padx=(8, 0))
            self._criteria_menu = CTkOptionMenu(
                self._row, fg_color="gray10", width=3, values=("------",), command=lambda x: self._validate(self._rows)
                )
            self._criteria_menu.pack(side="left", padx=(8, 0))
            self._comparison_label = CTkLabel(self._row, text="IS", anchor="w")
            self._comparison_label.pack(side="left", padx=(8, 0))
            self._comparison_operators = [
                "------", "EQUAL", "LESS", "MORE", "NOT EQUAL"
                ]
            self._comparison_menu = CTkOptionMenu(
                self._row, fg_color="gray10", width=3, values=(self._comparison_operators), 
                command=lambda x: self._validate(self._rows)
                )
            self._comparison_menu.pack(side="left", padx=(8, 0))
            self._condition_label = CTkLabel(self._row, text="Condition:", anchor="w")
            self._condition_label.pack(side="left", padx=(8, 0))
            self._condition_entry = CTkEntry(self._row, corner_radius=5, width=50)
            self._condition_entry.pack(side="left", padx=(8, 0))
            self._logical_operators = [
                "------", "AND", "OR"
                ]
            self._logical_operator_menu = CTkOptionMenu(
                self._row, fg_color="gray10", width=3, values=(self._logical_operators), 
                command=lambda x: self._validate(self._rows)
                )
            self._logical_operator_menu.pack(side="left", padx=(8, 0))
            
            self.validate_all_menus()
        
        def validate_all_menus(self): 
            """Returns increment value of validations, each integer increment signifying the option menu validated.
            """
            three_turn = []
            if self._get_criteria() != "------":
                three_turn.append(True)
            else:
                three_turn.append(False)
            if self._get_comparison_operator() != "------": 
                three_turn.append(True)
            else: 
                three_turn.append(False)
            if self._get_logical_operator() != "------": 
                three_turn.append(True)
            else:
                three_turn.append(False)

            return three_turn
        
        def _get_criteria(self): 
            return self._criteria_menu.get()
        
        def _get_comparison_operator(self): 
            return self._comparison_menu.get()
        
        def _get_condition_entry(self): 
            return self._condition_entry.get()
        
        def _get_logical_operator(self): 
            return self._logical_operator_menu.get()
        
        def get_value_set(self): 
            """Returns a dictionary of single row conditions i.e., no logical operator to chain.
            """
            return {
                "criteria": self._get_criteria(),
                "comparison_op": self._get_comparison_operator(), 
                "conditional_val": float(self._get_condition_entry()), # only called post validation # TODO - not necessarily float? 
            }
        
        def _validate(self, rows): 
            """Initiate outer method call for cipher lock and to make available / unavilable various options 
            in comparison_menu and logical_operator_menu. 

            Args:
                rows (list): list of instantiated judgment_snowball_row objects
            """
            self._row_object_validation(rows=rows) # check if ready for generation i.e. unlocking of cipher lock
            
            criteria_selection = self._get_criteria()
            if criteria_selection != "------": # type check criteria_menu for adjusting other menus
                self._configure_widgets(column=criteria_selection) # menu restrictions
                

        def _configure_widgets(self, column):
            """Used to configure comparison_menu and logical_operator_menu based on the data type of 
            the criteria_menu selection.

            Args:
                column (str): value of selected criteria menu
            """
            criteria_dtype = self._get_col_type(column=column)
            match self._get_pandas_datatype_group(criteria_dtype): 
                case "numeric" | "date_time": 
                    self._comparison_menu.configure(values=["------", "EQUAL", "LESS", "MORE", "NOT EQUAL"])
                case "categorical" | "boolean": 
                    self._comparison_menu.configure(values=["------", "EQUAL", "NOT EQUAL"])

        def convert_condition_to_criteria(self): 
            """Convert user input for condition (row instances for snowball & judgment) to match 
            selected criteria (column of data).

            Returns: 
                Int, float, string etc., judgment_snowball_row class definition's self._pandas_datatype_groups variable
            """
            criteria_dtype = self._get_col_type(column=self._get_criteria())
            condition = self._get_condition_entry().strip()

            match self._get_pandas_datatype_group(criteria_dtype): 
                case "numeric": # to be catered for "date_time"
                    try: 
                        if criteria_dtype in [
                            "int64", "int32", "int16", "int8", "UInt8", "UInt16", "UInt32", "UInt64", "int64Dtype"
                            ]:
                            assert condition.isdigit(), "condition is not an integer value."
                            return int(condition)
                        elif criteria_dtype in [
                            "float64", "float32", "complex", "float64Dtype"
                            ]: 
                            assert condition.isdigit(), "condition is not a float value."
                            return float(condition)
                    except AssertionError as e: 
                        raise e # catch and display in controller
                case "categorical" | "boolean": 
                    try: # future place holder to separate different types 
                        assert type(condition) == str, "condition is not a string value."
                        return condition
                    except AssertionError as e: 
                        raise e
        
        def refresh_widgets(self, column_headers, dtypes): 
            """depending 

            Args:
                column_headers (_type_): _description_
                dtypes (_type_): _description_
            """
            self._set_col_dtypes(dtypes=dtypes)
            self._set_criteria_menu(column_headers=column_headers)
        
        def _get_col_type(self, column): 
            """Return datatype from self._col_dtypes for the selected criteria menu.
            """
            return self._col_dtypes[column]
                
        def _set_col_dtypes(self, dtypes): 
            """Populate self._col_dtypes with a dictionary of column names to pandas datatypes for usage in 
            limiting which menu options are available for conditional / logical menus. 

            Args:
                dtypes (dict): Dictionary of column name to pandas type (string) value mappings.
            """
            if len(self._col_dtypes) == 0: # new instance! Populate - first time only
                self._col_dtypes = dtypes

        def _set_criteria_menu(self, column_headers):
            """_summary_
            """
            self._criteria_menu.configure(values=column_headers)

        def _get_pandas_datatype_group(self, dtype): 
            """Return the group of a particular data type.

            Args: 
                dtype (str): data type of the selected criteria menu.
            """
            for category in self._pandas_datatype_groups: 
                if dtype in self._pandas_datatype_groups[category]:
                    return category

    def get_generate_button_state(self):
        """Get the state of the generate button.

        Returns:
            str: state of button i.e., disabled or normal
        """
        return self.generate_button.cget("state")

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
            self.scrollable_frame, row_object_validation=self._row_object_validation, 
            rows = self._rows_of_operations
            ) 
        self._rows_of_operations.append(new_row)
        self.refresh_canvas()
        self._row_object_validation(rows=self._rows_of_operations) # ABV - always be validating, AIDA! 

    def remove_judgment_snowball_row(self):
        if len(self._rows_of_operations) > 0: 
            last_row = self._rows_of_operations[-1]
            last_row._row.destroy() # mojo
            self._rows_of_operations.pop()
        self.refresh_canvas()
        self._row_object_validation(rows=self._rows_of_operations) 

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

    def refresh_sample_widgets(self, mode, dtypes, column_headers):
        """Populate / update the values of the dropdown menus view with appropriate column headers 
        of the working dataset.

        Args:
            mode (str): "menus" or "rows", latter == Refresh criteria
                menus of judgment / snowball rows with column headers.
                former == standard menus outside of the rows. 
            dtypes (str): data type of the menu.
            column_headers (list): A list of column headers (str).
        """
        if mode == "menus": 
            self.stratified_dependant_col_menu.configure(values=column_headers)
            self.under_target_col_menu.configure(values=column_headers)
            self.over_target_col_menu.configure(values=column_headers)
            self.cluster_column_menu.configure(values=column_headers)
        elif mode == "rows": 
            if len(self._rows_of_operations) > 0: 
                for row in self._rows_of_operations: 
                    row.refresh_widgets(column_headers=column_headers, dtypes=dtypes)

    def update_algorithm_description_info(self, text):
        """Display examples and information for the selected algorithm.

        Args:
            text (str): description information of particular algorithm.
        """
        for widget in self.description_frame.winfo_children(): 
            widget.destroy()

        self._create_textbox(frame=self.description_frame, text=text, height=190)

    def get_reference_to_rows_of_operations(self): 
        """ref to self._rows_of_operations
        """
        return self._rows_of_operations

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
        return self.cluster_sample_size_entry.get()
    
    def get_cluster_column_menu(self): 
        """Cluster column menu prop
        """
        return self.cluster_column_menu.get()
    
    def get_snowball_sample_size_entry(self): 
        """Snowball sample size value
        """
        return self.js_sample_size_entry.get()
    
    def _row_object_validation(self, rows): 
        """Reconfigure generate button state based on selection of widgets in judgment_snowball_row objects.

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

        cipher_lock = [] # a series of Truthy values will unlock generate button

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
            self.generate_button.configure(state="normal")
        else: 
            self.generate_button.configure(state="disabled")

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
            self._rows_of_operations.clear()
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
                    self.generate_button.configure(state="normal")
                else: 
                    self.generate_button.configure(state="disabled")
            else: 
                self.generate_button.configure(state="disabled")
        elif level == "sub": 
            if option == "------":
                self.generate_button.configure(state="disabled")
            else: 
                self.generate_button.configure(state="normal")
        