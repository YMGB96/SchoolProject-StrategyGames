import pygame

class GamePiece():
    def __init__(self,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.clicked = False

    def draw(self, window, rect):
        self.rect.topleft = (rect.x, rect.y)
        window.blit(self.image, rect)