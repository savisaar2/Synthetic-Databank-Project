import pandas as pd

class DatasetModel:
    """Singleton. Working collection of datasets. _SNAPSHOTS is a list of dictionaries with keys representing 
    information about the dataset that will be manipulated / configured prior to saving or exporting to CSV file. 

    Pandas dataframe will hold in memory the actual loaded dataset from disk. This object is to be stored under
    the "Dataframe" key of each dictionary. Structure as follows:

    SNAPSHOTS is a [
        {
                # If new dataset, will be "New Dataset". If loaded dataset will be name of loaded dataset. 
                # If new snapshot as a result of successful Manipulations > Generate i.e. will be arbitrary name 
                # provided by user to name the snapshot in Manipulations:Rollback section.
            "Name": "", 
                # If new or loaded dataset will be "".
                # If new snapshot as a result of successful Manipulations > Generate, will be arbitrary description
                # provided by user to describe the manipulation set used to manipuate / generate data. 
            "Description": "", 
                # If new or loaded dataset will be "".
                # If snapshot as a result of successful Manipulations > Generate, will be the list of schedules 
                # from Manipulations > Schedule set. 
            "Schedule Set": "", 
                # Will hold Manipulations > Scheduler's set of manipulations (text descriptions) that describe 
                the generation of a new snapshot of a pandas dataframe.
                # the new snapshot (dataset).
            "Dataframe": pandas dataframe
                # Will hold either blank, loaded dataset OR a snapshot of the dataset as manipulated by actions
                # performed in a successful Manipulate > Generate. In all cases will be a unique pandas dataframe
        }
    ]
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatasetModel, cls).__new__(cls)
            cls._instance._SNAPSHOTS = []
        return cls._instance
        
    def new_dataset(self):
        """Method to generate a blank frame for the purpose of creating a user
        defined dataset from scratch. 
        """
        self._clear_all_snapshots() # Clear first!
        self._SNAPSHOTS.append(
            {
            "Name": "New Dataset",
            "Description": "",
            "Schedule Set": "",
            "Dataframe": pd.DataFrame()
            }
        )
        print("New dataset:", self._SNAPSHOTS[-1])

    def load_dataset(self, file_path, dataset_name):
        """Loads a csv file stored in the databank into memory i.e. _SNAPSHOTS list.
        """
        if file_path: 
            self._clear_all_snapshots()
            df = pd.read_csv(file_path)
            self._SNAPSHOTS.append(
                {
                    "Name": f"{dataset_name}", 
                    "Description": "Initial load.", 
                    "Schedule Set": "", 
                    "Dataframe": df
                }
            )
            print("Loaded data set:", self._SNAPSHOTS[-1])
        
    def get_column_headers(self):
        """Method to obtain column names for the current dataset in _SNAPSHOTS list.

        Returns:
            list: List of column names.
        """
        # Ternary operator to cater for drop menu widgets default selection when no dataset is loaded i.e. no columns.
        return list(self._SNAPSHOTS[-1]["Dataframe"].columns) if len(self._SNAPSHOTS) > 0 else ("------",)
    
    def get_column_data(self, column):
        """Method to obtain single column from the current dataset.

        Args:
            column (int): Column index position.

        Returns:
            Pandas series: Returns either a specified column (including header) or multiple columns depending on 
            whether column arg is string (single) or list of strings (multiple columns). Note that this 
            returns a VIEW i.e. pandas series type. It is not a reference to the original column of data
            thus, modifications to it will be discarded unless specifically commited to memory (original
            or otherwise). Data type akin to SQL query result.
        """
        return self._SNAPSHOTS[-1]["Dataframe"][column]
    
    def get_dataset_name(self): 
        """Method to get current dataset's name i.e _SNAPSHOTS[-1]. 
        Should be stored here as opposed to grabbing directly from label state in Library view.

        Returns: 
            str: Name of loaded dataset. 
        """
        return self._SNAPSHOTS[-1]["Name"]
    
    def get_column_datatype(self, column_index):
        """Method to obtain the datatype of a defined column in the 
        current dataset's dataframe object.

        Args:
            column_index (int): Column index position.

        Returns:
            dtype: Datatype of defined column in current dataset's dataframe.
        """
        column_data_type = self.get_column_data(column_index)
        return column_data_type.dtypes

    def rollback(self, index):
        """Method to move a user defined dataset at specifed index within
        the _SNAPSHOTS list - effectively truncating list to make the selected  to the front to signifiy it as the current dataset.

        Args:
            index (int): User specified index of dataset to define as current.
        """
        self._SNAPSHOTS[:index + 1] # Slicing to truncate.

    def get_df_row_by_range(self, start_row, end_row):
        """Method to obtain rows of current dataset within a defined range.
        Starting at 0 and up to but not including end_row

        Args:
            start_row (int): Start index of row.
            end_row (int): End index of row.

        Returns:
           pandas DataFrame: A dataframe with a specified row range.
        """
        return self._SNAPSHOTS[-1]["Dataframe"].iloc[start_row-1:end_row]

    def get_df_row_count(self):
        """Method to obtain number of rows in the current dataset stored in self._SNAPSHOTS

        Returns:
            int: Number of rows in the current dataset.
        """
        # Ternary to cater for no loads.
        return len(self._SNAPSHOTS[-1]["Dataframe"]) if len(self._SNAPSHOTS) > 0 else 0
    
    def get_reference_to_current_snapshot(self):
        """Use specifically when needing to refer to current snapshot i.e. as opposed to 
        SNAPSHOTS[-1] of the model. Used for purposes of debugging and ease of comprehension. 
        I.e. usage sytax similar to get_column_headers() etc. 
        """
        return self._SNAPSHOTS[-1]["Dataframe"]

    def _clear_all_snapshots(self):
        """Method to clear all snapshots.
        """
        self._SNAPSHOTS.clear()
        print("snapshots cleared!")