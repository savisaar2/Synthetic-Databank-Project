from utils.logger_utils import Logger
from faker import Faker

class ConfigNewDatasetModel():
    def __init__(self):
        """
        Initialise the ConfigNewDatasetModel component of the application.

        This class represents the ConfigNewDatasetModel component of the application's MVC (Model-View-Controller) architecture.
        It initialises the models to be consumed by the controllers of this applicaiton.
        """
        self.action_set = []
        self.logger = Logger()
        super().__init__()

    def _faker_collection(self):
        """Dictionary of manipulation functions with their associated key value.
        """
        self.faker_collection = {
                "Custom Integer Range": self.custom_int_range
        }

    def action_churner(self, action_set:list):
        """Action churner function iterates through user's scheduled actions and
        applies them to the current dataframe. 

        Args:
            action_set (list): List of scheduled actions.

        Returns:
            pandas dataframe: dataframe with applied actions.
                                        
        """
        self.current_df = ""
        for r in action_set:
            self.current_df = self._faker_collection[r["action"]](r["arg_a"], r["arg_b"], r["rows"], r["df"])

        return self.current_df

    def update_action_set(self, action_set:dict):
        """Builds the action set user clicks schedule button. Initiates from the manipulation controller.

        Args:
            manip_set (dict): Dictionary of variables to apply to a dataset.
        """
        self.action_set.append(action_set)
        print(self.action_set)

    def custom_int_range(self, arg_a, arg_b, rows, df):
        generated_data = []
        for _ in range(rows):
            generated_data.append(Faker.random_int(min=arg_a, max=arg_b))

        print(generated_data)