import game_logic as gl
from random import random

class AI:
    def __init__(self, game:int, difficulty:int):
        self.game = game
        self.difficulty = difficulty

    def next_move(self, board:list[list[int]], consecutive_moves = None) -> tuple[tuple[int,int],tuple[int,int]]:
        """Give back the best move the AI thinks it can make"""
        # Setup variables
        best_moves = []
        best_move_value = None
        # loop through all possible moves
        moves = consecutive_moves if consecutive_moves else gl.game_logic.get_valid_moves(board)
        if not moves: return ((-1,-1),(-1,-1))
        for move in moves:
            # Get the value of this move recursively
            new_board = gl.game_logic.preview_move(board, move, False)
            depth = self.difficulty*4+1
            value = self.get_board_value(new_board, depth, False)
            # If this move is better then a previous one - take it
            if not best_move_value or value > best_move_value:
                best_move_value = value
                best_moves = [move]
            elif value == best_move_value:
                best_moves.append(move)
        # return ONE of the best moves
        if best_moves:
            return best_moves[int(random()*len(best_moves))]
        else: return ((-1,-1),(-1,-1))

    def get_board_value(self, board:list[list[int]], depth:int, ai_turn:bool, alpha=float('inf'), beta=float('-inf')) -> int:
        """Gets the value of the board recursively up to a specified depth using alpha-beta pruning"""
        board_value = 0
        for move in gl.game_logic.get_valid_moves(board_preview=board):
            # get new board from game logic
            new_board = gl.game_logic.preview_move(board, move, not ai_turn)
            # update alpha and beta
            if ai_turn:
                this_value = self.rate_board(new_board)
                board_value = max(this_value, board_value)
                alpha = min(alpha, this_value)
                if beta >= alpha: break
            else:
                this_value = self.rate_board(new_board)
                board_value = min(this_value, board_value)
                beta = max(beta, this_value)
                if beta >= alpha: break
            # get deeper values
            next_value = self.get_board_value(new_board, depth-1, not ai_turn, alpha, beta) if depth > 0 else None
            # correct the board value
            if ai_turn and next_value:
                board_value = max(next_value, board_value)
            elif next_value:
                board_value = min(next_value, board_value)
        return board_value
    
    def rate_board(self, board) -> int:
        """Determine how good a given board is according to the AI"""
        # Count pieces of each player
        ai_pieces = player_pieces = 0
        for row in board:
            for piece in row:
                if piece == 1: player_pieces += 1
                elif piece == 2: ai_pieces += 1
        # How far is the furthes own piece
        ai_highest_piece = player_highest_piece = 0
        for idx, row in enumerate(board):
            if 1 in row and player_highest_piece == 0:
                player_highest_piece = len(board) - idx
            elif 2 in row:
                ai_highest_piece = idx
        # Pawn alone in a collumn
        ai_sole_pawn = player_sole_pawn = 0
        if self.game == 0:
            sole_pawn_list = [0,0,0,0,0,0]
            for row in board:
                for col, piece in enumerate(row):
                    if sole_pawn_list[col] == 0 and piece != 0:
                        sole_pawn_list[col] = piece
                    if (sole_pawn_list[col] == 1 and piece == 2 or
                        sole_pawn_list[col] == 2 and piece == 1):
                        sole_pawn_list[col] = -1
            for piece in sole_pawn_list:
                if piece == 1: player_sole_pawn += 1
                elif piece == 2: ai_sole_pawn += 1
        # Checkers diagonal empty spaces
        ai_diagonal = player_diagonal = 0
        if self.game == 1:
            for x, row in enumerate(board):
                for y, piece in enumerate(row):
                    if piece == 0: continue
                    none_diagonal = True
                    # Go through all diagonal neightbours
                    for sx, sy in [(x-1, y-1), (x+1, y-1), (x-1, y+1), (x+1, y+1)]:
                        if (none_diagonal and
                            0 <= sx < len(board) and
                            0 <= sy < len(board) and
                            board[sx][sy] != 0):
                            none_diagonal = False
                    if none_diagonal and piece == 1:
                        player_diagonal += 1
                    if none_diagonal and piece == 2:
                        ai_diagonal += 1
        # return all values but weighted
        return (
            ai_pieces * 100 +
            player_pieces * -130 +
            ai_highest_piece * 160 +
            player_highest_piece * -180 +
            ai_sole_pawn * 120 +
            player_sole_pawn * -150 +
            ai_diagonal * -70 +
            player_diagonal * 80 )
