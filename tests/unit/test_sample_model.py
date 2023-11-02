import pandas as pd
import pytest
from models.sample import SampleModel  # Import your SampleModel class

class TestSampleModel:
    @pytest.fixture
    def sample_model(self):
        return SampleModel()

    def test_get_algorithm_info(self, sample_model):
        selection = "Simple Random"
        info = sample_model.get_algorithm_info(selection)
        assert isinstance(info, str)
        assert "Simple Random Sampling" in info

    def test_convert_to_number_valid_input(self, sample_model):
        val = "42"
        custom_error_warning = "Custom error message"
        result = sample_model.convert_to_number(val, custom_error_warning)
        assert result == 42

    def test_convert_to_number_invalid_input(self, sample_model):
        val = "not_a_number"
        custom_error_warning = "Custom error message"
        with pytest.raises(AssertionError):
            sample_model.convert_to_number(val, custom_error_warning)

    def test_simple_random(self, sample_model):
        df = pd.DataFrame({'col1': [1, 2, 3, 4, 5]})
        sample_size = 3
        new_sample = sample_model.simple_random(df, sample_size)
        assert len(new_sample) == sample_size

    def test_stratified(self, sample_model):
        df = pd.DataFrame({'col1': [1, 2, 3, 4, 5], 'col2': ['A', 'B', 'A', 'B', 'A']})
        sample_size = 2
        dependant_col = 'col2'
        new_sample = sample_model.stratified(df, sample_size, dependant_col)
        assert len(new_sample) == sample_size