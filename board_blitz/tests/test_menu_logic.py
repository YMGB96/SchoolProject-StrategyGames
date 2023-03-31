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
    menu_logic: MenuLogic = MenuLogic()

    @classmethod
    def setUpClass(cls):
        cls.mock_get_users = patch('database.get_users')
        cls.mock_get_users.start().return_value = cls.users

    @classmethod
    def tearDownClass(cls):
        cls.mock_get_users.stop()

    def test_missing_username(self):
        err = self.menu_logic.login("", "test")
        self.assertIsInstance(err, str)

    def test_missing_password(self):
        err = self.menu_logic.login("Susi", "")
        self.assertIsInstance(err, str)

    def test_missing_user(self):
        err = self.menu_logic.login("Sabine", "hehehe")
        self.assertIsInstance(err, str)

    def test_wrong_password(self):
        err = self.menu_logic.login("Susi", "not_lmao")
        self.assertIsInstance(err, str)

    def test_succeed(self):
        err = self.menu_logic.login("Susi", "lmao")
        self.assertIsNone(err)

class TestRegister(unittest.TestCase):
    users = [{
            "name": "Susi", # pw: "lmao"
            "user_id": "2",
            "salt": "4c7d9b6418c49f35f9371805af57f396",
            "password": "4e857af91d0359157ead176cae92fea42d693f1ee7f1f79ec2e1ed2d9b89077e"
        }]
    menu_logic: MenuLogic = MenuLogic()

    @classmethod
    def setUpClass(cls):
        cls.mock_get_users = patch('database.get_users')
        cls.mock_get_users.start().return_value = cls.users
        cls.mock_add_user = patch('database.add_user')
        cls.mock_add_user.start().return_value = True

    @classmethod
    def tearDownClass(cls):
        cls.mock_get_users.stop()
        cls.mock_add_user.stop()

    def test_missing_username(self):
        err = self.menu_logic.register("", "test", "test")
        self.assertIsInstance(err, str)

    def test_missing_password(self):
        err = self.menu_logic.register("Fredrick", "", "")
        self.assertIsInstance(err, str)

    def test_existing_user(self):
        err = self.menu_logic.register("Susi", "a_pw", "a_pw")
        self.assertIsInstance(err, str)

    def test_unmatching_password(self):
        err = self.menu_logic.register("Kurt", "password", "a_different_password")
        self.assertIsInstance(err, str)

    def test_succeed(self):
        err = self.menu_logic.register("Ben", "supersecret", "supersecret")
        self.assertIsNone(err)
