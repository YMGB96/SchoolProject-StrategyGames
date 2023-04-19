from hashlib import sha256 # https://docs.python.org/3/library/hashlib.html
from os import urandom
from database import database
from game_logic import game_logic

class Error:
    UNSET = "Benutzername oder Passwort können nicht leer gelassen werden"
    UNMATCH = "Das Passwort gleicht dem wiederholten Passwort nicht"
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
            if user['username'] == username:
                return Error.EXISTS
            uid: int = int(user['user_id'])
            if uid > user_id: user_id = uid
        user_id += 1
        # save registration to database
        database.add_user(user_id, username, hashed_password, salt.hex())
        # set active user id and return no error
        self.active_user = user_id
        return ''

    def login(self, username: str, password: str) -> str:
        """Log in with username and password - returns str on error and None on success"""
        if not username or not password: return Error.UNSET
        # get user with matching username
        users: list[dict] = database.get_users()
        try:
            user = next(filter( # https://stackoverflow.com/questions/8534256/find-first-element-in-a-sequence-that-matches-a-predicate
                lambda user:
                    user['username'] == username,
                users))
        except: return Error.NOT_EXIST
        # compare passwords
        salt = bytes.fromhex(user['salt'])
        hashed = sha256(salt + password.encode())
        hashed_password: str = hashed.hexdigest()
        if user['hashed_password'] != hashed_password:
            return Error.WRONG
        # set active user if login was successful
        self.active_user = int(user['user_id'])
        return ''

    def logout(self):
        """Resets the user"""
        self.active_user = 0

    def set_difficulty(self, difficulty): self.active_difficulty = difficulty
    def set_game(self, game: int): self.active_game = game

    def start_game(self):
        """Start the game, this expects difficulty and game to be set"""
        game_logic.start(self.active_user, self.active_game, self.active_difficulty)

    def get_leaderboard(self, game_id: int, sort_by: str, reverse: bool) -> list[dict]:
        """Get a sorted leaderboard to be displayed"""
        # Get all rated games from the database
        games: list[dict] = database.get_leaderboard(game_id)
        # (username, gamename, difficulty, game_won) ==>> (username, easy, normal, hard)
        users = {}
        for game in games:
            if game['gamename'] != game_id:
                continue
            user = users.get(game['username'])
            if not user:
                user = users[game['username']] = {
                    'username': game['username'],
                    'easy': '0',
                    'normal': '0',
                    'hard': '0',
                }
            a = game['game_won'] or -1 # define what to add
            match game['difficulty']:
                case 0: user['easy'] = str(int(user['easy']) + a)
                case 1: user['normal'] = str(int(user['normal']) + a)
                case 2: user['hard'] = str(int(user['hard']) + a)
        # convert dict to list containing only the values
        leaderboard = [entry for _, entry in users.items()]
        # Add name of user with matching id to leaderboard entries
        leaderboard.sort(
            # sort leaderboard by value of the key 'sort_by'
            key=lambda entry: entry[sort_by or 'username'],
            reverse=reverse)
        return leaderboard

menu_logic: MenuLogic = MenuLogic()
