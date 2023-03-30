import pygame
import gamePieces

class GamePiecePlayer(gamePieces.GamePiece):
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self, window):
        doStuff = False
        mousePosition = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePosition):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                doStuff = True
                print("Klick")
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        window.blit(self.image, (self.rect.x, self.rect.y))
        return doStuff