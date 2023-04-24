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

The source can be found [here](board_blitz/menu_logic.py)

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

If there is any error, the method returns a string (`str`) containing an error message, an empty string otherwise
```py
err: str = menu_logic.register("username", "password", "password")
if err:
    print("An Error has occured:")
    print(err)
else:
    print("No Error has occured")
```
Internally it generates a **random 16 byte salt**, combines it with the **encoded password** and **hashes** the reult

Both salt and the hashed product get **stored in the database** and the user id get's set to this **new user**

### **Logging in as a User**
Use the `login` method to check the account's details and set that user as the active one

If there is any error, the method returns a string (`str`) containing an error message, an empty string otherwise

```py
err: str = menu_logic.login("username", "password")
if err:
    print("An Error has occured:")
    print(err)
else:
    print("No Error has occured")
```
Generates the hashed password using the **salt from the database** and **compares the result with the stored result** from the database

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
To get a sorted leaderboard, you can use the `get_leaderboard` method and pass in the game type as an integer, a field to sort by and if the sorting should be reversed or not
```py
sorted_leaderboard: list[dict] = menu_logic.get_leaderboard(0, "username", False)
```

### **Start the Game**
To start the game, use `start_game` and pass it the game type and the difficulty as an integer
```py
menu_logic.start_game(1, 2)
```
This method tells the game logic to **start a new** game with the given **user, game type and difficulty**

## **Database**
In the file [`database.py`](board_blitz/database.py) a database named '`gamesdb.db`' is created to connect with the `SQLite3` module, two tables follow to store the login information of the registered users and to store the result values after every game finishes.

Following, some methods are defined to `add` entries to the database and to `fetch` contents from it, this methods can be called from other classes in the application.

`connection.row_factory = sqlite3.Row` was added to not only read the queried data as tuples, but to also have the corresponding keys for it.

## **Menu GUI**
Contains a class that displays the user menu and take the user's input

### **Constructor**
After running the  ```menu_gui.render() ``` function, the def  ```_init_ ```, will initialize the attributes and save all the necessary elements for the GUI. The MenuGui.class includes all the tools for designing all GUI pages and methods for each page that render its elements and are responsible for their functioning, for example,  ```draw_main_menu() ```.

### **Rendering**
Using the  ```menu_gui.render() ``` function, depending on the  ```screen_id() ``` number,
to which the corresponding menu window is assigned, it displays it.
In this case, by default, the number  ```screen_id() = 0 ```, which corresponds to the main menu, further actions of the player in the menu by pressing the corresponding buttons will change its number and menu windows accordingly.

The function will be used for rendering:<br />
       ```self.font.render()```<br />
set the text, color, and antialias values.<br />
        ```self.screen.blit()```<br />
draw the text<br />
        ```pg.Rect()```<br />
set the position of the buttons and backgrounds in the menu.<br />
        ```pg.draw.rect()```<br />
draw the buttons and backgrounds<br />
       
### **Navigate through the menu buttons **

 ```if event.type == pg.MOUSEBUTTONDOWN and event.button == 1: ```

If the user clicks on the button with the left mouse button, the menu will be navigated depending on its function.

## **Game GUI**
Contains a class that displays the game and handles the user's input

It also contains a sprite class, that is an abstration of a clickable image or text with a background

You can find it [here](board_blitz/game_gui.py)

### **Constructor**
In it's `__init__` method, most of the object's fields get set, according to the optional `width` and `height` parameters where applicable

It also takes a `difficulty` and a `playername` as arguments so that it can display the correct names

### **Rendering**
The main module calls this method, it **decides what to render** and get's all the information needed for that from the game logic

It uses **helper methods** that are explained below for **most of the rendering** but everything that is not done by said methods, this method does itself

How many **captures** to show per player and what **state** the game is in are also determined by this method

### **Ending the Game**
Calling this method sets the object's fields, so that the **game finished screen is shown**

The parameter determines if the game counts as **won or lost**

### **Variables of Note**
Like other modules, the game gui has a global variable that contains a single shared instance of the class, it is initialized as `None`

As soon as this variable is set, the `__main__` will try to call it's render method

### **Other Methods**
The following methods assist in **rendering parts of the game**

