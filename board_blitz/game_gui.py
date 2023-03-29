import pygame

class game_gui:
    def __init__(self) -> None:
        pass

    
def drawBoard():
    renderStartX = 100
    renderStartY = 70
    tileSize = 60
    positionBlack = [renderStartX,renderStartY,tileSize,tileSize]
    positionWhite = [tileSize*2,renderStartY,tileSize,tileSize]
    for height in range(0,6):
        if (height%2 == 0):
            positionBlack[0] = renderStartX+tileSize
            positionWhite[0] = renderStartX
        else:
            positionBlack[0] = renderStartX
            positionWhite[0] = renderStartX+tileSize
        for width in range (0,3):
            pygame.draw.rect(window,(90,90,90),(positionBlack))
            pygame.draw.rect(window,(255,255,255),(positionWhite))
            positionBlack[0] += tileSize*2
            positionWhite[0] += tileSize*2
            width += 1
        height += 1
        positionBlack[1] += tileSize
        positionWhite[1] += tileSize

pygame.init()
window = pygame.display.set_mode((640,480))

while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break

    drawBoard()
    pygame.display.update()      

pygame.quit()