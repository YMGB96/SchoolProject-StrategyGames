class game_logic:
    def __init__(self) -> None:
        pass

import ai as ai
# test case

board = [[0,0,0,1,1,1],
         [0,0,1,0,0,0],
         [1,1,0,0,0,0],
         [0,2,0,0,0,0],
         [0,0,0,0,0,0],
         [2,0,2,2,2,2]]



chosen_piece = (5,1)
game_over = False
game_won: bool
player_turn: bool
# board = list[list[int]]
moves: list[tuple[tuple[int]]]


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
    game_is_finished() #if game_over true then end
    if player_turn == True: #valid moves for single selected piece by player
        if board[posY-1][posX] == 0:
            board[posY-1][posX] = 3
        if posX >= 1:
            if board[posY-1][posX-1] == 1:
                board[posY-1][posX-1] = 3
        if posX <= 4:
            if board[posY-1][posX+1] == 1:
                board[posY-1][posX+1] = 3
        print(board)
        return board
    if player_turn == False: #all available valid moves
        print("all possible moves for AI")
        for y,x in find_all(board, 1):
            if board[y+1][x] == 0:
                moves.append([(y,x),(y+1,x)])
            if x >= 1:
                if board[y+1][x-1] == 2:
                    moves.append([(y,x),(y+1,x-1)])
            if x <= 4:
                if board[y+1][x+1] == 2:
                    moves.append([(y,x),(y+1,x+1)])
        print(moves)
        


def start_ai(board):
    ai.next_move(board, 3) #placeholder for communication with AI 


#checks to see if winning conditions are met
def game_is_finished():
    for column in board[0]:
        if column == 2:
            print("placeholder, send win bool")
            game_over = True
            game_won = True
    for column in board[5]:
        if column == 1:
            print("placeholder, send loss bool")
            game_over = True
            game_won = False
