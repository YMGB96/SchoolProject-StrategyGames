import pygame

class GamePiece():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))