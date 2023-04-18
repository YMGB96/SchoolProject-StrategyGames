import sqlite3

class Database:
    def __init__(self) -> None:
        pass
    connection = sqlite3.connect('gamesdb.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    sql_table_login ="""
    CREATE TABLE IF NOT EXISTS Login (
    user_id INTEGER PRIMARY KEY,
    username VARCHAR(30),
    hashed_password VARCHAR(64),
    salt VARCHAR(32)
    );""" 
    #PLAIN TEXT USER NAME; SALTED HASH FOR THE PASSWORD
    cursor.execute(sql_table_login)


    sql_table_scores = """
    CREATE TABLE IF NOT EXISTS scores (        
        pid INTEGER PRIMARY KEY,
        username VARCHAR(30),
        gamename VARCHAR(30),
        difficulty INTEGER,
        game_won INTEGER
        );"""

    cursor.execute(sql_table_scores)

    connection.commit()
    connection.close()

#difficulty:  1 = leicht / 2 = mittel / 3 = schwer
#game_won: win, lose, giveup
