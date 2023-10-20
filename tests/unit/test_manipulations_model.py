import pytest
import pandas as pd
from models.manipulations import ManipulationsModel as manip
from os import path

@pytest.fixture
def diabetes_dataset():
    df = pd.read_csv("db/databank/diabetes.csv")
    column = "Pregnancies"
    return df, column

@pytest.fixture
def manip_obj():
    return manip()

@pytest.mark.parametrize("sub_action, a, expected_columns", [
    ("Algorithmic PCA", 3, 4),
    ("Algorithmic LDA", 2, 3),
    ("Algorithmic SVD", 4, 5),
    ("Algorithmic Sklearn", 3, 4),   
])
def test_reduce_columns(sub_action, a, expected_columns, diabetes_dataset, manip_obj):
    df, column = diabetes_dataset
    args = {"a": a, "b": "", "c": ""}

    reduced_df = manip_obj.reduce_columns(sub_action, df, column, args)

    assert reduced_df.shape[1] == expected_columns

# Test - add new column function
def test_add_new_column(diabetes_dataset, manip_obj):
    #   def add_column(self, sub_action, df, column, args):
    df, column = diabetes_dataset # Unpack df and column name 
    args = {"a": "New Column", "b": "", "c": ""} # Manually specify args for each test

    # Create a test df by calling the function and passing the args.
    test_df_1 = manip_obj.add_column("New", df, column, args)
    
    # Apply Boolean assert statements to check the validity of df.
    assert len(test_df_1.columns) == 10

# Test - reduce column manual function
def test_reduce_column_manual(diabetes_dataset, manip_obj):
    df, column = diabetes_dataset # Unpack df and column name 
    args = {"a": "", "b": "", "c": ""} # Manually specify args for each test

    # Create a test df by calling the function and passing the args.
    test_df_1 = manip_obj.reduce_columns("Manual", df, column, args)

    # Apply Boolean assert statements to check the validity of df.
    assert len(test_df_1.columns) == 8

# Test - add noise - add random customer valuefunction
def test_add_noise_random(diabetes_dataset, manip_obj):
    df, column = diabetes_dataset  # Unpack df and column name
    args = {"a": 1000, "b": 2, "c": ""}  # Manually specify args for each test

    # Create a test data frame for "Add Random Custome Value"
    test_df = manip_obj.add_noise("Add Random Custom Value", df, column, args)
    
    # Verify that the "Pregancies" column has the custom value (1000)
    assert (test_df[column] == 1000).any()

# Test - add noise - add random customer valuefunction

# Test - add noise function for "Add Missing"
def test_add_noise_missing(diabetes_dataset, manip_obj):
    df, column = diabetes_dataset
    args = {"a": 300, "b": "", "c": ""}  # Manually specify args for each test

    # Create a test DataFrame by calling the function and passing the args.
    test_df = manip_obj.add_noise("Add Missing", df, column, args)

    # Verify that exactly 300 rows in the column have missing values
    num_missing_rows_after = pd.isnull(test_df[column]).sum()
    assert num_missing_rows_after == args["a"]

def test_add_missing_value_to_entire_dataset(diabetes_dataset, manip_obj):
    # Unpack the dataset and column from the fixture
    df, column = diabetes_dataset

    # Define the sub-action, column (None for entire dataset), and args
    sub_action = "Add Missing"    
    args = {"a": 33, "b": "", "c": ""}  # Manually specify args for each test

    # Call the add_noise method from the ManipulationsModel
    result = manip_obj.add_noise(sub_action, df, column, args)

    # Perform assertions
    assert isinstance(result, pd.DataFrame)
    assert result.isna().sum().sum() == 33  # Ensure that 10 missing values were added to the entire dataset

# Test - add noise function for "Add Outliers Z-score"
def test_add_noise_outliers_z_score(diabetes_dataset, manip_obj):
    df, column = diabetes_dataset
    args = {"a": 2, "b": "", "c": ""}  # Manually specify args for each test

    # Create a test DataFrame by calling the function and passing the args.
    test_df = manip_obj.add_noise("Add Outliers Z-score", df, column, args)

    # Verify that the DataFrame contains outliers based on z-scores
    z_scores = abs((test_df[column] - test_df[column].mean()) / test_df[column].std())
    assert (z_scores > args["a"]).any()

