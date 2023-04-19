import pygame as pg
from AfterLoginMenu import afterLogin
pg.init()
screen_gast_game = pg.display.set_mode((1080, 800))
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
background_gast_gamer = pg.Color(170,170,170)
white = (255, 255, 255)
black = (0, 0, 0)
shadow_color = (0, 0, 0, 64) 
# Set up the text for the buttons
register_text = FONT.render("Registrieren", True, black)
guest_text = FONT.render("Weiter als Gast", True, black)
title = FONT_titel.render("BRETTSPIELE", True, black)
oder_text = FONT_oder.render("oder", True, (157, 157, 157))
als_gast_fortfahren_text = FONT.render("Als Gast fortfahren", True, black)
abbrechen_text = FONT.render("Abbrechen", True, black)
sicher_als_gast_text1 = FONT.render("Sicher, dass du als Gast fortfahren möchtest?", True, black)
sicher_als_gast_text2 = FONT.render("Dein Spielstand wird nicht gespeichert und du", True, black)
sicher_als_gast_text3 = FONT.render("wirst nicht in der Bestenliste erscheinen.", True, black)

# Set up the buttons
guest_background = pg.Rect(120, 230, 840, 350)
name_password_background = pg.Rect(220, 230, 640, 350)
register_button = pg.Rect(420, 620, 240, 50)
guest_button = pg.Rect(420, 700, 240, 50)
als_gast_fortfahren_button = pg.Rect(280, 500, 240, 50)
abbrechen_button = pg.Rect(560, 500, 240, 50)


# Set up the variables to store the user input for name and password
name = ''
password = ''
def guestGamer():
    clock = pg.time.Clock()
    done = False
    global name, password
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN and als_gast_fortfahren_button.collidepoint(pg.mouse.get_pos()):
                if event.button == 1: #left mouse button
                    done = True
                    afterLogin()
                    #here function with login and password
            
            if event.type == pg.MOUSEBUTTONDOWN and abbrechen_button.collidepoint(pg.mouse.get_pos()):
                   if event.button == 1: #left mouse button
                        done = True
                        afterLogin()
               
                # Draw the other elements on the screen
        pg.draw.rect(screen_gast_game, (211, 211, 211), name_password_background, border_radius= 15)  
        pg.draw.rect(screen_gast_game, (157, 157, 157), register_button, border_radius=5)
        pg.draw.rect(screen_gast_game, (157, 157, 157), guest_button, border_radius=5)
        pg.draw.rect(screen_gast_game, (157, 157, 157), als_gast_fortfahren_button, border_radius=5)
        pg.draw.rect(screen_gast_game, (157, 157, 157), abbrechen_button, border_radius=5)
        
        screen_gast_game.blit(title, (1080//2 - title.get_width()//2, 90))
        screen_gast_game.blit(register_text, (register_button.x + register_button.w / 2 - register_text.get_width() / 2, 
                            register_button.y + register_button.h / 2 - register_text.get_height() / 2))
        screen_gast_game.blit(guest_text, (guest_button.x + guest_button.w / 2 - guest_text.get_width() / 2, 
                         guest_button.y + guest_button.h / 2 - guest_text.get_height() / 2))
        screen_gast_game.blit(als_gast_fortfahren_text, (als_gast_fortfahren_button.x + als_gast_fortfahren_button.w / 2 - als_gast_fortfahren_text.get_width() / 2, 
                         als_gast_fortfahren_button.y + als_gast_fortfahren_button.h / 2 - als_gast_fortfahren_text.get_height() / 2))
        screen_gast_game.blit(oder_text, (520, 667))
        screen_gast_game.blit(abbrechen_text, (abbrechen_button.x + abbrechen_button.w / 2 - abbrechen_text.get_width() / 2, 
                         abbrechen_button.y + abbrechen_button.h / 2 - abbrechen_text.get_height() / 2))
        screen_gast_game.blit(sicher_als_gast_text1, (260, 280))
        screen_gast_game.blit(sicher_als_gast_text2, (260, 320))
        screen_gast_game.blit(sicher_als_gast_text3, (260, 360))
        # Draw the input fields and their backgrounds
        pg.display.flip()
        clock.tick(FPS)
        screen_gast_game.fill(background_gast_gamer)  
if __name__ == '__main__':
    guestGamer()
    pg.quit()

