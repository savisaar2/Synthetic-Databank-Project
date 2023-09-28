import json, os, re

class LibraryModel():
    def __init__(self):
        """
        Initialise the LibraryModel component of the application.

        This class represents the LibraryModel component of the application's MVC (Model-View-Controller) architecture.
        It initialises the models to be consumed by the controllers of this applicaiton.
        """
        pass

    def convert_to_megabytes(self, byte_val): 
        if byte_val >= 1024 * 1024:  # larger than 1 mb
            size = byte_val / (1024 * 1024)
            return f"{round(size, 2)} mb" 
        else:
            size = byte_val / 1024
            return f"{round(size, 2)} kb"

    def sort_datasets_alphabetically(self, json_data): 
        return sorted(json_data.keys(), key=str.lower)

    def get_datasets(self):
        pass
    
    def get_file_metadata(self):
        pass
    
    def _load_all_metadata(self): 
        pass

    def search_metadata(self):
        pass