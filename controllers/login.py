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
        self.menu_frame = self.view.frames["menu"]
        self.exception = self.view.frames["exception"]
        self.failed_attempts = 0
        self._bind()

    def _authenticate_user(self, event):
        # Get authentication info from view.
        username, password = self.frame.get_login_info()

        # Ensure fields are not blank.
        if username == "" or password == "":
            self.exception.display_error("AUTH: Invalid username & password.")
            self.frame.overlay_frame.focus() # Remove focus from widgets.
            return
        
        user = self.model.user.get_user_by_username(username)

        if user:
            authenticated = self.model.user.login(username, password)

            if authenticated:
                self.frame.hide_view()
            else:
                # Display generic error for failure.
                self.exception.display_error("AUTH: Invalid username & password.")
        else:
            # Display generic error for failure.
            self.exception.display_error("AUTH: Invalid username & password.")

    def _bind(self):
        """
        Private method to establish event bindings.
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the login page.
        """
        self.frame.login_button.bind("<Button-1>", lambda event: self._authenticate_user(event))