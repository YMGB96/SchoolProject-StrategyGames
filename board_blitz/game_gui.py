import pygame as pg
from math import floor

class GameGui:
    is_paused = False
    colors = {
        'black': (116, 116, 116),
        'white': (222, 222, 222),
        'background': (245, 245, 245),
        'text': (0, 0, 0),
        'button': (158, 158, 158),
    }
    texts = {
        'menu': 'Menu',
        'resume': 'Zurück zum Spiel',
        'surrender': 'Spiel aufgeben',
    }
    selected_piece = [-1, -1]
    was_pressed = False
    def __init__(self, width = 1125, height = 800):
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
        piece_scale = tile_size * 0.8
        self.images = {
            'player': pg.transform.scale(pg.image.load('./board_blitz/resources/testPiece.png'), (piece_scale, piece_scale)),
            'enemy': pg.transform.scale(pg.image.load('./board_blitz/resources/testPieceEnemy.png'), (piece_scale, piece_scale)),
            'valid': pg.transform.scale(pg.image.load('./board_blitz/resources/validMove.png'), (piece_scale, piece_scale)),
        }
        # Set up all menu buttons
        fontsize = floor(height * 0.023)
        font = pg.font.SysFont('Arial Black', fontsize)
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

    def draw_board(self, board: list[list[int]]):
        """Updates all sprites according to the given board and renders it"""
        # go through the whole board
        for x, row in enumerate(self.board):
            for y, piece in enumerate(row):
                # set correct sprites
                match board[x][y]:
                    case 1: piece.surface = self.images['player']
                    case 2: piece.surface = self.images['enemy']
                    case 3: piece.surface = self.images['valid']
                # draw each piece
                piece.draw()
                # remember what piece was last clicked
                if not self.was_pressed and not self.is_paused and piece.is_clicked():
                    last_piece = self.selected_piece
                    self.selected_piece = [x, y]
                    if last_piece != self.selected_piece:
                        # here we know that a new piece was selected and board[x][y] is it's id
                        print(board[x][y])

    def render(self):
        # fill the background
        background = pg.Surface(self.window.get_size())
        background.fill(self.colors['background'])
        self.window.blit(background, (0,0))
        # draw the current board
        test_board = [[0,2,0,2,0,2],
                      [2,0,2,0,2,0],
                      [0,0,0,0,0,0],
                      [0,0,0,0,0,0],
                      [0,1,0,1,0,1],
                      [1,0,1,0,1,0]]
        self.draw_board(test_board)
        # draw the menu button in the corner
        self.menu_buttons['menu'].draw()
        # check if it has been clicked
        if not self.was_pressed and self.menu_buttons['menu'].is_clicked():
            self.is_paused = True
        # render additional elements if the game is paused
        if self.is_paused:
            # overlay to darken the game elements
            overlay = pg.Surface(self.window.get_size())
            overlay.set_alpha(110)
            overlay.fill((0,0,0))
            self.window.blit(overlay, (0,0))
            # render 'paused' buttons
            self.menu_buttons['resume'].draw()
            self.menu_buttons['surrender'].draw()
            # check if the buttons have been clicked
            if not self.was_pressed and self.menu_buttons['resume'].is_clicked():
                self.is_paused = False
        # update mouse was pressed
        self.was_pressed = pg.mouse.get_pressed()[0]

class Sprite:
    """Abstraction of a 'thing to render', knows if it is clicked or not"""
    border_radius = 5
    def __init__(self, window, surface, dimensions, color):
        self.color = color
        self.window = window
        self.surface = surface
        self.dimensions = dimensions

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
        x, y = self.get_offset()
        dx, dy = self.get_size()
        mx, my = pg.mouse.get_pos()
        pressed = pg.mouse.get_pressed()[0]
        return (pressed and
                x < mx < x+dx and
                y < my < y+dy)



pg.init()
pg.font.init()
game_gui = GameGui()

run = True
while run:

    game_gui.render()

    # drawText("Spielername",font,textColour,30,(screenHeight-30))
    # drawText("Gegner",font,textColour,(screenWidth-100),30)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    
    pg.display.update()
    pg.time.wait(50)

pg.quit()
