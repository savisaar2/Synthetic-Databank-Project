from utils.logger_utils import Logger

class SaveController:
    def __init__(self, model, view):
        """
        Initialises an instance of the SaveController class.

        This class handles logic and interaction between the SaveController view and dataframe model.

        Parameters
        ----------
        model : Model
            The applicaiton's model instance.
        name : View
            The application's view instance.
        """
        self.logger = Logger()
        self.model = model
        self.view = view
        self.frame = self.view.frames["save"]
        self.exception = self.view.frames["exception"]
        self._bind()

    def _show_metadata_export_widgets(self): 
        """_summary_
        """
        checkbox_state = self.frame.get_export_metadata_checkbox_state()
        if checkbox_state == 1:
            self.frame.show_metadata_widgets()
        else:
            self.frame.hide_metadata_widgets()

    def _save_or_export_dataset(self, mode): 
        """Covers save, save as and export.

        Args:
            mode (str): "A type of save" or "Export". 
        """
        # Get the mode if it's "A type of save"
        if mode == "A type of save":
            mode = self.frame.get_save_button_mode()  # Separate for future use case, e.g., confirmation of overwrite

        # Initialise metadata values
        name = description = source = None

        # Try to obtain metadata info from entry widgets
        name = self.frame.get_name_entry(mode=mode)
        description = self.frame.get_desc_entry(mode=mode)
        source = self.frame.get_source_entry(mode=mode)

        # Execute relevant action based on mode.
        if mode == "Save As":
            self._handle_save_as_mode(name, description, source)
        elif mode == "Overwrite":
            self._handle_overwrite_mode(name, description, source)
        elif mode == "Export":
            self._handle_export_mode(name, description, source)
            
        self._update_databank_library()

    def _handle_save_as_mode(self, name, description, source):
        """Saves current dataset as a new file.

        Args:
            name (str): Name of dataset.
            description (str): Description of dataset.
            source (str): Source relevant to dataset. 
        """
        full_path = self.model.DATASET.databank_dir + name + ".csv"
        self.model.DATASET.save_export_dataset(full_path=full_path)
        self.model.DATASET.add_metadata(name, description, source)

    def _handle_overwrite_mode(self, name, description, source):
        """Overwrites existing dataset with current dataset.

        Args:
            name (str): Name of dataset.
            description (str): Description of dataset.
            source (str): Source relevant to dataset. 
        """
        confirm_overwrite = self.exception.display_confirm(
            message="Are you sure you wish to overwrite a built-in dataset with modifications?"
        )
        if confirm_overwrite:
            self._handle_save_as_mode(name, description, source)

    def _handle_export_mode(self, name, description, source):
        """Exports current dataset.

        Args:
            name (str): Name of dataset.
            description (str): Description of dataset.
            source (str): Source relevant to dataset. 
        """
        file_for_export = self.frame.show_export_dialogue(file_name=name)
        self.model.DATASET.save_export_dataset(full_path=file_for_export)

        if self.frame.get_export_metadata_checkbox_state() == 1:
            selected_dir = file_for_export.replace(name + ".csv", "")
            self.model.DATASET.export_metadata_to_file(
                destination_dir=selected_dir, name=name, desc=description, source=source
            )

    def _update_databank_library(self):
        """
        Updates the library list.
        """
        self.view.frames["library"].populate_treeview(file_list=self.model.library.get_datasets(mode="all"))

    def _refresh_saveexport_widgets(self, event): 
        """
        Obtain metadata info for the loaded dataset to be populated in the appropriate widgets for 
        save / export.
        """
        # Check if button is disabled.
        button = event.widget
        parent_frame = button.master
        if parent_frame.cget("state") == "disabled":
            return
        
        # Retrieve metadata for selected dataset.
        metadata_repository = self.model.DATASET.load_all_metadata()
        name = self.model.DATASET.get_dataset_name()
        loaded_dataset = self.model.DATASET.get_file_metadata(metadata_collection=metadata_repository, name=name)
        
        # Initialise metadata values
        description = source = ""

        # If metadata exists load description and source.
        if loaded_dataset:
            description, source = loaded_dataset.get("Description", ""), loaded_dataset.get("Source", "")

        # Populate metadata if found otherwise blank.
        self.frame.populate_metadata_widgets(name=name, description=description, source=source)

        
    def _save_as_toggle_upon_name_modification(self): 
        """Check new name vs old name... if changed, then change button text to "Save As", otherwise 
        change back to "Save".
        """
        new_name = self.frame.get_name_entry(mode="Overwrite")
        current_name = self.model.DATASET.get_dataset_name()

        if new_name == current_name or self.model.DATASET.get_file_metadata(self.model.DATASET.load_all_metadata(), name=new_name):
            self.frame.change_save_button_text(mode="Overwrite")
        else:
            self.frame.change_save_button_text(mode="Save As")

    def _bind(self):
        """
        Private method to establish event bindings.
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the save page.
        """
        self.view.frames["menu"].save_button.bind("<Button-1>", self._refresh_saveexport_widgets)
        self.frame.save_name_entry.bind("<KeyRelease>", lambda event: self._save_as_toggle_upon_name_modification())
        self.frame.export_metadata_checkbox.bind("<Button-1>", lambda event: self._show_metadata_export_widgets)
        self.frame.save_button.bind("<Button-1>", lambda event, mode="A type of save": self._save_or_export_dataset(mode))
        self.frame.export_button.bind("<Button-1>", lambda event, mode="Export": self._save_or_export_dataset(mode))