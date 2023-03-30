import unittest # https://docs.python.org/3/library/unittest.html
from unittest.mock import patch # https://docs.python.org/3/library/unittest.mock.html
from menu_logic import MenuLogic

class TestLogin(unittest.TestCase):
    users = [{
            "name": "Susi", # pw: "lmao"
            "user_id": "2",
            "salt": "4c7d9b6418c49f35f9371805af57f396",
            "password": "4e857af91d0359157ead176cae92fea42d693f1ee7f1f79ec2e1ed2d9b89077e"
        }]
    
    @patch("database.get_users")
    def test_missing_username(self, mocked_get_users):
        mocked_get_users.return_value = self.users
        menu_logic: MenuLogic = MenuLogic()
        err = menu_logic.login("", "test")
        self.assertIsInstance(err, str)
    
    @patch("database.get_users")
    def test_missing_password(self, mocked_get_users):
        mocked_get_users.return_value = self.users
        menu_logic: MenuLogic = MenuLogic()
        err = menu_logic.login("Susi", "")
        self.assertIsInstance(err, str)
    
    @patch("database.get_users")
    def test_missing_user(self, mocked_get_users):
        mocked_get_users.return_value = self.users
        menu_logic: MenuLogic = MenuLogic()
        err = menu_logic.login("Sabine", "hehehe")
        self.assertIsInstance(err, str)
    
    @patch("database.get_users")
    def test_wrong_password(self, mocked_get_users):
        mocked_get_users.return_value = self.users
        menu_logic: MenuLogic = MenuLogic()
        err = menu_logic.login("Susi", "not_lmao")
        self.assertIsInstance(err, str)
    
    @patch("database.get_users")
    def test_succeed(self, mocked_get_users):
        mocked_get_users.return_value = self.users
        menu_logic: MenuLogic = MenuLogic()
        err = menu_logic.login("Susi", "lmao")
        self.assertIsNone(err)
