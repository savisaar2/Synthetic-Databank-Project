import json as j
from cryptography.fernet import Fernet

class UserModel():
    def __init__(self):
        """
        Initialise the UserModel component of the application.

        This class represents the UserModel component of the application's MVC (Model-View-Controller) architecture.
        It initialises the models to be consumed by the controllers of this applicaiton.
        """
        # Define a secret to be used for encryption activities.
        key = b'net5Gs6Mt6-guRLj-o7r4nmCgXOA8_RUnOKvkXoROdk='
        self.cipher = Fernet(key)   # Initilise the cipher.
        self.accounts = None        # Holds all accounts for reference.
        self.user_info = None       # Holds authenticated user info.

        # Accounts should be read on initialise.
        self.read_accounts()

    def read_accounts(self):
        '''
        Opens and reads accounts json file.
        '''
        with open("./db/system/accounts.json", "r") as file:
            jsonArray = file.read()

        self.accounts = j.loads(jsonArray)

    def write_accounts(self):
        '''
        Opens and writes to accounts json file.
        '''
        with open('./db/system/accounts.json', 'w') as file:
            j.dump(self.accounts, file)

        self.read_accounts()

    def get_user_by_username(self, username):
        '''
        Retrieve user from the accounts dictionary if exists.

        Parameters
        ----------
        username : str
            Plain username as string.
        '''
        for account in self.accounts:
            if account["username"] == username:
                return True
            
        return False # If no user return False.
    
    def get_user_role(self):
        """
        Return authenticated user role.
        """
        return self.user_info["role"]
    
    def get_username(self):
        """
        Return authenticated user username.
        """
        return self.user_info["username"]
    
    def get_profile_by_username(self, username):
        """
        Return authenticated user profile.

        Parameters
        ----------
        username : str
            Plain username as string.
        """
        for account in self.accounts:
            if account["username"] == username:
                return account
    
    def get_all_accounts(self):
        """
        Return all accounts.
        """
        return self.accounts
    
    def add_user(self, user):
        """
        Add a new user to the accounts store and writes to file.
        """
        account = user
        account["password"] = self.encrypt(account["password"])
        self.accounts.append(user)

        self.write_accounts()

    def delete_user(self, username):
        """
        Deletes a user from the accounts store and writes to file.

        Parameters
        ----------
        username : str
            Plain username as string.
        """
        for account in self.accounts:
            if account["username"] == username:
                self.accounts.remove(account)

        self.write_accounts()
    
    def save_profile(self, user, profile):
        """
        Save specified user profile and write to file.

        Parameters
        ----------
        user : str
            Plain username as string.
        profile: dict
            Dictionary of key values representing user profile.
        """
        for account in self.accounts:
            if account["username"] == user:
                account["profile_info"] = profile["profile_info"]
                if "username" in profile:
                    account["username"] = profile["username"]
                if user == self.get_username():
                    self.profile = profile["profile_info"]
                if "role" in profile:
                    account["role"] = profile["role"]
                break

        self.write_accounts()

    def save_user_password(self, user, data):
        """
        Save specified user password and write to file.

        Parameters
        ----------
        user : str
            Plain username as string.
        data : dict
            Dictionary of key values.
        """
        info = data
        info["password"] = self.encrypt(info["password"])
        for account in self.accounts:
            if account["username"] == user:
                self.accounts.remove(account)
                self.accounts.append(data)
                break
        
        self.write_accounts()

    def login(self, username, password):
        '''
        Authenticates user against accounts dictionary.

        Parameters
        ----------
        username : str
            Plain username as string.
        password : str
            Plain password as string.
        '''
        # Loop through accoutns and find match.
        for account in self.accounts:
            if account["username"] == username and self.decrypt(account["password"]) == password:
                self.user_info = account
                return True
            
        return False # If no match return False.
    
    def encrypt(self, data):
        '''
        Encrypts a value to an unreadable byte format.

        Parameters
        ----------
        data : str|int
            Value to be encrypted.
        '''
        encrypted_data = self.cipher.encrypt(data.encode('utf-8')).decode('utf-8')
        return encrypted_data
    
    def decrypt(self, data):
        '''
        Decrypts a value to from unreadable byte format to human readable.

        Parameters
        ----------
        data : byte
            Value to be decrypted.
        '''
        decrypted_data = self.cipher.decrypt(data)
        return decrypted_data.decode('utf-8')