# Test - add noise function for "Add Outliers Percentile"
def test_add_noise_outliers_percentile(diabetes_dataset, manip_obj):
    df, column = diabetes_dataset
    args = {"a": 2, "b": "", "c": ""}  # Manually specify args for each test

    # Create a test DataFrame by calling the function and passing the args.
    test_df = manip_obj.add_noise("Add Outliers Percentile", df, column, args)

    # Calculate the IQR (Interquartile Range) for the selected column
    Q1 = test_df[column].quantile(0.25)
    Q3 = test_df[column].quantile(0.75)
    IQR = Q3 - Q1

    # Calculate lower_bound and upper_bound for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Verify that the DataFrame contains outliers based on the bounds
    assert ((test_df[column] < lower_bound) | (test_df[column] > upper_bound)).any()

# Test - reduce column function for "Algorithmic PCA"
def test_reduce_algorithmic_pca(diabetes_dataset, manip_obj):       
    df, column = diabetes_dataset
    args = {"a": 3, "b": "", "c": ""}
    reduced_df = manip_obj.reduce_columns("Algorithmic PCA", df, column, args)
    assert reduced_df.shape[1] == args["a"] +1

# Test - reduce column function for "Algorithmic SVD"
def test_reduce_algorithmic_svd(diabetes_dataset, manip_obj):
    df, column = diabetes_dataset
    args = {"a": 7, "b": "", "c": ""}
    reduced_df = manip_obj.reduce_columns("Algorithmic SVD", df, column, args)
    assert reduced_df.shape[1] == args["a"] + 1 

# Test - reduce column function for "Algorithmic Sklearn"
def test_reduce_algorithmic_sklearn(diabetes_dataset, manip_obj):
    df, column = diabetes_dataset
    args = {"a": 1, "b": "", "c": ""}
    reduced_df = manip_obj.reduce_columns("Algorithmic Sklearn", df, column, args)
    assert reduced_df.shape[1] == args["a"] + 1
   
# Test the "Missing Values" sub-action
def test_remove_rows_missing_values(diabetes_dataset, manip_obj):
    df, column = diabetes_dataset
    original_shape = df.shape
    sub_action = "Missing Values"

    # Perform the "Missing Values" sub-action
    args = {"a": 0, "b": 0, "c": 0}  # Customize args based on the behavior
    df_result = manip_obj.remove_rows(sub_action, df, column, args=args)

    # Ensure that the resulting DataFrame has fewer or the same number of rows (since we're removing rows)
    assert df_result.shape[0] <= original_shape[0]

    # Ensure that the resulting DataFrame has the same number of columns
    assert df_result.shape[1] == original_shape[1]

# Test the "Duplicate Rows" sub-action
def test_remove_rows_duplicate_rows(diabetes_dataset, manip_obj):
    df, column = diabetes_dataset
    original_shape = df.shape
    sub_action = "Duplicate Rows"

    # Perform the "Duplicate Rows" sub-action
    args = {"a": 0, "b": 0, "c": 0}  # Customize args based on the behavior
    df_result = manip_obj.remove_rows(sub_action, df, column, args=args)

    # Ensure that the resulting DataFrame has fewer or the same number of rows (since we're removing rows)
    assert df_result.shape[0] <= original_shape[0]

    # Ensure that the resulting DataFrame has the same number of columns
    assert df_result.shape[1] == original_shape[1]

# Test the "Algorithmic Numerical" sub-action for replacing null values with median
def test_replace_null_values_algorithmic_numerical_median(diabetes_dataset, manip_obj):
    df, column = diabetes_dataset
    sub_action = "Algorithmic Numerical"
    a = "Median"

    args = {"a": a, "b": 0, "c": 0}
    df_result = manip_obj.replace_null_values(sub_action, df, column, args=args)

    assert df_result[column].isna().sum() == 0

# Test the "Algorithmic Numerical" sub-action for replacing null values with KNN imputation
def test_replace_null_values_algorithmic_numerical_knn(diabetes_dataset, manip_obj):
    df, column = diabetes_dataset
    sub_action = "Algorithmic Numerical"
    a = "KNN"

    args = {"a": a, "b": 5, "c": 0}  # Customize the number of neighbors as needed
    df_result = manip_obj.replace_null_values(sub_action, df, column, args=args)

    assert df_result[column].isna().sum() == 0

