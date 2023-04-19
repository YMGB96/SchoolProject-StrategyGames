import pygame as pg
from math import floor
from game_logic import game_logic

class GameGui:
    colors = {
        'black': (116, 116, 116),
        'white': (222, 222, 222),
        'background': (245, 245, 245),
        'text': (0, 0, 0),
        'button': (158, 158, 158),
    }
    texts = {
        'menu': 'Menü',
        'resume': 'Zurück zum Spiel',
        'surrender': 'Spiel aufgeben',

        'won': 'GEWONNEN!',
        'lost': 'VERLOREN...',

        'easy': 'Leichte KI',
        'normal': 'Mittlere KI',
        'hard': 'Schwere KI',
        'unknown': '???',
        'guest': 'Gast',
    }
    selected_piece = [(-1, -1), -1]
    was_pressed = False
    is_paused = False
    is_finished = False
    is_won = False
    checkers = None
    checkers_move_from = None
    def __init__(self, difficulty: int, playername = None, width = 1125, height = 800):
        if not playername: playername = self.texts['guest']
        # Set up window
        self.window = pg.display.set_mode((width,height))
        # Get tile size and offset
        tile_size = floor(height * 0.146)
        start_x = floor(width * 0.223)
        start_y = height // 2 - tile_size * 3
        # Fill board with black/white squares
        self.board = []
        for i in range(6):
            self.board.append([])
            for j in range(6):
                dimensions = [start_x + tile_size * j,
                              start_y + tile_size * i,
                              tile_size, tile_size]
                color = (self.colors['black'] if (i+j)%2 == 0
                    else self.colors['white'])
                sprite = Sprite(self.window, None, dimensions, color)
                sprite.border_radius = 0
                self.board[i].append(sprite)
        # Scale and set images for player, enemy and valid spots
        piece_scale = tile_size * 0.85
        self.images = {
            'player': pg.transform.scale(pg.image.load('./board_blitz/resources/white_piece.png'), (piece_scale, piece_scale)),
            'enemy': pg.transform.scale(pg.image.load('./board_blitz/resources/black_piece.png'), (piece_scale, piece_scale)),
            'valid': pg.transform.scale(pg.image.load('./board_blitz/resources/valid_move.png'), (piece_scale, piece_scale)),
            'capture': pg.transform.scale(pg.image.load('./board_blitz/resources/valid_capture.png'), (piece_scale, piece_scale)),
        }
        # Set up all menu buttons
        font_size = floor(height * 0.023)
        font = pg.font.Font('./board_blitz/resources/ShipporiAntique.ttf', font_size)
        button_height = floor(height * 0.060)
        y_buffer = floor(height * 0.030)
        self.menu_buttons = {
            'menu': Sprite(self.window, font.render(
                self.texts['menu'], True, self.colors['text'] ), 
                [floor(width * 0.026), floor(height * 0.060),
                 floor(width * 0.174), button_height],
                self.colors['button']),
            'resume': Sprite(self.window, font.render(
                self.texts['resume'], True, self.colors['text'] ), 
                [floor(width * 0.043), height//2 - y_buffer//2 - button_height,
                 floor(width * 0.328), button_height],
                self.colors['background']),
            'surrender': Sprite(self.window, font.render(
                self.texts['surrender'], True, self.colors['text'] ), 
                [floor(width * 0.043), height//2 + y_buffer//2,
                 floor(width * 0.328), button_height],
                self.colors['background']),
        }
        player_font_size = floor(height * 0.035)
        player_font = pg.font.Font('./board_blitz/resources/ShipporiAntique.ttf', player_font_size)
        match difficulty:
            case 0: enemyname = self.texts['easy']
            case 1: enemyname = self.texts['normal']
            case 2: enemyname = self.texts['hard']
            case _: enemyname = self.texts['unknown']
        player_surface = player_font.render(playername, True, self.colors['text'])
        enemy_surface = font.render(enemyname, True, self.colors['text'])
        self.names = {
            'player': (player_surface, (
                floor(width * 0.110),
                floor(height * 0.913))),
            'enemy': (enemy_surface, (
                floor(width * 0.920),
                floor(height * 0.077))),
        }

    def draw_board(self, board: list[list[int]]):
        """Updates all sprites according to the given board and renders it"""
        # go through the whole board
        for x, row in enumerate(self.board):
            for y, piece in enumerate(row):
                # set correct sprites
                match board[x][y]:
                    case 0: piece.surface = None
                    case 1: piece.surface = self.images['player']
                    case 2: piece.surface = self.images['enemy']
                    case 3: piece.surface = self.images['valid']
                    case 4: piece.surface = self.images['capture']
                # draw each piece
                piece.draw()
                # remember what piece was last clicked
                if (not self.is_paused and not self.was_pressed and piece.is_clicked()):
                    last_piece = self.selected_piece
                    self.selected_piece = [(x, y), board[x][y]]
                    if last_piece != self.selected_piece:
                        # tell game_logic to make a move, handle result on checkers consecutive moves
                        if board[x][y] == 3 or board[x][y] == 4:
                            move_from = (self.checkers_move_from if self.checkers and self.checkers_move_from
                                         else last_piece[0])
                            self.checkers = game_logic.switch_turn(((move_from),(x, y)))
                            self.checkers_move_from = (x,y)
                        else:
                            self.checkers = None

    def draw_game_finished(self):
        # overlay to darken the game elements
        overlay = pg.Surface(self.window.get_size())
        overlay.set_alpha(110)
        overlay.fill((0,0,0))
        self.window.blit(overlay, (0,0))
        # show text depending on result
        width, height = self.window.get_size()
        font_size = floor(height * 0.125)
        font = pg.font.Font('./board_blitz/resources/Staatliches.ttf', font_size)
        text_surface = font.render(
            self.texts['won'] if self.is_won else self.texts['lost'],
            True,
            self.colors['white'] if self.is_won else self.colors['text']
        )
        # calculate offset
        dx, dy = text_surface.get_size()
        location = (width//2 - dx//2,
                    height//2 - dy//2)
        # actually draw the text
        self.window.blit(text_surface, location)

    def draw_names(self, player_captures: int, enemy_captures: int):
        # get player center coordinates
        for key, (surface, (cx, cy)) in self.names.items():
            dx, dy = surface.get_size()
            # draw names centered around cx/cy
            self.window.blit(surface, (cx-dx//2, cy-dy//2))
            # make sure that player captures are displayed above and enemies below, also set different colors
            if key == 'player':
                m = -1
                color = self.colors['text']
                captures = player_captures
            else: # key == 'enemy'
                m = 1
                color = self.colors['button']
                captures = enemy_captures
            # draw the actual circles
            width = self.window.get_size()[0]
            circle_radius = floor(width * 0.0065)
            circle_offset = circle_radius*2.7
            circle_x = cx - circle_offset * (captures-1)/2
            circle_y = cy + dy*m
            for i in range(captures):
                pg.draw.circle(self.window, color, (circle_x, circle_y), circle_radius)
                circle_x += circle_offset

    def draw_rules(self, game: int):
        width, height = self.window.get_size()
        # draw background
        x = floor(width * 0.500)
        y = floor(height * 0.140)
        pg.draw.rect(self.window, self.colors['background'], [x,y, floor(width * 0.463), floor(height * 0.722)], border_radius=floor(0.015 * height))
        # draw font
        bolt_font = pg.font.Font('./board_blitz/resources/Staatliches.ttf', floor(width * 0.040))
        base_font = pg.font.Font('./board_blitz/resources/ShipporiAntique.ttf', floor(width * 0.012))
        underline_font = pg.font.Font('./board_blitz/resources/ShipporiAntique.ttf', floor(width * 0.012))
        underline_font.underline = True
        fy = y + floor(height * 0.011)
        fx = x + floor(width * 0.030)
        # open file with rules
        for line in open('./board_blitz/resources/rules_chess.txt' if game == 0 else './board_blitz/resources/rules_checkers.txt', encoding='utf-8'):
            line = line.rstrip()
            if not line: line = ' '
            match line[0]:
                # budget formatting ^^
                case '*': surface = bolt_font.render(line[1:], True, (0,0,0))
                case '_': surface = underline_font.render(line[1:], True, (0,0,0))
                case _: surface = base_font.render(line, True, (0,0,0))
            self.window.blit(surface, (fx,fy))
            fy += surface.get_size()[1]

    def end_game(self, is_won: bool):
        self.is_paused = True
        self.is_finished = True
        self.is_won = is_won

    def render(self):
        """Render the whole 'in-game' screen"""
        # fill the background
        background = pg.Surface(self.window.get_size())
        background.fill(self.colors['background'])
        self.window.blit(background, (0,0))
        # draw the current board
        board = (self.checkers if self.checkers
                 else game_logic.get_valid_moves(chosen_piece=self.selected_piece[0]) if self.selected_piece[1] == 1
                 else game_logic.board)
        self.draw_board(board)
        # draw the names of both parties
        player_captures = enemy_captures = 6
        for row in board:
            for field in row:
                if field == 1: enemy_captures -= 1
                elif field == 2 or field == 4: player_captures -= 1
        self.draw_names(player_captures, enemy_captures)
        # draw the menu button in the corner
        self.menu_buttons['menu'].draw()
        # check if it has been clicked
        if not self.was_pressed and self.menu_buttons['menu'].is_clicked():
            self.is_paused = True
        # render additional elements if the game is paused
        if self.is_finished:
            self.draw_game_finished()
            if not self.was_pressed and pg.mouse.get_pressed()[0]:
                game_logic.game_is_finished(game_cancelled=True)
                global run  #! -----> tell menu to do it's thing again
                run = False #! -----> tell menu to do it's thing again
                global game_gui
                game_gui = None
        elif self.is_paused:
            # overlay to darken the game elements
            overlay = pg.Surface(self.window.get_size())
            overlay.set_alpha(110)
            overlay.fill((0,0,0))
            self.window.blit(overlay, (0,0))
            # draw the rules onto the screen
            game = game_logic.game
            self.draw_rules(game)
            # render 'paused' buttons
            self.menu_buttons['resume'].draw()
            self.menu_buttons['surrender'].draw()
            # check if the buttons have been clicked
            if not self.was_pressed and self.menu_buttons['resume'].is_clicked():
                self.is_paused = False
            if not self.was_pressed and self.menu_buttons['surrender'].is_clicked():
                self.end_game(False)
        # update mouse was pressed
        self.was_pressed = pg.mouse.get_pressed()[0]

class Sprite:
    """Abstraction of a 'thing to render', knows if it is clicked or not"""
    def __init__(self, window, surface, dimensions, color):
        self.color = color
        self.window = window
        self.surface = surface
        self.dimensions = dimensions
        self.border_radius = floor(self.window.get_size()[1] * 0.005)

    def draw(self):
        """Draws the Sprite to the screen including it's background"""
        # Draw background
        pg.draw.rect(self.window, self.color, self.dimensions, border_radius = self.border_radius)
        # Return early if there is no surface
        if not self.surface: return
        # Calculate offset to have image/text centered on background
        x, y, dx, dy = self.dimensions
        dx2, dy2 = self.surface.get_size()
        x += dx//2 - dx2//2
        y += dy//2 - dy2//2
        # Draw the image/text
        self.window.blit(self.surface, (x, y))

    def get_offset(self) -> tuple[int, int]:
        return (self.dimensions[0], self.dimensions[1])

    def get_size(self) -> tuple[int, int]:
        return (self.dimensions[2], self.dimensions[3])

    def is_clicked(self) -> bool:
        """Return if this Sprite is being clicked"""
        x, y = self.get_offset()
        dx, dy = self.get_size()
        mx, my = pg.mouse.get_pos()
        pressed = pg.mouse.get_pressed()[0]
        return (pressed and
                # mouse is between offset and offset + size
                x < mx < x+dx and
                y < my < y+dy)
game_gui = None
