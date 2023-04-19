import pygame as pg
from math import floor
from BestScore import bestScore
pg.init()
screen = pg.display.set_mode((1080, 800))
pg.display.set_caption("Login")
icon = pg.image.load("images/211667_a_controller_game_icon.png")
pg.display.set_icon(icon)
HEIGHT = 1080
WIDTH = 800
FPS = 60
FONT_titel = pg.font.Font("Schriftart/Staatliches.ttf", 90)
FONT = pg.font.Font("Schriftart/ShipporiAntique.ttf", 25)
FONT_oder = pg.font.Font("Schriftart/ShipporiAntique.ttf", 20)
# Set up the colors
white = (255, 255, 255)
black = (0, 0, 0)
shadow_color = (0, 0, 0, 64) 
# Set up the text for the buttons
brettspiele_title = FONT_titel.render("BRETTSPIELE", True, black)
neues_spiel_text = FONT.render("Neues Spiel starten", True, black)
spiel_fortsetzen_text = FONT.render("Spiel fortsetzen", True, black)
bestenliste_text = FONT.render("Bestenliste",True, black)
logout_text = FONT.render("Logout", True, black)

# Set up the buttons
neues_spiel_button = pg.Rect(365, 275, 350, 50)
spiel_fortzetzen_button = pg.Rect(365, 350, 350, 50)
bestenliste_button = pg.Rect(365, 425, 350, 50)
logout_button = pg.Rect(420, 700, 240, 50)
def afterLogin():
    clock = pg.time.Clock()
    done = False
    global name, password
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN and logout_button.collidepoint(pg.mouse.get_pos()):
                if event.button == 1: #left mouse button
                    done = True
                    #here function with login and password
            if event.type == pg.MOUSEBUTTONDOWN and bestenliste_button.collidepoint(pg.mouse.get_pos()):
                if event.button == 1: #left mouse button
                    done = True 
                    bestScore()
            
        screen.fill('white')
        # Draw the other elements on the screen  
        pg.draw.rect(screen, (157, 157, 157), neues_spiel_button, border_radius=5)
        pg.draw.rect(screen, (157, 157, 157), spiel_fortzetzen_button, border_radius=5)
        pg.draw.rect(screen, (157, 157, 157), logout_button, border_radius=5)
        pg.draw.rect(screen, (157, 157, 157), bestenliste_button, border_radius=5)

        screen.blit(brettspiele_title, (1080//2 - brettspiele_title.get_width()//2, 90))
        screen.blit(neues_spiel_text, (neues_spiel_button.x + neues_spiel_button.w / 2 - neues_spiel_text.get_width() / 2, 
                            neues_spiel_button.y + neues_spiel_button.h / 2 - neues_spiel_text.get_height() / 2))
        screen.blit(spiel_fortsetzen_text, (spiel_fortzetzen_button.x + spiel_fortzetzen_button.w / 2 - neues_spiel_text.get_width() / 2, 
                         spiel_fortzetzen_button.y + spiel_fortzetzen_button.h / 2 - neues_spiel_text.get_height() / 2))
        screen.blit(logout_text, (logout_button.x + logout_button.w / 2 - logout_text.get_width() / 2, 
                         logout_button.y + logout_button.h / 2 - logout_text.get_height() / 2))
        screen.blit(bestenliste_text, (bestenliste_button.x + bestenliste_button.w / 3 - 15 - bestenliste_text.get_width() / 3, 
                         (bestenliste_button.y + bestenliste_button.h / 2) - bestenliste_text.get_height() / 2))
        pg.display.flip()
        clock.tick(FPS)
if __name__ == '__main__':
    afterLogin()
    pg.quit()

