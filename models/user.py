import json as j
import sqlite3
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
        self.connection = None

    def connect_to_db(self):
        """
        Connect to the SQLite database with the provided password.
        """
        try:
            self.connection = sqlite3.connect("./db/system/data.db")
            self.connection.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            print("Error connecting to the database:", str(e))

    def close_db_connection(self):
        """
        Close the SQLite database connection.
        """
        if self.connection:
            self.connection.close()

    def get_user_by_username(self, username):
        '''
        Retrieve user from the database if it exists.

        Parameters:
        username (str): Plain username as a string.

        Returns:
        bool: True if the user exists, False if not.
        '''
        self.connect_to_db()

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT username, password FROM users")
            encrypted_users = cursor.fetchall()

            for user in encrypted_users:
                decrypted_username = self.decrypt(user[0])
                decrypted_password = self.decrypt(user[1])
                if decrypted_username == username:
                    return {
                        "username": decrypted_username,
                        "password": decrypted_password
                    }

        except sqlite3.Error as e:
            print("Error checking user existence:", str(e))
        finally:
            self.close_db_connection()

        return False  # If no user or error, return False.
    
    def get_user_role(self):
        """
        Return authenticated user role.
        """
        self.connect_to_db()

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT username, role FROM users")
            encrypted_users = cursor.fetchall()

            for user in encrypted_users:
                decrypted_username = self.decrypt(user[0])
                if decrypted_username == self.user:
                    return self.decrypt(user[1])

        except sqlite3.Error as e:
            print("Error checking user role:", str(e))
        finally:
            self.close_db_connection()

        return False  # If no user or error, return False.
    
    def get_username(self):
        """
        Return authenticated user username.
        """
        return self.user
    
    def get_profile_by_username(self, username):
        """
        Return authenticated user profile from the 'profiles' table using decrypted username.

        Parameters:
        username (str): Plain username as a string.

        Returns:
        dict: Dictionary containing user profile data.
        """
        self.connect_to_db()

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, username, role FROM users")
            encrypted_users = cursor.fetchall()

            for user in encrypted_users:
                decrypted_username = self.decrypt(user[1])
                if decrypted_username == username:
                    # If the decrypted username matches the provided username,
                    # query the 'profiles' table to fetch the profile info.
                    cursor.execute("SELECT * FROM profiles WHERE user_id = ?", (user[0],))
                    profile_row = cursor.fetchone()

                    if profile_row:
                        return {
                            "firstname": self.decrypt(profile_row["firstname"]),
                            "lastname": self.decrypt(profile_row["lastname"]),
                            "username": username,
                            "role": self.decrypt(user["role"]),
                            "initials": self.decrypt(profile_row["initials"]),
                            "department": self.decrypt(profile_row["department"]),
                            "office": self.decrypt(profile_row["office"]),
                            "email": self.decrypt(profile_row["email"]),
                            "bio": self.decrypt(profile_row["bio"])
                        }

        except sqlite3.Error as e:
            print("Error retrieving user profile from the database:", str(e))
        finally:
            self.close_db_connection()

        # Return an empty dictionary or None if no matching profile is found.
        return {}
    
    def get_all_accounts(self):
        """
        Return all accounts.
        """
        self.connect_to_db()
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT profiles.*, users.username, users.role FROM profiles JOIN users ON profiles.user_id = users.id")
            rows = cursor.fetchall()

            decrypted_profiles = []
            for row in rows:
                decrypted_profile = {
                    "firstname": self.decrypt(row["firstname"]),
                    "lastname": self.decrypt(row["lastname"]),
                    "username": self.decrypt(row["username"]),
                    "role": self.decrypt(row["role"]),
                    "initials": self.decrypt(row["initials"]),
                    "department": self.decrypt(row["department"]),
                    "office": self.decrypt(row["office"]),
                    "email": self.decrypt(row["email"]),
                    "bio": self.decrypt(row["bio"])
                }
                decrypted_profiles.append(decrypted_profile)

            return decrypted_profiles

        except sqlite3.Error as e:
            print("Error reading accounts from the database:", str(e))
        finally:
            self.close_db_connection()

    def add_user(self, user):
        """
        Add a new user to the accounts store and write to the database.

        Parameters:
        user (dict): Dictionary containing user data, including username, password, role, and profile_info.
        """
        self.connect_to_db()
    
        try:
            cursor = self.connection.cursor()
            
            # Insert a new user
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?);",
                        (self.encrypt(user["username"]), self.encrypt(user["password"]), self.encrypt(user["role"])))
            
            # Get the user_id of the newly inserted user
            user_id = cursor.lastrowid
            
            # Insert a new profile associated with the user
            cursor.execute("INSERT INTO profiles (user_id, firstname, lastname, initials, department, office, email, bio) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
                        (user_id, self.encrypt(user["profile_info"]["firstname"]), self.encrypt(user["profile_info"]["lastname"]), self.encrypt(user["profile_info"]["initials"]),
                            self.encrypt(user["profile_info"]["department"]), self.encrypt(user["profile_info"]["office"]), self.encrypt(user["profile_info"]["email"]), self.encrypt(user["profile_info"]["bio"])))
            
            self.connection.commit()
            
        except sqlite3.Error as e:
            print("Error adding user and profile:", str(e))
        finally:
            self.close_db_connection()

    def delete_user(self, username):
        """
        Delete a user and their corresponding profile from the database by their plain (decrypted) username.
        """
        self.connect_to_db()
        try:
            cursor = self.connection.cursor()

            # Decrypt the usernames in the database and check for a match.
            cursor.execute("SELECT id, username FROM users")
            rows = cursor.fetchall()

            for row in rows:
                db_id = row["id"]
                db_username = self.decrypt(row["username"])
                if db_username == username:
                    # Delete the user's profile first (assuming there's a foreign key relationship).
                    cursor.execute("DELETE FROM profiles WHERE user_id = ?", (db_id,))
                    cursor.execute("DELETE FROM users WHERE id = ?", (db_id,))
                    self.connection.commit()
                    break
        except sqlite3.Error as e:
            print("Error deleting user and profile from the database:", str(e))
        finally:
            self.close_db_connection()
    
    def save_profile(self, username, profile):
        """
        Save specified user profile and write to the database.

        Parameters:
        user (str): Plain username as a string.
        profile (dict): Dictionary of key values representing user profile.
        """
        self.connect_to_db()

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, username FROM users")
            encrypted_users = cursor.fetchall()

            for user in encrypted_users:
                decrypted_username = self.decrypt(user[1])
                if decrypted_username == username:
                    # If the decrypted username matches the provided username,
                    # query the 'profiles' table to fetch the profile info.
                    cursor.execute("UPDATE profiles SET firstname = ?, lastname = ?, initials = ?, department = ?, office = ?, email = ?, bio = ? WHERE user_id = ?", 
                                (self.encrypt(profile["profile_info"]["first"]), self.encrypt(profile["profile_info"]["last"]), self.encrypt(profile["profile_info"]["initials"]),
                                    self.encrypt(profile["profile_info"]["department"]), self.encrypt(profile["profile_info"]["office"]), self.encrypt(profile["profile_info"]["email"]),
                                    self.encrypt(profile["profile_info"]["bio"]), user[0]))

                    self.connection.commit()
        except sqlite3.Error as e:
            print("Error retrieving user profile from the database:", str(e))
        finally:
            self.close_db_connection()

        # Return an empty dictionary or None if no matching profile is found.
        return {}

    def save_user_password(self, username, data):
        """
        Save specified user password and write to the database.

        Parameters:
        user (str): Plain username as a string.
        data (dict): Dictionary of key values.
        """
        self.connect_to_db()
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT username FROM users")
            rows = cursor.fetchall()

            for row in rows:
                db_username = row["username"]
                if self.decrypt(db_username) == username:
                    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (self.encrypt(data["password"]), db_username))
                    self.connection.commit()
                    break
        except sqlite3.Error as e:
            print("Error deleting user from the database:", str(e))
        finally:
            self.close_db_connection()

    def login(self, username, password):
        '''
        Authenticates the user against the database.

        Parameters:
        username (str): Plain username as a string.
        password (str): Plain password as a string.

        Returns:
        bool: True if authentication succeeds, False if not.
        '''
        '''
        Retrieve user from the database if it exists.

        Parameters:
        username (str): Plain username as a string.

        Returns:
        bool: True if the user exists, False if not.
        '''
        self.connect_to_db()

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT username, password FROM users")
            encrypted_users = cursor.fetchall()

            for user in encrypted_users:
                decrypted_username = self.decrypt(user[0])
                decrypted_password = self.decrypt(user[1])
                if decrypted_username == username and decrypted_password == password:
                    self.user = decrypted_username
                    return True

        except sqlite3.Error as e:
            print("Error checking user existence:", str(e))
        finally:
            self.close_db_connection()

        return False  # If no user or error, return False.

    
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