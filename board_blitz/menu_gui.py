
import pygame as pg
from menu_logic import menu_logic

class MenuGui:
    colors = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'shadow': (0, 0, 0, 64),
        'gray': (157, 157, 157),
        'background': (211, 211, 211, 1),
        'table_row': (242, 242, 242, 1),
    }
    name = password = second_password = ''
    screen_id = 0
    leaderboard = 0
    sort_by = 'username'
    def __init__(self, width = 1080, height = 800):
        self.screen = pg.display.set_mode((width, height))
        self.font_titel = pg.font.Font("./board_blitz/resources/Staatliches.ttf", 90)
        self.font = pg.font.Font("./board_blitz/resources/ShipporiAntique.ttf", 25)
        self.font_small = pg.font.Font("./board_blitz/resources/ShipporiAntique.ttf", 20)
        pg.display.set_caption("Board Blitz")
        icon = pg.image.load("./board_blitz/resources/211667_a_controller_game_icon.png")
        pg.display.set_icon(icon)
        self.texts = {
            'main_menu': {
                'register': self.font.render("Registrieren", True, self.colors['black']),
                'guest': self.font.render("Weiter als Gast", True, self.colors['black']),
                'title': self.font_titel.render("BRETTSPIELE", True, self.colors['black']),
                'or': self.font_small.render("oder", True, self.colors['gray']),
                'login': self.font.render("Login", True, self.colors['black']),
                'name_placeholder': self.font.render("Name", True, self.colors['gray']),
                'password_placeholder': self.font.render("Passwort", True, self.colors['gray']),
                'name': None,
                'password': None,
            },
            'register': {
                'register': self.font.render("Registrieren", True, self.colors['black']),
                'back': self.font.render("Zurück", True, self.colors['black']),
                'title': self.font_titel.render("BRETTSPIELE", True, self.colors['black']),
                'or': self.font_small.render("oder", True, self.colors['gray']),
                'name_placeholder': self.font.render("Name", True, self.colors['gray']),
                'password_placeholder': self.font.render("Passwort", True, self.colors['gray']),
                'second_password_placeholder': self.font.render("Passwort wiederholen", True, self.colors['gray']),
                'name': None,
                'password': None,
                'second_password': None,
            },
            'after_login': {
                'title': self.font_titel.render("BRETTSPIELE", True, self.colors['black']),
                'new_game': self.font.render("Neues Spiel starten", True, self.colors['black']),
                'leaderboard_chess': self.font.render("Bestenliste Bauernschach", True, self.colors['black']),
                'leaderboard_checkers': self.font.render("Bestenliste Dame", True, self.colors['black']),
                'logout': self.font.render("Logout", True, self.colors['black']),
            },
            'leaderboard': {
                'title': self.font_titel.render("BRETTSPIELE", True, self.colors['black']),
                'place': self.font.render("Platz", True, self.colors['black']),
                'username': self.font.render("Spielername", True, self.colors['black']),
                'easy': self.font.render("Leicht", True, self.colors['black']),
                'normal': self.font.render("Mittel", True, self.colors['black']),
                'hard': self.font.render("Schwer", True, self.colors['black']),
                'back': self.font.render("Zurück", True, self.colors['black']),
            },
        }
        self.backgrounds = {
            'main_menu': {
                'name_password': pg.Rect(270, 230, 540, 350),
            },
            'register': {
                'name_password': pg.Rect(270, 230, 540, 380),
            },
            'leaderboard': {
                'table_header': pg.Rect(60, 210, 965, 50),
            },
        }
        self.buttons = {
            'main_menu': {
                'register': pg.Rect(420, 620, 240, 50),
                'guest': pg.Rect(420, 700, 240, 50),
                'login': pg.Rect(420, 500, 240, 50),
            },
            'register': {
                'back': pg.Rect(420, 660, 240, 50),
                'register': pg.Rect(420, 535, 240, 50),
            },
            'after_login': {
                'new_game': pg.Rect(365, 275, 350, 50),
                'leaderboard_chess': pg.Rect(365, 350, 350, 50),
                'leaderboard_checkers': pg.Rect(365, 425, 350, 50),
                'logout': pg.Rect(420, 700, 240, 50),
            },
            'leaderboard': {
                'username': pg.Rect(155, 210, 330, 50),
                'easy': pg.Rect(485, 210, 175, 50),
                'normal': pg.Rect(660, 210, 180, 50),
                'hard': pg.Rect(840, 210, 185, 50),
                'back': pg.Rect(60, 30, 240, 50),
            }
        }
        self.inputs = {
            'main_menu': {
                'name': pg.Rect(350, 320, 380, 50),
                'password': pg.Rect(350, 390, 380, 50),
            },
            'register': {
                'name': pg.Rect(350, 320, 380, 50),
                'password': pg.Rect(350, 390, 380, 50),
                'second_password': pg.Rect(350, 460, 380, 50),
            }
        }

    def switch_screen(self, screen_id):
        self.screen_id = screen_id
        self.name = self.password = self.second_password = ''
        self.texts['main_menu']['name'] = self.texts['main_menu']['password'] = None
        self.texts['register']['name'] = self.texts['register']['password'] = self.texts['register']['second_password'] = None
        self.sort_by = 'username'

    def draw_main_menu(self):
        mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                # If the user hit a letter/number key
                if event.unicode.isalnum():
                    # Should write into name
                    if self.inputs['main_menu']['name'].collidepoint(mouse):
                        # Extend and rerender name
                        if len(self.name) < 16:
                            self.name += event.unicode
                        self.texts['main_menu']['name'] = self.font.render(self.name, True, self.colors['black'])
                    # Should write into password
                    elif self.inputs['main_menu']['password'].collidepoint(mouse):
                        # Extend and rerender password
                        if len(self.password) < 25:
                            self.password += event.unicode
                        self.texts['main_menu']['password'] = self.font.render("*" * len(self.password), True, self.colors['black'])
                # If the user hit backspace
                elif event.key == pg.K_BACKSPACE:
                    # And is writing into name
                    if self.inputs['main_menu']['name'].collidepoint(mouse):
                        # Remove last character of name
                        self.name = self.name[:-1]
                        # rerender or unset name
                        if self.name:
                            self.texts['main_menu']['name'] = self.font.render(self.name, True, self.colors['black'])
                        else:
                            self.texts['main_menu']['name'] = None
                    # And is writing into password
                    elif self.inputs['main_menu']['password'].collidepoint(mouse):
                        # Remove last character of password
                        self.password = self.password[:-1]
                        # rerender or unset password
                        if self.password:
                            self.texts['main_menu']['password'] = self.font.render("*" * len(self.password), True, self.colors['black'])
                        else:
                            self.texts['main_menu']['password'] = None
                # After pressing return
                elif event.key == pg.K_RETURN:
                    #! Attempt login on return
                    ...
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.buttons['main_menu']['login'].collidepoint(mouse) and event.button == 1: #left mouse button
                    if error := menu_logic.login(self.name, self.password):
                        print(error)
                        self.password = ''
                        self.texts['main_menu']['password'] = None
                    else:
                        self.switch_screen(2) # -> switch to after_login screen
                if self.buttons['main_menu']['guest'].collidepoint(mouse):
                   if event.button == 1: #left mouse button
                        self.switch_screen(2) # -> switch to after_login screen
                if self.buttons['main_menu']['register'].collidepoint(mouse):
                    if event.button == 1: #left mouse button
                        self.switch_screen(1) # -> switch to register screen
            
        # Draw the other elements on the screen
        # Draw Background
        pg.draw.rect(self.screen, self.colors['background'], self.backgrounds['main_menu']['name_password'], border_radius= 15)
        # Draw all main menu buttons and their text
        for key, button in self.buttons['main_menu'].items():
            pg.draw.rect(self.screen, self.colors['gray'], button, border_radius=5)
            if text := self.texts['main_menu'].get(key):
                self.screen.blit(
                    text,
                    (button.x + button.w / 2 - text.get_width() / 2,
                     button.y + button.h / 2 - text.get_height() / 2))
        
        # Draw standalone text
        width = self.screen.get_size()[0]
        self.screen.blit(self.texts['main_menu']['title'], (width//2 - self.texts['main_menu']['title'].get_width()//2, 90))
        self.screen.blit(self.texts['main_menu']['or'], (520, 667))

        # Draw the input fields' backgrounds
        pg.draw.rect(self.screen, self.colors['white'], self.inputs['main_menu']['name'], border_radius=5)
        pg.draw.rect(self.screen, self.colors['white'], self.inputs['main_menu']['password'], border_radius=5)
        
        # Draw name and password
        name_text = self.texts['main_menu']['name'] or self.texts['main_menu']['name_placeholder']
        password_text = self.texts['main_menu']['password'] or self.texts['main_menu']['password_placeholder']
        self.screen.blit(name_text, (self.inputs['main_menu']['name'].x + 10, self.inputs['main_menu']['name'].y + 10))
        self.screen.blit(password_text, (self.inputs['main_menu']['password'].x + 10, self.inputs['main_menu']['password'].y + 10))

    def draw_register(self):
        mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.unicode.isalnum():
                    # Should write into name
                    if self.inputs['register']['name'].collidepoint(mouse):
                        # Extend and rerender name
                        if len(self.name) < 16:
                            self.name += event.unicode
                        self.texts['register']['name'] = self.font.render(self.name, True, self.colors['black'])
                    # Should write into password
                    elif self.inputs['register']['password'].collidepoint(mouse):
                        # Extend and rerender password
                        if len(self.password) < 25:
                            self.password += event.unicode
                        self.texts['register']['password'] = self.font.render("*" * len(self.password), True, self.colors['black'])
                    # Should write into second second password
                    elif self.inputs['register']['second_password'].collidepoint(mouse):
                        # Extend and rerender second password
                        if len(self.second_password) < 25:
                            self.second_password += event.unicode
                        self.texts['register']['second_password'] = self.font.render("*" * len(self.second_password), True, self.colors['black'])
                # If the user hit backspace
                elif event.key == pg.K_BACKSPACE:
                    # And is writing into name
                    if self.inputs['register']['name'].collidepoint(mouse):
                        # Remove last character of name
                        self.name = self.name[:-1]
                        # rerender or unset name
                        if self.name:
                            self.texts['register']['name'] = self.font.render(self.name, True, self.colors['black'])
                        else:
                            self.texts['register']['name'] = None
                    # And is writing into password
                    elif self.inputs['register']['password'].collidepoint(mouse):
                        # Remove last character of password
                        self.password = self.password[:-1]
                        # rerender or unset password
                        if self.password:
                            self.texts['register']['password'] = self.font.render("*" * len(self.password), True, self.colors['black'])
                        else:
                            self.texts['register']['password'] = None
                    # And is writing into password
                    elif self.inputs['register']['second_password'].collidepoint(mouse):
                        # Remove last character of second password
                        self.second_password = self.second_password[:-1]
                        # rerender or unset password
                        if self.second_password:
                            self.texts['register']['second_password'] = self.font.render("*" * len(self.second_password), True, self.colors['black'])
                        else:
                            self.texts['register']['second_password'] = None
                # After pressing return
                elif event.key == pg.K_RETURN:
                    #! Attempt login on return
                    ...
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.buttons['register']['register'].collidepoint(mouse) and event.button == 1: #left mouse button
                    if error := menu_logic.register(self.name, self.password, self.second_password):
                        print(error)
                        self.password = self.second_password = ''
                        self.texts['register']['password'] = None
                        self.texts['register']['second_password'] = None
                    else:
                        self.switch_screen(2) # -> switch to after_login screen
                if self.buttons['register']['back'].collidepoint(mouse):
                   if event.button == 1: #left mouse button
                        self.switch_screen(0) # -> switch to after_login screen
                        
        # Draw the other elements on the screen
        pg.draw.rect(self.screen, self.colors['background'], self.backgrounds['register']['name_password'], border_radius= 15)

        # Draw all main menu buttons and their text
        for key, button in self.buttons['register'].items():
            pg.draw.rect(self.screen, self.colors['gray'], button, border_radius=5)
            if text := self.texts['register'].get(key):
                self.screen.blit(
                    text,
                    (button.x + button.w / 2 - text.get_width() / 2,
                     button.y + button.h / 2 - text.get_height() / 2))
        
        # Draw standalone text
        width = self.screen.get_size()[0]
        self.screen.blit(self.texts['register']['title'], (width//2 - self.texts['register']['title'].get_width()//2, 90))
        self.screen.blit(self.texts['register']['or'], (520, 620))

        # Draw the input fields' backgrounds
        pg.draw.rect(self.screen, self.colors['white'], self.inputs['register']['name'], border_radius=5)
        pg.draw.rect(self.screen, self.colors['white'], self.inputs['register']['password'], border_radius=5)
        pg.draw.rect(self.screen, self.colors['white'], self.inputs['register']['second_password'], border_radius=5)

        # Draw name and passwords
        name_text = self.texts['register']['name'] or self.texts['register']['name_placeholder']
        password_text = self.texts['register']['password'] or self.texts['register']['password_placeholder']
        second_password_text = self.texts['register']['second_password'] or self.texts['register']['second_password_placeholder']
        self.screen.blit(name_text, (self.inputs['register']['name'].x + 10, self.inputs['register']['name'].y + 10))
        self.screen.blit(password_text, (self.inputs['register']['password'].x + 10, self.inputs['register']['password'].y + 10))
        self.screen.blit(second_password_text, (self.inputs['register']['second_password'].x + 10, self.inputs['register']['second_password'].y + 10))

    def draw_after_login(self):
        mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1: # left mouse button is pressed
                if self.buttons['after_login']['new_game'].collidepoint(mouse):
                    self.switch_screen(4) # -> go to game select screen
                elif self.buttons['after_login']['leaderboard_chess'].collidepoint(mouse):
                    self.leaderboard = 0
                    self.switch_screen(3) # -> go to leaderboard screen
                elif self.buttons['after_login']['leaderboard_checkers'].collidepoint(mouse):
                    self.leaderboard = 1
                    self.switch_screen(3) # -> go to leaderboard screen
                elif self.buttons['after_login']['logout'].collidepoint(mouse):
                    menu_logic.logout()
                    self.switch_screen(0) # -> go back to login screen

        # Draw all buttons and their text
        for key, button in self.buttons['after_login'].items():
            pg.draw.rect(self.screen, self.colors['gray'], button, border_radius=5)
            if text := self.texts['after_login'].get(key):
                self.screen.blit(
                    text,
                    (button.x + button.w / 2 - text.get_width() / 2,
                     button.y + button.h / 2 - text.get_height() / 2))
    
        # Draw standalone text
        width = self.screen.get_size()[0]
        self.screen.blit(self.texts['register']['title'], (width//2 - self.texts['register']['title'].get_width()//2, 90))

    def draw_leaderboard(self):
        # Handle interactions
        mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.buttons['leaderboard']['back'].collidepoint(mouse):
                    self.switch_screen(2) # -> return to after login
                if self.buttons['leaderboard']['username'].collidepoint(mouse):
                    self.sort_by = 'username'
                if self.buttons['leaderboard']['easy'].collidepoint(mouse):
                    self.sort_by = 'easy'
                if self.buttons['leaderboard']['normal'].collidepoint(mouse):
                    self.sort_by = 'normal'
                if self.buttons['leaderboard']['hard'].collidepoint(mouse):
                    self.sort_by = 'hard'
        # Get sorted leaderboard
        leaderboard = menu_logic.get_leaderboard(self.leaderboard, '', False)
        # Draw standalone text
        width = self.screen.get_size()[0]
        self.screen.blit(self.texts['leaderboard']['title'], (width//2 - self.texts['register']['title'].get_width()//2, 90))
        # Draw table rows
        for i in range(5):
            pg.draw.rect(self.screen, self.colors['table_row'], [60, 260+100*i, 965, 50])
        # Draw all buttons and their text
        for key, button in self.buttons['leaderboard'].items():
            pg.draw.rect(self.screen, self.colors['gray'], button, border_radius=5)
            if text := self.texts['leaderboard'].get(key):
                self.screen.blit(
                    text,
                    (button.x + button.w / 2 - text.get_width() / 2,
                     button.y + button.h / 2 - text.get_height() / 2))
        # Draw table lines
        pg.draw.line(self.screen,self.colors['black'], (155,210), (155,750))
        pg.draw.line(self.screen,self.colors['black'], (485,210), (485,750))
        pg.draw.line(self.screen,self.colors['black'], (660,210), (660,750))
        pg.draw.line(self.screen,self.colors['black'], (840,210), (840,750))
        # Draw column names
        self.screen.blit(self.texts['leaderboard']['place'], (80, 220, 965, 50))
        self.screen.blit(self.texts['leaderboard']['username'], (180, 220, 965, 50))
        self.screen.blit(self.texts['leaderboard']['easy'], (515, 220, 965, 50))
        self.screen.blit(self.texts['leaderboard']['normal'], (695, 220, 965, 50))
        self.screen.blit(self.texts['leaderboard']['hard'], (870, 220, 965, 50))
        # Draw each row
        for i, row in enumerate(leaderboard):
            place = self.font_small.render(str(i+1), True, self.colors['black'])
            username = self.font_small.render(row['username'], True, self.colors['black'])
            easy = self.font_small.render(row['easy'], True, self.colors['black'])
            normal = self.font_small.render(row['normal'], True, self.colors['black'])
            hard = self.font_small.render(row['hard'], True, self.colors['black'])
            self.screen.blit(place, (100, 267+i*50, 965, 50))
            self.screen.blit(username, (180, 267+i*50, 965, 50))
            self.screen.blit(easy, (515, 267+i*50, 965, 50))
            self.screen.blit(normal, (695, 267+i*50, 965, 50))
            self.screen.blit(hard, (875, 267+i*50, 965, 50))

    def draw_game_select(self):
        ...

    def render(self):
        self.screen.fill(self.colors['white'])
        match self.screen_id:
            case 0: self.draw_main_menu()
            case 1: self.draw_register()
            case 2: self.draw_after_login()
            case 3: self.draw_leaderboard()
            case 4: self.draw_game_select()

menu_gui = None
