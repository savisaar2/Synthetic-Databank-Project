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

    def _refresh_sample_widgets(self, event): 
        """
        Obtain column headers from the loaded dataset to be populated in the appropriate widgets e.g. 
        option menues. Called whenever Sample side panel is clicked to ensure correct data.
        """
        column_headers = self.model.DATASET.get_column_headers()
        column_headers.insert(0, "------")
        self.frame.refresh_sample_widgets(column_headers=column_headers)

    def _update_view(self, snapshots):
        self.rollback_tags = self.frame.display_snapshot_ui(snapshots)
        for index, rect in enumerate(self.frame.sliding_snapshot_canvas.find_all()):
            self.frame.sliding_snapshot_canvas.tag_bind(
                rect, "<Button-1>", lambda event, index=index: self._get_specific_snapshot(index)
                )

    def _get_specific_snapshot(self, index):
        """_summary_

        Args:
            index (_type_): _description_
        """
        index = index // 2
        snapshot_collection_length = self.model.DATASET.get_length_of_snapshot_collection()
        if index == snapshot_collection_length: # Green block selected
            self.frame.display_specific_snapshot_info(
                name="Current", 
                desc=f"Current working snapshot. Will become snapshot {index + 1} once samples are generated.", 
                schedule_set="", txt_color="lime"
                )
        elif index < snapshot_collection_length: # Previous snapshots selected
            target_snap = self.model.DATASET.get_specific_snapshot(index)
            name, desc, schedule_set = target_snap["Name"], target_snap["Description"], target_snap["Schedule Set"]
            self.frame.display_specific_snapshot_info(name, desc, schedule_set, "white")

    def _run(self, event): # Generate Sample
        self.model.DATASET.append_new_snapshot(snapshot={
            "Name": "SAMPLE of DATASET", # TODO overlay prompt to ask name and description of dataset
            "Description": "Newly created sample using sampling algorithms", 
            "Schedule Set": "", 
            "Dataframe": "test" # TODO replace with newly configured sample DF from SampleModel
            }
        )
        snapshots = self.model.DATASET.get_reference_to_all_snapshots()
        self._update_view(snapshots=snapshots)

    def _bind(self):
        """
        Private method to establish event bindings.
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the sample page.
        """
        self.view.frames["menu"].sample_button.bind("<Button-1>", self._refresh_sample_widgets)
        self.view.frames["menu"].sample_button.bind("<Button-1>", self._update_view(self.model.DATASET.get_reference_to_all_snapshots()))
        self.frame.sample_button.bind("<Button-1>", self._run)