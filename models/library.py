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
        if byte_val >= 1024 * 1024:  # larger than 1 mb
            size = byte_val / (1024 * 1024)
            return f"{round(size, 2)} mb" 
        else:
            size = byte_val / 1024
            return f"{round(size, 2)} kb"

    def sort_datasets_alphabetically(self, json_data): 
        return sorted(json_data.keys(), key=str.lower)

    def get_datasets(self, mode, subset=None):
        """
        Returns list of tuples. Tuples of datasets to file size. 
        """
        file_size = []
        
        if mode == "all": 
            # Replaced to enable pulling for metadata for import functionality.
            self._metadata = self._load_all_metadata()
            datasets = list(self._metadata.keys())
        elif mode == "specific": 
            datasets = subset

        for d in self._metadata:
            if d in datasets: 
                file_path = os.path.join("{}{}.csv".format(self.databank_dir, d))
                if os.path.exists(file_path): 
                    file_size.append(self.convert_to_megabytes(os.path.getsize(file_path)))
                else: 
                    file_size.append("-")

        return [(file, size) for file, size in zip(datasets, file_size)]
    
    def get_file_metadata(self):
        pass
    
    def _load_all_metadata(self): 
        """
        Load or refresh databank's metadata information.
        """
        with open("db/system/dataset_metadata.json", "r") as json_file: 
            json_data = json.load(json_file)

        sorted_json = self.sort_datasets_alphabetically(json_data)
        
        return {key: json_data[key] for key in sorted_json} # Alphabetically sorted json_file by key

    def search_metadata(self):
        pass