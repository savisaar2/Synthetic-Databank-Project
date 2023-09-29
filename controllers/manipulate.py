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
        self.scheduler_actions = []
        self.step_count = 0 
        self.MAX_STEPS = 10

        # TODO - to be removed once Alex has finished feature which loads chosen dataset from Library component.
        # Once Alex is finished, the methods should work natively with obtaining information directly from 
        # dataset model's method calls. 
        self.model.DATASET.load_dataset(file_path="./db/databank/wine_dataset.csv", dataset_name="wine_dataset")

    def _bind(self):
        """
        Private method to establish event bindings.
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the manipulate page.
        """
        self.view.frames["menu"].manipulate_button.bind("<Button-1>", self._refresh_manipulate_widgets)
        
        # Add manipulations to scheduler
        self.frame.schedule_button.bind("<Button-1>", lambda _: self.frame.add_manipulation_to_scheduler(), add="+")
        self.frame.schedule_button.bind("<Button-1>", lambda _: self._populate_scheduler_list(), add="+")

        # Delete all sceduled manipulations
        self.frame.delete_all_button.bind("<Button-1>", lambda _: self._delete_all_scheduled_manipulations())

        # Save column name bind
        self.frame.save_column_name_button.bind("<Button-1>", lambda _: self._save_column_name())

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
            text="Current Dataset: " + 
            str(self.model.DATASET.get_dataset_name()) + ", Rows: " +
            str(self.model.DATASET.get_df_row_count()))

    def _populate_scheduler_list(self):

        if self.frame.schedule_button._state == "normal" and self.step_count < self.MAX_STEPS:
            self.step_count +=1
            self.scheduler_actions.append({
                "step": self.step_count,
                "action": self.frame.action_menu_var,
                "variable_1": self.frame.variable_1,
                "variable_2": self.frame.variable_2,
                "variable_3": self.frame.variable_3,
                "outcome": "in_queue"
            })
            print(self.scheduler_actions)
            self.frame.schedule_button.configure(state="disabled")
            self.frame.generate_button.configure(state="normal")

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

    def _save_column_name(self):
        if len(self.frame.user_entry_box.get()) > 0:
            self.frame.schedule_button.configure(state="normal")
            self.frame.save_column_name_button.configure(state="disabled")
            self.frame.user_entry_box.configure(state="disabled")
            self.frame.variable_3 = self.frame.user_entry_box.get()
        else:
            self.frame.user_entry_box.pack_forget()
            self.frame.user_entry_box = self.frame._user_entry_box_template()
            self.frame.user_entry_box.configure(placeholder_text="Invalid column name, please retry...")

    # Temp method for testing
    def remove_column(self):
        
        df = self.model.DATASET.get_reference_to_current_snapshot()
        column_name = str(self.scheduler_actions[self.step_count-1]["variable_2"])
        df = df.drop([column_name], axis=1)
        df.to_csv("./db/temp/temp.csv", index=False)
        self.model.DATASET.load_dataset(file_path="./db/temp/temp.csv", dataset_name="wine_dataset")
              
    def generate(self):
        if self.frame.generate_button._state == "normal":
            for manip in self.scheduler_actions:
                if manip["outcome"] == "in_queue" and self.frame.scheduler_items[manip["step"]-1]["step"].get() == "on":
                    self._update_frame_scheduler_status(manip)

                    match manip["action"]:
                        case "Add":
                            print("add column generate")

                        case "Reduce":
                            match manip["variable_1"]:
                                case "Algorithmic":
                                    match manip["variable_2"]:
                                        case "A":
                                            print("reduce, algo, tech A")
                                        case "B":
                                            print("reduce, algo, tech B")
                                        case "C":
                                            print("reduce, algo, tech C")
                                case "Manual":
                                    print("reduce, manual")

                        case "Manipulate":
                            match manip["variable_1"]:
                                case "Single":
                                    print("manipulate, single")
                                case "Multiple":
                                    print("manipulate, multiple")
                                case "Entire Set":
                                    print("manipulate, entire set")                                   

                    manip["outcome"] = "Complete"

        self.frame.generate_button.configure(state="disabled")

    def _update_frame_scheduler_status(self,manip):
            self.frame.scheduler_items[manip["step"]-1]["outcome"].configure(text="Complete")
            self.frame.scheduler_items[manip["step"]-1]["outcome"].configure(text_color="Green")
            self.frame.scheduler_items[manip["step"]-1]["step"].configure(state="disabled")

    
