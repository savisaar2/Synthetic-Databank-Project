class LoginController:
    def __init__(self, model, view, logger):
        """
        Initialises an instance of the LoginController class.

        This class handles logic and interaction between the Login view and user model.

        Parameters
        ----------
        model : Model
            The applicaiton's model instance.
        name : View
            The application's view instance.
        """
        self.logger = logger
        self.model = model
        self.view = view
        self.frame = self.view.frames["login"]
        self._bind()

    def _bind(self):
        """
        Private method to establish event bindings.
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the login page.
        """
        pass