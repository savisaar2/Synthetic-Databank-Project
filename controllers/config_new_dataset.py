from utils.logger_utils import Logger
from tkinter import END
import pandas

class ConfigNewDatasetController:
    def __init__(self, model, view):
        """
        Initialises an instance of the ConfigNewDatasetController class.

        This class handles logic and interaction between the ConfigNewDataset overlay and dataframe/config_new_dataset model.

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
        self.frame = self.view.frames["config_new_dataset"]
        self._bind()

    def _bind(self):
        """
        Private method to establish event bindings.
        
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the config_new_dataset overlay.
        """
        self.frame.cancel_button.bind("<Button-1>", lambda _: self.frame.hide_view(), add="+")
        self.frame.cancel_button.bind("<Button-1>", lambda _: self._delete_actions(), add="+")
        self.frame.add_col_button.bind("<Button-1>", lambda _: self.add_action_to_model(), add="+")
        self.frame.add_col_button.bind("<Button-1>", lambda _: self.frame.add_col_to_config(), add="+")
        self.frame.confirm_button.bind("<Button-1>", lambda _: self.populate_dataset())

    def add_action_to_model(self):
        """
        Method to populate user actions to the action set in the UI and model.
        Bound to "add_col_button" located in the config_new_dataset overlay.
        """
        if self.frame.add_col_button._state == "normal":
            action_set = {
                "action": self.frame.variables["action"],
                "arg_a": self.frame.variables["arg_a"],
                "arg_b": self.frame.variables["arg_b"],
                "col_name": self.frame.variables["col_name"],
                "df": self.model.DATASET.get_reference_to_current_snapshot()
            }
            print(action_set)
            self.model.config_new_dataset.update_action_set(action_set)

    def populate_dataset(self):

        try:
            if self.frame.confirm_button._state == "normal" and len(self.model.config_new_dataset.action_set) > 0:
                self.model.config_new_dataset.rows = self.frame.rows
                generated_df = self.model.config_new_dataset.action_churner(self.model.config_new_dataset.action_set)
                self.model.DATASET.add_generated_dataset_to_snapshot(self.model.config_new_dataset.action_set, 
                                                                    "Generated Dataset", generated_df)
                self._delete_actions()
                self.frame.hide_view()
                self.model.config_new_dataset.rows = 10
                self.frame.rows_entry_box.delete(0, END)
        except:
            self.logger.log_error("Population of data to new data set failed.")
            
    def _delete_actions(self):
        self.model.config_new_dataset.action_set = []
        
        for widget in self.frame.frame_5.winfo_children():
            widget.destroy()

