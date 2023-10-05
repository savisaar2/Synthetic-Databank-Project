import pandas as pd
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
                 "Reduce Columns (Dimensionality)": self.reduce_columns
            }
    
    def generate_churner(self, scheduler_row):
        for index, r in enumerate(scheduler_row):
            # Set in dataframe as current, but not for the first item.
            if not index:
                pass
            else:
                r["df"] = self.current_df

            self.generated_df = self.manip_collection[r["action"]](r["sub_action"], r["df"], r["column"], r["args"])
            self.current_df = self.generated_df
        self.current_df = []
        self.schedule_set = []
        return self.generated_df

    def update_schedule_set(self, manip_set):
          self.schedule_set.append(manip_set)

    def add_noise(self, sub_action, df, column, args):
        a, b, c = args["a"], args["b"], args["c"]  #unpack args

        match sub_action:
            case "Add Random Custom Value":
                # Insert function here!!!
                pass
            case "Add Missing":
                # Insert function here!!!
                pass
            case "Add Outliers Z-score":
                # Insert function here!!!
                pass
            case "Add Outliers Percentile":
                # Insert function here!!!
                pass
            case "Add Outliers Min/Max":
                # Insert function here!!!
                pass

    def add_column(self, sub_action, df, column, args):
        """Adds a column(s) to a pandas dataframe.

        Args:
            sub_action (str): Description of user selected chosen technique
            df (_type_): The dataframe to be manipulated.
            column (_type_): Name of single column (if selected by user as "single").
            args (_type_): Dictinory of the arguments associated with the sceduled manipulation.

        Returns:
            pandas_dataframe: A Pandas dataframe which has been manipulated.
        """
        a, b, c = args["a"], args["b"], args["c"]  #unpack args

        match sub_action:
            case "Duplicate":
                # Function to add an extra column by duplicating an existing column
                df_with_duplicate_column = df.copy()
                df_with_duplicate_column[random.randrange(1,100)] = df_with_duplicate_column[column]
                return df_with_duplicate_column
            case "New":
                # Function to add new column to dataframe.
                df.insert(0, a, " ")
                return df
            case "Feature Engineering Polynominal Features":
                # Insert function here!!!
                pass
            case "Feature Engineering Interaction Features":
                # Insert function here!!!
                pass

    def reduce_columns(self, sub_action, df, column, args): 
        a, b, c = args["a"], args["b"], args["c"]  #unpack args

        match sub_action:
            case "Algorithmic PCA":
                # Insert function here!!!
                pass
            case "Algorithmic LDA":
                # Insert function here!!!
                pass
            case "Algorithmic SVD":
                # Insert function here!!!
                pass
            case "Algorithmic Sklearn":
                # Insert function here!!!
                pass
            case "Manual":
                # Insert function here!!!
                pass

    def remove_rows(self, sub_action, df, column, args):   
        a, b, c = args["a"], args["b"], args["c"]  #unpack args

        match sub_action:
            case "Missing Values":
                # Insert function here!!!
                pass
            case "Duplicate Rows":
                # Insert function here!!!
                pass




