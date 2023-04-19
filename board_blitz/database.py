import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('gamesdb.db')
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        sql_table_login ="""
        CREATE TABLE IF NOT EXISTS Login (
        user_id INTEGER PRIMARY KEY,
        username VARCHAR(30),
        hashed_password CHAR(64),
        salt CHAR(32)
        );""" 
        #PLAIN TEXT USER NAME; SALTED HASH FOR THE PASSWORD
        self.cursor.execute(sql_table_login)


        sql_table_scores = """
        CREATE TABLE IF NOT EXISTS scores (        
            pid INTEGER,
            gamename INTEGER,
            difficulty INTEGER,
            game_won INTEGER
            );"""

        self.cursor.execute(sql_table_scores)

        self.connection.commit()
    
    # Function to add score to the leaderboard
    def add_leaderboard_entry(self, pid, difficulty, gamename, game_won):
        self.cursor.execute('INSERT INTO scores(pid, gamename, difficulty, game_won) VALUES (?, ?, ?, ?);', (pid, gamename, difficulty, game_won))
        self.connection.commit()
    
    # SQL command to be called in the menu "show highscores" 
    def get_leaderboard(self, gamename):
        self.cursor.execute("""SELECT Login.username, scores.gamename, scores.difficulty, scores.game_won
        FROM Login INNER JOIN scores ON Login.user_id = scores.pid 
        WHERE scores.gamename = ?;""", (gamename,))
        return self.cursor.fetchall()
    
    # SQL command to fetch all users in the login table
    def get_users(self):
        self.cursor.execute("""SELECT user_id, username, hashed_password, salt FROM Login;""")
        return self.cursor.fetchall()
    
    # SQL command to fetch one user from the login table
    def get_user(self, username):
        self.cursor.execute("""SELECT user_id FROM Login WHERE username = ?;""", (username,))
        return self.cursor.fetchone()

    # Function to add user to the login table
    def add_user(self, user_id, username, password, salt):
        self.cursor.execute('INSERT INTO Login(user_id, username, hashed_password, salt) VALUES (?, ?, ?, ?);', (user_id, username, password, salt))
        self.connection.commit()
    
    def close(self):
        self.connection.close()

database = Database()

#difficulty:  1 = leicht / 2 = mittel / 3 = schwer
#game_won: win, lose, giveup; 0 or 1
