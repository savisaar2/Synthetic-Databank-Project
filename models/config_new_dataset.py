from utils.logger_utils import Logger
from faker import Faker

class ConfigNewDatasetModel():
    def __init__(self):
        """
        Initialise the ConfigNewDatasetModel component of the application.

        This class represents the ConfigNewDatasetModel component of the application's MVC (Model-View-Controller) architecture.
        It initialises the models to be consumed by the controllers of this applicaiton.
        """
        super().__init__()
        self.action_set = []
        self.logger = Logger()
        self._faker_collection()
        self.fake = Faker()
        

    def _faker_collection(self):
        """Dictionary of manipulation functions with their associated key value.
        """
        self.faker_collection = {
                "Custom Integer Range": self._custom_int_range,
                "Custom Float Range": self._custom_float_range,
        }

    def action_churner(self, action_set:list):
        """Action churner function iterates through user's scheduled actions and
        applies them to the current dataframe. 

        Args:
            action_set (list): List of scheduled actions.

        Returns:
            pandas dataframe: dataframe with applied actions.
                                        
        """
        for index, r in enumerate(action_set):
            if not index:
                self.current_df = self.faker_collection[r["action"]](r["arg_a"], r["arg_b"], 
                                                                    r["rows"], r["df"], r["col_name"])
            else:
                r["df"] = self.current_df
                self.current_df = self.faker_collection[r["action"]](r["arg_a"], r["arg_b"], 
                                                                    r["rows"], r["df"], r["col_name"])
        return self.current_df

    def update_action_set(self, action_set:dict):
        """Builds the action set user clicks schedule button. Initiates from the manipulation controller.

        Args:
           action_set (dict): Dictionary of variables to apply to a dataset.
        """
        self.action_set.append(action_set)
        print(self.action_set)

    def _custom_int_range(self, arg_a, arg_b, rows, df, col_name):
        generated_data = []
        for _ in range(rows):
            generated_data.append(self.fake.random_int(min=arg_a, max=arg_b))
        df[col_name] = generated_data
        return df

    def _custom_float_range(self, arg_a, arg_b, rows, df, col_name):
        generated_data = []
        for _ in range(rows):
            generated_data.append(self.fake.pyfloat(right_digits=2, min_value=arg_a, max_value=arg_b))
        df[col_name] = generated_data
        return df
