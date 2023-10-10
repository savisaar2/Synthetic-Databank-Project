import pandas as pd
import random
import numpy as np
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.preprocessing import StandardScaler
from sklearn.impute import KNNImputer
from sklearn.ensemble import RandomForestRegressor
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import category_encoders as ce

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
                 "Reduce Remove Rows": self.remove_rows,
                 "Reduce Columns (Dimensionality)": self.reduce_columns,
                 "Replace Missing Values": self.replace_null_values,
                 "Replace Value (x) with New Value": self.replace_x_with_new_value,
                 "Change Column Name": self.change_column_name,
                 "Expand (add rows)": self.add_rows,
                 "Data Transformation": self.data_transformation,
            }
    
    def generate_churner(self, scheduler_row):
        # Set dataframe as current, but not for the first item. 
        for index, r in enumerate(scheduler_row):
            if not index:
                self.current_df = self.manip_collection[r["action"]](r["sub_action"], r["df"], r["column"], 
                                                   r["args"], r["sme"])
                match self.current_df:
                    case False:
                        r["outcome"] = "Failed"
                    case _:
                        r["outcome"] = "Success"          
            else:
                match self.current_df:
                    case False:
                        r["outcome"] = "Pending"
                    case _:
                        r["df"] = self.current_df
                        self.current_df  = self.manip_collection[r["action"]](r["sub_action"], 
                                                                r["df"], r["column"], r["args"], r["sme"])
                        match self.current_df:
                            case False:
                                r["outcome"] = "Failed"
                            case _:
                                r["outcome"] = "Success"
  
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
                outlier_indices = np.where(z_scores > a)[0]
                # Ensure the target column has a floating-point dtype
                df[column] = df[column].astype(float)
                # Introduce outliers using .loc to set values
                outlier_values = np.random.uniform(5, 10, len(outlier_indices)).astype(float) 
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
                # column = the target column; a = number of features to keep
                # Extract the features (X) from the DataFrame
                X = df.drop(columns=[column])  
                #Initialize and fit the PCA model
                pca = PCA(n_components=a)
                X_pca = pca.fit_transform(X)
                # Create a DataFrame with the reduced dimensionality
                columns = [f'PC{i+1}' for i in range(a)]
                df_pca = pd.DataFrame(data=X_pca, columns=columns)
                # Add the target column back to df_pca 
                df_pca[column] = df[column]     
                
                return df_pca
            
            case "Algorithmic LDA":                           
                # Function to reduce dataset dimensionality using LDA  
                # column =target (dependent) column; a = number of features (columns) to keep

                # Extract the features (X) and target variable (y) from the DataFrame
                X = df.drop(columns=[column])
                y = df[column]   
               
                # Initialize and fit the LDA model
                lda = LinearDiscriminantAnalysis(n_components=a)
                X_lda = lda.fit_transform(X, y)

                # Create a DataFrame with the reduced dimensionality
                columns = [f'LD{i + 1}' for i in range(a)]
                df_lda = pd.DataFrame(data=X_lda, columns=columns)
                
                df_lda[column] = y # Add the target column back to df_lda if needed
                return df_lda
            
            case "Algorithmic SVD":
                # Function to reduce dataset dimensionality using SVD
                # column: the selected column; a: numbers of column to keep                
                # a > 1 and a <= df.shape[1]-1:           

                # Extract the features (X) from the DataFrame
                X = df.drop(columns=[column])

                # Initialize and fit the TruncatedSVD model
                svd = TruncatedSVD(n_components=a)
                X_svd = svd.fit_transform(X)

                # Create a DataFrame with the reduced dimensionality
                columns = [f'SVD{i+1}' for i in range(a)]
                df_svd = pd.DataFrame(data=X_svd, columns=columns)

                # Add the target column back to df_svd if needed
                df_svd[column] = df[column]                       
                return df_svd
            
            case "Algorithmic Sklearn":
                # Function to reduce dataset dimensionality using SKlearn Feature Selection
                # column = target (dependent) column; a = number of columns(features) to retain

                X = df.drop(column, axis=1)
                y = df[column]

                # Standardize the features (important for feature selection)
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)                    

                # Create a SelectKBest model using ANOVA F-statistic (can change this metric)
                select_best = SelectKBest(score_func=f_classif, k=a)

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
                        # column = the selected column
                        # Function to replace missing value with Mean
                        # Calculate the mean of the selected column
                        mean_colum = df[column].mean()
                        # Replace missing values in the selected column with the mean
                        df[column].fillna(mean_colum, inplace=True)
                        return df
                    
                    case "Median":
                        # column = the selected column
                        # Function to replace missing value with Median
                        # Calculate the medina  of the selected column
                        median_column = df[column].median()
                        # Replace missing values in 'BMI' with the median
                        df[column].fillna(median_column, inplace=True)
                        return df
                        
            case "Manual Numerical":  
                # column = the selected column; a = new value
                # Function to replace all missing value in the selected column with fixed value
                # Replace all missing values with a fixed value 
                df[column].fillna(a, inplace=True)                        
                return df
            
            case "Algorithmic Categorial":
                match a:
                    case "Mode":
                        # column = the selected colum
                        # Function to replace all  missing values in the selected column woth MODE
                        # Calculate the mode of the 'Age' column
                        mode_val = df[column].mode().values[0]
                        # Perform fillna with mode
                        df[column].fillna(mode_val, inplace=True)
                        return df
                    
            case "Manual Categorical":
                # column = the selected column; a = new value
                # Function to replace all missing value in the selected column with fixed value
                # Replace all missing 'BMI' values with a fixed value of 180
                df[column].fillna(a, inplace=True)                        
                return df
            
            case "Algorithmic Categorial" | "Algorithmic Numerical":
                match a:
                    case "KNN":
                        # column = the selected column; b = the desired number of neighbours (int)
                        # Function to replace missing value using K-Nearest Neighbors (KNN) Imputation
                        # Initialize the KNNImputer with the desired number of neighbors (e.g. 5)
                        knn_imputer = KNNImputer(n_neighbors=b)
                        # Perform KNN imputation on the 'BMI' column
                        df[column] = knn_imputer.fit_transform(df[[column]])                        
                        return df                       

                    case "ML":
                        # column = the selected column
                        # Function to replace missing value using Machince Learning-Based Imputation
                        # Separate the dataset into two parts: one with missing  values and one without
                        df_missing = df[df[column].isna()].copy()  # Make a copy to avoid SettingWithCopyWarning
                        df_not_missing = df[~df[column].isna()]

                        # Prepare the features and target for imputation
                        X = df_not_missing.drop(columns=[column])
                        y = df_not_missing[column]
                        # Initialize the Random Forest Regressor 
                        rf_imputer = RandomForestRegressor(n_estimators=100, random_state=42)

                        # Train the model on non-missing data
                        rf_imputer.fit(X, y)

                        # Impute missing values using the trained model
                        imputed_values = rf_imputer.predict(df_missing.drop(columns=[column]))
                        df.loc[df[column].isna(), column] = imputed_values
                        return df

    def replace_x_with_new_value(self, sub_action, df, column, args, sme):   
        a, b, c = args["a"], args["b"], args["c"]  #unpack args

