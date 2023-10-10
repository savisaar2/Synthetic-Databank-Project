from models.dataset import DatasetModel
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
        self._bind()

    def _show_metadata_export_widgets(self, event): 
        """_summary_
        """
        if self.frame.get_export_metadata_checkbox_state() == 1: # ticked
            self.frame.show_metadata_widgets()
        else: # 0: unticked
            self.frame.hide_metadata_widgets()

    def _bind(self):
        """
        Private method to establish event bindings.
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the save page.
        """
        self.frame.export_metadata_checkbox.bind("<Button-1>", lambda event: self._show_metadata_export_widgets(event))