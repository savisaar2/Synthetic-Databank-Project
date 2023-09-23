class AnalyseController:
    def __init__(self, model, view):
        """
        Initialises an instance of the AnalyseController class.

        This class handles logic and interaction between the Analyse view and dataframe model.

        Parameters
        ----------
        model : Model
            The applicaiton's model instance.
        name : View
            The application's view instance.
        """
        self.model = model
        self.view = view
        self.frame = self.view.frames["analyse"]
        self._bind()

    def _bind(self):
        """
        Private method to establish event bindings.
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the analyse page.
        """
        pass