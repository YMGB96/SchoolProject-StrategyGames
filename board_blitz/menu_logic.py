from hashlib import sha256 # https://docs.python.org/3/library/hashlib.html
from os import urandom
import database

class Error:
    UNSET = "Benutzername oder Passwort können nicht leer gelassen werden"
    UNMATCH = "Das Passwort gleicht dem wiederholten Passwort nicht"
    SAVE = "Es konnte nicht gespeichert werden"
    EXISTS = "Der Name ist bereits vergeben"
    NOT_EXIST = "Dieser Nutzer existiert nicht"
    WRONG = "Falsches Passwort"
    UNKNOWN = "Etwas ist schief gegangen"

active_user: int = 0

def register(username: str, password: str, repeated_password: str) -> str:
    """Register a new user - returns str on error and None on súccess"""
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
    # set active user id and return no error
    active_user = user_id
    return None

def login(username: str, password: str) -> str:
    """Log in with username and password - returns str on error and None on success"""
    if not username or not password: return Error.UNSET
    # get user with matching username
    users: list[dict] = database.get_users()
    try:
        user = next(filter( # https://stackoverflow.com/questions/8534256/find-first-element-in-a-sequence-that-matches-a-predicate
            lambda user:
                user["name"] == username,
            users))
    except: return Error.NOT_EXIST
    # compare passwords
    salt = bytes.fromhex(user["salt"])
    hashed = sha256(salt + password.encode())
    hashed_password: str = hashed.hexdigest()
    if user["password"] != hashed_password:
        return Error.WRONG
    # return user id if login was successful
    active_user = user["user_id"]
    return None
