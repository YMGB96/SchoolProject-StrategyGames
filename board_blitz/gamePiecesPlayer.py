import pygame
import gamePieces

class GamePiecePlayer(gamePieces.GamePiece):
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.clicked = False

    def draw(self, window, x, y):
        self.rect.topleft = (x,y)
        isClicked = False
        mousePosition = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePosition):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                isClicked = True
                print("Klick")
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        window.blit(self.image, (self.rect.x, self.rect.y))
        return isClicked