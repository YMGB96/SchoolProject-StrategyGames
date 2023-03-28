from hashlib import sha256 # https://docs.python.org/3/library/hashlib.html
from os import urandom
from typing import Union
import database

# function that registers a new user
def register(username: str, password: str, repeated_password: str) -> Union[str, int]:
    if not username or not password: return Error.UNSET
    if password != repeated_password: return Error.UNMATCH
    # generate a salt, to offset the password randomly
    salt: bytes = urandom(16)
    # hash salt and password
    hashed = sha256(salt + password.encode())
    hashed_password: str = hashed.hexdigest()
    # create unique user id
    user_id: int = 0
    users: list[dict] = database.get_users()
    for user in users:
        if user.get("name") == username:
            return Error.EXISTS
        uid: int = user.get("user_id")
        if uid > user_id: user_id = uid
    user_id += 1
    # save registration to database, return error if it fails
    if not database.add_login(user_id, username, hashed_password, salt.hex()):
        return Error.SAVE
    # return user id if it succeeded
    return user_id

class Error:
    UNSET = "Benutzername oder Passwort können nicht leer gelassen werden"
    UNMATCH = "Das Passwort gleicht dem wiederholten Passwort nicht"
    SAVE = "Es konnte nicht gespeichert werden"
    EXISTS = "Der Name ist bereits vergeben"
    UNKNOWN = "Etwas ist schief gegangen"
