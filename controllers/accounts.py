from utils.logger_utils import Logger

class AccountsController:
    def __init__(self, model, view):
        """
        Initialises an instance of the AccountsController class.

        This class handles logic and interaction between Accounts view and user model.

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
        self.frame = self.view.frames["accounts"]

        self._bind()

    def _load_profile(self):
        self._load_profile_info()
        self._load_buttons_by_role()

    def _load_profile_info(self):
        profile = self.model.user.get_user_profile()
        self.frame.load_profile_info(profile)

    def _save_user_details(self):
        save_data = self.frame.toggle_edit()
        if save_data:
            self.model.user.save_profile(self.model.user.get_username(), save_data)

    def _load_buttons_by_role(self):
        role = self.model.user.get_user_role()
        self.frame.load_buttons_by_role(role)

        self.frame.edit_button.bind("<Button-1>", lambda event: self._save_user_details())

    def _bind(self):
        """
        Private method to establish event bindings.
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the user accounts.
        """
        self.view.frames["menu"].accounts_button.bind("<Button-1>", lambda event: self._load_profile())