import pygame
from gamePieces import GamePiece
from gamePiecesPlayer import GamePiecePlayer

class game_gui:
    def __init__(self) -> None:
        pass

testArrayInitial = [[0,2,0,2,0,2],[2,0,2,0,2,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,1,0,1,0,1],[1,0,1,0,1,0]]
testArrayValid = [[0,2,0,2,0,2],[2,0,2,0,2,0],[0,0,0,0,0,0],[3,0,3,0,0,0],[0,1,0,1,0,1],[1,0,1,0,1,0]]

testPlayerImg = pygame.image.load('./board_blitz/resources/testPiece.png')
testEnemyImg = pygame.image.load('./board_blitz/resources/testPieceEnemy.png')
testValidMove = pygame.image.load('./board_blitz/resources/validMove.png')

testPiecePlayer = GamePiecePlayer(testPlayerImg)
testEnemy = GamePiece(testEnemyImg)
testValidMoveIndicator = GamePiecePlayer(testValidMove)

renderStartX = 100
renderStartY = 70
tileSize = 60

isPieceClicked = False
pieceClickedPosition = []
    
def drawBoard():
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

def drawPieces(gameArray):
    print(gameArray)
    reiheNr = 0
    spalteNr = 0
    for reiheNr in range(0,6):
        for piece in gameArray[reiheNr]:
            if(piece == 2):
                testEnemy.draw(window,(renderStartX+(spalteNr*tileSize)),(renderStartY+(reiheNr*tileSize)))
                #draws the unclickable enemy pieces
            elif(piece == 1):
                if testPiecePlayer.draw(window,(renderStartX+(spalteNr*tileSize)),(renderStartY+(reiheNr*tileSize))):
                    # pieceClickedPosition = [reiheNr[spalteNr]] 
                    isPieceClicked = True
                    gameArray = displayValidMoves()
                    print(gameArray)
                #supposed to trigger visible moves :/
            elif(piece == 3) and isPieceClicked:
                print("not accessed")
                if testValidMoveIndicator.draw(window,(renderStartX+(spalteNr*tileSize)),(renderStartY+(reiheNr*tileSize))):
                    gameArray[reiheNr][spalteNr] == 1
                    isPieceClicked = False
                #supposed to, when valid move is clicked, to set new position of piece
            spalteNr += 1
        spalteNr = 0
        reiheNr += 1

def displayValidMoves():
    return testArrayValid

pygame.init()
window = pygame.display.set_mode((1040,800))

background = pygame.Surface(window.get_size())
background = background.convert()
background.fill((150,150,150))
window.blit(background, (0,0))

drawBoard()

run = True
while run:

    drawPieces(testArrayInitial)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()      

pygame.quit()