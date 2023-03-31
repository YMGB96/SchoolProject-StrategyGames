class game_logic:
    def __init__(self) -> None:
        pass

import ai as ai
import game_gui as game_gui


def start(active_user, active_game, active_difficulty):
    global user
    global game
    global difficulty   
    global board 
    user = active_user
    game = active_game
    difficulty = active_difficulty
    if game == 0:
        board = [[2,2,2,2,2,2],
                 [0,0,0,0,0,0],
                 [0,0,0,0,0,0],
                 [0,0,0,0,0,0],
                 [0,0,0,0,0,0],
                 [1,1,1,1,1,1]]
    elif game == 1:
        board = [[0,2,0,2,0,2],
                 [2,0,2,0,2,0],
                 [0,0,0,0,0,0],
                 [0,0,0,0,0,0],
                 [0,1,0,1,0,1],
                 [1,0,1,0,1,0]]
        
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
        if game == 0:     
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
        elif game == 1:
            if player_turn: #valid moves for single selected piece by player            
                if posX >= 2:
                    if board[posY-1][posX-1] == 2 and board[posY-2][posX-2] == 0:
                        board[posY-2][posX-2] = 3
                if posX <= 3:
                    if board[posY-1][posX+1] == 2 and board[posY-2][posX+2] == 0:
                        board[posY-2][posX+2] = 3
                if any(3 in row for row in board) == False:
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
                moves = []
                for y,x in find_all(board, 2):                
                    if x >= 2:
                        if board[y+1][x-1] == 1 and board[y+2][x-2] == 0:
                            moves.append([(y,x),(y+2,x-2)])
                    if x <= 3:
                        if board[y+1][x+1] == 1 and board[y+2][x+2] == 0:
                            moves.append([(y,x),(y+2,x+2)])
                if moves == []:
                    for y,x in find_all(board, 2):                
                        if x >= 1:
                            if board[y+1][x-1] == 0:
                                moves.append([(y,x),(y+1,x-1)])
                        if x <= 4:
                            if board[y+1][x+1] == 0:
                                moves.append([(y,x),(y+1,x+1)])
                    return moves
                else:
                    return moves
        


def switch_turn(board):
    # depending on what is sent, change board accordingly
    ai.next_move(board, difficulty) #placeholder for communication with AI
    game_gui.player_start(board) #placeholder for communication to gui



#checks to see if winning conditions are met
def game_is_finished(*args, **kwargs):
    game_cancelled = kwargs.get('game_cancelled', False)
    valid_moves_empty = kwargs.get('valid_moves_empty', False)
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
    if valid_moves_empty:
        return
    if game_cancelled:
        game_won = False
        #game_gui.gameover(game_won, game_cancelled)
        #SQL befehl mit daten  
        #fancy schmancy info to gui that game is over and lost, loss into database
        return
