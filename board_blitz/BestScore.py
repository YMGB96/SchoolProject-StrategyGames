import pygame as pg
pg.init()
screen_bestenliste = pg.display.set_mode((1080, 800))
pg.display.set_caption("Bestenliste")
icon = pg.image.load("images/211667_a_controller_game_icon.png")
pg.display.set_icon(icon)
HEIGHT = 1080
WIDTH = 800
FPS = 60
def getTableScores():
    import sqlite3
    connection = sqlite3.connect('gamesdb.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    connection = sqlite3.connect('gamesdb.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    truncate_table = "drop table scores"
    cursor.execute(truncate_table)
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
    data = [
    (1, "playername1", 5, 1, 1),
    (2, "playername2", 5, 2, 1),
    (3, "playername3", 5, 3, 1),
    (4, "playername4", 5, 3, 1),
    (5, "playername5", 5, 3, 1)
    ]
    cursor.executemany("INSERT or REPLACE INTO scores (pid, username, gamename, difficulty, game_won) VALUES(?, ?, ?, ?, ?)", data)
    connection.commit()
    cursor.execute("SELECT * FROM scores")
    input = cursor.fetchall()
    connection.commit()
    connection.close()
    return input
rows = getTableScores()
#Fonts
FONT_titel = pg.font.Font("Schriftart/Staatliches.ttf", 90)
FONT_buttons = pg.font.Font("Schriftart/ShipporiAntique.ttf", 25)
FONT_table_text = pg.font.Font("Schriftart/ShipporiAntique.ttf", 20 )
#title_text
title = FONT_titel.render("BESTENLISTE", True, 'black')
#table_text
place_field_text = FONT_table_text.render("Platz", True, 'black')
user_name_field_text = FONT_table_text.render("Spielername", True, 'black')
easy_wins_text =FONT_table_text.render("Leicht gew.", True, 'black')
middle_wins_text = FONT_table_text.render("Mittel gew.", True, 'black')
hard_wins_text = FONT_table_text.render("Schwer gew.", True, 'black')
#table_rect
table_columns_rect = pg.Rect(60, 210, 965, 50)
#Buttons
user_name_field_button = pg.Rect(155, 210, 330, 50)
easy_wins_button = pg.Rect(485, 210, 175, 50)
middle_wins_button =  pg.Rect(660, 210, 180, 50)
hard_wins_button = pg.Rect(840, 210, 185, 50)
#Rows
table_row_rect_grey_1 = pg.Rect(60, 260, 965, 50)
table_row_rect_grey_3 = pg.Rect(60, 360, 965, 50)
table_row_rect_grey_5 = pg.Rect(60, 460, 965, 50)
table_row_rect_grey_7 = pg.Rect(60, 560, 965, 50)
table_row_rect_grey_9 = pg.Rect(60, 660, 965, 50)
#back_button
back_button_text = FONT_buttons.render("Zurück", True, 'black')
back_button = pg.Rect(60, 30, 240, 50)
def bestScore():
    clock = pg.time.Clock()
    done = False
    global name, password
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN and back_button.collidepoint(pg.mouse.get_pos()):
                if event.button == 1: #left mouse button 
                    done = True
            if event.type == pg.MOUSEBUTTONDOWN and user_name_field_button.collidepoint(pg.mouse.get_pos()):
                if event.button == 1: #left mouse button 
                   print("name")
            if event.type == pg.MOUSEBUTTONDOWN and easy_wins_button.collidepoint(pg.mouse.get_pos()):
                if event.button == 1: #left mouse button 
                    print("easy")  
            if event.type == pg.MOUSEBUTTONDOWN and middle_wins_button.collidepoint(pg.mouse.get_pos()):
                if event.button == 1: #left mouse button 
                    print("middle")
            if event.type == pg.MOUSEBUTTONDOWN and hard_wins_button.collidepoint(pg.mouse.get_pos()):
                if event.button == 1: #left mouse button 
                   print("Hard")
                 
        #Draw titel
        screen_bestenliste.blit(title, (1080//2 - title.get_width()//2, 90))
        #Draw button with text
        pg.draw.rect(screen_bestenliste, (157, 157, 157), back_button, border_radius=5)
        screen_bestenliste.blit(back_button_text,(130, 33, 20, 25))
        #Draw table columns background
        pg.draw.rect(screen_bestenliste, 'Grey', table_columns_rect)
        pg.draw.rect(screen_bestenliste, 'Grey', user_name_field_button)
        pg.draw.rect(screen_bestenliste, 'Grey', easy_wins_button)
        pg.draw.rect(screen_bestenliste, 'Grey', middle_wins_button)
        pg.draw.rect(screen_bestenliste, 'Grey', hard_wins_button)
        
        pg.draw.rect(screen_bestenliste, (242, 242, 242, 1), table_row_rect_grey_1)
        pg.draw.rect(screen_bestenliste, (242, 242, 242, 1), table_row_rect_grey_3)
        pg.draw.rect(screen_bestenliste, (242, 242, 242, 1), table_row_rect_grey_5)
        pg.draw.rect(screen_bestenliste, (242, 242, 242, 1), table_row_rect_grey_7)
        pg.draw.rect(screen_bestenliste, (242, 242, 242, 1), table_row_rect_grey_9)
                #Draw table lines
        pg.draw.line(screen_bestenliste,'black', (155,210), (155,750))
        pg.draw.line(screen_bestenliste,'black', (485,210), (485,750))
        pg.draw.line(screen_bestenliste,'black', (660,210), (660,750))
        pg.draw.line(screen_bestenliste,'black', (840,210), (840,750))
        #Draw column names
        screen_bestenliste.blit(place_field_text, (80, 220, 965, 50))
        screen_bestenliste.blit(user_name_field_text, (180, 220, 965, 50))
        screen_bestenliste.blit(easy_wins_text, (515, 220, 965, 50))
        screen_bestenliste.blit(middle_wins_text, (695, 220, 965, 50))
        screen_bestenliste.blit(hard_wins_text, (870, 220, 965, 50))
        for i, row in enumerate(rows):
            a = FONT_table_text.render(str(i+1), True, 'black')
            b = FONT_table_text.render(str(row[1]), True, 'black')
            c = FONT_table_text.render(str(row[2]), True, 'black')
            d = FONT_table_text.render(str(row[3]), True, 'black')
            e = FONT_table_text.render(str(row[4]), True, 'black')
              
            screen_bestenliste.blit(a, (100, 267+i*50, 965, 50))
            screen_bestenliste.blit(b, (180, 267+i*50, 965, 50))
            screen_bestenliste.blit(c, (515, 267+i*50, 965, 50))
            screen_bestenliste.blit(d, (695, 267+i*50, 965, 50))
            screen_bestenliste.blit(e, (875, 267+i*50, 965, 50))
    
        pg.display.flip()  
        clock.tick(FPS)
        screen_bestenliste.fill('white')
if __name__ == '__main__':
    bestScore()
    pg.quit()
