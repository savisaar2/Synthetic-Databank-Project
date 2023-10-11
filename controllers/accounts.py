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
        self.frame.edit_pw_button.bind("<Button-1>", lambda event: self.view.frames["change_password"].show_view())

    def _save_user_password(self):
        chpass = self.view.frames["change_password"]
        exception = self.view.frames["exception"]
        old_password = chpass.old_pw_entry.get()
        new_password1 = chpass.new1_pw_entry.get()
        new_password2 = chpass.new2_pw_entry.get()

        # Find the user's account by username
        user_account = None
        user_account = self.model.user.get_user_profile()

        if not user_account:
            exception.display_error("User account not found")
            return

        if self.model.user.decrypt(user_account["password"]) != old_password:
            exception.display_error("Invalid Password")
            return

        if new_password1 != new_password2:
            exception.display_error("New Password Mismatch")
            return

        if not new_password1 or not new_password2:
            exception.display_info("New Password cannot be blank")
            return
        
        user_account["password"] = new_password2
        self.model.user.save_user_password(self.model.user.get_username(), user_account)
        chpass.clear_inputs()
        chpass.hide_view()

    def _bind(self):
        """
        Private method to establish event bindings.
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to the user accounts.
        """
        self.view.frames["menu"].accounts_button.bind("<Button-1>", lambda event: self._load_profile())
        self.view.frames["change_password"].cancel_button.bind("<Button-1>", lambda event: self.view.frames["change_password"].hide_view())
        self.view.frames["change_password"].save_button.bind("<Button-1>", lambda event: self._save_user_password())
        self.view.frames["change_password"].old_pw_entry.bind("<Return>", lambda event: self._save_user_password())
        self.view.frames["change_password"].new1_pw_entry.bind("<Return>", lambda event: self._save_user_password())
        self.view.frames["change_password"].new2_pw_entry.bind("<Return>", lambda event: self._save_user_password())