import game_logic
import math

board = [[1,1,1,1,1,1],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0],
         [2,2,2,2,2,2]]

# this function will count the pieces of the ai and player
def rate_board(board: list[list[int]]) -> int:
    player_pieces = 0 
    ai_pieces = 0
    for row in board: 
        for piece in row:
            # if there is a player piece (1) in the row then the count goes up by one
            if piece == 1:
                player_pieces += 1
            # if there is a ai piece (2) in the row then count goes up by one 
            elif piece == 2:
                ai_pieces += 1
    # returns the total number of pieces for both sides            
    return player_pieces - ai_pieces
            
# function to find out what the highest player piece on the board is
def get_highest_piece(board, player):
    # currently none of the pieces are higher then the rest 
    highest_piece = None
    # checks row after row for a piece 
    for row in board: 
        for piece in row:
            # if it finds a piece it checks if its higher than any other piece
            if piece == player and (highest_piece is None or piece > highest_piece):
                # if that piece is higher it changes the "highest Piece" to that new piece
                highest_piece = piece 
    return highest_piece

# same as before only now for ai
def get_highest_ai_piece(board, ai):
    highest_piece = None 
    for row in board: 
        for piece in row: 
            if piece == ai and (highest_piece is None or piece > highest_piece):
                highest_piece = piece 
    return highest_piece

# funtion checks if the ai piece is alone in a row or not
def is_ai_alone(board, ai_piece):
    # checks row after row for piece
    for row in board:
        count = 0 
        for piece in row:
            # if there is a piece count goes up by one  
            if piece == ai_piece:
                count +=1
        if count == 1:
            return True
        return False 

# same as before only now for the player
def is_player_alone(board, player):
    for row in board:
        count = 0
        for piece in row:
            if piece == player:
                count +=1
        if count == 1:
            return True 
    return False


##### Dame-Spiel #####

checkers_board = [
    [0, 2, 0, 2, 0, 2],
    [2, 0, 2, 0, 2, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1],
]

ai_num = 2
player_num = 1
#AI for checkers

#same as the rate_board function
def rate_checkers_board(checkers_board: list[list[int]]) -> int:
    player_pieces = 0 
    ai_pieces = 0
    for row in board: 
        for piece in row:
            if piece == 1:
                player_pieces += 1
            elif piece == 2:
                ai_pieces += 1
    return player_pieces - ai_pieces


# funtion to find the highest ai stone 
def highest_ai_stone(checkers_board, ai_num):
    # indices start at 0 so we have a position of (0, 0)
    highest_row = -1
    highest_col = -1
    # loop through the whole board searching for ai stones
    for row in range(len(checkers_board)):
        for col in range(len(checkers_board[row])):
            # if a ai stone is found it compares the row number to the highest_row
            if checkers_board[row][col] == ai_num:
                if row > highest_row:
                    # updates the highest_row and _col with the new position
                    highest_row = row
                    highest_col = col
    # if highest row and highest column still have their values -1 it returns None
    # to indicate that there are no ai stones on the board 
    if highest_row == -1 and highest_col == -1:
        return None
    # If it found a stone it returns the row and column position of the highest ai stone
    else:
        return (highest_row, highest_col)


# same as before only for the player
def highest_player_stone(checkers_board, player_num):
    highest_row = -1
    highest_col = -1
    for row in range(len(checkers_board)):
        for col in range(len(checkers_board[row])):
            if checkers_board[row][col] == player_num:
                if row > highest_row:
                    highest_row = row
                    highest_col = col
    if highest_row == -1 and highest_col == -1:
        return None
    else:
        return (highest_row, highest_col)
    


def next_move(board: list[list[int]], difficult: int, *args, **kwargs) ->  tuple[tuple[int,int], tuple[int,int]]:
    """returns the best possible move according to minimax"""
    consecutive_moves: list[tuple[tuple[int,int], tuple[int,int]]] = kwargs.get('consecutive_moves', None)
    # gets the valid moves of the ai
    if game_logic.game_logic.consecutive_move:
        ai_moves: list[tuple[tuple[int,int], tuple[int,int]]] = consecutive_moves
    else:
        ai_moves: list[tuple[tuple[int,int], tuple[int,int]]] = game_logic.game_logic.get_valid_moves()
    # best_board sets the lowest possible board
    best_board: int = -999999999
    # define dummy best_move
    best_move: tuple[tuple[int,int], tuple[int,int]] = ((0,0),(0,0))
    # for loop loops trough all moves that are valid for the ai
    for ai_move in ai_moves:
        # get board after ai move
        ai_board: list[list[int]] = game_logic.game_logic.preview_move(board, ai_move, 2)
        # looks for valid available player move
        player_moves: list[tuple[tuple[int,int], tuple[int,int]]] = game_logic.game_logic.player_move_list(ai_board)
        # for loop loops trough all moves that are valid for the player
        for player_move in player_moves:
            # gets board after player move
            player_board = game_logic.game_logic.preview_move(ai_board, player_move, 1)
            # rating is result of player board and recursive move (recursive looks at all possible depths)
            rating = rate_board(player_board) + recursive_move(
                player_board,
                # gets valid moves from the player board and depths is difficulty -1
                game_logic.game_logic.player_move_list(player_board),
                difficult-1)
            # if the rating is bigger than best board, the best board will be saved
            # and the ais move will be set to its current best move
            if rating > best_board:
                best_board = rating
                best_move = ai_move
    return best_move


def recursive_move(board: list[list[int]], moves: list[tuple[tuple[int,int], tuple[int,int]]], depth: int) -> int:
    """recursive checks all possible depths"""
    # depth gets set lower
    depth -= 1
    # if depth not available return 0
    if not depth: return 0

    # following code is only changed slightly from previous code
    best_board: int = -999999999
    for ai_move in moves:
        ai_board = game_logic.game_logic.preview_move(board, ai_move, 2)
        player_moves: list[tuple[tuple[int,int], tuple[int,int]]] = game_logic.game_logic.player_move_list(ai_board)
        for player_move in player_moves:
            player_board = game_logic.game_logic.preview_move(ai_board, player_move, 1)
            rating = rate_board(player_board) + recursive_move(
                player_board,
                game_logic.game_logic.player_move_list(player_board),
                # instead of difficulty -1 now we use the reduced depth 
                depth)
            if rating > best_board:
                best_board = rating
    return best_board
