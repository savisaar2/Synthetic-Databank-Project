import pytest
import pandas as pd
from models.dataset import DatasetModel

@pytest.fixture
def empty_dataframe_model():
    return DatasetModel()

# Test to check singleton pattern for dataframe model object.
def test_singleton(empty_dataframe_model):
    assert isinstance(empty_dataframe_model, DatasetModel)

# Test to create an empty dataset.
def test_new_dataset(empty_dataframe_model):
    # Ensure that the _SNAPSHOTS list is empty initially
    assert len(empty_dataframe_model._SNAPSHOTS) == 0

    # Call the new_dataset method
    empty_dataframe_model.new_dataset()

    # Check that the _SNAPSHOTS list has one entry after calling new_dataset
    assert len(empty_dataframe_model._SNAPSHOTS) == 1

    # Check that the Name of the new dataset is "New Dataset"
    assert empty_dataframe_model._SNAPSHOTS[-1]["Name"] == "New Dataset"

    # Check that Description is an empty string
    assert empty_dataframe_model._SNAPSHOTS[-1]["Description"] == ""

    # Check that Schedule Set is an empty dictionary
    assert empty_dataframe_model._SNAPSHOTS[-1]["Schedule Set"] == {}

    # Check that Dataframe is an empty pandas DataFrame
    assert isinstance(empty_dataframe_model._SNAPSHOTS[-1]["Dataframe"], pd.DataFrame)

# Test to load data from a sample CSV file.
def test_load_dataset(empty_dataframe_model):
    # Define our dataset to use.
    dataset_name = "test_dataset"
    file_path = 'db/databank/breast-cancer.csv'

    # Load data set for testing.
    empty_dataframe_model.load_dataset(file_path, dataset_name)

    # Check we have a new snapshot and dataset name can be retrieved.
    assert len(empty_dataframe_model._SNAPSHOTS) == 1
    assert empty_dataframe_model.get_dataset_name() == dataset_name

# Test method to get column headers of current dataset.
def test_get_column_headers(empty_dataframe_model):
    dataset_name = "test_dataset"
    file_path = 'db/databank/breast-cancer.csv'
    empty_dataframe_model.load_dataset(file_path, dataset_name)
    headers = empty_dataframe_model.get_column_headers()
    assert isinstance(headers, list)
    assert headers[0] == "Class"
    assert len(headers) == 10

# Test method to get data of a defined column.
def test_get_column_data(empty_dataframe_model):
    dataset_name = "test_dataset"
    file_path = 'db/databank/breast-cancer.csv'
    empty_dataframe_model.load_dataset(file_path, dataset_name)
    column_data = empty_dataframe_model.get_column_data("Class")
    assert isinstance(column_data, pd.Series)

# Test method to obtain a column's datatype.
def test_get_column_datatype(empty_dataframe_model):
    dataset_name = "breast-cancer"
    file_path = 'db/databank/breast-cancer.csv'
    empty_dataframe_model.load_dataset(file_path, dataset_name)
    data_type = empty_dataframe_model.get_column_datatype("Class")
    assert data_type == 'object'
    assert data_type != 'int64'

# Test method rollback functionality.
def test_rollback(empty_dataframe_model):
    dataset_name = "breast-cancer"
    file_path = 'db/databank/breast-cancer.csv'

    empty_dataframe_model.load_dataset(file_path, dataset_name)
    empty_dataframe_model._SNAPSHOTS.append(
            {
            "Name": "Another Dataset",
            "Description": "",
            "Schedule Set": {},
            "Dataframe": "df"
            }
        )
    
    # Rollback to the first dataset
    empty_dataframe_model.rollback(0)
    
    assert empty_dataframe_model.get_dataset_name() == dataset_name

# Test method for get rows by range and row count.
def test_get_df_row_by_range(empty_dataframe_model):
    dataset_name = "breast-cancer"
    file_path = 'db/databank/breast-cancer.csv'
    empty_dataframe_model.load_dataset(file_path, dataset_name)
    rows = empty_dataframe_model.get_df_row_by_range(1, 2)
    assert isinstance(rows, pd.DataFrame)
    assert len(rows.index) == 2

# Test method to obtain row count of the current dataset.
def test_get_df_row_count(empty_dataframe_model):
    dataset_name = "breast-cancer"
    file_path = 'db/databank/breast-cancer.csv'
    empty_dataframe_model.load_dataset(file_path, dataset_name)
    row_count = empty_dataframe_model.get_df_row_count()
    assert isinstance(row_count, int)
    assert row_count == 286

# Test method to clear all datasets in dataframe model.
def test_clear_all_snapshots(empty_dataframe_model):
    dataset_name = "breast-cancer"
    file_path = 'db/databank/breast-cancer.csv'
    empty_dataframe_model.load_dataset(file_path, dataset_name)
    
    assert len(empty_dataframe_model._SNAPSHOTS) == 1
    
    empty_dataframe_model.clear_all_snapshots()
    
    assert len(empty_dataframe_model._SNAPSHOTS) == 0

if __name__ == '__main__':
    pytest.main()
