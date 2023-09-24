import pandas as pd

class DataFrameModel:
    """Singleton object which contains a list of dataframes the user has loaded
    or generated.
    """
    _self = None

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self
        
    def __init__(self):
        self._snapshots = []

    def new_dataframe(self, file_path: str, dataset_name: str):
        """Method to generate a blank frame for the purpose of creating a user
        defined dataset from scratch. 

        Args:
            file_path (str): File path to be a location within the
        system's databank library allocated to user created datasets.
            dataset_name (str): User input name of new dataset.
        """
        df = pd.DataFrame()
        self._snapshots.insert(0,{
            "df_name": dataset_name,
            "df_file_path": file_path,
            "data_frame": df
            })

    def load_dataframe(self, file_path: str, dataset_name: str):
        """Loads a csv file located in the databank to snapshots attribute.
        Can be utilised to store additional generated synthetic dataframes to 
        facilitate rollback functionality. Current dataframe will always be at
        position 0.

        Args:
            file_path (str): Location of csv data file.
            dataset_name (str): Name of dataset, either user or from databank.
        """
        data = pd.read_csv(file_path)
        df = pd.DataFrame(data)
        self._snapshots.insert(0,{
            "df_name": dataset_name,
            "df_file_path": file_path,
            "data_frame": df
            })
        
    def get_column_headers(self) -> list:
        """Method to obtain column names for the current dataset.

        Returns:
            list: List of column names.
        """
        headers = list(self._snapshots[0]["data_frame"].columns)
        return headers
    
    def get_column_data(self, column: int):
        """Method to obtain single columnm from the current dataset.

        Args:
            column (int): Column index position.

        Returns:
            dataframe: A single dataframe from the current dataset.
        """
        column = self._snapshots[0]["data_frame"].iloc[:,column]
        return column
    
    def get_column_datatype(self, column_index):
        """Method to obtain the datatype of a defined column in the 
        current dataframe.

        Args:
            column_index (int): Column index position.

        Returns:
            dtype: Datatype of defined column in current dataframe.
        """
        column_data_type = self.get_column_data(column_index)
        return column_data_type.dtypes

    def rollback(self, index: int):
        """Method to move a user defined dataset at specifed index within
        the snapshots list to the front to signifiy it as the current dataset.

        Args:
            index (int): User specified index of dataset to define as current.
        """
        self._snapshots.insert(0, self._snapshots.pop(index))

    def get_df_row_by_range(self, start_row: int, end_row: int):
        """Method to obtain rows of current dataset within a defined range.

        Args:
            start_row (int): Start index of row.
            end_row (int): End index of row.

        Returns:
           dataFrame: A dataframe with a specified row range.
        """
        df = self._snapshots[0]["data_frame"].iloc[start_row:end_row]
        return df

    def get_df_row_count(self) -> int:
        """Method to obtain number of rows in the current dataset.

        Returns:
            int: Number of rows in the current dataset.
        """
        row_count = len(self._snapshots[0]["data_frame"].index)
        return row_count
    
    def get_reference_to_current_snapshot(self):
        # Not required as current dataset is always push to position 0.
        pass

    def _clear_all_snapshots(self):
        """Method to clear all snapshots.
        """
        self._snapshots = []
