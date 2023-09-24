import pytest
import pandas as pd
import sys
import os

for path in sys.path:
    print(path)

from ...models.dataframe import DataFrameModel

@pytest.fixture
def empty_dataframe_model():
    return DataFrameModel()

def test_new_dataframe(empty_dataframe_model):
    empty_dataframe_model.new_dataframe('file_path', 'dataset_name')
    assert len(empty_dataframe_model._snapshots) == 1

if __name__ == '__main__':
    pytest.main()