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

    def _show_metadata_export_widgets(self, event): 
        """_summary_
        """
        if self.frame.get_export_metadata_checkbox_state() == 1: # ticked
            self.frame.show_metadata_widgets()
        else: # 0: unticked
            self.frame.hide_metadata_widgets()

    def _save_or_export_dataset(self, mode): 
        """Covers save, save as and export.

        Args:
            mode (str): "A type of save" or "Export". 
        """
        if mode == "A type of save": # get the type of button. 
            mode = self.frame.get_save_button_mode() # Separated for future use case e.g. confirmation of overwrite
        try: 
            name = self.frame.get_name_entry(mode=mode) # obtain metadata info from entry widgets
            description = self.frame.get_desc_entry(mode=mode)
            source = self.frame.get_source_entry(mode=mode)
        except Exception as e: 
            print(e)

        if mode == "Save As": 
            self.model.DATASET.save_export_dataset(full_path=self.model.DATASET.databank_dir + name + ".csv")
            self.model.DATASET.add_metadata(name, description, source)
        elif mode == "Overwrite": 
            confirm_overwrite = self.exception.display_confirm(
                message="Are you sure you wish to overwrite a built-in dataset with modifications?"
                )
            if confirm_overwrite: 
                self.model.DATASET.save_export_dataset(full_path=self.model.DATASET.databank_dir + name + ".csv")
                self.model.DATASET.add_metadata(name, description, source)
        elif mode == "Export": 
            file_for_export = self.frame.show_export_dialogue(file_name=name) # Entire path including filename.
            self.model.DATASET.save_export_dataset(full_path=file_for_export) # Export to user specified location.
            if self.frame.get_export_metadata_checkbox_state() == 1: # Export metadata as well as txt
                selected_dir = file_for_export.replace(name+".csv", "")
                self.model.DATASET.export_metadata_to_file(
                    destination_dir=selected_dir, name=name, desc=description, source=source)
            
        self._update_databank_library()

    def _update_databank_library(self):
        data = self.model.library.get_datasets(mode="all")
        self.view.frames["library"].populate_treeview(file_list=data)

    def _refresh_saveexport_widgets(self, event): 
        """
        Obtain metadata info for the loaded dataset to be populated in the appropriate widgets for 
        save / export.
        """
        button = event.widget
        parent_frame = button.master

        if parent_frame.cget("state") == "disabled":
            return
        
        metadata_repository = self.model.DATASET.load_all_metadata()
        name = self.model.DATASET.get_dataset_name()
        loaded_dataset = self.model.DATASET.get_file_metadata(metadata_collection=metadata_repository, name=name)
        
        self.frame.populate_metadata_widgets(
            name=name, description=loaded_dataset["Description"], source=loaded_dataset["Source"]
            )
        
    def _save_as_toggle_upon_name_modification(self): 
        """Check new name vs old name... if changed, then change button text to "Save As", otherwise 
        change back to "Save".
        """
        name = self.model.DATASET.get_dataset_name()
        if self.frame.get_name_entry(mode="Overwrite") == name: # no change
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
        self.frame.export_metadata_checkbox.bind("<Button-1>", lambda event: self._show_metadata_export_widgets(event))
        self.frame.save_button.bind("<Button-1>", lambda mode: self._save_or_export_dataset("A type of save"))
        self.frame.export_button.bind("<Button-1>", lambda mode: self._save_or_export_dataset("Export"))