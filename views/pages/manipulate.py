from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkOptionMenu, StringVar, CTkCheckBox, CTkScrollableFrame, CTkEntry, CTkProgressBar, CTkSegmentedButton
from .base import BaseView
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
        # Pass some base title and description to our BaseView class.
        super().__init__(root, "Manipulate", "Configure your Dataset.", *args, **kwargs)
        self._render_page()
        self.widget_list = []
        self.variables = {"var_1":"", "var_2":"", "var_3":"", "var_4":"", "sme":""}
        self.sme_variable = ""
        self.scheduler_items = []
        self.step_count = 0

    def _render_page(self):
        """Renders widgets on the ManipulateView page."""

        # Rollback frames and labels
        self.rollback_frame_1 = CTkFrame(self, fg_color="gray20")
        self.rollback_frame_1.pack(fill="both", pady=(0, 2), padx=20, expand=False)
        self.rollback_label = CTkLabel(self.rollback_frame_1, text="Rollback", font=("Arial", 14, "bold"))
        self.rollback_label.pack(side="left", padx=(8, 0))

        # Rollback button
        self.rollback_button = self.button_template(self.rollback_frame_1, "Rollback")
        self.rollback_button.pack(side="right", padx=8, pady=8)

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

        self.current_dataset_label = CTkLabel(self.rollback_frame_2)
        self.current_dataset_label.pack(side="right", padx=(8, 8))

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
        self.scheduler_scroll_frame = CTkScrollableFrame(self, fg_color="gray20")
        self.scheduler_scroll_frame.pack(fill="both", pady=(0, 2), padx=20, expand=True)

        # Action label
        self.sched_action_label = CTkLabel(self.scheduler_scroll_frame, text="Action", font=("Arial", 14))
        self.sched_action_label.grid(row=0, column=0, padx=(8, 30), pady=(0, 0), sticky="w")

        # Variable 1 label
        self.variable_1_label = CTkLabel(self.scheduler_scroll_frame, text="Variable 1", font=("Arial", 14))
        self.variable_1_label.grid(row=0, column=1, padx=(0, 60), pady=(0, 0), sticky="w")

        # Variable 2 label
        self.variable_2_label = CTkLabel(self.scheduler_scroll_frame, text="Variable 2", font=("Arial", 14))
        self.variable_2_label.grid(row=0, column=2, padx=(0, 60), pady=(0, 0), sticky="w")

        # Variable 3 label
        self.variable_3_label = CTkLabel(self.scheduler_scroll_frame, text="Variable 3", font=("Arial", 14))
        self.variable_3_label.grid(row=0, column=3, padx=(0, 60), pady=(0, 0), sticky="w")

        # Variable 4 label
        self.variable_4_label = CTkLabel(self.scheduler_scroll_frame, text="Variable 4", font=("Arial", 14))
        self.variable_4_label.grid(row=0, column=4, padx=(0, 40), pady=(0, 0), sticky="w")

        # SME label
        self.sme_label = CTkLabel(self.scheduler_scroll_frame, text="SME", font=("Arial", 14))
        self.sme_label.grid(row=0, column=5, padx=(0, 20), pady=(0, 0), sticky="w")

        # Outcome label
        self.outcome_label = CTkLabel(self.scheduler_scroll_frame, text="Outcome", font=("Arial", 14))
        self.outcome_label.grid(row=0, column=6, padx=(0, 10), pady=(0, 0), sticky='w')

        # Step label
        self.step_label = CTkLabel(self.scheduler_scroll_frame, text="Step", font=("Arial", 14))
        self.step_label.grid(row=0, column=7, padx=(0, 0), pady=(0, 0), sticky="w")

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

        # Save column name button
        self.save_column_name_button = self.button_template(self.manipulations_frame_2,"Save")
        self.save_column_name_button. configure(width=50)
 
    def add_manipulation_to_scheduler(self):

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

                # Name of scheduled action 
                self.manipulation_label_for_scheduler = CTkLabel(self.scheduler_scroll_frame, text=str(self.action_menu_var))
                self.manipulation_label_for_scheduler.grid(row=self.step_count, column=0, padx=(8, 0), pady=(0, 0), sticky='w')

                # Varible 1 name for scheduled manipulation
                self.variable_1_label_for_scheduler = CTkLabel(
                    self.scheduler_scroll_frame, 
                    text=self.variables["var_1"]
                    )
                self.variable_1_label_for_scheduler.grid(row=self.step_count, column=1, padx=(0, 0), pady=(0, 0), sticky='w')

                # Varible 2 name for scheduled manipulation
                self.variable_2_label_for_scheduler = CTkLabel(
                    self.scheduler_scroll_frame, 
                    text=self.variables["var_2"],  
                    )
                self.variable_2_label_for_scheduler.grid(row=self.step_count, column=2, padx=(0, 0), pady=(0, 0), sticky='w')

                # Varible 3 name for scheduled manipulation
                self.variable_3_label_for_scheduler = CTkLabel(
                    self.scheduler_scroll_frame, 
                    text=self.variables["var_3"],  
                    )
                self.variable_3_label_for_scheduler.grid(row=self.step_count, column=3, padx=(0, 0), pady=(0, 0), sticky='w')

                # Varible 4 name for scheduled manipulation
                self.variable_4_label_for_scheduler = CTkLabel(
                    self.scheduler_scroll_frame, 
                    text=self.variables["var_4"],  
                    )
                self.variable_4_label_for_scheduler.grid(row=self.step_count, column=4, padx=(0, 0), pady=(0, 0), sticky='w')

                # SME name for scheduled manipulation
                self.sme_label_for_scheduler = CTkLabel(
                    self.scheduler_scroll_frame, 
                    text=self.variables["sme"],  
                    )
                self.sme_label_for_scheduler.grid(row=self.step_count, column=5, padx=(0, 0), pady=(0, 0), sticky='w')

                # Label for scheduled manipulation outcome
                self.outcome_label_for_scheduler = CTkLabel(
                    self.scheduler_scroll_frame, 
                    text="In Queue",
                    text_color="yellow"
                    )
                self.outcome_label_for_scheduler.grid(row=self.step_count, column=6, padx=(0, 0), pady=(0, 0), sticky='w')

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
                self.step_checkbox.grid(row=self.step_count, column=7, padx=(5, 0), pady=(0, 0), sticky='e')
                self.step_checkbox.select()              
                # Scheduled manipulations widgets added to a dict to be deleted by user via delete all button.
                scheduled_items_dict = {"step": self.step_checkbox, 
                                        "action": self.manipulation_label_for_scheduler, 
                                        "variable_1": self.variable_1_label_for_scheduler,
                                        "variable_2": self.variable_2_label_for_scheduler,
                                        "variable_3": self.variable_3_label_for_scheduler,
                                        "variable_4": self.variable_4_label_for_scheduler,
                                        "sme": self.sme_label_for_scheduler,
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
        self.action_menu_var = choice
        self.schedule_button.configure(state="disabled")  
        self.variables = {"var_1":"", "var_2":"", "var_3":"", "var_4":"", "sme":""}
        # Reset SME selector
        self.sme_selector.configure(state="disabled")
        self.sme_selector.configure(values=["Single", "Multiple", "Entire"])
        self.sme_selector.set("")

        # Remove all previously packed widgets in manipulations frame.
        for widget in self.widget_list:
            widget["widget"].grid_forget()
        self.widget_list =[]

        match self.action_menu_var:
            case "Add":
                self.add_selection_menu = self._drop_down_menu_template("Select Variable", 
                    ["Noise", "Column"], self.add_select_callback, 1) 
                
            case "Reduce":
                # Show reduce method menu drop down
                self.method_selection_menu = self._drop_down_menu_template("Select Method", 
                    ["Data Dimensionality", "Rows"], self.reduce_method_select_callback, 1) 

            case "Manipulate":
                # Show variable menu drop down
                self.maniuplate_variable_menu = self._drop_down_menu_template("Select Technique", 
                    ["Replace Missing Values", "Replace Other Values", "Expand (add rows)", "Data Transformation"],
                    self.manipulate_col_select_callback, 1)

    def add_select_callback(self, choice):
        self.variables["var_1"] = choice
        self.schedule_button.configure(state="disabled")
        self.sme_selector.configure(state="disabled")
        self.sme_selector.set("")

        # Remove all previously packed widgets in manipulations frame.
        for widget in self.widget_list:
            if widget["col_pos"] != 1:
                widget["widget"].grid_forget()

        match choice:
            case "Noise":
                self.noise_technique_selection_menu = self._drop_down_menu_template("Select Technique", 
                ["Custom value", "Number of Values", "Add Outliers"], self.add_noise_technique_callback, 2)
            case "Column":
                self.column_technique_selection_menu = self._drop_down_menu_template("Select Technique", 
                ["Duplicate", "New", "Feature Engineering"], self.add_column_technique_callback, 2)

    def add_noise_technique_callback(self, choice):
        self.variables["var_2"] = choice
        self.schedule_button.configure(state="disabled")
        self.sme_selector.configure(state="disabled")
        self.sme_selector.set("")

        # Remove all previously packed widgets in manipulations frame.
        for widget in self.widget_list:
            if widget["col_pos"] != 1 and widget["col_pos"] != 2:
                widget["widget"].grid_forget()

        match choice:
            case "Custom value":
                self.user_entry_box = self.user_entry_box_template(3, self.entry_box_standard_callback)
            case "Number of Values":
                self.user_entry_box = self.user_entry_box_template(3, self.entry_box_numerical_callback)
            case "Add Outliers":
                self.outliers_technique_selection_menu = self._drop_down_menu_template("Select Technique", 
                ["Z-score(lower percentile)", "Z-score(upper percentile)", "Percentile", "Min/Max"], 
                self.outliers_technique_callback, 3)
    
    def outliers_technique_callback(self, choice):
        self.variables["var_3"] = choice
        self.schedule_button.configure(state="disabled")
        self.sme_selector.configure(state="disabled")
        self.sme_selector.set("")

        # Remove all previously packed widgets in manipulations frame.
        for widget in self.widget_list:
            if widget["col_pos"] != 1 and widget["col_pos"] != 2 and widget["col_pos"] != 3:
                widget["widget"].grid_forget()

        match choice:
            case "Z-score(lower percentile)":
                self.sme_selector.configure(values=["Single"])
                self.sme_selector.configure(state="normal")
            case "Z-score(upper percentile)":
                self.sme_selector.configure(values=["Single"])
                self.sme_selector.configure(state="normal")
            case "Percentile":
                self.user_entry_box = self.user_entry_box_template(4, self.entry_box_numerical_pos_4_callback)
                self.sme_selector.configure(values=["Single"])
            case "Min/Max":
                pass

    def add_column_technique_callback(self, choice):
        self.variables["var_2"] = choice
        self.schedule_button.configure(state="disabled")
        self.sme_selector.configure(state="disabled")
        self.sme_selector.set("")

        # Remove all previously packed widgets in manipulations frame.
        for widget in self.widget_list:
            if widget["col_pos"] != 1 and widget["col_pos"] != 2:
                widget["widget"].grid_forget()

        match choice:
            case "Duplicate":
                self.column_technique_selection_menu = self._drop_down_menu_template("Select Column", 
                self.column_headers, self._sme_selector_col_3_callback, 3)
                self.sme_selector.configure(values=["Single"])
            case "New":
                self.user_entry_box = self.user_entry_box_template(3, self.entry_box_standard_callback)
                self.sme_selector.configure(values=["Single"])
            case "Feature Engineering":
                self.column_technique_selection_menu = self._drop_down_menu_template("Select Technique", 
                ["Polynomial Features", "Interaction Features", "Feature Aggregation", "Feature Crosses"],
                self._sme_selector_col_3_callback, 3)
                self.sme_selector.configure(values=["Single", "Multiple"])

    def reduce_method_select_callback(self, choice):
        self.variables["var_1"] = choice
        self.schedule_button.configure(state="disabled")
        self.sme_selector.configure(state="disabled")
        self.sme_selector.configure(values=["Entire"])
        self.sme_selector.set("")

        # Remove all previously packed widgets in manipulations frame.
        for widget in self.widget_list:
            if widget["col_pos"] != 1:
                widget["widget"].grid_forget()

        if choice == "Data Dimensionality":
            # Add technique selection drop down menu
            self.technique_selection_menu = self._drop_down_menu_template("Select Technique", 
                ["Algorithmic", "Manual"], self._dimensionality_reduction_callback, 2) 

        elif choice == "Rows":
            # Add drop down menu for column selection
            self.reduce_column_menu = self._drop_down_menu_template("Select Variable", 
                ["Missing Values", "Duplicate Rows"], self._sme_selector_col_2_callback, 2)

    def _dimensionality_reduction_callback(self, choice):
        self.variables["var_2"] = choice
        self.schedule_button.configure(state="disabled")
        self.sme_selector.configure(state="disabled")
        self.sme_selector.set("")

        # Remove all previously packed widgets in manipulations frame.
        for widget in self.widget_list:
            if widget["col_pos"] != 1 and widget["col_pos"] != 2:
                widget["widget"].grid_forget()

        match choice:
            case "Algorithmic":
                self.algorithmic_selection_menu = self._drop_down_menu_template("Select Technique", 
                ["PCA(Existing)", "PCA(Retain)", "LDA", "SVD(Existing)", "SVD(Retain)", "Sklearn(Existing)", 
                 "Sklearn(Retain)"], self._dimension_reduction_algo_callback, 3) 

            case "Manual":
                self.algorithmic_selection_menu = self._drop_down_menu_template("Select Technique", 
                ["Retain", "Remove"], self._dimension_reduction_manual_callback, 3) 


    def _dimension_reduction_manual_callback(self, choice):
        self.variables["var_3"] = choice
        self.schedule_button.configure(state="disabled")
        self.sme_selector.configure(state="disabled")
        self.sme_selector.configure(values=["Entire"])
        self.sme_selector.set("")  

        # Remove all previously packed widgets in manipulations frame.
        for widget in self.widget_list:
            if widget["col_pos"] != 1 and widget["col_pos"] != 2 and widget["col_pos"] != 3:
                widget["widget"].grid_forget() 

        match choice:
            case "Retain":
                self.pca_existing_drop_down = self._drop_down_menu_template("Select Column",
                self.column_headers, self._sme_selector_col_4_callback, 4)                
            case "Remove":
                self.pca_existing_drop_down = self._drop_down_menu_template("Select Column",
                self.column_headers, self._sme_selector_col_4_callback, 4)    

    def _dimension_reduction_algo_callback(self, choice):
        self.variables["var_3"] = choice
        self.schedule_button.configure(state="disabled")
        self.sme_selector.configure(state="disabled")
        self.sme_selector.configure(values=["Entire"])
        self.sme_selector.set("")       

        # Remove all previously packed widgets in manipulations frame.
        for widget in self.widget_list:
            if widget["col_pos"] != 1 and widget["col_pos"] != 2 and widget["col_pos"] != 3:
                widget["widget"].grid_forget() 

        match choice:
            case "PCA(Existing)":
                self.pca_existing_drop_down = self._drop_down_menu_template("Select Column",
                    self.column_headers, self._sme_selector_col_4_callback ,4)
            case "PCA(Retain)":
                self.user_entry_box = self.user_entry_box_template(4, self.entry_box_numerical_pos_4_callback)
            case "LDA":
                self.pca_existing_drop_down = self._drop_down_menu_template("Select Column",
                    self.column_headers, self._sme_selector_col_4_callback ,4)
            case "SVD(Existing)":
                self.pca_existing_drop_down = self._drop_down_menu_template("Select Column",
                    self.column_headers, self._sme_selector_col_4_callback ,4)
            case "SVD(Retain)":
                self.user_entry_box = self.user_entry_box_template(4, self.entry_box_numerical_pos_4_callback)
            case "Sklearn(Existing)":
                self.pca_existing_drop_down = self._drop_down_menu_template("Select Column",
                    self.column_headers, self._sme_selector_col_4_callback ,4)
            case "Sklearn(Retain)":
                self.user_entry_box = self.user_entry_box_template(4, self.entry_box_numerical_pos_4_callback)

    def manipulate_col_select_callback(self, choice):
        self.variables["var_1"] = choice
        self.schedule_button.configure(state="disabled")
        self.sme_selector.configure(state="disabled")
        self.sme_selector.set("")

         # Remove all previously packed widgets in manipulations frame.
        for widget in self.widget_list:
            if widget["col_pos"] != 1:
                widget["widget"].grid_forget()

        match choice:
            case "Replace Missing Values":
                self.replace_missing_values_menu = self._drop_down_menu_template("Select Manipulation", 
                ["Numerical Column", "Categorial Column"], None, 2)
            case "Replace Other Values":
                self.replace_other_values_menu = self._drop_down_menu_template("Select Manipulation", 
                ["Value to Replace", "New Value"], None, 2)
            case "Expand (add rows)":
                self.expand_menu = self._drop_down_menu_template("Select Manipulation", 
                ["Random Sampling", "Bootstrap Resamping", "SMOTE", "Add Noise"], None, 2)  
            case "Data Transformation":
                self.data_transformation_menu = self._drop_down_menu_template("Select Manipulation", 
                ["Feature Scaling/Normalisation", "Feature Encoding"], None, 2)                            

    def _label_template(self, text, col_pos):
        label = CTkLabel(
            self.manipulations_frame_2, 
            text=text, 
            anchor="w")
        label.grid(row=0, column=col_pos, padx=(8, 10), pady=(8, 8), sticky="w")
        self.widget_list.append({"col_pos": col_pos, "widget": label})
        return label
    
    def user_entry_box_template(self, col_pos, callback):
        # User entry text box template
        entry_box_command = self.register(callback)
        user_entry_box = CTkEntry(
            self.manipulations_frame_2,
            textvariable=StringVar(value=""),
            corner_radius=5, 
            width=150,
            validate='key',
            validatecommand=(entry_box_command, '%P')
            ) 
        user_entry_box.grid(row=0, column=col_pos, padx=(8, 10), pady=(8, 8), sticky="w")
        self.widget_list.append({"col_pos": col_pos, "widget": user_entry_box})
        
        return user_entry_box
    
    def entry_box_standard_callback(self, choice):
        if len(choice) > 0:
            self.variables["var_3"] = choice
            self.sme_selector.configure(state="normal")  
            return True
        elif len(choice) == 0:
            self.sme_selector.configure(state="disabled") 
            return True

    def entry_box_numerical_callback(self, choice):
        if choice.isdigit():
            self.variables["var_3"] = choice
            self.sme_selector.configure(state="normal")
            return True        
        elif len(choice) == 0:
            self.sme_selector.configure(state="disabled") 
            return True
        else:
            self.sme_selector.configure(state="disabled") 
            return False
    
    def entry_box_numerical_pos_4_callback(self, choice):
        if choice.isdigit():
            self.variables["var_4"] = choice
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
        drop_down_menu.grid(row=0, column=col_pos, padx=(0, 4), pady=(8, 8), sticky="w")
        self.widget_list.append({"col_pos": col_pos, "widget": drop_down_menu})
        return drop_down_menu
       
    def _set_sme_variable(self, choice):
        self.variables["sme"] = choice
        self.schedule_button.configure(state="normal")

    def _sme_selector_col_2_callback(self, choice):
        self.variables["var_2"] = choice
        self.sme_selector.configure(state="enabled")

    def _sme_selector_col_3_callback(self, choice):
        self.variables["var_3"] = choice
        self.sme_selector.configure(state="enabled")

    def _sme_selector_col_4_callback(self, choice):
        self.variables["var_4"] = choice
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

    def refresh_manipulate_widgets(self, column_headers):
        """Refresh, update or populate the values of various widgets on Manipulate view with appropriate
        information pulled from the loaded dataset e.g. column headers for option menues, row count etc. 

        Args:
            dataset_attributes (tuple): A tuple consisting of row count and list of column headers (str).
        """
        self.column_headers = column_headers
