import pandas as pd
import random
import numpy as np
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.preprocessing import StandardScaler

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
                 "Data Transformation": self.data_transformation,
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
                # Function to add random custom value to the selected column  
                # a = custom value; b = number of random custom values; column = the selected column

                # Get the number of rows in the DataFrame
                num_rows = df.shape[0]
                # Generate a random set of row indices to replace       
                random_row_indices = random.sample(range(num_rows), b)                    
                # Replace the selected rows with the custom value
                df.loc[random_row_indices, column] = a                                   
                return df

            case "Add Missing":
                # a = number of missing values; column = the selected column

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
                # Functionto add outliers to the selected to column  based on z-score              
                # a = z-score threshold; column = the selected column
                               
                z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
                # Identify the rows where z-scores exceed the threshold
                outlier_indices = np.where(z_scores > float(a))[0]
                # Ensure the target column has a floating-point dtype
                df[column] = df[column].astype(float)
                # Introduce outliers using .loc to set values
                outlier_values = np.random.uniform(5, 10, len(outlier_indices)).astype(float) #### should user has option to enter the range?
                df.loc[df.index[outlier_indices], column] += outlier_values
                return df

            case "Add Outliers Percentile":
                # Functionto add outliers to the selected to column  based on lower bound and upper bound
                # a= number of outliers; column = the selected column

                # Calculate the IQR (Interquartile Range) for the selected column

                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1

                # Calculate lower_bound and upper_bound for outliers
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                # Randomly select n rows from the DataFrame
                selected_rows = df.sample(n=a, replace=True)

                # Generate n random outliers below the lower bound and above the upper bound
                lower_outliers = np.random.uniform(lower_bound - 1.5 * IQR, lower_bound, a // 2)
                upper_outliers = np.random.uniform(upper_bound, upper_bound + 1.5 * IQR, (a- (a // 2)))
                outliers = np.concatenate([lower_outliers, upper_outliers])

                # Add the outliers to the selected rows in the BMI column
                selected_rows[column] = outliers[:a]

                # Update the modified rows in the original DataFrame
                df.update(selected_rows)

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
                # a = new column's name; column = the selected column

                df_with_duplicate_column = df.copy()
                df_with_duplicate_column[a] = df_with_duplicate_column[column]
                return df_with_duplicate_column
            
            case "New":
                # Function to add new column to dataframe.
                # a = new column's name
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
                # a = target (dependent) column); b = number of features to keep

                # Extract the features (X) from the DataFrame
                X = df.drop(columns=[a])  
                #Initialize and fit the PCA model
                pca = PCA(n_components=b)
                X_pca = pca.fit_transform(X)
                # Create a DataFrame with the reduced dimensionality
                columns = [f'PC{i+1}' for i in range(b)]
                df_pca = pd.DataFrame(data=X_pca, columns=columns)
                # Add the target column back to df_pca 
                df_pca[a] = df[a]     
                print(df_pca.head(10))
                return df_pca
            
            case "Algorithmic LDA":                           
                # Function to reduce dataset dimensionality using LDA  
                # a = target (dependent) column); b = number of features to keep

                # Extract the features (X) and target variable (y) from the DataFrame
                X = df.drop(columns=[a])
                y = df[a]

                # Initialize and fit the LDA model
                lda = LinearDiscriminantAnalysis(n_components=b)
                X_lda = lda.fit_transform(X, y)

                # Create a DataFrame with the reduced dimensionality
                columns = [f'LD{i + 1}' for i in range(b)]
                df_lda = pd.DataFrame(data=X_lda, columns=columns)
                
                df_lda[a] = y # Add the target column back to df_lda if needed
                return df_lda
            
            case "Algorithmic SVD":
                # Function to reduce dataset dimensionality using SVD
                # a: selected column; b: numbers of column to keep                
                # b > 1 and b <= df.shape[1]-1:           

                # Extract the features (X) from the DataFrame
                X = df.drop(columns=[a])

                # Initialize and fit the TruncatedSVD model
                svd = TruncatedSVD(n_components=b)
                X_svd = svd.fit_transform(X)

                # Create a DataFrame with the reduced dimensionality
                columns = [f'SVD{i+1}' for i in range(b)]
                df_svd = pd.DataFrame(data=X_svd, columns=columns)

                # Add the target column back to df_svd if needed
                df_svd[a] = df[a]                       
                return df_svd
            
            case "Algorithmic Sklearn":
                # Function to reduce dataset dimensionality using SKlearn Feature Selection
                # a = target (dependent) column; b = number of columns(features) to retain

                X = df.drop(column, axis=1)
                y = df[column]

                # Standardize the features (important for feature selection)
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)                    

                # Create a SelectKBest model using ANOVA F-statistic (can change this metric)
                select_best = SelectKBest(score_func=f_classif, k=b)

                # Fit the SelectKBest model to your standardised data
                X_selected = select_best.fit_transform(X_scaled, y)

                # Get the indices of the selected features
                selected_feature_indices = select_best.get_support(indices=True)

                # Create a DataFrame with the reduced-dimensionality data
                reduced_data = pd.DataFrame(data=X_selected, columns=[X.columns[i] for i in selected_feature_indices])

                # Add the target variable back to the generated dataset
                reduced_data[column] = y
                return reduced_data

            case "Manual":
                # Funtion to remove the selected column
                df = df.drop(column)
                return df

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
            case "Algorithmic Numerical":
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
            case "Manual Numerical":  
                # Insert function here!!!
                pass
            case "Algorithmic Categorial":
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
            case "Manual Categorical":
                # Insert function here!!!
                pass

    def change_column_name(self, sub_action, df, column, args, sme):   
        a, b, c = args["a"], args["b"], args["c"]  #unpack args

        # Function to rename selected column
        df.rename(columns={column: a}, inplace=True)

        return df

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

    def data_transformation(self, sub_action, df, column, args, sme): 
        a, b, c = args["a"], args["b"], args["c"]  #unpack args

        match sub_action:
            case "Feature Scaling Min/Max Scaler":
                pass
            case "Feature Scaling Z-score":
                pass
            case "Feature Encoding One-hot Encoding":
                pass
            case "Feature Encoding Label Encoding":
                pass
            case "Feature Encoding Embedding":
                pass