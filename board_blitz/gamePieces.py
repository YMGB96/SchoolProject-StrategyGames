import pygame

class GamePiece():
    def __init__(self,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.clicked = False

    def draw(self, window, x, y):
        self.rect.topleft = (x,y)
        window.blit(self.image, (self.rect.x, self.rect.y))