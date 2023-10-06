import json as j

class UserModel():
    def __init__(self):
        """
        Initialise the UserModel component of the application.

        This class represents the UserModel component of the application's MVC (Model-View-Controller) architecture.
        It initialises the models to be consumed by the controllers of this applicaiton.
        """
        self.accounts = None
        self.user_info = None
        self.is_locked = False
        self.read_accounts()

    def read_accounts(self):
        with open("./db/system/accounts.json", "r") as file:
            jsonArray = file.read()

        self.accounts = j.loads(jsonArray)

    def get_user_by_username(self, username):
        for account in self.accounts:
            if account["username"] == username:
                return True
            
        return False

    def login(self, username, password):
        for account in self.accounts:
            if account["username"] == username and account["password"] == password:
                self.user_info = account
                return True
            
        return False