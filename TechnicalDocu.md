# **Technical Documentation**
In this documentation, technical details will be explained

## **Menu Logic**
### **How to use**
To talk to any part of the menu logic, you can import it the variable `menu_logic` of type `MenuLogic` using the following line:
```py
from menu_logic import menu_logic
```

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
Use the `login` method to check the accounts details and set that user as the active one

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

The entered plain text `password` then gets encoded into bytes, added onto the salt and hashed using SHA-256

Both the `salt` and the combined, hashed `password` get stored as hex strings in the database

When loggin in and the username is matching, the plain text `password`, that the user typed in, and the `salt` form the database, get added onto one another and hashed

If the resulting hash matches the `password` from the database, the user is logged in.

Because of the `salt`, even passwords that are the same, won't look the same in the database, increasing security

### **Get a sorted Leaderboard**
To get a sorted leaderboard, you can use the `get_leaderboard` method and pass in a field to sort by and if the sorting should be reversed or not
```py
sorted_leaderboard: list[dict] = menu_logic.get_leaderboard("name", False)
```

### **Logging out**
To log out a user, you can call the `logout` method, it just resets the active user
```py
menu_logic.logout()
```

### **Start the Game**
To start the game, you first need to set the game type using the method `set_game` and the diffuculty using the method `set_difficulty`

Then you can start the game using `start_game`
```py
menu_logic.set_game(1)
menu_logic.set_difficulty(2)
menu_logic.start_game()
```
