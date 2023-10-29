import json, os, re

class LibraryModel():
    def __init__(self):
        """
        Initialise the LibraryModel component of the application.

        This class represents the LibraryModel component of the application's MVC (Model-View-Controller) architecture.
        It initialises the models to be consumed by the controllers of this applicaiton.
        """
        self.databank_dir = "db/databank/"

    def convert_to_megabytes(self, byte_val):
        """
        Converts bytes to readable format.

        Parameters
        ----------
        byte_val : int
            Byte value.
        """
        # Return 0 if 0.
        if byte_val <= 0:
            return "0 bytes"
        
        # Define our sizes.
        units = ["bytes", "KB", "MB", "GB", "TB"]
        index = 0
        
        # Loop through units until correct size found.
        while byte_val >= 1024 and index < len(units) - 1:
            byte_val /= 1024.0
            index += 1
        
        # Return size value in 2 decimals.
        return f"{byte_val:.2f} {units[index]}"

    def sort_datasets_alphabetically(self, json_data):
        """
        Sorts json data into into alphabetical order.

        Parameters
        ----------
        json_data : json
            This parameter should be in json format.
        """
        return sorted(json_data.keys(), key=str.lower)

    def get_datasets(self, mode, subset=None):
        """
        Returns list of tuples. Tuples of datasets to file size.
        """
        dataset_file_sizes = {}

        if mode == "all":
            # Load all metadata and extract datasets.
            self._metadata = self.load_all_metadata()
            datasets = list(self._metadata.keys())
        elif mode == "specific":
            # Use the provided subset of datasets.
            datasets = subset

        # Iterate through dataset names in the metadata.
        for d in self._metadata:
            # Check if the dataset name is in the selected dataset list.
            if d in datasets:
                # Construct the full file path for the dataset csv file.
                file_path = os.path.join("{}{}.csv".format(self.databank_dir, d))

                # Check if the file exists
                if os.path.exists(file_path):
                    # Get the file size and convert it to megabytes.
                    dataset_file_sizes[d] = self.convert_to_megabytes(os.path.getsize(file_path))
                else:
                    # If the file doesn't exist, add "-" to indicate missing data.
                    dataset_file_sizes[d] = "-"

        # Convert the dictionary to a list of tuples
        return [(dataset, size) for dataset, size in dataset_file_sizes.items()]
    
    def get_file_metadata(self, file_name):
        """
        Return metadata for a specific file (dataset)
        """
        return self._metadata[file_name]
    
    def load_all_metadata(self): 
        """
        Load or refresh databank's metadata information.
        """
        # Open and store json data.
        with open("db/system/dataset_metadata.json", "r") as json_file: 
            json_data = json.load(json_file)

        # Sort data into alphabetical order.
        sorted_json = self.sort_datasets_alphabetically(json_data)
        
        # Return data.
        return {key: json_data[key] for key in sorted_json} # Alphabetically sorted json_file by key

    def search_metadata(self, keywords):
        """
        Search for specified keywords in metadata and return a dictionary of identified datasets.
        Matches string in filename, source, and description fields of metadata (json) file. 

        Parameters
        ----------
        keywords : str
            Search string.
        """
        # Split the input keywords into individual words
        keyword_list = keywords.split()
        # Initialize a set to store matching metadata
        matching_metadata = set()

        # Iterate through metadata items (string is the key, metadata is the value)
        for string, metadata in self._metadata.items():
            description_lower = string.lower()
            meta_source_lower = metadata["Source"].lower()
            meta_description_lower = metadata["Description"].lower()

            # Check if all the keywords match the key, Source, or Description
            if all(re.search(word, description_lower) or re.search(word, meta_source_lower) or re.search(word, meta_description_lower) for word in keyword_list):
                # Add the matching metadata to the set
                matching_metadata.add(string)

        # Convert the set of matching metadata to a list and return it
        return list(matching_metadata)

    
    def add_metadata(self, obj):
        """
        Adds metadata to the metadata store file.

        Parameters
        ----------
        obj : dict
            Dictionary object to store in metadata file.
        """
        # Load the existing metadata.
        existing_data = self.load_all_metadata()

        # Update the existing metadata with new data.
        existing_data.update(obj)

        # Open the metadata file for writing
        with open("db/system/dataset_metadata.json", "w") as json_file:
            # Write the updated metadata to the json file
            json.dump(existing_data, json_file, indent=4)