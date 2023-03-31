import pygame
from gamePieces import GamePiece
from gamePiecesPlayer import GamePiecePlayer

class game_gui:
    def __init__(self) -> None:
        pass

pygame.font.init()

testArrayInitial = [[0,2,0,2,0,2],[2,0,2,0,2,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,1,0,1,0,1],[1,0,1,0,1,0]]
testArrayValid = [[0,2,0,2,0,2],[2,0,2,0,2,0],[0,0,0,0,0,0],[3,0,3,0,0,0],[0,1,0,1,0,1],[1,0,1,0,1,0]]
currentArray = testArrayInitial

testPlayerImg = pygame.image.load('./board_blitz/resources/testPiece.png')
testEnemyImg = pygame.image.load('./board_blitz/resources/testPieceEnemy.png')
testValidMove = pygame.image.load('./board_blitz/resources/validMove.png')

testButtonRect = pygame.image.load('./board_blitz/resources/validMove.png')

testPiecePlayer = GamePiecePlayer(testPlayerImg)
testEnemy = GamePiece(testEnemyImg)
testValidMoveIndicator = GamePiecePlayer(testValidMove)

testButton = GamePiecePlayer(testButtonRect)
testButtonMenu = GamePiecePlayer(testButtonRect)

screenWidth = 1040
screenHeight = 800

renderStartX = 100
renderStartY = 70
tileSize = 60

isPaused = False

isPieceClicked = False
pieceClickedPosition = []
    
font = pygame.font.SysFont("arialblack",20)
textColour = (0,0,0)

#functions

def drawText(textToDraw, font, textColour, x, y):
    text = font.render(textToDraw, True, textColour)
    window.blit(text, (x,y))


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
    rowNumber = 0
    columnNumber = 0
    # following code iterates over every row and column to draw the game pieces
    for rowNumber in range(0,6):
        for piece in gameArray[rowNumber]:
            position = pygame.Rect((renderStartX+(columnNumber*tileSize)),(renderStartY+(rowNumber*tileSize)),tileSize,tileSize)
            if(piece == 2):
                testEnemy.draw(window,position)
                #draws the unclickable enemy pieces
            elif(piece == 1):
                if testPiecePlayer.draw(window,position):
                    # pieceClickedPosition = [rowNumber,columnNumber] 
                    global currentArray 
                    global isPieceClicked
                    currentArray = displayValidMoves()
                    isPieceClicked = True
                    # gets the valid moves and saves that a piece has been clicked
            elif(piece == 3 and isPieceClicked):
                if testValidMoveIndicator.draw(window,position):
                    global testArrayInitial
                    global testArrayValid
                    testArrayInitial[rowNumber][columnNumber] = 1 # sets the clicked valid move to player piece
                    testArrayValid[rowNumber][columnNumber] = 1 # this will be made obsolete as soon as we get actual valid move data
                    currentArray = testArrayInitial
                    isPieceClicked = False
            columnNumber += 1
        columnNumber = 0
        rowNumber += 1

def displayValidMoves():
    return testArrayValid
    # TODO: access game logic for valid moves

def pauseButton():
    positionPauseButton = pygame.Rect(10,10,60,60)
    global isPaused
    if testButton.draw(window,positionPauseButton) and not isPaused:
        isPaused = True
        print("Pause clicked")
        # pygame.draw.rect(window,(0,0,0),(screenWidth,screenHeight,0,0)) # should do an overlay screen but doesn't :)
        

def drawPauseMenu():
    positionAbortButton = pygame.Rect(30,(screenHeight/2+120),tileSize,tileSize)
    positionMainMenuButton = pygame.Rect(30,(screenHeight/2),tileSize,tileSize)
    positionBackButton = pygame.Rect(30,(screenHeight/2-120),tileSize,tileSize)
    global isPaused
    if testButtonMenu.draw(window,positionAbortButton) and isPaused == True:
        print("Spiel aufgeben")
    if testButtonMenu.draw(window,positionMainMenuButton) and isPaused == True:
        print("Hauptmenü")
    if testButtonMenu.draw(window,positionBackButton) and isPaused == True:
        print("Zurück zum Spiel")
        isPaused = False

pygame.init()
window = pygame.display.set_mode((screenWidth,screenHeight))

background = pygame.Surface(window.get_size())
background = background.convert()
background.fill((150,150,150))
window.blit(background, (0,0))

run = True
while run:

    drawBoard()
    drawPieces(currentArray)
    pauseButton()
    if isPaused:
        drawPauseMenu()
    drawText("Spielername",font,textColour,30,(screenHeight-30))
    drawText("Gegner",font,textColour,(screenWidth-100),30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()      
    pygame.time.wait(50)

pygame.quit()