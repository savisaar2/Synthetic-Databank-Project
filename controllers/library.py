from os import path
from shutil import copy
import pandas as pd

class LibraryController:
    def __init__(self, model, view):
        """
        Initialises an instance of the LibraryController class.

        This class handles logic and interaction between the library view and dataframe model.

        Parameters
        ----------
        model : Model
            The applicaiton's model instance.
        name : View
            The application's view instance.
        """
        self.model = model
        self.view = view
        self.frame = self.view.frames["library"]
        self.import_overlay = self.view.frames["import"]
        
        # Trigger to determine if new_file has been selected from import overlay.
        self.new_file = None

        # Ensure databank is listed to view on run.
        self._display_dataset_list(mode="all")

        self._bind()

    def _display_dataset_list(self, mode, subset=None):
        """
        Get list of datasets from databank and send it to the view.

        Parameters
        ----------
        mode : str
            Select a mode all|specific.
        subset : list, optional
            A specific list of datasets from databank.
        """
        # Get data and send it to view for population.
        data = self.model.library.get_datasets(mode, subset)
        self.frame.populate_treeview(file_list=data)

    def _search_databank(self):
        """
        Search for meta-data upon each key press inside search (input widget).
        """
        keywords = self.frame.search_input.get()            # Get search term from library view.
        mode = "specific" if len(keywords) > 1 else "all"   # If keywords has content then execute search otherwise list all.

        # Execute the search and update the dataset list.
        self._display_dataset_list(mode=mode, subset=self.model.library.search_metadata(keywords))

    def _create_new_dataset(self):
        """
        Creates a blank dataset to be generated by the application.
        """
        # Initalise a new dataset in the model.
        self.model.DATASET.new_dataset()
        # Provide visual cue.
        self.frame.dataset_status.configure(text=f"New Unsaved Data Set", text_color="yellow")

    def _show_metadata(self):
        """
        Retrieves metadata for selected dataset item in treeview list of library page and displays
        in the metadata field of the page.
        """
        # Get the selected item(s) from the Treeview
        selected_items = self.frame.tree_view.selection()

        # Get the metadata for the first selected item (assuming single selection)
        metadata = None
        if selected_items:
            item = selected_items[0]
            values = self.frame.tree_view.item(item, "values")
            name, size = values
            metadata = self.model.library.get_file_metadata(name)

        # Update the view with the selected file's metadata
        self.frame.update_metadata_display(metadata)

    def _load_dataset(self):
        """
        Loads a dataset from the databank based on selected item in treeview.
        """
        # Get the selected item(s) from the Treeview
        selected_items = self.frame.tree_view.selection()

        # Get the name of the file
        if selected_items:
            item = selected_items[0]
            values = self.frame.tree_view.item(item, "values")
            name, size = values
            file_path = self.model.library.databank_dir + name + ".csv"
            #print(f"Double-clicked on file: {name}")
            
            # Loads selected items corrisponding file to memory.
            self.model.DATASET.load_dataset(file_path=file_path, dataset_name=name)
            # Provide visual cue.
            self.frame.dataset_status.configure(text=f"{name} has been loaded", text_color="lime")

    def _import_dataset(self):
        """
        Copies dataset into databank folder and saves metadata into metadata store.

        TODO: Might relook at the choice of exceptions.
        """
        try:
            # Check if a new file has been selected.
            if not self.new_file:
                raise AttributeError("Please select a file to import.")

            # Define inputs from the view.
            filename = self.import_overlay.loaded_file_label.cget("text")
            description = self.import_overlay.description_entry.get("1.0", "end-1c")
            source = self.import_overlay.source_entry.get()

            # Read the CSV file into a DataFrame.
            df = pd.read_csv(self.new_file)

            # Define the destination path for the dataset.
            destination_folder = self.model.library.databank_dir
            file_name = path.basename(self.new_file)
            destination_path = path.join(destination_folder, file_name)

            # Error handling: Check if the dataset name already exists in the databank.
            if path.exists(destination_path):
                raise ValueError("A dataset with the same name already exists in the databank.")

            # Enforce source and description fields.
            if not source or not description:
                raise ValueError("Please provide values for both the source and description fields.")

            # Continue with the copy process.
            copy(self.new_file, destination_path)  # Copy the file to the databank location.
            self._add_meta_data(filename, description, source)  # Save metadata into the metastore.
            self._display_dataset_list(mode="all")  # Refresh the treeview list of datasets.
            self.new_file = None  # Reset the new_file trigger.
            self.import_overlay.clear_fields()  # Clear the form.
            self.import_overlay.hide_view()  # Hide the import overlay.

        except pd.errors.EmptyDataError:
            print("The selected dataset contains no data.")
        except (AttributeError, ValueError) as e:
            print(str(e))
        except Exception as e:
            print(f"An error occurred: {e}")

    def _add_meta_data(self, name, description, source):
        """
        Saves metadata into metastore to fasciliate databank lookup.

        Parameters
        ----------
        name : str
            Name of file to be stored in databank.
        description : str
            Description metadata for file.
        source : str
            Source metadata for file.
        """
        # Define payload to send to model.
        new_data = {
            path.splitext(name)[0]: {
                "Source": source,
                "Description": description
            }
        }

        # Send payload back to model for saving.
        self.model.library.add_metadata(new_data)

    def _import_new_dataset(self):
        """
        Define a new_file returned from file selector in import view.

        This variable will be used to determine a file is selected 
        during import process.
        """
        self.new_file = self.import_overlay.import_new_dataset()

    def _bind(self):
        """
        Private method to establish event bindings.
        
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the library page.
        """
        self.frame.search_input.bind("<Key>", lambda event: self._search_databank())
        self.frame.import_button.bind("<Button-1>", lambda _: self.import_overlay.show_view())
        self.frame.new_button.bind("<Button-1>", lambda event: self._create_new_dataset())
        self.frame.tree_view.bind("<<TreeviewSelect>>", lambda event: self._show_metadata())
        self.frame.tree_view.bind("<Double-1>", lambda event: self._load_dataset())
        self.import_overlay.add_file_button.bind("<Button-1>", lambda _: self._import_new_dataset())
        self.import_overlay.cancel_button.bind("<Button-1>", lambda _: self.import_overlay.hide_view())
        self.import_overlay.import_button.bind("<Button-1>", lambda _: self._import_dataset())