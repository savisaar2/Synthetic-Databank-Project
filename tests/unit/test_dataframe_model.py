import pytest
import pandas as pd
import sys
sys.path.append('../../')
from models.dataframe import DataFrameModel

@pytest.fixture
def empty_dataframe_model():
    return DataFrameModel()

# Test cases for DataFrameModel
def test_new_dataframe(empty_dataframe_model):
    empty_dataframe_model.new_dataframe('file_path', 'dataset_name')
    assert len(empty_dataframe_model._snapshots) == 1