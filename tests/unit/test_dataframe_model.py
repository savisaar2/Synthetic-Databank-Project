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
    empty_dataframe_model.load_dataframe('file_path', 'dataset_name')
    assert len(empty_dataframe_model._snapshots) == 1

# Test to get column headers of current dataset.
def test_get_column_headers(empty_dataframe_model):
    empty_dataframe_model.new_dataframe('file_path', 'dataset_name')
    headers = empty_dataframe_model.get_column_headers()
    assert isinstance(headers, list)

if __name__ == '__main__':
    pytest.main()