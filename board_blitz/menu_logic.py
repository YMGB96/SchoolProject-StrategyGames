from hashlib import sha256 # https://docs.python.org/3/library/hashlib.html
from os import urandom
import database
import game_logic

class Error:
    UNSET = "Benutzername oder Passwort können nicht leer gelassen werden"
    UNMATCH = "Das Passwort gleicht dem wiederholten Passwort nicht"
    SAVE = "Es konnte nicht gespeichert werden"
    EXISTS = "Der Name ist bereits vergeben"
    NOT_EXIST = "Dieser Nutzer existiert nicht"
    WRONG = "Falsches Passwort"
    UNKNOWN = "Etwas ist schief gegangen"

class MenuLogic:
    active_user: int = 0
    active_game: int = 0
    active_difficulty: int = 0

    def register(self, username: str, password: str, repeated_password: str) -> str:
        """Register a new user - returns str on error and None on success"""
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
            uid: int = int(user.get("user_id"))
            if uid > user_id: user_id = uid
        user_id += 1
        # save registration to database, return error if it fails
        if not database.add_user(user_id, username, hashed_password, salt.hex()):
            return Error.SAVE
        # set active user id and return no error
        self.active_user = user_id
        return None

    def login(self, username: str, password: str) -> str:
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
        # set active user if login was successful
        self.active_user = int(user["user_id"])
        return None

    def logout(self):
        """Resets the user"""
        self.active_user = 0

    def set_difficulty(self, difficulty): self.active_difficulty = difficulty
    def set_game(self, game: int): self.active_game = game

    def start_game(self):
        """Start the game, this expects difficulty and game to be set"""
        game_logic.start(self.active_user, self.active_game, self.active_difficulty)

    def get_leaderboard(self, sort_by: str, reverse: bool) -> list[dict]:
        """Get a sorted leaderboard to be displayed"""
        leaderboard: list[dict] = database.get_leaderboard()
        users: list[dict] = database.get_users()
        # Add name of user with matching id to leaderboard entries
        for entry in leaderboard:
            entry["name"] = next(filter(
                lambda user:
                    user["user_id"] == entry["user_id"],
                users
                ))["name"]
        leaderboard.sort(
            # sort leaderboard by value of the key 'sort_by'
            key=lambda entry: entry.get(sort_by),
            reverse=reverse)
        return leaderboard

menu_logic: MenuLogic = MenuLogic()
