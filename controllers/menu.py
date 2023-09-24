class MenuController:
    def __init__(self, model, view):
        """
        Initialises an instance of the MenuController class.

        This class handles logic and interaction between the Menu view.

        Parameters
        ----------
        model : Model
            The applicaiton's model instance.
        name : View
            The application's view instance.
        """
        self.model = model
        self.view = view
        self.frame = self.view.frames["menu"]
        self._bind()

    def _bind(self):
        """
        Private method to establish event bindings.
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the menu.
        """
        pass