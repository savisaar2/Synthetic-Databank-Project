import pandas as pd

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
        self.model = model
        self.view = view
        self.frame = self.view.frames["manipulate"]
        self._bind()
        self.step_count = 0 
        self.MAX_STEPS = 4

        # TODO - to be removed once Alex has finished feature which loads chosen dataset from Library component.
        # Once Alex is finished, the methods should work natively with obtaining information directly from 
        # dataset model's method calls. 
        #self.model.DATASET.load_dataset(file_path="./db/databank/wine_dataset.csv", dataset_name="wine_dataset")

    def _bind(self):
        """
        Private method to establish event bindings.
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the manipulate page.
        """
        self.view.frames["menu"].manipulate_button.bind("<Button-1>", self._refresh_manipulate_widgets)
        
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
        self.frame.refresh_manipulate_widgets(self.model.DATASET.get_column_headers())
        self.frame.current_dataset_label.configure(
            text=f"Current Dataset: {self.model.DATASET.get_dataset_name()} | Rows: {self.model.DATASET.get_df_row_count()} | "
                    f"Columns: {len(self.model.DATASET.get_column_headers())}")

    def populate_schedule_set(self):

        if self.frame.schedule_button._state == "normal" and self.step_count < self.MAX_STEPS:
            self.step_count +=1

            match self.frame.variables["sme"]:
                case "Single":
                    df = self.model.DATASET.get_column_data(self.frame.variables["column"])
                case "Multiple":
                    pass
                case "Entire":
                    df = self.model.DATASET.get_reference_to_current_snapshot()

            schedule_set = {
                "step": self.step_count,
                "action": self.frame.variables["action"],
                "sub_action": self.frame.variables["sub_action"],
                "args": self.frame.variables["args"],
                "column": self.frame.variables["column"],
                "outcome": "in_queue",
                "df": self.model.DATASET.get_reference_to_current_snapshot()
            }
            self.model.manipulations.update_schedule_set(schedule_set)
 
            self.frame.schedule_button.configure(state="disabled")
            self.frame.generate_button.configure(state="normal")
            self.frame.column_dropdown.configure(state="disbled")
            self.frame.sme_selector.configure(state="disbled")

            if self.step_count == self.MAX_STEPS:
                self.frame.schedule_button.configure(state="disabled")
                self.frame.action_selection_menu.configure(state="disabled")

    def _delete_all_scheduled_manipulations(self):
        for items_dict in self.frame.scheduler_items:
            for widget in items_dict:
                items_dict[widget].grid_forget()

        self.frame.scheduler_items = []
        self.scheduler_actions = []
        self.step_count = 0
        self.frame.action_selection_menu.configure(state="normal")
        self.frame.step_count = 0
        self.frame.generate_button.configure(state="disabled")
        
          
    def generate(self):
        self.model.manipulations.generate_churner(self.model.manipulations.schedule_set)
        
        
        

        

    def _update_frame_scheduler_status(self,manip):
            self.frame.scheduler_items[manip["step"]-1]["outcome"].configure(text="Complete")
            self.frame.scheduler_items[manip["step"]-1]["outcome"].configure(text_color="Green")
            self.frame.scheduler_items[manip["step"]-1]["step"].configure(state="disabled")

    
