import pytest
import pandas as pd
from models.manipulations import ManipulationsModel as manip

class TestManipulations:
    @pytest.fixture
    def diabetes_dataset(self):
        df = pd.read_csv("db/databank/diabetes.csv")
        column = "Pregnancies"
        return df, column

    @pytest.fixture
    def manip_obj(self):
        return manip()

    @pytest.mark.parametrize("sub_action, a, expected_columns", [
        ("Algorithmic PCA", 3, 4),
        ("Algorithmic LDA", 2, 3),
        ("Algorithmic SVD", 4, 5),
        ("Algorithmic Sklearn", 3, 4),
    ])
    def test_reduce_columns(self, sub_action, a, expected_columns, diabetes_dataset, manip_obj):
        df, column = diabetes_dataset
        args = {"a": a, "b": "", "c": ""}

        reduced_df = manip_obj.reduce_columns(sub_action, df, column, args)

        assert reduced_df.shape[1] == expected_columns

    def test_add_new_column(self, diabetes_dataset, manip_obj):
        df, column = diabetes_dataset
        args = {"a": "New Column", "b": "", "c": ""}

        test_df_1 = manip_obj.add_column("New", df, column, args)

        assert len(test_df_1.columns) == 10

    def test_reduce_column_manual(self, diabetes_dataset, manip_obj):
        df, column = diabetes_dataset
        args = {"a": "", "b": "", "c": ""}

        test_df_1 = manip_obj.reduce_columns("Manual", df, column, args)

        assert len(test_df_1.columns) == 8

    def test_add_noise_random(self, diabetes_dataset, manip_obj):
        df, column = diabetes_dataset
        args = {"a": 1000, "b": 2, "c": ""}

        test_df = manip_obj.add_noise("Add Random Custom Value", df, column, args)

        assert (test_df[column] == 1000).any()

    def test_add_noise_missing(self, diabetes_dataset, manip_obj):
        df, column = diabetes_dataset
        args = {"a": 300, "b": "", "c": ""}

        test_df = manip_obj.add_noise("Add Missing", df, column, args)

        num_missing_rows_after = pd.isnull(test_df[column]).sum()
        assert num_missing_rows_after == args["a"]

    def test_add_missing_value_to_entire_dataset(self, diabetes_dataset, manip_obj):
        df, column = diabetes_dataset
        sub_action = "Add Missing"
        args = {"a": 33, "b": "", "c": ""}

        result = manip_obj.add_noise(sub_action, df, column, args)

        assert isinstance(result, pd.DataFrame)
        assert result.isna().sum().sum() == 33

    def test_add_noise_outliers_z_score(self, diabetes_dataset, manip_obj):
        df, column = diabetes_dataset
        args = {"a": 2, "b": "", "c": ""}

        test_df = manip_obj.add_noise("Add Outliers Z-score", df, column, args)

        z_scores = abs((test_df[column] - test_df[column].mean()) / test_df[column].std())
        assert (z_scores > args["a"]).any()

    def test_add_noise_outliers_percentile(self, diabetes_dataset, manip_obj):
        df, column = diabetes_dataset
        args = {"a": 2, "b": "", "c": ""}

        test_df = manip_obj.add_noise("Add Outliers Percentile", df, column, args)

        Q1 = test_df[column].quantile(0.25)
        Q3 = test_df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        assert ((test_df[column] < lower_bound) | (test_df[column] > upper_bound)).any()

    def test_reduce_algorithmic_pca(self, diabetes_dataset, manip_obj):
        df, column = diabetes_dataset
        args = {"a": 3, "b": "", "c": ""}
        reduced_df = manip_obj.reduce_columns("Algorithmic PCA", df, column, args)
        assert reduced_df.shape[1] == args["a"] + 1

    def test_reduce_algorithmic_svd(self, diabetes_dataset, manip_obj):
        df, column = diabetes_dataset
        args = {"a": 7, "b": "", "c": ""}
        reduced_df = manip_obj.reduce_columns("Algorithmic SVD", df, column, args)
        assert reduced_df.shape[1] == args["a"] + 1

    def test_reduce_algorithmic_sklearn(self, diabetes_dataset, manip_obj):
        df, column = diabetes_dataset
        args = {"a": 1, "b": "", "c": ""}
        reduced_df = manip_obj.reduce_columns("Algorithmic Sklearn", df, column, args)
        assert reduced_df.shape[1] == args["a"] + 1

    def test_remove_rows_missing_values(self, diabetes_dataset, manip_obj):
        df, column = diabetes_dataset
        original_shape = df.shape
        sub_action = "Missing Values"
        args = {"a": 0, "b": 0, "c": 0}
        df_result = manip_obj.remove_rows(sub_action, df, column, args=args)
        assert df_result.shape[0] <= original_shape[0]
        assert df_result.shape[1] == original_shape[1]

    def test_remove_rows_duplicate_rows(self, diabetes_dataset, manip_obj):
        df, column = diabetes_dataset
        original_shape = df.shape
        sub_action = "Duplicate Rows"
        args = {"a": 0, "b": 0, "c": 0}
        df_result = manip_obj.remove_rows(sub_action, df, column, args=args)
        assert df_result.shape[0] <= original_shape[0]
        assert df_result.shape[1] == original_shape[1]

    def test_replace_null_values_algorithmic_numerical_median(self, diabetes_dataset, manip_obj):
        df, column = diabetes_dataset
        sub_action = "Algorithmic Numerical"
        a = "Median"
        args = {"a": a, "b": 0, "c": 0}
        df_result = manip_obj.replace_null_values(sub_action, df, column, args=args)
        assert df_result[column].isna().sum() == 0

    def test_replace_null_values_algorithmic_numerical_knn(self, diabetes_dataset, manip_obj):
        df, column = diabetes_dataset
        sub_action = "Algorithmic Numerical"
        a = "KNN"
        args = {"a": a, "b": 5, "c": 0}
        df_result = manip_obj.replace_null_values(sub_action, df, column, args=args)
        assert df_result[column].isna().sum() == 0

    def test_replace_null_values_algorithmic_numerical_random_forest(self, diabetes_dataset, manip_obj):
        df, column = diabetes_dataset
        sub_action = "Algorithmic Numerical"
        a = "Random Forest"
        args = {"a": a, "b": 0, "c": 0}
        df_result = manip_obj.replace_null_values(sub_action, df, column, args=args)
        assert df_result[column].isna().sum() == 0

    def test_replace_null_values_manual_numerical(self, diabetes_dataset, manip_obj):
        df, column = diabetes_dataset
        sub_action = "Manual Numerical"
        a = 0
        args = {"a": a, "b": 0, "c": 0}
        df_result = manip_obj.replace_null_values(sub_action, df, column, args=args)
        assert df_result[column].isna().sum() == 0

    def test_replace_null_values_algorithmic_categorical_mode(self, diabetes_dataset, manip_obj):
        df, column = diabetes_dataset
        sub_action = "Algorithmic Categorical"
        a = "Mode"
        args = {"a": a, "b": 0, "c": 0}
        df_result = manip_obj.replace_null_values(sub_action, df, column, args=args)
        assert df_result[column].isna().sum() == 0

    def test_replace_null_values_manual_categorical(self, diabetes_dataset, manip_obj):
        df, column = diabetes_dataset
        sub_action = "Manual Categorical"
        a = "Custom Value"
        args = {"a": a, "b": 0, "c": 0}
        df_result = manip_obj.replace_null_values(sub_action, df, column, args=args)
        assert df_result[column].isna().sum() == 0

    @pytest.mark.parametrize("a, b, input_values, expected_values", [
        (3, 10, [1, 2, 3, 4, 5], [1, 2, 10, 4, 5]),
        ("A", "X", ["A", "B", "A", "C"], ["X", "B", "X", "C"]),
    ])
    def test_replace_x_with_new_value(self, a, b, input_values, expected_values, manip_obj):
        df = pd.DataFrame({"ColumnToReplace": input_values})
        result_df = manip_obj.replace_x_with_new_value("Replace X with New Value", df, "ColumnToReplace", {"a": a, "b": b, "c": None})
        assert result_df["ColumnToReplace"].tolist() == expected_values

    def test_change_column_name(self, diabetes_dataset, manip_obj):
        df, column = diabetes_dataset
        sub_action = "Change Column Name"
        new_column = "New_Column"
        result_df = manip_obj.change_column_name(sub_action, df.copy(), column, {"a": new_column, "b": "", "c": ""})
        assert new_column in result_df.columns
        assert column not in result_df.columns

    @pytest.mark.parametrize("num_rows", [5, 10, 15])
    def test_add_rows_random_sampling(self, diabetes_dataset, manip_obj, num_rows):
        df, column = diabetes_dataset
        sub_action = "Random Sampling"
        args = {"a": num_rows, "b": 0, "c": 0}
        result_df = manip_obj.add_rows(sub_action, df.copy(), column, args)
        assert len(result_df) == len(df) + num_rows

    @pytest.mark.parametrize("num_rows", [5, 10, 15])
    def test_add_rows_bootstrap_resampling(self, diabetes_dataset, manip_obj, num_rows):
        df, column = diabetes_dataset
        sub_action = "Bootstrap Resampling"
        args = {"a": num_rows, "b": 0, "c": 0}
        result_df = manip_obj.add_rows(sub_action, df.copy(), column, args)
        assert len(result_df) == len(df) + num_rows
