import pytest
from models.user import UserModel
import sqlite3

class TestUserModel:
    # Mock the SQLite database using an in-memory database (for testing purposes)
    @pytest.fixture
    def user_model(self):
        user_model = UserModel()
        user_model.connection = sqlite3.connect(':memory:')
        return user_model

    def test_get_user_by_username(self, user_model):
        # Add a user to the in-memory database for testing
        user = {
            "username": "testuser",
            "password": "testpassword",
            "role": "user",
            "profile_info": {
                "firstname": "testfirst",
                "lastname": "testlast",
                "initials": "Mr",
                "department": "testdept",
                "office": "testoffice",
                "email": "test@test.com",
                "bio": "testbio"
            }
        }
        user_model.add_user(user)

        # Test getting a user by username
        result = user_model.get_user_by_username("testuser")
        assert result["username"] == "testuser"
        assert result["password"] == "testpassword"

    def test_get_user_role(self, user_model):
        # Add a user to the in-memory database for testing
        user = {
            "username": "testuser",
            "password": "testpassword",
            "role": "user",
            "profile_info": {
                "firstname": "testfirst",
                "lastname": "testlast",
                "initials": "Mr",
                "department": "testdept",
                "office": "testoffice",
                "email": "test@test.com",
                "bio": "testbio"
            }
        }
        user_model.add_user(user)

        # Test getting the user role
        user_model.user = "testuser"
        result = user_model.get_user_role()
        assert result == "user"

    def test_login(self, user_model):
        # Add a user to the in-memory database for testing
        user = {
            "username": "testuser",
            "password": "testpassword",
            "role": "user",
            "profile_info": {
                "firstname": "testfirst",
                "lastname": "testlast",
                "initials": "Mr",
                "department": "testdept",
                "office": "testoffice",
                "email": "test@test.com",
                "bio": "testbio"
            }
        }
        user_model.add_user(user)

        # Test user login
        result = user_model.login("testuser", "testpassword")
        assert result is True

    def test_encrypt_decrypt(self):
        user_model = UserModel()

        # Test encryption and decryption
        original_data = "test_data"
        encrypted_data = user_model.encrypt(original_data)
        decrypted_data = user_model.decrypt(encrypted_data)
        assert decrypted_data == original_data