# Test the "Algorithmic Numerical" sub-action for replacing null values with Random Forest imputation
def test_replace_null_values_algorithmic_numerical_random_forest(diabetes_dataset, manip_obj):
    df, column = diabetes_dataset
    sub_action = "Algorithmic Numerical"
    a = "Random Forest"

    args = {"a": a, "b": 0, "c": 0}
    df_result = manip_obj.replace_null_values(sub_action, df, column, args=args)

    assert df_result[column].isna().sum() == 0

# Test the "Manual Numerical" sub-action for replacing null values with a fixed value
def test_replace_null_values_manual_numerical(diabetes_dataset, manip_obj):
    df, column = diabetes_dataset
    sub_action = "Manual Numerical"
    a = 0  # Customize the replacement value

    args = {"a": a, "b": 0, "c": 0}
    df_result = manip_obj.replace_null_values(sub_action, df, column, args=args)

    assert df_result[column].isna().sum() == 0

# Test the "Algorithmic Categorical" sub-action for replacing null values with mode
def test_replace_null_values_algorithmic_categorical_mode(diabetes_dataset, manip_obj):
    df, column = diabetes_dataset
    sub_action = "Algorithmic Categorical"
    a = "Mode"

    args = {"a": a, "b": 0, "c": 0}
    df_result = manip_obj.replace_null_values(sub_action, df, column, args=args)

    assert df_result[column].isna().sum() == 0

# Test the "Manual Categorical" sub-action for replacing null values with a fixed value
def test_replace_null_values_manual_categorical(diabetes_dataset, manip_obj):
    df, column = diabetes_dataset
    sub_action = "Manual Categorical"
    a = "Custom Value"  # Customize the replacement value

    args = {"a": a, "b": 0, "c": 0}
    df_result = manip_obj.replace_null_values(sub_action, df, column, args=args)

    assert df_result[column].isna().sum() == 0

@pytest.mark.parametrize("a, b, input_values, expected_values", [
    (3, 10, [1, 2, 3, 4, 5], [1, 2, 10, 4, 5]),  # Replace 3 with 10
    ("A", "X", ["A", "B", "A", "C"], ["X", "B", "X", "C"]),  # Replace "A" with "X"
])
def test_replace_x_with_new_value(a, b, input_values, expected_values, manip_obj):
    # Create a test DataFrame
    df = pd.DataFrame({"ColumnToReplace": input_values})

    # Call the replace_x_with_new_value function
    result_df = manip_obj.replace_x_with_new_value("Replace X with New Value", df, "ColumnToReplace", {"a": a, "b": b, "c": None})

    # Check if the column values match the expected values
    assert result_df["ColumnToReplace"].tolist() == expected_values

# Test the change_column_name function
def test_change_column_name(diabetes_dataset, manip_obj):
    df, column = diabetes_dataset  # Unpack the DataFrame and column from the fixture

    # Define the sub-action and args
    sub_action = "Change Column Name"
    new_column = "New_Column"  # Specify a new column name

    # Call the change_column_name method from the ManipulationsModel
    result_df = manip_obj.change_column_name(sub_action, df.copy(), column, {"a": new_column, "b": "", "c": ""})

    # Verify that the column name has been changed
    assert new_column in result_df.columns
    assert column not in result_df.columns

# Test the "Random Sampling" sub-action in add_rows
@pytest.mark.parametrize("num_rows", [5, 10, 15])
def test_add_rows_random_sampling(diabetes_dataset, manip_obj, num_rows):
    df, column = diabetes_dataset
    sub_action = "Random Sampling"
    args = {"a": num_rows, "b": 0, "c": 0}
    
    result_df = manip_obj.add_rows(sub_action, df.copy(), column, args)
    
    # Verify that the number of rows in the result_df has increased by num_rows
    assert len(result_df) == len(df) + num_rows

# Test the "Bootstrap Resampling" sub-action in add_rows
@pytest.mark.parametrize("num_rows", [5, 10, 15])
def test_add_rows_bootstrap_resampling(diabetes_dataset, manip_obj, num_rows):
    df, column = diabetes_dataset
    sub_action = "Bootstrap Resampling"
    args = {"a": num_rows, "b": 0, "c": 0}
    
    result_df = manip_obj.add_rows(sub_action, df.copy(), column, args)
    
    # Verify that the number of rows in the result_df has increased by num_rows
    assert len(result_df) == len(df) + num_rows
