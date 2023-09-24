import pytest
import pandas as pd
from models.dataframe import DataFrameModel

@pytest.fixture
def empty_dataframe_model():
    return DataFrameModel()

@pytest.fixture
def empty_dataframe_model_dup():
    return DataFrameModel()

# Test to check singleton pattern for dataframe model object.
def test_singleton(empty_dataframe_model, empty_dataframe_model_dup):
    assert empty_dataframe_model == empty_dataframe_model_dup

# Test to create an empty dataframe.
def test_new_dataframe(empty_dataframe_model):
    empty_dataframe_model.new_dataframe('file_path', 'dataset_name')
    assert len(empty_dataframe_model._snapshots) == 1

# Test to load data from datastore csv file.
def test_load_dataframe(empty_dataframe_model):
    empty_dataframe_model.load_dataframe('db/databank/breast-cancer.csv', 'test_dataset')
    assert len(empty_dataframe_model._snapshots) == 1
    assert empty_dataframe_model._snapshots[0]["df_file_path"] == 'db/databank/breast-cancer.csv'
    assert empty_dataframe_model._snapshots[0]["df_name"] == 'test_dataset'

# Test method to get column headers of current dataset.
def test_get_column_headers(empty_dataframe_model):
    empty_dataframe_model.load_dataframe('db/databank/breast-cancer.csv', 'test_dataset')
    headers = empty_dataframe_model.get_column_headers()
    assert isinstance(headers, list)
    assert headers[0] == "Class"
    assert len(headers) == 10

# Test method to get data of a defined column.
def test_get_column_data(empty_dataframe_model):
    empty_dataframe_model.load_dataframe('db/databank/breast-cancer.csv', 'test_dataset')
    column_data = empty_dataframe_model.get_column_data(0)
    assert isinstance(column_data, pd.Series)

# Test method to obtain a columns datatype.
def test_get_column_datatype(empty_dataframe_model):
    empty_dataframe_model.load_dataframe('db/databank/breast-cancer.csv', 'test_dataset')
    data_type = empty_dataframe_model.get_column_datatype(0)
    assert data_type == 'object'
    assert data_type != 'int64'

# Test method rollback fuctionality.
def test_rollback(empty_dataframe_model):
    empty_dataframe_model.load_dataframe('db/databank/breast-cancer.csv', 'breast-cancer')
    empty_dataframe_model.load_dataframe('db/databank/diabetes.csv', 'diabetes')
    empty_dataframe_model.rollback(1)
    assert empty_dataframe_model._snapshots[0]['df_name'] == 'breast-cancer'
    assert empty_dataframe_model._snapshots[1]['df_name'] == 'diabetes'

# Test method for get rows by range and row count.
def test_get_df_row_by_range(empty_dataframe_model):
    empty_dataframe_model.load_dataframe('db/databank/breast-cancer.csv', 'breast-cancer')
    rows = empty_dataframe_model.get_df_row_by_range(0, 2)
    assert isinstance(rows, pd.DataFrame)
    assert len(rows.index) == 2

# Test method to obtain row count of current dataset.
def test_get_df_row_count(empty_dataframe_model):
    empty_dataframe_model.load_dataframe('db/databank/breast-cancer.csv', 'breast-cancer')
    row_count = empty_dataframe_model.get_df_row_count()
    assert isinstance(row_count, int)
    assert row_count == 286

# Test method to clear all datasets in dataframe model.
def test_clear_all_snapshots(empty_dataframe_model):
    empty_dataframe_model.load_dataframe('db/databank/breast-cancer.csv', 'breast-cancer')
    assert len(empty_dataframe_model._snapshots) == 1
    empty_dataframe_model._clear_all_snapshots()
    assert len(empty_dataframe_model._snapshots) == 0

if __name__ == '__main__':
    pytest.main()