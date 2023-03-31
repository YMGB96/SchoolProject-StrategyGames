class game_logic:
    def __init__(self) -> None:
        pass

import ai as ai
import game_gui as game_gui
# test case

board = [[0,2,0,2,0,2],
         [2,0,2,0,2,0],
         [0,0,0,1,0,0],
         [0,0,0,0,0,0],
         [0,1,0,1,0,1],
         [1,0,1,0,1,0]]



chosen_piece = (4,1)
game_won: bool
player_turn: bool


def find_all(matrix, element): #helperfunction for get_valid_moves ai version
    yield from ((row_no, col_no)   #Iterate through all row, column indexes in a 2D Matrix where matrix[row][col] == element
        for row_no, row in enumerate(matrix)  
        for col_no, matrix_element in enumerate(row)  
        if matrix_element == element)  
        
#checks and returns valid move possibilities, for a single piece for the player, all pieces for the AI
def get_valid_moves(board, *args, **kwargs):
    chosen_piece = kwargs.get('chosen_piece', None)
    player_turn = kwargs.get('player_turn', False)
    if chosen_piece != None:
        posY = chosen_piece[0]
        posX = chosen_piece[1]
    #game_is_finished() #if game_over true then end
    if game_is_finished():
        return
    else:
        if player_turn: #valid moves for single selected piece by player
            if board[posY-1][posX] == 0:
                board[posY-1][posX] = 3
            if posX >= 1:
                if board[posY-1][posX-1] == 2:
                    board[posY-1][posX-1] = 3
            if posX <= 4:
                if board[posY-1][posX+1] == 2:
                    board[posY-1][posX+1] = 3
            return board
        else: #all available valid moves
            print("all possible moves for AI")
            moves = []
            for y,x in find_all(board, 2):
                if board[y+1][x] == 0:
                    moves.append([(y,x),(y+1,x)])
                if x >= 1:
                    if board[y+1][x-1] == 1:
                        moves.append([(y,x),(y+1,x-1)])
                if x <= 4:
                    if board[y+1][x+1] == 1:
                        moves.append([(y,x),(y+1,x+1)])
            print(moves)
            return moves
        


def switch_turn(board):
    # depending on what is sent, change board accordingly
    ai.next_move(board, 3) #placeholder for communication with AI
    game_gui.player_start(board) #placeholder for communication to gui 


#checks to see if winning conditions are met
def game_is_finished(*args, **kwargs):
    game_cancelled = kwargs.get('game_cancelled', False)
    for column in board[0]:
        if column == 1:
            print("placeholder, send win bool")
            game_won = True
            #game_gui.gameover(game_won)
            # SQL befehl mit daten  
            #fancy schmancy info to gui that game is over and lost, loss into database
            return
    for column in board[5]:
        if column == 2:
            print("placeholder, send loss bool")
            game_won = False
            #game_gui.gameover(game_won)
            # SQL befehl mit daten  
            #fancy schmancy info to gui that game is over and lost, loss into database
            return
    if game_cancelled:
        game_won = False
        #game_gui.gameover(game_won, game_cancelled)
        # SQL befehl mit daten  
        #fancy schmancy info to gui that game is over and lost, loss into database
        return


## Dame here as placeholder, depending on brains opinion

def find_all2(matrix, element): #helperfunction for get_valid_moves ai version
    yield from ((row_no, col_no)   #Iterate through all row, column indexes in a 2D Matrix where matrix[row][col] == element
        for row_no, row in enumerate(matrix)  
        for col_no, matrix_element in enumerate(row)  
        if matrix_element == element)  
        
#checks and returns valid move possibilities, for a single piece for the player, all pieces for the AI
def get_valid_moves2(board, *args, **kwargs):
    chosen_piece = kwargs.get('chosen_piece', None)
    player_turn = kwargs.get('player_turn', False)
    if chosen_piece != None:
        posY = chosen_piece[0]
        posX = chosen_piece[1]
    #game_is_finished() #if game_over true then end
    if game_is_finished2():
        return
    else:
        if player_turn: #valid moves for single selected piece by player            
            if posX >= 2:
                if board[posY-1][posX-1] == 2 and board[posY-2][posX-2] == 0:
                    board[posY-2][posX-2] = 3
            if posX <= 3:
                if board[posY-1][posX+1] == 2 and board[posY-2][posX+2] == 0:
                    board[posY-2][posX+2] = 3
            if any('3' in row for row in board) == False:
                if posX >= 1:
                    if board[posY-1][posX-1] == 0:
                        board[posY-1][posX-1] = 3
                if posX <= 4:
                    if board[posY-1][posX+1] == 0:
                        board[posY-1][posX+1] = 3
                print (board)
                return board
            else:
                print (board)
                return board
        else: #all available valid moves
            print("all possible moves for AI")
            moves = []
            for y,x in find_all2(board, 2):                
                if x >= 2:
                    if board[y+1][x-1] == 1 and board[y+2][x-2] == 0:
                        moves.append([(y,x),(y+2,x-2)])
                if x <= 4:
                    if board[y+1][x+1] == 1 and board[y+2][x+2] == 0:
                        moves.append([(y,x),(y+2,x+2)])
                if any("3" in row for row in board) == False:
                    if x >= 1:
                        if board[y+1][x-1] == 0:
                            moves.append([(y,x),(y+1,x-1)])
                    if x <= 4:
                        if board[y+1][x+1] == 0:
                            moves.append([(y,x),(y+1,x+1)])
                    print(moves)
                    return moves
                else:
                    print(moves)
                    return moves
        


def switch_turn2(board):
    # depending on what is sent, change board accordingly
    ai.next_move(board, 3) #placeholder for communication with AI
    game_gui.player_start(board) #placeholder for communication to gui
    #check to see if jumps are possible, if yes back to turn player, else switch turn


#checks to see if winning conditions are met
def game_is_finished2(*args, **kwargs):
    game_cancelled = kwargs.get('game_cancelled', False)
    for column in board[0]:
        if column == 1:
            print("placeholder, send win bool")
            game_won = True
            #game_gui.gameover(game_won)
            # SQL befehl mit daten  
            #fancy schmancy info to gui that game is over and lost, loss into database
            return
    for column in board[5]:
        if column == 2:
            print("placeholder, send loss bool")
            game_won = False
            #game_gui.gameover(game_won)
            # SQL befehl mit daten  
            #fancy schmancy info to gui that game is over and lost, loss into database
            return
    if game_cancelled:
        game_won = False
        #game_gui.gameover(game_won, game_cancelled)
        # SQL befehl mit daten  
        #fancy schmancy info to gui that game is over and lost, loss into database
        return
