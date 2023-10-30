from utils.logger_utils import Logger
from tkinter import messagebox

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

        # Define additional views to handle.
        self.menu = self.view.frames["menu"]
        self.password_editor = self.view.frames["change_password"]
        self.global_password_editor = self.view.frames["change_global_password"]
        self.accounts_editor = self.view.frames["accounts_editor"]
        self.accounts_manager = self.view.frames["accounts_manager"]
        self.new_account = self.view.frames["new_account"]
        self.exception = self.view.frames["exception"]

        self.user_to_edit = None
        self._bind()

    def _load_profile(self):
        """
        Initiates loading of profile and generating role specific action buttons.
        """
        self._load_profile_info()
        self._load_buttons_by_role()

    def _load_profile_info(self):
        """
        Retreieve authenticated user profile and return profile to view for rendering.
        """
        profile = self.model.user.get_profile_by_username(self.model.user.get_username())
        self.frame.load_profile_info(profile)

    def _save_user_details(self):
        """
        Toggle profile editing on view and save returned data.

        Toggle returns data from profile view on button save is clicked.
        """
        save_data = self.frame.toggle_edit()
        if save_data:
            username = self.model.user.get_username()
            self.model.user.save_profile(username, save_data)
            self.logger.log_info(f"ACCOUNTS - User '{username}' has updated their own profile.")

    def _save_user_details_manager(self):
        """
        Allows an authenticated administrator to make profile changes to any users.
        """
        # Retrieve and format profile data payload.
        account = {
            "username": self.accounts_editor.username_entry.get(),
            "role": self.accounts_editor.role_entry.get(),
            "profile_info": {
                "first": self.accounts_editor.first_name_entry.get(),
                "last": self.accounts_editor.last_name_entry.get(),
                "initials": self.accounts_editor.initial_entry.get(),
                "department": self.accounts_editor.department_entry.get(),
                "office": self.accounts_editor.office_entry.get(),
                "email": self.accounts_editor.email_entry.get(),
                "bio": self.accounts_editor.bio_entry.get("1.0", "end-1c")
            }
        }
        # Send account payload to user model for processing.
        self.model.user.save_profile(self.user_to_edit, account)
        self.logger.log_info(f"ACCOUNTS - User '{self.model.user.get_username()}' has updated profile for user '{self.user_to_edit}'.")

        # Refresh Accounts Manager users list by repopulation.
        self.accounts_manager.populate_user_accounts(self.model.user.get_all_accounts())
        self._dynamic_row_binds() # Rebind each user delete and edit buttons after generating.
        self.accounts_editor.hide_view()
        # If the authenticated administrator changes own profile
        # update profile page with new data.
        if self.model.user.get_username() == self.user_to_edit:
            self._load_profile()

    def _load_and_populate_global_accounts(self):
        """
        Populates accounts list with accounts from model and binds click events to generated 
        buttons before revealing view.
        """
        self.accounts_manager.populate_user_accounts(self.model.user.get_all_accounts())
        self._dynamic_row_binds()
        self.accounts_manager.show_view()

    def _load_buttons_by_role(self):
        """
        Retreive authenticated user role and send to view to generate role specific buttons and
        bind click events to generated buttons.
        """
        role = self.model.user.get_user_role()
        self.frame.load_buttons_by_role(role)

        # Add click event binds to role generated buttons.
        self.frame.edit_button.bind("<Button-1>", lambda event: self._save_user_details())
        self.frame.edit_pw_button.bind("<Button-1>", lambda event: self.view.frames["change_password"].show_view())
        self.frame.manage_button.bind("<Button-1>", lambda event: self._load_and_populate_global_accounts())

    def _update_password(self, editor, username, isAdmin=False):
        """
        Retreives form values from editor, applies validation logic and 
        if passes sends payload to model for processing.
        """
        # Get our form values from view.
        if not isAdmin:
            old_password = editor.old_pw_entry.get()

            # Retrieve the user's account by username.
            user_account = self.model.user.get_user_by_username(username)

            # Check if the user exists in the accounts database.
            if not user_account:
                self.exception.display_error("User account not found")
                return

            # Validate the old password (only for non-admin users).
            if user_account["password"] != old_password:
                self.exception.display_error("Invalid Password")
                return

        new_password1 = editor.new1_pw_entry.get()
        new_password2 = editor.new2_pw_entry.get()

        # Validate the new passwords.
        if new_password1 != new_password2:
            self.exception.display_error("New Password Mismatch")
            return

        # Check for blank passwords.
        if not new_password1 or not new_password2:
            self.exception.display_error("New Password cannot be blank")
            return

        # Create the password payload and send it to the model for processing.
        user_account["password"] = new_password2
        self.model.user.save_user_password(username, user_account)

        editor.clear_inputs()
        editor.hide_view()

    def _save_user_password(self):
        """
        Save password initiated by authententicated user.
        """
        username = self.model.user.get_username()
        self._update_password(self.password_editor, username)
        self.logger.log_info(f"ACCOUNTS - User '{username}' has changed their own password.")

    def _save_global_pass(self):
        """
        Save password initiated by an Administrator account.
        """
        self._update_password(self.global_password_editor, self.user_to_edit, isAdmin=True)
        self.logger.log_info(f"ACCOUNTS - User '{self.model.user.get_username()}' has changed the password for user '{self.user_to_edit}'.")
        

    def _create_new_account(self):
        """
        Sends new account payload to model for creation processing.
        """
        # Retrieve new account form values.
        firstname = self.new_account.first_name_entry.get()
        lastname = self.new_account.last_name_entry.get()
        username = self.new_account.username_entry.get()
        initials = self.new_account.initial_entry.get()
        department = self.new_account.department_entry.get()
        office = self.new_account.office_entry.get()
        email = self.new_account.email_entry.get()
        role = self.new_account.role_entry.get()
        bio = self.new_account.bio_entry.get("1.0", "end-1c")
        password = self.new_account.password_entry.get()
        vpassword = self.new_account.verify_password_entry.get()

        # Fiels cannot be blank.
        if not firstname:
            self.exception.display_error("Firstname cannot be blank!")
            return
        if not lastname:
            self.exception.display_error("Lastname cannot be blank!")
            return
        if not username:
            self.exception.display_error("Username cannot be blank!")
            return
        if not email:
            self.exception.display_error("Email cannot be blank!")
            return
        if not password or not vpassword:
            self.exception.display_error("Password cannot be blank!")
            return

        # Passwords must match.
        if not password == vpassword:
            self.exception.display_error("Password Mismatch!")
            return
        
        # Create and format our new account payload.
        account = {
            "username": username,
            "password": vpassword,
            "profile_info": {
                "firstname": firstname,
                "lastname": lastname,
                "initials": initials,
                "department": department,
                "office": office,
                "email": email,
                "bio": bio,
            },
            "role": role
        }

        # Send new account payload to model for processing.
        self.model.user.add_user(account)
        self.logger.log_info(f"ACCOUNTS - User '{self.model.user.get_username()}' has created user '{username}'.")

        # Update administrative accounts manager view with new account.
        self.accounts_manager.populate_user_accounts(self.model.user.get_all_accounts())

        # Bind new buttons on account manager and hide new account view.
        self._dynamic_row_binds()
        self.new_account.hide_view()

    def _delete_user(self, event):
        """
        Removes user from accounts.
        """
        # Identify the master frame containing user's username.
        button = event.widget
        parent_frame = button.master
        grand_frame = parent_frame.master

        # Define the username selected and confirm for deletion.
        username = list(grand_frame.children.values())[3].cget("text")
        result = messagebox.askyesno("Confirmation", f"Delete user: {username}?")

        # If user confirmed send username to model for deletion processing
        # and remove from view.
        if result:
            self.model.user.delete_user(username)
            self.accounts_manager.populate_user_accounts(self.model.user.get_all_accounts())
            self.logger.log_info(f"ACCOUNTS - User '{self.model.user.get_username()}' has removed user '{username}' from accounts database.")

    def _show_user_editor(self, event):
        """
        Opens a specific users profile.
        """
        # Identify the master frame containing the user's username.
        grand_frame = event.widget.master.master

        # Retrieve the username (use of name in dictionary) selected and retrieve the user's profile from the model.
        self.user_to_edit = grand_frame.children["!ctklabel3"].cget("text")
        profile = self.model.user.get_profile_by_username(self.user_to_edit)

        # Populate the profile data into the profile view and show the view.
        self.accounts_editor.populate_fields(profile)
        self.accounts_editor.show_view()

    def _dynamic_row_binds(self):
        """
        Adds event bindings to each button of listed user rows in
        administrative accounts manager.
        """
        for d in self.accounts_manager.delete_buttons:
            d.bind("<Button-1>", lambda event: self._delete_user(event))
        for e in self.accounts_manager.edit_buttons:
            e.bind("<Button-1>", lambda event: self._show_user_editor(event))

    def _bind(self):
        """
        Private method to establish event bindings.
        Implement this method to set up event handlers and connections
        for user interactions with widgets on the view related to user accounts.
        """
        # Bind menu button.
        self.menu.accounts_button.bind("<Button-1>", lambda event: self._load_profile())

        # Bind events to password editor widgets.
        self.password_editor.cancel_button.bind("<Button-1>", lambda event: self.password_editor.hide_view())
        self.password_editor.save_button.bind("<Button-1>", lambda event: self._save_user_password())
        self.password_editor.old_pw_entry.bind("<Return>", lambda event: self._save_user_password())
        self.password_editor.new1_pw_entry.bind("<Return>", lambda event: self._save_user_password())
        self.password_editor.new2_pw_entry.bind("<Return>", lambda event: self._save_user_password())

        # Bind events to global password editor widgets.
        self.global_password_editor.cancel_button.bind("<Button-1>", lambda event: self.global_password_editor.hide_view())
        self.global_password_editor.save_button.bind("<Button-1>", lambda event: self._save_global_pass())

        # Bind events to Administrator Accounts Manager widgets.
        self.accounts_manager.cancel_button.bind("<Button-1>", lambda event: self.accounts_manager.hide_view())
        self.accounts_manager.new_user_button.bind("<Button-1>", lambda event: self.view.frames["new_account"].show_view())

        # Bind events to new account editor widgets.
        self.new_account.save_button.bind("<Button-1>", lambda event: self._create_new_account())
        self.new_account.cancel_button.bind("<Button-1>", lambda event: self.new_account.hide_view())

        # Bind events to account editor.
        self.accounts_editor.save_button.bind("<Button-1>", lambda _: self._save_user_details_manager())
        self.accounts_editor.done_button.bind("<Button-1>", lambda _: self.accounts_editor.hide_view())
        self.accounts_editor.reset_pw_button.bind("<Button-1>", lambda _: self.global_password_editor.show_view())