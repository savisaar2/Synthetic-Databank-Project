import json
import pandas as pd
from os import path, remove
import io
import re
import threading

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
            cls.databank_dir = "db/databank/"
            cls._instance._SNAPSHOTS = []
        return cls._instance
        
    def new_dataset(self):
        """Method to generate a blank frame for the purpose of creating a user
        defined dataset from scratch. 
        """
        self.clear_all_snapshots() # Clear first!
        self._SNAPSHOTS.append(
            {
            "Name": "New Dataset",
            "Description": "",
            "Schedule Set": {},
            "Dataframe": pd.DataFrame()
            }
        )
        #print("New dataset:", self._SNAPSHOTS[-1])

    def load_dataset_in_thread(self, file_path, dataset_name):
        """Loads a csv file stored in the databank into memory i.e. _SNAPSHOTS list.
        """
        if file_path:
            self.clear_all_snapshots()
            df = pd.read_csv(file_path)
            self._SNAPSHOTS.append(
                {
                    "Name": f"{dataset_name}",
                    "Description": "Initial load.",
                    "Schedule Set": {},
                    "Dataframe": df
                }
            )
            #print("Loaded data set:", self._SNAPSHOTS[-1])

    def load_dataset(self, file_path, dataset_name):
        load_thread = threading.Thread(target=self.load_dataset_in_thread, args=(file_path, dataset_name))
        load_thread.start()

    def save_export_dataset(self, full_path): 
        """Save / save as or export the most current dataframe in memory back to specified file (CSV) on disk.

        Args:
            full_path (str): entire path including filename.
        """
        if full_path: 
            self._SNAPSHOTS[-1]["Dataframe"].to_csv(f"{full_path + '.csv'}", index=False)

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
    
    def get_dataset_name(self, first_snapshot=False): 
        """Method to get current dataset's name i.e _SNAPSHOTS[-1]. 
        Should be stored here as opposed to grabbing directly from label state in Library view.

        Returns: 
            str: Name of loaded dataset. 
        """
        if first_snapshot == True: # Caters for save / export - show original snap details prior to sampling / manip.
            return self._SNAPSHOTS[0]["Name"] 
        else: 
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
        del self._SNAPSHOTS[index+1:] # Slicing to truncate.

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
        _SNAPSHOTS[-1] of the model. Used for purposes of debugging and ease of comprehension. 
        I.e. usage sytax similar to get_column_headers() etc. 
        """
        return self._SNAPSHOTS[-1]["Dataframe"]
    
    def get_reference_to_all_snapshots(self): 
        """Used specifically in rollback functionality. Returns a mutable reference to _SNAPSHOTS list.
        Note any changes to the returned list will directly modify the objects therein.
        """
        return self._SNAPSHOTS
    
    def get_length_of_snapshot_collection(self):
        """Return the length of self._SNAPSHOTS
        """
        return len(self._SNAPSHOTS)
    
    def get_specific_snapshot(self, index): 
        """return the particular snapshot i.e. 
        {"Name": "", "Description": "", "Schedule Set": "", "Dataframe": pandas dataframe}
        """
        return self._SNAPSHOTS[index]

    def clear_all_snapshots(self):
        """Method to clear all snapshots.
        """
        self._SNAPSHOTS.clear()

    def append_new_snapshot(self, snapshot):
        self._SNAPSHOTS.append(snapshot)
        #print("snapshot appended!")

    def _sort_datasets_alphabetically(self, json_data):
        """
        Sorts json data into into alphabetical order. TODO: to subsume method of the same name in library.

        Parameters
        ----------
        json_data : json
            This parameter should be in json format.
        """
        return sorted(json_data.keys(), key=str.lower)

    def load_all_metadata(self): 
        """Generalised method to be used from Library and Save & Export. TODO: subsume Library Model 
        method by the name of "load_all_metadata" with this method.

        Returns:
            dictionary: metadata values
        """
        # Open and store json data.
        with open("db/system/dataset_metadata.json", "r") as json_file: 
            json_data = json.load(json_file)

        # Sort data into alphabetical order.
        sorted_json = self._sort_datasets_alphabetically(json_data)
        
        # Return data.
        return {key: json_data[key] for key in sorted_json} # Alphabetically sorted json_file by key
    
    def add_metadata(self, name, description, source):
        """
        Adds metadata to the metadata store file. TODO: subsumes Library Model's method by the same name.

        Parameters
        ----------
        name : str
            Name of file to be stored in databank.
        description : str
            Description metadata for file.
        source : str
            Source metadata for file.
        """
        new_data = { # new payload
            path.splitext(name)[0]: { 
                "Source": source, 
                "Description": description
            }
        }
        # Load the existing metadata.
        existing_data = self.load_all_metadata()

        # Update the existing metadata with new data.
        existing_data.update(new_data)

        # Open the metadata file for writing
        with open("db/system/dataset_metadata.json", "w") as json_file:
            # Write the updated metadata to the json file
            json.dump(existing_data, json_file, indent=4)

    def export_metadata_to_file(self, name, desc, source): 
        """_summary_

        Args:
            name (str): metadata name i.e. dataset name specified by user
            desc (str): metadata desc
            source (scr): metadata source
        """
        file_name = re.search(r"[^/]+$", name)
        with open(name + ".txt", "w") as file: 
            file.write(f"Name: {file_name.group(0)}\n")
            file.write(f"Description: {desc}\n")
            file.write(f"Source: {source}")
    
    def get_file_metadata(self, metadata_collection, name): 
        """Return specific metadata from the loaded databank metadata repository. 
        TODO: subsume Library Model method by the name of "get_file_metadata" with this method 
        so it can be used in both Library and Save & Export components.

        Args: 
            metadata_collection (dict): dictionary containing the databank's metadata repository.
            name (str): specific name of the metadata file being sort.
        
        Returns: 
            Dictionary: specific metadata entry.
        """
        try:
            return metadata_collection[name]
        except KeyError:
            # Handle the case where 'name' is not found in metadata_collection
            return None
    
    def add_generated_dataset_to_snapshot(self, schedule_set, dataset_name, df):
        """Appends the successfully generated dataframe to the SNAPSHOTS list.
        """
        if len(self._SNAPSHOTS) > 9:
             del self._SNAPSHOTS[0]
        self._SNAPSHOTS.append(
            {
                "Name": f"{dataset_name}", 
                "Description": "Generated dataset.", 
                "Schedule Set": schedule_set, 
                "Dataframe": df
            }
        )
        #print("Generated data set:", self._SNAPSHOTS[-1]["Dataframe"])

    def get_dataset_info(self, file_path):
        """Reads the selected dataframe, calls the pandas.info() function and returns the dataframe info, such as
        columns: dtypes, count, null count, row count etc.
        Args:
            file_path (str): Path to dataset in databank.

        Returns:
            string: info of the selected dataset.
        """
        buffer = io.StringIO()
        temp_df = pd.read_csv(file_path)
        temp_df.info(buf=buffer)
        info = buffer.getvalue()
        info = info.split("\n",1)[1]
        info = f"Info:\n{info}"
        return info
    
    def get_all_column_datatypes(self): 
        """Method to obtain the datatype listing of the entire dataframe.
        Returns a dictionary of column name keys and pandas data types. 
        """
        return {column: str(data_type) for column, data_type in self._SNAPSHOTS[-1]["Dataframe"].dtypes.items()}
    
    def remove_dataset(self, file_name):
        # Define the paths
        file_path = path.join(self.databank_dir, file_name + ".csv")
        meta_file = "db/system/dataset_metadata.json"  # Replace with the path to your JSON file

        # Check if the dataset file exists before attempting to remove it
        if path.exists(file_path):
            remove(file_path)

        # Load the JSON data from the metadata file
        with open(meta_file, 'r') as file:
            data = json.load(file)

        # Check if the dataset exists in the metadata
        if file_name in data:
            del data[file_name]
            # Save the updated JSON back to the metadata file
            with open(meta_file, 'w') as file:
                json.dump(data, file, indent=4)