#       # column = the selected column; a = value to replace; b = new value
        # Function to replace x value with new value

        df[column].replace(a, b, inplace=True)
        return df

    def change_column_name(self, sub_action, df, column, args, sme):   
        a, b, c = args["a"], args["b"], args["c"]  #unpack args

        # Function to rename the selected column
        df.rename(columns={column: a}, inplace=True)
        return df

    def add_rows(self, sub_action, df, column, args, sme):   
        a, b, c = args["a"], args["b"], args["c"]  #unpack args
        
        match sub_action:
            case "Random Sampling":
                # a = number of rows to resample & expand                
                # Randomly select rows from the existing dataset
                random_rows = df.sample(n=a, replace=False)
                # Append the randomly selected rows to the existing dataset
                df = pd.concat([df, random_rows], ignore_index=True)
                return df
            
            case "Bootstrap Resampling": 
               # a = number of rows to resample & expand                
                # Randomly select rows from the existing dataset
                bt_rows = df.sample(n=a, replace=True)
                # Append the randomly selected rows to the existing dataset
                df = pd.concat([df, bt_rows], ignore_index=True)
                return df
            
            case "SMOTE":
                # column = the selected column
                # Function to expand rows using SMOTE
                # Split the dataset into features (X) and the target variable (y)
                X = df.drop(column, axis=1)  
                y = df[column] 
                # Initialize the SMOTE resampler
                smote = SMOTE(sampling_strategy='auto', random_state=42)  # You can adjust the sampling_strategy parameter if needed

                # Apply SMOTE to generate synthetic samples
                X_resampled, y_resampled = smote.fit_resample(X, y)

                # Create a new DataFrame with the resampled data
                df_resampled = pd.concat([pd.DataFrame(X_resampled), pd.DataFrame({column: y_resampled})], axis=1)       
                return df_resampled
            

    def data_transformation(self, sub_action, df, column, args, sme): 

        a, b, c = args["a"], args["b"], args["c"]  #unpack args

        match sub_action:
            case "Feature Scaling Min/Max Scaler":
                # column = dependent column
                # Exclude the target column to get the feature columns                             
                
                target_column = column
                # Exclude the target column to get the feature columns
                feature_columns = df.drop(columns=[target_column])

                # Separate the features and target variable
                X = feature_columns
                y = df[target_column]

                # Initialize the MinMaxScaler
                scaler = MinMaxScaler()

                # Fit the scaler to your feature data and transform it
                X_scaled = scaler.fit_transform(X)

                # Convert X_scaled back to a DataFrame with the same column names as the original features
                X_scaled_df = pd.DataFrame(X_scaled, columns=feature_columns.columns)

                # Add the target column back to the scaled feature dataset
                X_scaled_df[target_column] = y

                return X_scaled_df
                
            case "Feature Scaling Z-score":
                # column = the dependent (target) column
                target_column = column

                # Exclude the target column to get the feature columns
                feature_columns = df.drop(columns=[target_column])

                # Separate the features and target variable
                X = feature_columns
                y = df[target_column]

                # Initialize the StandardScaler
                scaler = StandardScaler()

                # Fit the scaler to your feature data and transform it
                X_scaled = scaler.fit_transform(X)

                # Convert X_scaled back to a DataFrame with the same column names as the original features
                X_scaled_df = pd.DataFrame(X_scaled, columns=feature_columns.columns)

                # Add the target column back to the scaled feature dataset
                X_scaled_df[target_column] = y
                return X_scaled_df
            
            case "Feature Encoding One-hot Encoding":
                # column = the selected column; a = dependent (target) column
                # Exclude the target column to get the feature columns                
                feature_columns = df.drop(columns=[a])
                # Separate the features and target variable
                X = feature_columns
                y = df[a]
                # Perform one-hot encoding on the categorical columns
                X_encoded = pd.get_dummies(X, columns=[column], drop_first=True)         
                # Add the target column back to the encoded feature dataset
                X_encoded[a] = y
                # Now, X_encoded contains the one-hot encoded feature data with the target column
                return df
            
            case "Feature Encoding Label Encoding":
                # column = the selected column; a = dependent (target) column         
                # Identify categorical columns (replace this list with your actual categorical columns)
                categorical_column = [column]              
                # Separate the features and target variable
                X = df.drop(columns=[a])
                y = df[column]

                # Use LabelEncoder for categorical columns without a loop
                label_encoder = LabelEncoder()
                X[column] = X[column].apply(label_encoder.fit_transform)
                # Now, X contains label encoded feature data with the target column
                # Add the target column back to the encoded feature dataset
                X[a] = y
                return X
            
            case "Feature Encoding Target Encoding":
                # column = the selected column; a = dependent (target) column         
                # Encode the categorical column using target encoding
                encoding_map = df.groupby(column)[a].mean()
                df[column + '_encoded'] = df[column].map(lambda x: encoding_map.get(x, encoding_map.mean()))
                return df