#### **Drawing the Board**
This method **draws the given board** and **handles clicks** on pieces

The only parameter is the **board** it will draw

When the mouse started getting pressed on this frame while hovering over any field of the 6x6 grid, the `selected_piece` **changes to that field**

#### **Overlay on Finished Game**
Once the game is finished, this method is used to **display an overlay**, darkening the screen and **showing the result**

#### **Drawing Names and Captures**
**Names get drawn** onto the screen according to the fields set in the constructor

The method also takes in the **amount of captures** and displays them above/below the names

#### **Drawing Rules**
**Displays the rules** according to the provided game type

The Rules are only shows while the **game is paused**


## **Game Logic**
Contains a class that handles the logic for both games.

### **Variables of Note**
The logic stores whether it currently is the **users turn**, the **user id**, which **game** is being played, the **board** state and whether or not a player is currently doing **consecutive moves** in checkers in the fields `player_turn` `user` `game` `difficulty` `board` and `consecutive move` respectively.

The logic also stores an **instance** of itself as a **global variable** in the `game_logic` field, to ensure that other modules access the same **instance**.

### **Starting a game**
Use the `start` method to start a new game. This method requires arguments for which **user** is playing, which **game** is to be played and the chosen **difficulty**
The method then sets the **board**, fetches the correct **username** from the database and instanciates both the **game gui** and the **ai**, sending the necessary information.

### **Checking which moves are possible**
The `get_valid_moves` method is used to check which moves are possible based on the rules of the chosen game. It uses the optional arguments of `chosen_piece`, a single variable in the **board** array, and `board_preview`, a hypothetical state of the **board**. When it is the **player_turn**, it returns a copy of the **board**, setting variables which show where the **chosen_piece** can move to and if it lands on an opponent piece. For checkers, it first checks if there are pieces which can jump over an opponents piece and only if this check returns no result will it check which single move the **chosen_piece** can do. It will return nothing if `consecutive_move` is true, however, to prevent the switching of board pieces.
For the AI, the method returns the `moves`array, checking for all possible **moves** based on the given **board_preview**. Again, for checkers the method first sees whether there are jumping moves available before considering any non jumping moves.
Before returning the moves to the AI, the `game_is_finished` method gets called with an argument of `valid_ai_moves_empty`as true, if the `moves`array is empty and the AI is out of moves.

### **Changing the turn**
The `switch_turn` method is to be called after a move has been made. It calls the `game_is_finished` method to see if the game is done, then it changes the variables of the **board** based on the given `move`argument, which is expected to be a tuple of two **board** positions, the first being the one where the moved piece came from, the other where it landed.
Based on the `player_turn` Bool, it either recursively calls itself again, this time with an argument calling the method which starts the **AI**, which gets a **board_preview** as an argument, or it returns nothing, allowing the Player to make their next move.
In case checkers is being played, the method also checks whether a `consecutive_move`is being made where a player may move again after beating an opponents piece, in which case it returns a new **board_preview** for the **Game Gui**, only setting the possible moves of the one valid piece, or it recursively calls itself again, this time immediatly giving a `consecutive_moves`argument to the **AI** method, an array of the only valid moves.
After every turn the **AI** makes, `game_is_finished` gets called.

### **Creating hypothetical board states**
The method `preview_move` exists to return a hypothetical **board**, called `ai_board`, based on a given `board`, `move` and whether it is a `player_move`or not, to the **AI** while its algorythm checks for the best possible outcome.

### **Checking for hypothetical player moves**
The method `player_move_list` returns an array of all possible **moves** the player could make, called `player_moves`, using a given `board`, so that the **AI**s algorythm can make use of them.

### **Checking if a game has ended**
The `game_is_finished` method is responsible for checking whether a game has ended or not, if the player has won and sending that information to the **Database**, along with the **user id**, **difficulty** and which **game** was played.
It accepts the optional arguments of `game_cancelled` and `valid_ai_moves_empty`.

It checks the following possibilities:

    - The player moved a piece to the opponents row, the player has won
    - The opponent moved a piece to the players row, the player has lost
    - The player is out of moves, the player has lost
    - `valid_ai_moves_empty` is true, the AI has no available moves, the player has won
    - `game_cancelled` is true, the player has forfeit, the player has lost
