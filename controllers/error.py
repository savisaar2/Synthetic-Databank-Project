class ErrorController:
    def __init__(self, model, view):
        """
        Initialises an instance of the ErrorController class.

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
        self._bind

    def _go_back(self):
        """
        Private method to close error window.
        """
        self.root.destroy()

    def _bind(self):
        """
        Private method to establish event bindings.
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the sample page.
        """
        self.frame.new_button.bind("<Button-1>", lambda event: self._go_back())