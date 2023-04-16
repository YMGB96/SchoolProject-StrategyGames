# **Technical Documentation**
**Technical details** like interfaces and important variables will be explained in this technical documentation

## **Tests**
Tests are there to ensure that all nessecary logic still works correctly so a developer can quickly see the effects of their changes

### **Starting the Tests**
To run the tests, you first need to `cd` into the package directory using:
```bash
cd board_blitz
```
Then you can start the tests by running:
```bash
python -m unittest tests
```
For subsequent runs of the tests, you don't need to `cd` again since you are allready in the correct folder

### **Adding a Test**
1. Create a file called `test_<filename>.py`
2. In that file, import the test framework using:
    ```py
    import unittest
    ```
3. Create a class for each endpoint you want to test (each function/method that you want to test), call it `Test<FunctionName>` and have it extend `unittest.TestCase` so it is seen as a test case by the framework
    ```py
    class TestMyFunction(unittest.TestCase):
    ```
4. Now you can set up the different ways this function should be tested by creating methods, that are called `test_<thing_to_test>`
    ```py
    def test_first_error(self):
    ```
5. To test if your function gives the correct output, you can use the [assetion methods](https://docs.python.org/3/library/unittest.html#assert-methods) provided by the framework
6. Finally, go into the [`/tests/__init__`](board_blitz/tests/__init__.py) file and import your classes:
    ```py
    from tests.test_my_file import *
    ```
You can look at [this file](board_blitz/tests/test_menu_logic.py) for an example

### **Mocking a Function call**
You might be **calling a function** that you don't want to test the functionality of or that you need a **specific output** from, then you can redirect or change that function call in your tests

First, import `patch` from the `unittest.mock` module:
```py
from unittest.mock import patch
```

Use the `setUpClass` classmethod to start a mock and make sure to stop it in the `tearDownClass` classmethod
```py
@classmethod
def setUpClass(cls):
    cls.mock_do_something = patch('database.do_something')
    cls.mock_do_something.start().return_value = True

@classmethod
def tearDownClass(cls):
    cls.mock_do_something.stop()
```

## **Menu Logic**
Contains a class that handles the logic of everything **outside of the game**, from registration and login to the leaderboard

### **How to use**
To talk to any part of the menu logic, you can import it the variable `menu_logic` of type `MenuLogic` using the following line:
```py
from menu_logic import menu_logic
```

### **Variables of Note**
To store the active **user**, **game** that is to be played and the ais **difficulty**, the fields `active_user`, `active_game` and `active_difficulty` are used

The file also has the **global variable** `menu_logic`, that is an **instance** of the featured `MenuLogic` **class**, so that other modules can easily access the **same instance**

### **Registering a User**
Use the `register` method, to register a user and set them as the active user

If there is any error, the method returns a string (`str`) containing an error message, `None` otherwise
```py
err: str = menu_logic.register("username", "password", "password")
if err:
    print("An Error has occured:")
    print(err)
else:
    print("No Error has occured")
```

### **Logging in as a User**
Use the `login` method to check the account's details and set that user as the active one

If there is any error, the method returns a string (`str`) containing an error message, `None` otherwise

```py
err: str = menu_logic.login("username", "password")
if err:
    print("An Error has occured:")
    print(err)
else:
    print("No Error has occured")
```

### **Hashing Passwords**
When registering a user, the `salt` is set to a random sequence of bytes

The entered plain text `password` then gets encoded into bytes, added onto the salt and **hashed using SHA-256**

Both the `salt` and the combined, hashed `password` get stored as hex strings in the database

When loggin in, and the username is matching, the plain text `password` the user typed in and the `salt` form the database get added onto one another and hashed

If the **resulting hash matches the hashed `password` from the database**, the user is logged in

Because of the `salt`, even passwords that are the same, won't look the same in the database, **increasing security**

### **Logging out**
To log out a user, you can call the `logout` method, it just resets the active user
```py
menu_logic.logout()
```

### **Get a sorted Leaderboard**
To get a sorted leaderboard, you can use the `get_leaderboard` method and pass in a field to sort by and if the sorting should be reversed or not
```py
sorted_leaderboard: list[dict] = menu_logic.get_leaderboard("name", False)
```

### **Start the Game**
To start the game, you first need to set the game type using the method `set_game` and the diffuculty using the method `set_difficulty`

Then you can start the game using `start_game`
```py
menu_logic.set_game(1)
menu_logic.set_difficulty(2)
menu_logic.start_game()
```
