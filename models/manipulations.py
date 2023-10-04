from pandas import *
import random

class ManipulationsModel():
    def __init__(self):
        """
        Initialise the ManipulationsModel component of the application.

        This class represents the ManipulationsModel component of the application's MVC (Model-View-Controller) architecture.
        It initialises the models to be consumed by the controllers of this applicaiton.
        """
        self.schedule_set = []
        self._manip_collection()
        self.current_df = ""
        
        super().__init__()

    def _manip_collection(self):
            self.manip_collection = {
                 "Add Noise": self.add_noise,
                 "Add Column": self.add_column,
                 "Remove Rows": self.remove_rows,
            }
    
    def generate_churner(self, scheduler_row):
        for r in scheduler_row:
            match r["step"]:
                 case 1:
                    generated_df = self.manip_collection[r["action"]](r["sub_action"], r["df"], r["column"], r["args"])
                    self.current_df = generated_df
                 case _:
                    r["df"] = self.current_df
                    generated_df = self.manip_collection[r["action"]](r["sub_action"], r["df"], r["column"], r["args"])
                    self.current_df = generated_df

    def update_schedule_set(self, manip_set):
          self.schedule_set.append(manip_set)

    def add_noise(self, sub_action, df, column, args=None):
        a,b,c = args #unpack

        match sub_action:
            case "Add Random Custom Value":
                pass
            case "Add Outliers":
                pass   
    
    def add_column(self, sub_action, df, column, args):
        match sub_action:
            case "Duplicate":
                # Function to add an extra column by duplicating an existing column
                df_with_duplicate_column = df.copy()
                df_with_duplicate_column[random.randrange(1,100)] = df_with_duplicate_column[column]
                return df_with_duplicate_column
            case "New":
                pass
            case "Feature Engineering":
                pass

    def remove_columns(self, sub_action, df, column, args=None): 
        a,b,c = args #unpack

        match sub_action:
            case "Algorithmic":
                pass
            case "Manual":
                pass

    def remove_rows(self, sub_action, df, column, args=None):   
        a,b,c = args #unpack

        match sub_action:
            case "Missing Values":
                pass
            case "Duplicate Rows":
                pass




