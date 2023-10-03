from pandas import *

class ManipulationsModel():
    def __init__(self):
        """
        Initialise the ManipulationsModel component of the application.

        This class represents the ManipulationsModel component of the application's MVC (Model-View-Controller) architecture.
        It initialises the models to be consumed by the controllers of this applicaiton.
        """
        self.schedule_set = []
        self._manip_collection()
        
        super().__init__()

    def _manip_collection(self):
            self.manip_collection = {
                 "add_noise": "add noise function"
            }
    
    def churner(scheduler_row):
        # for r in scheduler_row:
        #     manip_collection[r["action"]](r["args"])
            pass

    def update_schedule_set(self, manip_set):
          self.schedule_set.append(manip_set)
          print(self.schedule_set)

    def get_schedule_set(self):
          return self.schedule_set
          
    # Temp method for testing
    def remove_column(self):   
        df = self.model.DATASET.get_reference_to_current_snapshot()
        column_name = str(self.scheduler_actions[self.step_count-1]["variable_2"])
        df = df.drop([column_name], axis=1)
        df.to_csv("./db/temp/temp.csv", index=False)
        self.model.DATASET.load_dataset(file_path="./db/temp/temp.csv", dataset_name="wine_dataset")

    # Temp method for testing
    def add_noise(self, args=None):
        a,b = args #unpack


        # Define the variable to introduce noise to and the value to replace
        variable_to_noise = 'Age'  # Replace with the actual variable name
        value_to_replace = 200  # Replace with the value you want to replace

        # Define the percentage of rows to be replaced
        percent_to_replace = 10  # Replace with the desired percentage

        # Calculate the number of rows to replace
        num_rows_to_replace = int(len(df) * (percent_to_replace / 100))

        # Create a mask to select rows to replace
        mask = random.sample(range(len(df)), num_rows_to_replace)

        # Use the mask to replace the specified variable
        df.loc[mask, variable_to_noise] = value_to_replace

        # Save the noisy dataset to a new CSV file
        noisy_dataset_path = r'C:\Users\61408\noisy_breast_cancer_dataset.csv'
        df.to_csv(noisy_dataset_path, index=False)

        print(f"Noisy dataset saved to {noisy_dataset_path}")