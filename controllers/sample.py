from utils.logger_utils import Logger


class SampleController:
    def __init__(self, model, view):
        """
        Initialises an instance of the SampleController class.

        This class handles logic and interaction between the Sample view and dataframe model.

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
        self.frame = self.view.frames["sample"]
        self.exception = self.view.frames["exception"]
        
        self._bind()

    def _refresh_sample_widgets(self, event, mode): 
        """
        Obtain column headers from the loaded dataset to be populated in the appropriate widgets e.g. 
        option menues. Called whenever Sample side panel is clicked to ensure correct data.
        """
        column_headers = self.model.DATASET.get_column_headers()
        column_headers.insert(0, "------")
        self.frame.refresh_sample_widgets(mode=mode, column_headers=column_headers)

    def _generate(self, event): # Generate Sample
        self.model.DATASET.append_new_snapshot(snapshot={
            "Name": "SAMPLE of DATASET", # TODO overlay prompt to ask name and description of dataset
            "Description": "Newly created sample using sampling algorithms", 
            "Schedule Set": "", 
            "Dataframe": "test" # TODO replace with newly configured sample DF from SampleModel
            }
        )
        snapshots = self.model.DATASET.get_reference_to_all_snapshots()

    def _get_algorithm_info(self, event):
        """Get text description of algorithm. 
        """
        selection = self.frame.get_sample_algo_menu_selection()
        description = self.model.sample.get_algorithm_info(selection=selection)
        self.frame.update_algorithm_description_info(text=description)

    def _bind(self):
        """
        Private method to establish event bindings.
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the sample page.
        """
        self.view.frames["menu"].sample_button.bind(
            "<Button-1>", lambda event, mode="menus": self._refresh_sample_widgets(event, mode)
            )
        self.frame.add_row.bind("<Button-1>", lambda event, mode="rows": self._refresh_sample_widgets(event, mode))
        self.frame.generate.bind("<Button-1>", self._generate)
        self.frame.sampling_algo_menu.bind("<Configure>", self._get_algorithm_info)