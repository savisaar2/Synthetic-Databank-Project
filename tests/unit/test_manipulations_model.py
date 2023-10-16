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
    return manip

# Test - add new column function
def test_add_new_column(diabetes_dataset, manip_obj):
    df, column = diabetes_dataset # Unpack df and column name 
    args = {"a": "New Column", "b": "", "c": ""} # Manually specify args for each test

    # Create a test df by calling the function and passing the args.
    test_df_1 = manip_obj.add_column(manip_obj ,"New", df, column, args)
    
    # Apply Boolean assert statements to check validity of df.
    assert len(test_df_1.columns) == 10

# Test - reduce column manual function
def test_reduce_column_manual(diabetes_dataset, manip_obj):
    df, column = diabetes_dataset # Unpack df and column name 
    args = {"a": "", "b": "", "c": ""} # Manually specify args for each test

    # Create a test df by calling the function and passing the args.
    test_df_1 = manip_obj.reduce_columns(manip_obj,"Manual", df, column, args)

    # Apply Boolean assert statements to check validity of df.
    assert len(test_df_1.columns) == 8