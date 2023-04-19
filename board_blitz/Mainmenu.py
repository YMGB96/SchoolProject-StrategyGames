import pygame as pg
from AfterLoginMenu import afterLogin
from GuestGamer import guestGamer
from Registration import registration
from BestScore import bestScore
pg.init()
screen_main_menu = pg.display.set_mode((1080, 800))
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
register_text = FONT.render("Registrieren", True, black)
zuruck_text = FONT.render("Weiter als Gast", True, black)
title = FONT_titel.render("BRETTSPIELE", True, black)
oder_text = FONT_oder.render("oder", True, (157, 157, 157))
login_text = FONT.render("Login", True, black)

# Set up the buttons
name_password_background = pg.Rect(270, 230, 540, 350)
register_button = pg.Rect(420, 620, 240, 50)
guest_button = pg.Rect(420, 700, 240, 50)
login_button = pg.Rect(420, 500, 240, 50)

# Set up the input fields
name_input = pg.Rect(350, 320, 380, 50)
password_input = pg.Rect(350, 390, 380, 50)

# Set up the placeholder text for the input fields
name_placeholder = FONT.render("Name", True, (157, 157, 157))
password_placeholder = FONT.render("Password", True, (157, 157, 157))

# Set up the variables to store the user input for name and password
name = ''
password = ''
def mainMenu():
    clock = pg.time.Clock()
    done = False
    global name, password
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                if event.unicode.isalnum():
                    if name_input.collidepoint(pg.mouse.get_pos()):
                        name += event.unicode
                    elif password_input.collidepoint(pg.mouse.get_pos()):
                        password += event.unicode
                        screen_main_menu.blit(FONT.render("*" * len(password), True, black), (password_input.x + 10, password_input.y + 10))
                elif event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE:
                    if name_input.collidepoint(pg.mouse.get_pos()):
                        name = name[:-1]
                    elif password_input.collidepoint(pg.mouse.get_pos()):
                        password = password[:-1]
                        screen_main_menu.blit(FONT.render("*" * len(password), True, black), (password_input.x + 10, password_input.y + 10))
                        #this code can be deleted, when "Login" button will be done.
                elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    if name_input.collidepoint(pg.mouse.get_pos()):
                        print("Name:", name)
                    elif password_input.collidepoint(pg.mouse.get_pos()):
                        print("Password:", password)     
            if event.type == pg.MOUSEBUTTONDOWN and login_button.collidepoint(pg.mouse.get_pos()):
                if event.button == 1: #left mouse button
                    done = True
                    afterLogin()
                    #done = True
                    #here function with login and password
                    if name != '' and password != '':
                        print(name, password)
                        password = ''
                        name = name[:25]
                        password = password[:25]
            if event.type == pg.MOUSEBUTTONDOWN and guest_button.collidepoint(pg.mouse.get_pos()):
                   if event.button == 1: #left mouse button
                        done = True
                        guestGamer()
            if event.type == pg.MOUSEBUTTONDOWN and register_button.collidepoint(pg.mouse.get_pos()):
                if event.button == 1: #left mouse button
                    done = True 
                    registration()  
            
                # Draw the other elements on the screen
        pg.draw.rect(screen_main_menu, (211, 211, 211, 1), name_password_background, border_radius= 15)  
        pg.draw.rect(screen_main_menu, (157, 157, 157), register_button, border_radius=5)
        pg.draw.rect(screen_main_menu, (157, 157, 157), guest_button, border_radius=5)
        pg.draw.rect(screen_main_menu, (157, 157, 157), login_button, border_radius=5)
        
        screen_main_menu.blit(title, (1080//2 - title.get_width()//2, 90))
        screen_main_menu.blit(register_text, (register_button.x + register_button.w / 2 - register_text.get_width() / 2, 
                            register_button.y + register_button.h / 2 - register_text.get_height() / 2))
        screen_main_menu.blit(zuruck_text, (guest_button.x + guest_button.w / 2 - zuruck_text.get_width() / 2, 
                         guest_button.y + guest_button.h / 2 - zuruck_text.get_height() / 2))
        screen_main_menu.blit(login_text, (login_button.x + login_button.w / 2 - login_text.get_width() / 2, 
                         login_button.y + login_button.h / 2 - login_text.get_height() / 2))
        screen_main_menu.blit(oder_text, (520, 667))
        # Draw the input fields and their backgrounds
        pg.draw.rect(screen_main_menu, white, name_input, border_radius= 5)
        pg.draw.rect(screen_main_menu, white, password_input, border_radius= 5)
        screen_main_menu.blit(name_placeholder, (name_input.x + 10, name_input.y + 10))
        screen_main_menu.blit(password_placeholder, (password_input.x + 10, password_input.y + 10))
        pg.draw.rect(screen_main_menu, white, name_input, border_radius=5)
        pg.draw.rect(screen_main_menu, white, password_input, border_radius=5)
        # Draw the input fields and their backgrounds
        
        if name == '':
            screen_main_menu.blit(name_placeholder, (name_input.x + 10, name_input.y + 10))
        else:
            name_text = FONT.render(name, True, black)
            screen_main_menu.blit(name_text, (name_input.x + 10, name_input.y + 10))
        if password == '':
            screen_main_menu.blit(password_placeholder, (password_input.x + 10, password_input.y + 10))
        else:
            password_text = FONT.render("*" * len(password), True, black)
            screen_main_menu.blit(password_text, (password_input.x + 10, password_input.y + 10))
        pg.display.flip()
        clock.tick(FPS)
        screen_main_menu.fill('white')  
if __name__ == '__main__':
    mainMenu()
    pg.quit()
