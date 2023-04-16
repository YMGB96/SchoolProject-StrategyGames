class database:
    def __init__(self) -> None:
        pass

import sqlite3

connection = sqlite3.connect('gamesdb.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

sql_table_login ="""
    CREATE TABLE IF NOT EXISTS Login (
    pid_login INTEGER PRIMARY KEY,
    username VARCHAR(30),
    pwhash VARCHAR(64),
    pwsalt VARCHAR(32)
    );""" 
#PLAIN TEXT USER NAME; SALTED HASH FOR THE PASSWORD
cursor.execute(sql_table_login)

sql_table_scores ="""
    CREATE TABLE IF NOT EXISTS scores (
    pid INTEGER,
    username VARCHAR(30),
    gamename VARCHAR(16),
    difficulty INTEGER, 
    game_won INTEGER 
    );"""
cursor.execute(sql_table_scores)

#difficulty:  1 = leicht / 2 = mittel / 3 = schwer
#game_won: 0 = FALSE lost / 1 = TRUE won, no boolean type in SQLite

connection.commit()
connection.close()



#Function to add score to the leaderboard
# def add_leaderboard_entry(pid, difficulty, gamename, game_won):
#   connection = sqlite3.connect('gamesdb.db')
#   connection.row_factory = sqlite3.Row    
#   cursor = connection.cursor()
#   cursor.execute('INSERT INTO scores(pid, username, gamename, difficulty, game_won) VALUES (?, ?, ?, ?, ?)', (pid, username, gamename, difficulty, game_won))
# connection.commit()
# connection.close()




# SQL command to order the Leaderboard, to be called in the GUI menu "show highscores" 
# def get_leaderboard(difficulty):
#   connection = sqlite3.connect('gamesdb.db')
#   connection.row_factory = sqlite3.Row
#   cursor = connection.cursor()
#   cursor.execute('SELECT Login.username, scores.gamename, scores.difficulty, scores.game_won \
#   FROM Login INNER JOIN scores ON Login.pid_login = scores.pid \
#   WHERE scores.difficulty = ? \
#   ORDER BY scores.gamename DESC, scores.game_won DESC LIMIT 15', (difficulty,)) 
#   rows = cursor.fetchall()
#   connection.commit()
#   connection.close()
#   return rows
