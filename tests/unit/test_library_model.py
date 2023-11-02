import json
import os
import pytest
from models.library import LibraryModel
from models.dataset import DatasetModel

class TestLibraryModel:
    @pytest.fixture
    def library_model(self):
        return LibraryModel()

    def test_convert_to_megabytes(self, library_model):
        assert library_model.convert_to_megabytes(0) == "0 bytes"
        assert library_model.convert_to_megabytes(1024) == "1.00 KB"
        assert library_model.convert_to_megabytes(1048576) == "1.00 MB"
        assert library_model.convert_to_megabytes(1073741824) == "1.00 GB"

    def test_sort_datasets_alphabetically(self, library_model):
        input_data = {
            "dataset1": {},
            "dataset3": {},
            "dataset2": {},
        }
        sorted_data = library_model.sort_datasets_alphabetically(input_data)
        expected_result = ["dataset1", "dataset2", "dataset3"]
        assert sorted_data == expected_result

    def test_load_all_metadata(self, library_model):
        metadata = library_model.load_all_metadata()
        assert isinstance(metadata, dict)

    def test_search_metadata(self, library_model):
        # Mock metadata dataset for testing
        mock_metadata = {
            "breast-cancer": {"Source": "Source1", "Description": "Breast Cancer dataset"},
            "diabetes": {"Source": "Source2", "Description": "Diabetes dataset"},
            "heart-disease": {"Source": "Source3", "Description": "Heart Disease dataset"}
        }
        
        # Assign the mock metadata dataset to the model's _metadata attribute
        library_model._metadata = mock_metadata
        
        # Define search keywords
        keywords = "breast cancer"
        
        # Call the search_metadata method
        matching_datasets = library_model.search_metadata(keywords)
        
        # Assert the result based on the mock dataset
        assert isinstance(matching_datasets, list)
        assert len(matching_datasets) == 1  # Only "breast-cancer" matches
        assert "breast-cancer" in matching_datasets

    def test_get_datasets_all(self, library_model):
        datasets = library_model.get_datasets("all")
        # Assuming you have some dataset files, you can assert the result based on your dataset files
        assert isinstance(datasets, list)

    def test_get_datasets_specific(self, library_model):
        # Mock dataset of datasets and their file sizes
        mock_datasets = {
            "bcdata": "121.71 KB",
            "breast-cancer": "18.46 KB"
        }

        # Assign the mock dataset to the model's _metadata attribute
        library_model._metadata = mock_datasets

        # Define the dataset names for the specific search
        specific_datasets = ["bcdata", "breast-cancer"]

        # Call the get_datasets method with "specific" mode and the specific dataset names
        datasets = library_model.get_datasets("specific", specific_datasets)

        # Assert that the result matches the expected mock dataset
        assert isinstance(datasets, list)
        assert len(datasets) == len(specific_datasets)

        # Check that each specific dataset is in the result and the file sizes match
        for dataset_name in specific_datasets:
            assert (dataset_name, mock_datasets[dataset_name]) in datasets

    def test_get_file_metadata(self, library_model):
        # Mock metadata for datasets
        mock_metadata = {
            "bcdata": {
                "Source": "Breast Cancer Wisconsin (Diagnostic)",
                "Description": "Features are computed from a digitized image of a fine" +
                "needle aspirate (FNA) of a breast mass. They describe characteristics of the cell nuclei present in the image.\n\nCategory:" + 
                "Health\n\nKey Words: breast cancer"
            }
        }

        # Assign the mock metadata to the model's _metadata attribute
        library_model._metadata = mock_metadata

        # Define the dataset name for which you want to get metadata
        dataset_name = "bcdata"

        # Call the get_file_metadata method with the dataset name
        metadata = library_model.get_file_metadata(dataset_name)

        # Assert that the result matches the expected metadata for dataset2
        expected_metadata = mock_metadata[dataset_name]
        assert metadata == expected_metadata

    def test_add_metadata(self, library_model):
        test_metadata = {
            "test_dataset": {
                "Source": "Test Source",
                "Description": "Test Description"
            }
        }
        library_model.add_metadata(test_metadata)
        loaded_metadata = library_model.load_all_metadata()
        # Assuming you added the test metadata, you can assert the result based on your test data
        assert "test_dataset" in loaded_metadata
