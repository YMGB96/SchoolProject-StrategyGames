class database:
    def __init__(self) -> None:
        pass

import sqlite3

connection = sqlite3.connect('gamesdb.db')
cursor = connection.cursor()

sql_table_login ="""
    CREATE TABLE IF NOT EXISTS Login (
    pid_login INTEGER PRIMARY KEY,
    username VARCHAR(30),     
    pwhash VARCHAR(30),
    pwsalt VARCHAR(16)       
    );""" 
cursor.execute(sql_table_login)

#PLAIN TEXT USER NAME; SALTED HASH FOR THE PASSWORD

sql_table_scores ="""
    CREATE TABLE IF NOT EXISTS scores (
    pid INTEGER,
    username VARCHAR(30),
    gamename VARCHAR(16),
    score INT,
    difficulty INT    
    );"""
cursor.execute(sql_table_scores)


connection.commit()
connection.close()

    
