from utils.logger_utils import Logger

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
        self.frame.cancel_button.bind("<Button-1>", lambda _: self.frame.hide_view())
        self.frame.add_col_button.bind("<Button-1>", lambda _: self.frame.add_col_to_config(), add="+")
        self.frame.add_col_button.bind("<Button-1>", self.add_action_to_model(), add="+")
        self.frame.confirm_button.bind("<Button-1>", lambda _: self.populate_dataset())

    def add_action_to_model(self):
        """
        Method to populate user actions to the action set in the UI and model.
        Bound to "add_col_button" located in the config_new_dataset overlay.
        """
        print("in add action to model func")
        if self.frame.add_col_button._state == "normal":
        
            action_set = {
                "action": self.frame.variables["action"],
                "arg_a": self.frame.variables["arg_a"],
                "arg_b": self.frame.variables["arg_b"],
                "rows": 100,
                "df": self.model.DATASET.get_reference_to_current_snapshot()
            }
            print(action_set)
            self.model.config_new_dataset.update_action_set(action_set)

    def populate_dataset(self):
        generated_df = self.model.config_new_dataset.action_churner(self.model.config_new_dataset.action_set)
        self.model.DATASET.add_generated_dataset_to_snapshot(self.model.config_new_dataset.action_set, 
                                                            "Generated Dataset", generated_df)
        


