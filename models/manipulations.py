import pandas as pd
import random
import numpy as np
from sklearn.decomposition import PCA

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
                 "Add Noise": self.add_noise,
                 "Add Column": self.add_column,
                 "Reduce Remove Rows": self.remove_rows,
                 "Reduce Columns (Dimensionality)": self.reduce_columns,
                 "Replace Missing Values": self.replace_null_values,
                 "Change Column Name": self.change_column_name,
                 "Expand (add rows)": self.add_rows,
            }
    
    def generate_churner(self, scheduler_row):
        # Set dataframe as current, but not for the first item. 
        for index, r in enumerate(scheduler_row):
            if not index:
                pass
            else:
                r["df"] = self.current_df
                         
            self.current_df  = self.manip_collection[r["action"]](r["sub_action"], 
                                                        r["df"], r["column"], r["args"], r["sme"])
        self.schedule_set = [] # Clear schedule set
        return self.current_df

    def update_schedule_set(self, manip_set):
          self.schedule_set.append(manip_set)

    def add_noise(self, sub_action, df, column, args, sme):
        a, b, c = args["a"], args["b"], args["c"]  #unpack args

        match sub_action:
            case "Add Random Custom Value":
                # Function to add a random custom value to the selected column                
                column_data_type = df[column].dtype # Get the data type of the column                
                # Check for datatype mismatch
                try:
                    if column_data_type == 'int64':
                        a = int(float(a))  
                    elif column_data_type == 'float64':
                        a = float(a)
                    # Get the number of rows in the DataFrame
                    num_rows = df.shape[0]
                    # Generate a random set of row indices to replace       
                    random_row_indices = random.sample(range(num_rows), int(b))                    
                    # Replace the selected rows with the custom value
                    df.loc[random_row_indices, column] = a                                   
                    return df
                except ValueError:                                 
                    print(f"Error: Datatype mismatch. Custom value '{a}' is incompatible with '{column_data_type}'.")

            case "Add Missing":
                a=int(a) # Convert a to int for numbers of value to replace
                match column:                 
                    case "" | None:
                        # Function to add missing value to the entrie dataset                     
                        num_values_to_set_nan = min(a, df.size)
                        random_indices = random.sample(range(df.size), num_values_to_set_nan)
                        mask = np.zeros(df.shape, dtype=bool)
                        mask.ravel()[random_indices] = True
                        df[mask] = np.nan
                        
                        return df
                    case _:
                        # Function to add missing value to the selected column                        
                        # Generate a random set of row indices to replace                
                        random_row_indices = np.random.choice(len(df), a, replace=False)
                        # Introduce missing values to the selected variable
                        df.loc[random_row_indices, column] = np.nan
                        return df
                    
            case "Add Outliers Z-score":
                # Functionto add outliers to the selected to column
                # Check if the selected column is numeric
                if pd.api.types.is_numeric_dtype(df[column]):
                    # Add outliers to the selected variable
                    z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
                    # Identify the rows where z-scores exceed the threshold
                    outlier_indices = np.where(z_scores > float(a))[0]
                    # Ensure the target column has a floating-point dtype
                    df[column] = df[column].astype(float)
                    # Introduce outliers using .loc to set values
                    outlier_values = np.random.uniform(5, 10, len(outlier_indices)).astype(float) #### should user has option to enter the range
                    df.loc[df.index[outlier_indices], column] += outlier_values
                    return df
                else:
                     print(f"'{column}' is not a valid numeric column in the dataset.") 

            case "Add Outliers Percentile":
                # Fucntion to add outliers directly to the selected variable based on percentiles
                lower_bound = np.percentile(df[column], int(a))
                upper_bound = np.percentile(df[column], int(b))
                outliers = np.random.uniform(lower_bound, upper_bound, len(df))
                df[column] += outliers
                return df 
            
            case "Add Outliers Min/Max":
                # Insert function here!!!
                pass

    def add_column(self, sub_action, df, column, args, sme):
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
                df_with_duplicate_column[a] = df_with_duplicate_column[column]
                return df_with_duplicate_column
            case "New":
                # Function to add new column to dataframe.
                df[a]=None
                return df
            case "Feature Engineering Polynominal Features":
                # Insert function here!!!
                pass
            case "Feature Engineering Interaction Features":
                # Insert function here!!!
                pass

    def reduce_columns(self, sub_action, df, column, args, sme): 
        a, b, c = args["a"], args["b"], args["c"]  #unpack args

        match sub_action:
            case "Algorithmic PCA":
                # Function to reduce dataset dimensionality using PCA
                # All features must be numerical
                # Numbers of column/features to keep must be less than the total features
                
                print(a,column)
                
                # Check if there are non-numeric features
                non_numeric_columns = df.select_dtypes(exclude=['int64','int32','float64','float32']).columns
                if not non_numeric_columns.empty:
                    print("Cannot perform PCA on non-numeric features:")
                    print(non_numeric_columns)
                else:
                    # Get the total number of variables (features)
                    total_variables = df.shape[1] - 1  # Subtract 1 for the target column
                    num_components = int(b)
                    if num_components >= df.shape[1]:
                        print("Error: num_components should be less than the total number of features - 1")
                    else:
                        # Extract the features (X) from the DataFrame
                        X = df.drop(columns=[a])  
                        #Initialize and fit the PCA model
                        pca = PCA(n_components=num_components)
                        X_pca = pca.fit_transform(X)
                        # Create a DataFrame with the reduced dimensionality
                        columns = [f'PC{i+1}' for i in range(num_components)]
                        df_pca = pd.DataFrame(data=X_pca, columns=columns)
                        # Add the target column back to df_pca 
                        df_pca[a] = df[a]     
                        print(df_pca.head(10))
                        return df_pca
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

    def remove_rows(self, sub_action, df, column, args, sme):   
        a, b, c = args["a"], args["b"], args["c"]  #unpack args

        match sub_action:
            case "Missing Values":
                # Function to remove rows with missing values
                df_no_misiing = df.dropna()
                return df_no_misiing
            case "Duplicate Rows":
                df_no_duplicate = df.drop_duplicates()
                return df_no_duplicate

    def replace_null_values(self, sub_action, df, column, args, sme):   
        a, b, c = args["a"], args["b"], args["c"]  #unpack args

        match sub_action:
            case "Numerical Column":
                match a:
                    case "Mean":
                        # Insert function here!!!
                        pass
                    case "Median":
                        # Insert function here!!!
                        pass
                    case "KNN":
                        # Insert function here!!!
                        pass
                    case "ML":
                        # Insert function here!!!
                        pass
                    case "Manual":
                        # Insert function here!!!
                        pass
            case "Categorial Column":
                match a:
                    case "Mode":
                        # Insert function here!!!
                        pass
                    case "Similarity":
                        # Insert function here!!!
                        pass
                    case "ML":
                        # Insert function here!!!
                        pass
                    case "Manual":
                        # Insert function here!!!
                        pass

    def change_column_name(self, sub_action, df, column, args, sme):   
        a, b, c = args["a"], args["b"], args["c"]  #unpack args

        # Insert function here!!!
        pass

    def add_rows(self, sub_action, df, column, args, sme):   
        a, b, c = args["a"], args["b"], args["c"]  #unpack args
        
        match sub_action:
            case "Random Sampling":
                # Insert function here!!!
                pass
            case "Bootstrap Resampling":
                # Insert function here!!!
                pass
            case "SMOTE":
                # Insert function here!!!
                pass        
