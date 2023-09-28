from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkOptionMenu, StringVar, CTkCheckBox, CTkScrollableFrame, CTkEntry, CTkProgressBar
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
        self.action_widget_list =[]
        self.pos2_widget_list =[]
        self.pos3_widget_list =[]
        self.variable_1 = ""
        self.variable_2 = ""
        self.scheduler_items = []
        self.step_count = 0

    def _render_page(self):
        """Renders widgets on the ManipulateView page."""

        # Rollback frames and labels
        self.rollback_frame_1 = CTkFrame(self, fg_color="gray20")
        self.rollback_frame_1.pack(fill="both", pady=(0, 2), padx=20, expand=False)
        self.rollback_label = CTkLabel(self.rollback_frame_1, text="Rollback", font=("Arial", 14, "bold"))
        self.rollback_label.pack(side="left", padx=(8, 0))

        self.rollback_frame_2 = CTkFrame(self, fg_color="gray20")
        self.rollback_frame_2.pack(fill="both", pady=(0, 20), padx=20, expand=False)
        self.current_dataset_label = CTkLabel(self.rollback_frame_2)
        self.current_dataset_label.pack(side="left", padx=(8, 0))

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

        # Action label
        self.action_label = CTkLabel(self.manipulations_frame_2, text="Action:", anchor="w")
        self.action_label.pack(fill="both", side="left", padx=(10, 10))

        # Action menu selector
        self.action_menu_var = StringVar(value="Select Action")
        self.action_selector = ["Add Column", "Reduce Dataset", "Manipulate Dataset"]
        self.action_selection_menu = CTkOptionMenu(
            self.manipulations_frame_2, 
            fg_color="gray10", 
            width=3, 
            values=self.action_selector, 
            command=self.action_callback,
            variable=self.action_menu_var
            )
        self.action_selection_menu.pack(side="left", padx=(10, 10), pady=8, fill='x')

        # Scheduler frame
        self.scheduler_frame = CTkFrame(self, fg_color="gray20")
        self.scheduler_frame.pack(fill="both", pady=(0, 2), padx=20, expand=False)

        # Scheduler Label
        self.scheduler_label = CTkLabel(self.scheduler_frame, text="Scheduler", anchor="w", font=("Arial", 14, "bold"))
        self.scheduler_label.pack(side="left", padx=(8, 0))

        # Scrollable frame for manipulations
        self.scheduler_scroll_frame = CTkScrollableFrame(self, fg_color="gray20")
        self.scheduler_scroll_frame.pack(fill="both", pady=(0, 2), padx=20, expand=True)

        # Step label
        self.step_label = CTkLabel(self.scheduler_scroll_frame, text="Step", font=("Arial", 14))
        self.step_label.grid(row=0, column=0, padx=(8, 50), pady=(0, 10), sticky="w")

        # Action label
        self.sched_action_label = CTkLabel(self.scheduler_scroll_frame, text="Action", font=("Arial", 14))
        self.sched_action_label.grid(row=0, column=1, padx=(0, 150), pady=(0, 10), sticky="w")

        # Variable label
        self.variable_label = CTkLabel(self.scheduler_scroll_frame, text="Variable(s)", font=("Arial", 14))
        self.variable_label.grid(row=0, column=2, padx=(0, 250), pady=(0, 10), sticky="w")

        # Outcome label
        self.outcome_label = CTkLabel(self.scheduler_scroll_frame, text="Outcome", font=("Arial", 14))
        self.outcome_label.grid(row=0, column=3, padx=(0, 0), pady=(0, 10), sticky='w')

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
 
    def add_manipulation_to_scheduler(self):

        if self.schedule_button._state == "normal":
            try:
                self.step_count +=1 # Increase step count

                # Checkbox
                self.step_checkbox = CTkCheckBox(self.scheduler_scroll_frame, text="("+str(self.step_count)+")")
                self.step_checkbox.grid(row=self.step_count, column=0, padx=(10, 0), pady=(10, 0), sticky='w')
                self.step_checkbox.select()
                self.scheduler_items.append(self.step_checkbox)

                # Name of scheduled manipulation
                self.manipulation_label_for_scheduler = CTkLabel(self.scheduler_scroll_frame, text=str(self.action_menu_var), font=("Arial", 14))
                self.manipulation_label_for_scheduler.grid(row=self.step_count, column=1, padx=(0, 0), pady=(10, 0), sticky='w')
                self.scheduler_items.append(self.manipulation_label_for_scheduler)

                if self.action_menu_var == "Add Column":
                    # Get user input for col name
                    self.variable_1 = self.user_entry_box.get()

                # Varible name for scheduled manipulation
                self.variable_label_for_scheduler = CTkLabel(
                    self.scheduler_scroll_frame, 
                    text=self.variable_1 + ", " + self.variable_2,  
                    font=("Arial", 14)
                    )
                self.variable_label_for_scheduler.grid(row=self.step_count, column=2, padx=(0, 0), pady=(10, 0), sticky='w')
                self.scheduler_items.append(self.variable_label_for_scheduler)

                # Label for scheduled manipulation outcome
                self.outcome_label_for_scheduler = CTkLabel(
                    self.scheduler_scroll_frame, 
                    text="In Queue",  
                    font=("Arial", 14)
                    )
                self.outcome_label_for_scheduler.grid(row=self.step_count, column=3, padx=(0, 0), pady=(10, 0), sticky='w')
                self.scheduler_items.append(self.outcome_label_for_scheduler)   

                # # Delete button
                # self.delete_button = CTkButton(
                #     self.scheduler_scroll_frame, 
                #     text="DELETE", 
                #     corner_radius=5, 
                #     border_spacing=5, 
                #     anchor="center", 
                #     state="normal"
                #     )
                # self.delete_button.pack(side="right", padx=(8, 8), pady=(8,8))
                # self.scheduler_items.append(self.delete_button)

            finally:
                # Pack forget for all previously packed widgets for action menu.
                for widget in self.action_widget_list:
                    widget.pack_forget()

                # Reset action menu
                self.action_selection_menu.set("Select Action")

                # Delete text in user entry box
                self._clear_entry()

    def action_callback(self, choice):
        self.action_menu_var = choice
        self.schedule_button.configure(state="disabled")  
        self.variable_1 = ""
        self.variable_2 = ""   

        # Pack forget for all previously packed widgets for action menu.
        for widget in self.action_widget_list:
            widget.pack_forget()

        match self.action_menu_var:
            case "Add Column":
                # Show column name label
                self.add_column_name_label = self._label_template("Column Name:")

                # User column name entry box
                self.user_entry_box = self._user_entry_box_template()

                # Save column name button
                self.save_column_name_button.pack(side="right", padx=(8, 8), pady=(8,8))
                self.save_column_name_button.configure(state='normal')
                self.action_widget_list.append(self.save_column_name_button)
                
            case "Reduce Dataset":
                # Show method label
                self.method_label = self._label_template("Method:")

                # Show reduce method menu drop down
                self.method_selection_menu = self._drop_down_menu_pos2_template("Select Method", 
                    ["Algorithmic", "Manual"]) 
                self.method_selection_menu.configure(command=self.reduce_method_select_callback)

            case "Manipulate Dataset":
                # Show variable label
                self.variable_label = self._label_template("Variable:")

                # Show variable menu drop down
                self.maniuplate_variable_menu = self._drop_down_menu_pos2_template("Select Variable", 
                    ["Single", "Multiple", "Entire Set"])   
            
    def reduce_method_select_callback(self, choice):
        self.method_menu_var = choice
        self.variable_1 = choice
        self.schedule_button.configure(state="disabled")

        for widget in self.pos3_widget_list:
            widget.pack_forget()

        if self.method_menu_var == "Algorithmic":
            # Add technique selection drop down menu
            self.technique_selection_menu = self._drop_down_menu_pos3_template("Select Technique", 
                ["A", "B", "C"]) 

        elif self.method_menu_var == "Manual":
            # Add column name label
            self.add_column_name_label = self._label_template("Column Name:")

            # Add drop down menu for column selection
            self.reduce_column_menu = self._drop_down_menu_pos3_template("Select Column", 
                self.column_headers)

    def _clear_entry(self):
        self.user_entry_box.delete(0, 'end')

    def _label_template(self, text):
        label = CTkLabel(
            self.manipulations_frame_2, 
            text=text, 
            anchor="w")
        label.pack(side="left", padx=(10, 0))
        self.action_widget_list.append(label)
        self.pos2_widget_list.append(label)
        self.pos3_widget_list.append(label)
        return label
    
    def _user_entry_box_template(self):
        # User entry text box template
        user_entry_box = CTkEntry(
            self.manipulations_frame_2,
            placeholder_text="Enter column name...",
            corner_radius=5, 
            width=300,
            ) 
        user_entry_box.pack(side="left", padx=(5, 0))
        self.action_widget_list.append(user_entry_box)
        return user_entry_box
    
    def _drop_down_menu_pos2_template(self, start_text: str, menu_options: list):    
        menu_var = StringVar(value=start_text)
        selector = menu_options
        drop_down_menu = CTkOptionMenu(
            self.manipulations_frame_2, 
            fg_color="gray10", 
            width=3, 
            values=selector, 
            command=self._set_scheduler_variable_1,
            variable=menu_var
            )
        drop_down_menu.pack(side="left", padx=(10, 10), fill='x')
        self.action_widget_list.append(drop_down_menu)
        self.pos2_widget_list.append(drop_down_menu)
        return drop_down_menu
    
    def _drop_down_menu_pos3_template(self, start_text: str, menu_options: list):    
        menu_var = StringVar(value=start_text)
        selector = menu_options
        drop_down_menu = CTkOptionMenu(
            self.manipulations_frame_2, 
            fg_color="gray10", 
            width=3, 
            values=selector, 
            command=self._set_scheduler_variable_2,
            variable=menu_var
            )
        drop_down_menu.pack(side="left", padx=(10, 10), fill='x')
        self.action_widget_list.append(drop_down_menu)
        self.pos3_widget_list.append(drop_down_menu)
        
        return drop_down_menu
    
    def _set_scheduler_variable_1(self, choice):
        self.variable_1 = choice
        self.schedule_button.configure(state="normal")

    def _set_scheduler_variable_2(self, choice):
        self.variable_2 = choice
        self.schedule_button.configure(state="normal")

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

    def refresh_manipulate_widgets(self, dataset_attributes):
        """Refresh, update or populate the values of various widgets on Amnipulate view with appropriate
        information pulled from the loaded dataset e.g. column headers for option menues, row count etc. 

        Args:
            dataset_attributes (tuple): A tuple consisting of row count and list of column headers (str).
        """
        self.column_headers = dataset_attributes
        #self.reduce_column_menu.configure(values=self.column_headers)
