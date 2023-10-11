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

        self._load_profile_info()
        self._bind()

    def _load_profile_info(self):
        #profile_info = self.model.user.get_user_profile()
        
        profile = {
            "username": "admin",
            "role": "admin",
            "profile_info": {
                "first": "John", 
                "last": "Doe", 
                "initials": "JD",
                "title": "Online Tutor", 
                "department": "Teaching", 
                "office": "Main Campus", 
                "email": "johndoe@mymail.unisa.edu.au", 
                "bio": "Sample biography"},
        }
        
        self.frame.load_profile_info(profile)

    def _load_buttons_by_role(self):
        #role = self.model.user.get_user_role()
        role = "admin"
        self.frame.load_buttons_by_role(role)

    def _bind(self):
        """
        Private method to establish event bindings.
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the user accounts.
        """
        self.view.frames["menu"].accounts_button.bind("<Button-1>", self._load_buttons_by_role())