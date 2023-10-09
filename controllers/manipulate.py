import pandas as pd

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
        

    def _bind(self):
        """
        Private method to establish event bindings.
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the manipulate page.
        """
        self.view.frames["menu"].manipulate_button.bind("<Button-1>", lambda _: self._scan_dataset(), add="+")
        self.view.frames["menu"].manipulate_button.bind("<Button-1>", self._refresh_manipulate_widgets, add="+")
        
        # Add manipulations to scheduler
        self.frame.schedule_button.bind("<Button-1>", lambda _: self.frame.add_manipulation_to_scheduler(), add="+")
        self.frame.schedule_button.bind("<Button-1>", lambda _: self.populate_schedule_set(), add="+")

        # Delete all sceduled manipulations
        self.frame.delete_all_button.bind("<Button-1>", lambda _: self._delete_all_scheduled_manipulations())

        # Generate button bind
        self.frame.generate_button.bind("<Button-1>", lambda _: self.generate(), add="+")
        self.frame.generate_button.bind("<Button-1>", self._refresh_manipulate_widgets, add="+")
        
    def _refresh_manipulate_widgets(self, event): 
        """
        Obtain column headers from the loaded dataset to be populated in the appropriate widgets e.g. 
        option menues and row count of Manipulate view. Called whenever Manipulate side panel is clicked to 
        ensure correct data.
        """
        self.frame.refresh_manipulate_widgets(self.model.DATASET.get_column_headers(), self.col_dtype_dict)
        self.frame.current_dataset_label.configure(
            text=f"Current Dataset: {self.model.DATASET.get_dataset_name()} | Rows: {self.model.DATASET.get_df_row_count()} | "
                    f"Columns: {len(self.model.DATASET.get_column_headers())}")

    def populate_schedule_set(self):

        if self.frame.schedule_button._state == "normal" and self.step_count < self.MAX_STEPS:
            self.step_count +=1

            schedule_set = {
                "step": self.step_count,
                "action": self.frame.variables["action"],
                "sub_action": self.frame.variables["sub_action"],
                "args": self.frame.variables["args"],
                "column": self.frame.variables["column"],
                "sme": self.frame.variables["sme"],
                "outcome": "in_queue",
                "df": self.model.DATASET.get_reference_to_current_snapshot()
            }
            self.model.manipulations.update_schedule_set(schedule_set)
 
            self.frame.schedule_button.configure(state="disabled")
            self.frame.generate_button.configure(state="normal")
            self.frame.sme_selector.configure(state="disabled")

            if self.step_count == self.MAX_STEPS:
                self.frame.schedule_button.configure(state="disabled")
                self.frame.action_selection_menu.configure(state="disabled")

    def _delete_all_scheduled_manipulations(self):
        for items_dict in self.frame.scheduler_items:
            for widget in items_dict:
                items_dict[widget].grid_forget()

        self.frame.scheduler_items = []
        self.model.manipulations.schedule_set = []
        self.step_count = 0
        self.frame.action_selection_menu.configure(state="normal")
        self.frame.step_count = 0
        self.frame.generate_button.configure(state="disabled")
                 
    def generate(self):
        self.frame.generate_warning.configure(text="")

        if len(self.model.manipulations.schedule_set) > 0:
                manips = self.model.manipulations.schedule_set
                generated_df = self.model.manipulations.generate_churner(self.model.manipulations.schedule_set)
                self.model.DATASET.add_generated_dataset_to_snapshot(manips, "Generated Dataset",
                                                                    generated_df)
        else:
             self.frame.generate_warning.configure(text="Must have at least 1 manipulation scheduled")

        
                
        
    def _update_frame_scheduler_status(self,manip):
            self.frame.scheduler_items[manip["step"]-1]["outcome"].configure(text="Complete")
            self.frame.scheduler_items[manip["step"]-1]["outcome"].configure(text_color="Green")
            self.frame.scheduler_items[manip["step"]-1]["step"].configure(state="disabled")

    def _scan_dataset(self):  
        df = self.model.DATASET.get_reference_to_current_snapshot()
        self.col_dtype_dict ={}
        for col in self.model.DATASET.get_column_headers():
            self.col_dtype_dict[col] = df.dtypes[col]
        print(self.col_dtype_dict)
