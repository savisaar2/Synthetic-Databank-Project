from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkOptionMenu, StringVar, CTkCheckBox, CTkScrollableFrame, CTkEntry, CTkProgressBar, CTkSegmentedButton
from .base import BaseView
import re
class ManipulateView(BaseView):
    def __init__(self, root, *args, **kwargs):
        """
        Initialise the Manipulate view of the application.

        This class represents the ManipulateView page of the application.
        It renders the interactive widgets on the frontend of the application.

        Parameters
        ----------
        root : Root
            The applicaiton's root instance.
        """
        super().__init__(root, "Manipulate", "Configure your Dataset.", *args, **kwargs)
        self._render_page()
        self.widget_list = [] # List of widgets dispayed in manipulation frame; removed during user navigation.
        self.variables = {"action":"", "sub_action":"", # Variables accessed by controller.
                          "args":{"a":"", "b":"", "c":""},"column":"", "sme":""}
        self.scheduler_items = [] # List of widgets dispayed in scheduler frame; removed when user selects "delete all".
        self.step_count = 0 # Counter for scheduled manipulations.

    def _render_page(self):
        """Renders widgets on the ManipulateView page."""

        # Manipulations frames and label
        self.manipulations_frame_1 = CTkFrame(self, fg_color="gray20")
        self.manipulations_frame_1.pack(fill="both", padx=20)
        self.manipulations_frame_2 = CTkFrame(self, fg_color="gray20")
        self.manipulations_frame_2.pack(fill="both", pady=(2, 20), padx=20)
        self.manipulations_label = CTkLabel(
            self.manipulations_frame_1, 
            text="Manipulations", 
            anchor="w", 
            font=("Arial", 14, "bold")
            )
        self.manipulations_label.pack(side="left",padx=(8, 0), pady=(0, 0))

        # Schedule button in manipulate frame.
        self.schedule_button = CTkButton(
            self.manipulations_frame_1, 
            text="Schedule", 
            corner_radius=5, 
            border_spacing=5, 
            anchor="center", 
            state="disabled",
            )
        self.schedule_button.pack(fill="both",side="right", padx=(8, 8), pady=(8,8))

        # Column Selector
        self.column_dropdown = CTkOptionMenu(
            self.manipulations_frame_1, 
            fg_color="gray10", 
            width=3, 
            command=self._set_column_var,
            variable=StringVar(value="Select Column"),
            state="disabled"
            )
        self.column_dropdown.pack(fill="both",side="right", padx=(8, 8), pady=(8,8))

        # SME Selector
        self.sme_selector = CTkSegmentedButton(
            self.manipulations_frame_1,
            values=["Single", "Multiple", "Entire"],
            state="disabled",
            command=(self._set_sme_variable)   
        )
        self.sme_selector.pack(side="right", padx=(8, 2), pady=8)

        # Action menu selector
        self.action_menu_var = StringVar(value="Select Action")
        self.action_selector = ["Add", "Reduce", "Manipulate"]
        self.action_selection_menu = CTkOptionMenu(
            self.manipulations_frame_2, 
            fg_color="gray10", 
            width=3, 
            values=self.action_selector, 
            command=self.action_callback,
            variable=self.action_menu_var
            )
        self.action_selection_menu.grid(row=0, column=0, padx=(8, 4), pady=(8, 8), sticky="w")

        # Scheduler frame
        self.scheduler_frame = CTkFrame(self, fg_color="gray20")
        self.scheduler_frame.pack(fill="both", pady=(0, 2), padx=20, expand=False)

        # Scheduler Label
        self.scheduler_label = CTkLabel(self.scheduler_frame, text="Scheduler", anchor="w", font=("Arial", 14, "bold"))
        self.scheduler_label.pack(side="left", padx=(8, 0))

        # Scrollable frame for manipulations
        self.scheduler_scroll_frame = CTkScrollableFrame(self, fg_color="gray20", orientation="horizontal")
        self.scheduler_scroll_frame.pack(fill="both", pady=(0, 2), padx=20, expand=True)

        # Step label
        self.step_label = CTkLabel(self.scheduler_scroll_frame, text="Step", font=("Arial", 14))
        self.step_label.grid(row=0, column=0, padx=(2, 10), pady=(0, 0), sticky="w")

        # Outcome label
        self.outcome_label = CTkLabel(self.scheduler_scroll_frame, text="Outcome", font=("Arial", 14))
        self.outcome_label.grid(row=0, column=1, padx=(0, 15), pady=(0, 0), sticky='w')

        # Action label
        self.action_label = CTkLabel(self.scheduler_scroll_frame, text="Action", font=("Arial", 14))
        self.action_label.grid(row=0, column=2, padx=(0, 100), pady=(0, 0), sticky="w")

        # Sub-action label
        self.sub_action_label = CTkLabel(self.scheduler_scroll_frame, text="Sub-Action", font=("Arial", 14))
        self.sub_action_label.grid(row=0, column=3, padx=(0, 100), pady=(0, 0), sticky="w")

        # Args label
        self.args_label = CTkLabel(self.scheduler_scroll_frame, text="Args", font=("Arial", 14))
        self.args_label.grid(row=0, column=4, padx=(0, 100), pady=(0, 0), sticky="w")

        # SME label
        self.sme_label = CTkLabel(self.scheduler_scroll_frame, text="SME", font=("Arial", 14))
        self.sme_label.grid(row=0, column=5, padx=(0, 30), pady=(0, 0), sticky="w")
                
        # Column label
        self.column_label = CTkLabel(self.scheduler_scroll_frame, text="Column", font=("Arial", 14))
        self.column_label.grid(row=0, column=6, padx=(0, 0), pady=(0, 0), sticky="w")

        # Delete All button
        self.delete_all_button = CTkButton(
            self.scheduler_frame, 
            text="Delete All", 
            corner_radius=5, 
            border_spacing=5, 
            anchor="center", 
            state="normal"
            )
        self.delete_all_button.pack(side="right", padx=(8, 8), pady=(8,8))

        # Generate frame
        self.generate_frame = CTkFrame(self, fg_color="gray20")
        self.generate_frame.pack(fill="both", pady=(0, 20), padx=20, expand=False)

        # Progress bar label
        self.progress_bar_label = CTkLabel(
            self.generate_frame, 
            text="Progress: "
            )
        self.progress_bar_label.pack(side="left", padx=(8, 8), pady=(8,8))

        # Progress bar
        self.generate_progress_bar = CTkProgressBar(self.generate_frame)
        self.generate_progress_bar.pack(side="left", padx=(8, 8), pady=(8,8))

        # Progress % complete
        self.progress_bar_complete = CTkLabel(
            self.generate_frame, 
            text=str((self.generate_progress_bar.get() * 100)) + "% Complete"
            )
        self.progress_bar_complete.pack(side="left", padx=(8, 8), pady=(8,8))

        # Generate button
        self.generate_button = CTkButton(
            self.generate_frame, 
            text="Generate", 
            corner_radius=5, 
            border_spacing=5, 
            anchor="center", 
            state="disabled"
            )
        self.generate_button.pack(side="right", padx=(8, 8), pady=(8,8))

        # Rollback frames and labels
        self.rollback_frame_1 = CTkFrame(self, fg_color="gray20")
        self.rollback_frame_1.pack(fill="both", pady=(0, 2), padx=20, expand=False)
        self.rollback_label = CTkLabel(self.rollback_frame_1, text="Rollback", font=("Arial", 14, "bold"))
        self.rollback_label.pack(side="left", padx=(8, 0))

        # Rollback button
        self.rollback_button = self.button_template(self.rollback_frame_1, "Rollback")
        self.rollback_button.pack(side="right", padx=8, pady=8)
        self.rollback_button.configure(state="disabled")

        # Rollback frame 2 and dataset selector
        self.rollback_frame_2 = CTkFrame(self, fg_color="gray20")
        self.rollback_frame_2.pack(fill="both", pady=(0, 20), padx=20, expand=False)

        self.rollback_dataset_var = StringVar(value="Current")
        self.rollback_dataset_selector = CTkSegmentedButton(
            self.rollback_frame_2,
            values=["1", "2", "3", "Current"],
            variable=self.rollback_dataset_var,
        )
        self.rollback_dataset_selector.pack(side="left", padx=(8, 0), pady=8)

        # Current dataset label
        self.current_dataset_label = CTkLabel(self.rollback_frame_2)
        self.current_dataset_label.pack(side="right", padx=(8, 8))

    def add_manipulation_to_scheduler(self):
        """Method creates a set of widgets to display a users selected manipulation parameters."""

        if self.schedule_button._state == "normal":
            try:
                self.step_count +=1 # Increase step count

                # Logic for step checkbox
                def checkbox_event():
                    for items_dict in self.scheduler_items:
                        match items_dict["step"].get(), items_dict["outcome"].cget("text"):
                            case "on", "In Queue":
                                self.generate_button.configure(state="normal")
                                break
                            case "off", "Complete":
                                self.generate_button.configure(state="disabled")
                            case "off", "In Queue":
                                self.generate_button.configure(state="disabled")
                
                # Checkbox
                self.step_checkbox_var = StringVar(value="on")
                self.step_checkbox = CTkCheckBox(
                    self.scheduler_scroll_frame, 
                    text=str(self.step_count), 
                    command=checkbox_event,
                    variable=self.step_checkbox_var,
                    onvalue="on",
                    offvalue="off",
                    width=5,
                    height=5,
                    checkbox_height=15,
                    checkbox_width=15
                    )
                self.step_checkbox.grid(row=self.step_count, column=0, padx=(2, 0), pady=(0, 0), sticky='w')
                self.step_checkbox.select() 

                # Label for scheduled manipulation outcome
                self.outcome_label_for_scheduler = CTkLabel(
                    self.scheduler_scroll_frame, 
                    text="In Queue",
                    text_color="yellow"
                    )
                self.outcome_label_for_scheduler.grid(row=self.step_count, column=1, padx=(0, 0), pady=(0, 0), sticky='w')

                # Action label for scheduled manipulation
                self.action_label_for_scheduler = CTkLabel(
                    self.scheduler_scroll_frame, 
                    text=self.variables["action"]
                    )
                self.action_label_for_scheduler.grid(row=self.step_count, column=2, padx=(0, 10), pady=(0, 0), sticky='w')

                # Sub-action label for scheduled manipulation
                self.sub_action_label_for_scheduler = CTkLabel(
                    self.scheduler_scroll_frame, 
                    text=self.variables["sub_action"],  
                    )
                self.sub_action_label_for_scheduler.grid(row=self.step_count, column=3, padx=(0, 10), pady=(0, 0), sticky='w')

                # Args for scheduled manipulation
                self.args_label_for_scheduler = CTkLabel(
                    self.scheduler_scroll_frame, 
                    text=self.variables["args"],  
                    )
                self.args_label_for_scheduler.grid(row=self.step_count, column=4, padx=(0, 10), pady=(0, 0), sticky='w')

                # SME name for scheduled manipulation
                self.sme_label_for_scheduler = CTkLabel(
                    self.scheduler_scroll_frame, 
                    text=self.variables["sme"],  
                    )
                self.sme_label_for_scheduler.grid(row=self.step_count, column=5, padx=(0, 0), pady=(0, 0), sticky='w')

                # column name for scheduled manipulation
                self.column_label_for_scheduler = CTkLabel(
                    self.scheduler_scroll_frame, 
                    text=self.variables["column"],  
                    )
                self.column_label_for_scheduler.grid(row=self.step_count, column=6, padx=(0, 0), pady=(0, 0), sticky='w')                

                # Scheduled manipulations widgets added to a dict to be deleted by user via delete all button.
                scheduled_items_dict = {"step": self.step_checkbox, 
                                        "action": self.action_label_for_scheduler, 
                                        "sub_action": self.sub_action_label_for_scheduler,
                                        "args": self.args_label_for_scheduler,
                                        "sme": self.sme_label_for_scheduler,
                                        "column": self.column_label_for_scheduler,
                                        "outcome": self.outcome_label_for_scheduler}
                self.scheduler_items.append(scheduled_items_dict.copy())          

            finally:
                # Remove all previously packed widgets in manipulations frame.
                for widget in self.widget_list:
                    widget["widget"].grid_forget()

                # Reset action menu
                self.action_selection_menu.set("Select Action")

                # Reset SME selector
                self.sme_selector.configure(state="disabled")
                self.sme_selector.configure(values=["Single", "Multiple", "Entire"])
                self.sme_selector.set("")

    def action_callback(self, choice):
        """Action menu selector callback function.

        Args:
            choice (str): User selection via dropdown menu or entry box.
        """
        # Refresh widgets
        self.schedule_button.configure(state="disabled")  
        self.variables = self.variables = {"action":"", "sub_action":"", "args":{"a":"", "b":"", "c":""},"column":"", "sme":""}
        self.sme_selector.configure(state="disabled")
        self.sme_selector.configure(values=["Single", "Multiple", "Entire"])
        self.sme_selector.set("")

        # Remove all previously packed widgets in manipulations frame.
        for widget in self.widget_list:
            widget["widget"].grid_forget()
        self.widget_list =[]

        match choice:
            case "Add":
                self.pos_0_menu = self._drop_down_menu_template("Select Variable", 
                    ["Noise", "Column"], self.add_select_callback, 1)      
            case "Reduce":
                # Show reduce method menu drop down
                self.pos_0_menu = self._drop_down_menu_template("Select Method", 
                    ["Columns (Dimensionality)", "Remove Rows"], self.reduce_method_select_callback, 1) 

            case "Manipulate":
                # Show variable menu drop down
                self.pos_0_menu = self._drop_down_menu_template("Select Technique", 
                    ["Replace Missing Values", "Replace Value (x) with New Value", 
                     "Change Column Name", "Expand (add rows)", "Data Transformation"],
                    self.manipulate_col_select_callback, 1)

    def add_select_callback(self, choice):
        """Add menu selector callback function. New menu/entry box appears on user selection.

            Args:
                choice (str): User selection via dropdown menu or entry box.
        """
        self.variables["action"] = f"Add {choice}"
        self._refresh_menu_widgets(2)

        match choice:
            case "Noise":
                self.pos_1_menu = self._drop_down_menu_template("Select Technique", 
                ["Add Random Custom Value", "Add Missing", "Add Outliers"], self.add_noise_technique_callback, 2)
            case "Column":
                self.pos_1_menu = self._drop_down_menu_template("Select Technique", 
                ["Duplicate", "New", "Feature Engineering"], self.add_column_technique_callback, 2)

    def add_noise_technique_callback(self, choice):
        """Add noise selector callback function. New menu/entry box appears on user selection.

            Args:
                choice (str): User selection via dropdown menu or entry box.
        """
        self.variables["sub_action"] = choice
        self._refresh_menu_widgets(3)

        match choice:
            case "Add Random Custom Value":
                self.sme_selector.configure(values=["Single"])
                self.pos_3_entry_box = self.user_entry_box_template(3, 0, self.entry_box_standard_arg_a_callback,
                                                                    "Enter custom value") 
                self.pos_4_entry_box = self.user_entry_box_template(3, 1, self.entry_box_standard_arg_b_callback,
                                                                    "Enter number of values")
            case "Add Missing":
                self.sme_selector.configure(values=["Single", "Entire"])
                self.pos_3_entry_box = self.user_entry_box_template(3, 0, self.entry_box_standard_arg_a_callback,
                                                                    "Enter number of values")                
            case "Add Outliers":
                self.pos_2_menu = self._drop_down_menu_template("Select Technique", 
                ["Z-score", "Percentile", "Min/Max"], 
                self.outliers_technique_callback, 3)
                self.sme_selector.configure(values=["Single"])
    
    def outliers_technique_callback(self, choice):
        """Outliers callback function. New menu/entry box appears on user selection.

            Args:
                choice (str): User selection via dropdown menu or entry box.
        """
        previous_sub_type = self.variables["sub_action"]
        self.variables["sub_action"] = f"{previous_sub_type} {choice}"
        self._refresh_menu_widgets(4)

        match choice:
            case "Z-score":
                self.pos_4_entry_box = self.user_entry_box_template(4, 0, self.entry_box_standard_arg_a_callback,
                                                                    "Enter z-score threshold")
            case "Percentile":
                self.pos_4_entry_box = self.user_entry_box_template(4, 0, self.entry_box_standard_arg_a_callback,
                                                                    "Enter number of outliers") 
            case "Min/Max":
                pass

    def add_column_technique_callback(self, choice):
        """Add column callback function. New menu/entry box appears on user selection.

            Args:
                choice (str): User selection via dropdown menu or entry box.
        """
        self.variables["sub_action"] = choice
        self._refresh_menu_widgets(3)

        match choice:
            case "Duplicate":
                self.sme_selector.configure(values=["Single"])
                self.sme_selector.configure(state="normal")
                self.pos_3_entry_box = self.user_entry_box_template(3, 0, self.entry_box_standard_arg_a_callback,
                                                                    "Enter column name")
            case "New":
                self.pos_3_entry_box = self.user_entry_box_template(3, 0, self.entry_box_standard_arg_a_callback,
                                                                    "Enter column name")
                self.sme_selector.configure(values=["No Column Required"])
                self.sme_selector.set("No Column Required")
                self.sme_selector.configure(state="disabled")
                self.column_dropdown.configure(state="disabled")
                self.schedule_button.configure(state="normal")
            case "Feature Engineering":
                self.pos_3_menu = self._drop_down_menu_template("Select Technique", 
                                                                ["Polynomial Features", "Interaction Features"], 
                                                                self.feature_engineering_callback, 3)
                self.sme_selector.configure(values=["Single", "Multiple"])

    def feature_engineering_callback(self, choice):
        """Add feature engineering callback function. New menu/entry box appears on user selection.

            Args:
                choice (str): User selection via dropdown menu or entry box.
        """
        sub_action = self.variables["sub_action"]
        self.variables["sub_action"] = f"{sub_action} {choice}"
        self._refresh_menu_widgets(4)

        match choice:
            case "Polynomial Features":
                self.pos_3_entry_box = self.user_entry_box_template(3, 0, self.entry_box_standard_arg_a_callback,
                                                                    "Enter degree")
            case "Interaction Features":
                self.sme_selector.configure(state="normal")

    def reduce_method_select_callback(self, choice):
        """Reduce callback function. New menu/entry box appears on user selection.

            Args:
                choice (str): User selection via dropdown menu or entry box.
        """
        self.variables["action"] = f"Reduce {choice}"
        self.sme_selector.configure(values=["Entire"])
        self._refresh_menu_widgets(2)

        if choice == "Columns (Dimensionality)":
            # Add technique selection drop down menu
            self.pos_1_menu = self._drop_down_menu_template("Select Technique", 
                ["Algorithmic", "Manual"], self._dimensionality_reduction_callback, 2) 

        elif choice == "Remove Rows":
            # Add drop down menu for column selection
            self.pos_1_menu = self._drop_down_menu_template("Select Variable", 
                ["Missing Values", "Duplicate Rows"], self._sme_selector_col_2_callback, 2)
            self.sme_selector.configure(state="normal")
            

    def _dimensionality_reduction_callback(self, choice):
        """Dimensionality reduction callback function. New menu/entry box appears on user selection.

            Args:
                choice (str): User selection via dropdown menu or entry box.
        """
        self.variables["sub_action"] = choice
        self._refresh_menu_widgets(3)

        match choice:
            case "Algorithmic":
                self.pos_2_menu = self._drop_down_menu_template("Select Technique", 
                ["PCA", "LDA", "SVD", "Sklearn"], self._dimension_reduction_algo_callback, 3) 

            case "Manual":
                self.sme_selector.configure(values=["Single"])
                self.sme_selector.configure(state=["normal"])

    def _dimension_reduction_algo_callback(self, choice):
        """Dimension reduction algorithm callback function. New menu/entry box appears on user selection.

            Args:
                choice (str): User selection via dropdown menu or entry box.
        """
        first_sub = self.variables["sub_action"]
        self.variables["sub_action"] = f"{first_sub} {choice}"
        self.sme_selector.configure(values=["Entire"])
        self._refresh_menu_widgets(4)

        self.pos_4_menu = self._drop_down_menu_template("Select Dependent Column", self.column_headers, 
                                                        self._sme_selector_col_4_callback ,4)
        self.pos_5_entry_box = self.user_entry_box_template(4, 1, self.entry_box_standard_arg_b_callback,
                                                            "Number of columns to retain")

    def manipulate_col_select_callback(self, choice):
        """Add column callback function. New menu/entry box appears on user selection.

            Args:
                choice (str): User selection via dropdown menu or entry box.
        """
        self.variables["action"] = choice
        self._refresh_menu_widgets(2)
        
        match choice:
            case "Replace Missing Values":
                self.sme_selector.configure(values=["Single"])
                self.pos_2_menu = self._drop_down_menu_template("Select Manipulation", 
                ["Numerical Column", "Categorial Column"], self._replace_missing_values_callback, 2)
            case "Replace Value (x) with New Value":
                self.sme_selector.configure(values=["Single"])
                self.pos_2_entry_box = self.user_entry_box_template(2, 0, self.entry_box_standard_arg_a_callback, 
                                                                    "Enter value to replace")
                self.pos_3_entry_box = self.user_entry_box_template(3, 0, self.entry_box_standard_arg_b_callback, 
                                                                    "Enter New Value")
            case "Change Column Name":
                self.sme_selector.configure(values=["Single"])
                self.pos_2_entry_box = self.user_entry_box_template(2, 0, self.entry_box_standard_arg_a_callback, 
                                                                    "Enter new column name")
            case "Expand (add rows)":
                self.sme_selector.configure(values=["Entire"])
                self.pos_2_menu = self._drop_down_menu_template("Select Manipulation", 
                ["Random Sampling", "Bootstrap Resamping", "SMOTE", "Add Noise"], self._expand_rows_callback, 2)  
            case "Data Transformation":
                self.pos_2_menu = self._drop_down_menu_template("Select Manipulation", 
                ["Feature Scaling", "Feature Encoding"], self._data_transformation_callback, 2)                            

    def _data_transformation_callback(self, choice):
        """Data transformation callback function. New menu/entry box appears on user selection.

            Args:
                choice (str): User selection via dropdown menu or entry box.
        """
        self.variables["sub_action"] = choice
        self._refresh_menu_widgets(3)

        match choice:
            case "Feature Scaling":
                self.pos_3_menu = self._drop_down_menu_template("Select Technique", 
                ["Min/Max Scaler", "Z-score"], self._feature_scaling_callback, 3)
            case "Feature Encoding":
                self.pos_3_menu = self._drop_down_menu_template("Select Technique", 
                ["One-hot Encoding", "Label Encoding", "Embedding"], self._feature_encoding_callback, 3)

    def _feature_scaling_callback(self, choice):
        """Feature scaling callback function. New menu/entry box appears on user selection.

            Args:
                choice (str): User selection via dropdown menu or entry box.
        """
        sub_action = self.variables["sub_action"]
        self.variables["sub_action"] = f"{sub_action} {choice}"
        self.sme_selector.configure(values=["Entire"])
        self._refresh_menu_widgets(4)

        self.pos_4_menu = self._drop_down_menu_template("Select Dependant Variable", 
        self.column_headers, self._sme_selector_col_4_callback, 4)

    def _feature_encoding_callback(self, choice):
        """Feature encoding callback function. New menu/entry box appears on user selection.

            Args:
                choice (str): User selection via dropdown menu or entry box.
        """
        sub_action = self.variables["sub_action"]
        self.variables["sub_action"] = f"{sub_action} {choice}"
        self.sme_selector.configure(values=["Single"])
        self._refresh_menu_widgets(4)

        self.pos_4_menu = self._drop_down_menu_template("Select Dependant Variable", 
        self.column_headers, self._sme_selector_col_4_callback, 4)


    def _expand_rows_callback(self, choice):
        """Expand rows callback function. New menu/entry box appears on user selection.

            Args:
                choice (str): User selection via dropdown menu or entry box.
        """
        self.variables["sub_action"] = choice
        self.sme_selector.configure(values=["Entire"])
        self._refresh_menu_widgets(3)

        match choice:
            case "Random Sampling" | "Bootstrap Resamping":
                self.pos_3_entry_box = self.user_entry_box_template(3, 0, self.entry_box_standard_arg_a_callback, 
                                                                    "Enter number of rows to generate")
            case "SMOTE":
                self.pos_3_entry_box = self.user_entry_box_template(3, 0, self.entry_box_standard_arg_a_callback,
                                                                    "Enter dependent variable name")
            case "Add Noise":
                pass

    def _replace_missing_values_callback(self, choice):
        """Replace missing values callback function. New menu/entry box appears on user selection.

            Args:
                choice (str): User selection via dropdown menu or entry box.
        """
        self.variables["sub_action"] = choice
        self.sme_selector.configure(values=["Single"])
        self._refresh_menu_widgets(3)

        match choice:
            case "Numerical Column":
                self.pos_3_menu = self._drop_down_menu_template("Select Technique", 
                ["Algorithm", "Manual"], self._numerical_column_callback, 3)
            case "Categorial Column":
                self.pos_3_menu = self._drop_down_menu_template("Select Technique", 
                ["Algorithm", "Manual"], self._categorical_column_callback, 3)

    def _categorical_column_callback(self, choice):
        """Categorical column callback function. New menu/entry box appears on user selection.

            Args:
                choice (str): User selection via dropdown menu or entry box.
        """
        self.variables["args"]["a"] = choice
        self.sme_selector.configure(values=["Single"])
        self._refresh_menu_widgets(4)
        
        match choice:
            case "Algorithm":
                self.pos_4_menu = self._drop_down_menu_template("Select Technique", 
                ["Mode", "Similarity", "ML"], self._sme_selector_col_4_callback, 4)
            case "Manual":
                self.pos_4_entry_box = self.user_entry_box_template(4, 0, self.entry_box_standard_arg_b_callback, "Enter new value")

    def _numerical_column_callback(self, choice):
        """Numerical column callback function. New menu/entry box appears on user selection.

            Args:
                choice (str): User selection via dropdown menu or entry box.
        """
        self.variables["args"]["a"] = choice
        self.sme_selector.configure(values=["Single"])
        self._refresh_menu_widgets(4)

        match choice:
            case "Algorithm":
                self.pos_4_menu = self._drop_down_menu_template("Select Technique", 
                ["Mean", "Median", "KNN", "ML"], self._sme_selector_col_4_callback, 4)
            case "Manual":
                self.pos_4_entry_box = self.user_entry_box_template(4, 0, self.entry_box_standard_arg_b_callback, "Enter new number value")

    def _label_template(self, text, col_pos):
        """Template for label widgets.

        Args:
            text (string): Text to be displayed by label.
            col_pos (int): Column position to place on grid.

        Returns:
            Ctk widget: A Ctk label widget object.
        """
        label = CTkLabel(
            self.manipulations_frame_2, 
            text=text, 
            anchor="w")
        label.grid(row=0, column=col_pos, padx=(8, 10), pady=(8, 8), sticky="w")
        self.widget_list.append({"col_pos": col_pos, "widget": label})
        return label
    
    def user_entry_box_template(self, col_pos, row_pos, callback, start_text):
        """Entry box wiget template.

        Args:
            col_pos (int): Column position to place on grid.
            row_pos (int): Row position to place on grid.
            callback (function): Callback function associated with widget.
            start_text (_type_): Placeholder text of entry widget.

        Returns:
            Ctk widget: A Ctk entry box  widget object.
        """
        entry_box_command = self.register(callback)
        user_entry_box = CTkEntry(
            self.manipulations_frame_2,
            corner_radius=5, 
            width=200,
            validate='key',
            validatecommand=(entry_box_command, '%P')
            ) 
        user_entry_box.grid(column=col_pos, row=row_pos,  padx=(0, 2), pady=(8, 8), sticky="w")
        user_entry_box.configure(placeholder_text=start_text)
        self.widget_list.append({"col_pos": col_pos, "widget": user_entry_box})
        
        return user_entry_box
    
    def entry_box_standard_arg_a_callback(self, choice):
        if len(choice) > 0:
            self.variables["args"]["a"] = choice
            self.sme_selector.configure(state="normal")  
            return True
        elif len(choice) == 0:
            self.sme_selector.configure(state="disabled") 
            return True
        
    def entry_box_standard_arg_b_callback(self, choice):
        if len(choice) > 0:
            self.variables["args"]["b"] = choice
            self.sme_selector.configure(state="normal")  
            return True
        elif len(choice) == 0:
            self.sme_selector.configure(state="disabled") 
            return True

    def _validate_numerical_input(self, string):
        regex = re.compile(r"[0-9.]*$")
        result = regex.match(string)
        return (string == ""
                or (string.count('.') <= 1
                    and result is not None
                    and result.group(0) != ""))
    
    def entry_box_numerical_arg_a_callback(self, choice):
        match self._validate_numerical_input(choice):
            case True:
                if len(choice) > 0:
                    self.variables["args"]["a"] = choice
                    self.sme_selector.configure(state="normal")
            case False:
                self.sme_selector.configure(state="disabled")
        return self._validate_numerical_input(choice)
    
        
    def entry_box_numerical_arg_b_callback(self, choice):
        if len(choice) > 5:
            self.sme_selector.configure(state="disabled") 
            return True
        elif choice.isdigit():
            self.variables["args"]["b"] = choice
            self.sme_selector.configure(state="normal")
            return True          
        elif len(choice) == 0:
            self.sme_selector.configure(state="disabled") 
            return True
        else:
            self.sme_selector.configure(state="disabled") 
            return False
        
    def _drop_down_menu_template(self, start_text: str, menu_options: list, command_func, col_pos: int):    
        menu_var = StringVar(value=start_text)
        selector = menu_options
        drop_down_menu = CTkOptionMenu(
            self.manipulations_frame_2, 
            fg_color="gray10", 
            width=3, 
            values=selector, 
            command=command_func,
            variable=menu_var
            )
        drop_down_menu.grid(row=0, column=col_pos, padx=(0, 2), pady=(8, 8), sticky="w")
        self.widget_list.append({"col_pos": col_pos, "widget": drop_down_menu})
        return drop_down_menu
       
    def _set_sme_variable(self, choice):
        self.variables["sme"] = choice
        self.schedule_button.configure(state="disabled")
        self.column_dropdown.configure(values=self.column_headers)
        match choice:
            case "Single":
                self.column_dropdown.configure(state="normal")
            case "Multiple":
                pass
            case "Entire":
                self.variables["column"] = ""
                self.schedule_button.configure(state="normal")
                self.column_dropdown.configure(state="disabled")

    def _set_column_var(self, choice):
        self.variables["column"] = choice
        match self.variables["sme"]:
            case "Single":
                self.schedule_button.configure(state="normal")
            case "Multiple":
                pass
            case "Entire":
                self.schedule_button.configure(state="normal")

    def _sme_selector_col_2_callback(self, choice):
        self.variables["sub_action"] = choice
        self.sme_selector.configure(state="enabled")
      
    def _sme_selector_col_3_callback(self, choice):
        self.variables["args"]["a"] = choice
        self.sme_selector.configure(state="enabled")

    def _sme_selector_col_4_callback(self, choice):
        self.variables["args"]["a"] = choice
        self.sme_selector.configure(state="enabled")

    def button_template(self, frame, button_name: str):
        button = CTkButton(
            frame, 
            text=button_name, 
            corner_radius=5, 
            border_spacing=5, 
            anchor="center", 
            state="normal"
            )       
        return button    

    def _refresh_menu_widgets(self, col_ref):
        self.schedule_button.configure(state="disabled")
        self.sme_selector.configure(state="disabled")
        self.sme_selector.set("")
        self.column_dropdown.configure(state="disabled")

        match col_ref:
            case 2:
                for widget in self.widget_list:
                    if widget["col_pos"] != 1:
                        widget["widget"].grid_forget()
            case 3:
                for widget in self.widget_list:
                    if widget["col_pos"] != 1 and widget["col_pos"] != 2:
                        widget["widget"].grid_forget()
            case 4:
                for widget in self.widget_list:
                    if widget["col_pos"] != 1 and widget["col_pos"] != 2 and widget["col_pos"] != 3:
                        widget["widget"].grid_forget()
                    
    def refresh_manipulate_widgets(self, column_headers):
        """Refresh, update or populate the values of various widgets on Manipulate view with appropriate
        information pulled from the loaded dataset e.g. column headers for option menues, row count etc. 

        Args:
            dataset_attributes (tuple): A tuple consisting of row count and list of column headers (str).
        """
        self.column_headers = column_headers
