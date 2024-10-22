from utils.logger_utils import Logger
class ManipulateController:
    def __init__(self, model, view):
        """
        Initialises an instance of the ManipulateController class.

        This class handles logic and interaction between the Manipulate view and dataframe model.

        Parameters
        ----------
        model : Model
            The applicaiton's model instance.
        name : View
            The application's view instance.
        """
        self.logger = Logger()
        self.model = model
        self.view = view
        self.frame = self.view.frames["manipulate"]
        self.col_dtype_dict = {}
        self._bind()
        self.step_count = 0 
        self.MAX_STEPS = 4
        self.current_df =""
        self.snapshot_count = 0
        
    def _bind(self):
        """
        Private method to establish event bindings.
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the manipulate page.
        """
        # Refreshes widgets and scan of datatypes in dataframe.
        #self.view.frames["menu"].manipulate_button.bind("<Button-1>", lambda event: self._scan_dataset(event), add="+")
        #self.view.frames["menu"].manipulate_button.bind("<Button-1>", lambda event: self._refresh_manipulate_widgets(event), add="+")
        self.view.frames["menu"].manipulate_button.bind("<Button-1>", lambda _: self._scan_dataset(), add="+")
        self.view.frames["menu"].manipulate_button.bind("<Button-1>", self._refresh_manipulate_widgets, add="+")
        
        # Add manipulations to scheduler
        self.frame.schedule_button.bind("<Button-1>", lambda _: self._clear_generated_manips_from_scheduler(), add="+")
        self.frame.schedule_button.bind("<Button-1>", lambda _: self.frame.add_manipulation_to_scheduler(), add="+")
        self.frame.schedule_button.bind("<Button-1>", lambda _: self._populate_schedule_set(), add="+")
        
        # Delete all sceduled manipulations
        self.frame.delete_all_button.bind("<Button-1>", lambda _: self._delete_all_scheduled_manipulations())

        # Generate button bind
        self.frame.generate_button.bind("<Button-1>", lambda _: self._generate(), add="+")
        self.frame.generate_button.bind("<Button-1>", self._refresh_manipulate_widgets, add="+")

        # Rollback button bind
        self.frame.rollback_button.bind("<Button-1>", lambda _: self._rollback())
  
    def _refresh_manipulate_widgets(self, event): 
        """
        Obtain column headers from the loaded dataset to be populated in the appropriate widgets e.g. 
        option menues and row count of Manipulate view. Called whenever Manipulate side panel is clicked to 
        ensure correct data.
        """
        if self.view.frames["menu"].manipulate_button.cget("state") == "disabled":
            return

        self._scan_dataset()
        snapshots = self.model.DATASET.get_reference_to_all_snapshots()
        self._update_rollback_selector()
        self.frame.refresh_manipulate_widgets(self.model.DATASET.get_column_headers(), self.col_dtype_dict, snapshots)

        snapshot_name = snapshots[-1]["Name"]
        rows = snapshots[-1]["Dataframe"].shape[0]
        columns = snapshots[-1]["Dataframe"].shape[1]
        schedule_set = snapshots[-1]["Schedule Set"]
        manips = "\n"
        for action in schedule_set:
            new_line = f'{action["step"]}. {action["action"]} | {action["sub_action"]} | {action["column"]}\n' 
            manips = manips + new_line
        self.frame.current_dataset_label.configure(text=f"Selected Dataset: {snapshot_name} | Rows: {rows} | Columns: {columns}\n"
                                                        f"Manipulations:{manips}")
    def _populate_schedule_set(self):
        """
        Method to populate user manipulations to the schedule set in the UI and model.
        Bound to "schedule_button" located in the manipulate frame.
        """
        if self.frame.schedule_button._state == "normal" and self.step_count < self.MAX_STEPS:
            self.step_count +=1

            schedule_set = {
                "step": self.step_count,
                "action": self.frame.variables["action"],
                "sub_action": self.frame.variables["sub_action"],
                "args": self.frame.variables["args"],
                "column": self.frame.variables["column"],
                "outcome": "Pending",
                "df": self.model.DATASET.get_reference_to_current_snapshot()
            }
            self.model.manipulations.update_schedule_set(schedule_set)
 
            self.frame.schedule_button.configure(state="disabled")
            self.frame.generate_button.configure(state="normal")
            
            if self.step_count == self.MAX_STEPS:
                self.frame.schedule_button.configure(state="disabled")
                self.frame.action_selection_menu.configure(state="disabled")

        self.frame.generate_warning.configure(text="")
        self.frame.entry_description.configure(text="")

    def _delete_all_scheduled_manipulations(self):
        """
        Method to delete all UI widgets associated with a scheduled item and clear scheduled manipulations list 
        stored in the model. Bound to "delete_all_button" located in manipulation frame.
        """
        # Remove all widgets and clear variables associated with scheduled manipulations.
        for items_dict in self.frame.scheduler_items:
            for widget in items_dict:
                items_dict[widget].grid_forget()
        self.frame.scheduler_items = []
        self.model.manipulations.schedule_set = []
        self.step_count = 0
        self.frame.action_selection_menu.configure(state="normal")
        self.frame.step_count = 0
        self.frame.generate_button.configure(state="disabled")
        self.frame.generate_warning.configure(text="")
            
    def _generate(self):
        """
        Method to call manipulations churner located in the manipulations model which generates a dataset based on
        the manipulations specified by the user. 
        Refreshes, updates widgets in the UI associated with dataset generation.
        Calls logger utility to populate log file.
        Bound to generate button loacted in manipulation frame.
        """
        try:
            self.frame.generate_warning.configure(text="")

            if len(self.model.manipulations.schedule_set) > 0:   
                generated_df = self.model.manipulations.generate_churner(self.model.manipulations.schedule_set)
                # Logger INFO add
                self._add_manips_to_log()

                # If the generated dataframe returned from the churner failed, log and display user message.
                # Updates to current dataframe in SNAPSHOTS if successful, logs and dsplays user message.
                match generated_df:
                    case False:
                        error_msg = self.model.manipulations.error_msg
                        self.frame.generate_warning.configure(text=f"Generate has failed. Reason: {error_msg}")
                        self.frame.generate_warning.configure(text_color="yellow")
                        
                        # Logger INFO add
                        self.logger.log_info(f"Generate function failed to fully complete successfully.")
                    case _:
                        self.model.DATASET.add_generated_dataset_to_snapshot(self.model.manipulations.schedule_set, 
                                                                            "Generated Dataset", generated_df)
                        self.frame.generate_warning.configure(text="Generate was successful.")
                        self.frame.generate_warning.configure(text_color="green")
                        # Logger INFO add
                        self.logger.log_info(f"Generated dataset added to SNAPSHOTS as current dataframe.")
                        
                # Logic to change outcome label of manipulations.
                for item in self.model.manipulations.schedule_set:
                    index = item["step"]
                    widget = self.frame.scheduler_items[index-1]["outcome"]
            
                    match item["outcome"]:
                        case "Success":
                            widget.configure(text="Success")
                            widget.configure(text_color="green")
                        case "Failed":
                            widget.configure(text="Failed")
                            widget.configure(text_color="red")
                        case "Pending":
                            widget.configure(text="Pending")
                            widget.configure(text_color="yellow")           
            
            # User warning if no manipulations are scheduled and manipulate in clicked.
            else:
                self.frame.generate_warning.configure(text="Must have at least 1 pending manipulation scheduled")
                self.frame.generate_warning.configure(text_color="yellow")

            # Clear variables and widgets associated with post generate function.
            self.model.manipulations.schedule_set = [] 
            self.step_count = 0
            self.frame.step_count = 0
            self.frame.generate_button.configure(state="disabled")
            self._update_rollback_selector()
            self._refresh_manipulate_widgets

        except Exception as error:
            self.logger.log_exception("Generate failed to complete. Traceback:")

    def _scan_dataset(self):  
        """
        Function creates a dictionary of column headers and datatypes. Used for type checking in manipulation UI.
        """
        if self.view.frames["menu"].manipulate_button.cget("state") == "disabled":
            return
        
        df = self.model.DATASET.get_reference_to_current_snapshot()
        self.col_dtype_dict ={}
        for col in self.model.DATASET.get_column_headers():
            self.col_dtype_dict[col] = df.dtypes[col]

    def _clear_generated_manips_from_scheduler(self):
        """Function clears manipulations in the scheduler automatically after a generate function and when a
        new manipulation is added.
        """
        if self.step_count == 0:
            self._delete_all_scheduled_manipulations()

    def _add_manips_to_log(self):
        """Method to clean up the schedule set, and populate the system log during generate function.
        """
        logger_manips = self.model.manipulations.schedule_set
        self.logger.log_info(f"User initiated 'generate' function with schedule set:")
        for item in logger_manips:
            item.pop("df")
            self.logger.log_info(f"{item}")

    def _rollback(self):
        """Rollback function of the manipulate UI, bound to rollback button in manipulations UI.
        """
        try:
            index = self.frame.get_rollback_index()
            self.model.DATASET.rollback(int(index))
            self.logger.log_info(f"User successfully initiated 'rollback' function to snapshot at position: {int(index)}")
            self.snapshot_count = 0
            self._update_rollback_selector()
            self._refresh_manipulate_widgets
        except Exception as error:
            self.logger.log_exception("'Rollback' failed to complete. Traceback:")

    def _update_rollback_selector(self):
        """Function to update the rollback selector widget in the manipulations UI.
        """
        snapshots = self.model.DATASET.get_reference_to_all_snapshots()
        selector_list = []
        self.snapshot_count = 0
        for k in snapshots:
            selector_list.append(str(self.snapshot_count))
            self.snapshot_count +=1
        self.frame.rollback_dataset_selector.configure(values=selector_list)
        self.frame.rollback_dataset_selector.set(value=str(self.snapshot_count-1))