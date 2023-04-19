import ai
import database
import game_gui

class Game_Logic:

    player_turn: bool
    user: int
    game: int
    difficulty: int
    board: list[list[int]]
    consecutive_move = False

    def start(self, active_user, active_game, active_difficulty):
        self.player_turn = True
        self.user = active_user
        self.game = active_game
        self.difficulty = active_difficulty
        #board info: 0 = empty, 1 = own piece, 2 = opponents piece, 3 = move option to empty field, 4 = move option to opponent field
        if self.game == 0: #pawnchess
            self.board = [[2,2,2,2,2,2],
                          [0,0,0,0,0,0],
                          [0,0,0,0,0,0],
                          [0,0,0,0,0,0],
                          [0,0,0,0,0,0],
                          [1,1,1,1,1,1]]
        elif self.game == 1: #checkers
            self.board = [[0,2,0,2,0,2],
                          [2,0,2,0,2,0],
                          [0,0,0,0,0,0],
                          [0,0,0,0,0,0],
                          [0,1,0,1,0,1],
                          [1,0,1,0,1,0]]
        username = database.database.get_user(self.user)['username']
        game_gui.game_gui = game_gui.GameGui(self.difficulty, username)
        self.ai = ai.AI(self.game, self.difficulty)
        
            
    def find_all(self, matrix, element): #helperfunction for get_valid_moves ai version
        yield from ((row_no, col_no)   #Iterate through all row, column indexes in a 2D Matrix where matrix[row][col] == element
            for row_no, row in enumerate(matrix)  
            for col_no, matrix_element in enumerate(row)  
            if matrix_element == element)  
            
    #checks and returns valid move possibilities, for a single piece for the player, all pieces for the AI
    def get_valid_moves(self, chosen_piece = None, board_preview = None):
        if not board_preview:
            board_preview = [row.copy() for row in self.board]
        if self.game == 0:
            if self.player_turn: #valid moves for single selected piece by player
                if chosen_piece != None:
                    posY = chosen_piece[0]
                    posX = chosen_piece[1]
                else:
                    return
                if self.board[posY-1][posX] == 0:
                    board_preview[posY-1][posX] = 3
                if posX >= 1:
                    if self.board[posY-1][posX-1] == 2:
                        board_preview[posY-1][posX-1] = 4
                if posX <= 4:
                    if self.board[posY-1][posX+1] == 2:
                        board_preview[posY-1][posX+1] = 4
                return board_preview
            else: #all available valid moves
                moves = []
                for y,x in self.find_all(self.board, 2):
                    if self.board[y+1][x] == 0:
                        moves.append([(y,x),(y+1,x)])
                    if x >= 1:
                        if self.board[y+1][x-1] == 1:
                            moves.append([(y,x),(y+1,x-1)])
                    if x <= 4:
                        if self.board[y+1][x+1] == 1:
                            moves.append([(y,x),(y+1,x+1)])
                if moves == []:
                    self.game_is_finished(valid_ai_moves_empty= True)
                    return
                return moves
        elif self.game == 1:
            if self.player_turn and self.consecutive_move == False: #valid moves for single selected piece by player            
                if chosen_piece != None:
                    posY = chosen_piece[0]
                    posX = chosen_piece[1]
                else:
                    return
                unavoidable_moves= []
                for y,x in self.find_all(self.board, 1):                
                    if x >= 2:
                        if self.board[y-1][x-1] == 2 and self.board[y-2][x-2] == 0:
                            unavoidable_moves.append((y,x))
                    if x <= 3:
                        if self.board[y-1][x+1] == 2 and self.board[y-2][x+2] == 0:
                            unavoidable_moves.append((y,x))
                if (posY,posX) in unavoidable_moves or unavoidable_moves ==[]:
                    if posX >= 2:
                        if self.board[posY-1][posX-1] == 2 and self.board[posY-2][posX-2] == 0:
                            board_preview[posY-2][posX-2] = 3
                    if posX <= 3:
                        if self.board[posY-1][posX+1] == 2 and self.board[posY-2][posX+2] == 0:
                            board_preview[posY-2][posX+2] = 3
                    if any(3 in row for row in board_preview) == False:
                        if posX >= 1:
                            if self.board[posY-1][posX-1] == 0:
                                board_preview[posY-1][posX-1] = 3
                        if posX <= 4:
                            if self.board[posY-1][posX+1] == 0:
                                board_preview[posY-1][posX+1] = 3
                        return board_preview
                    else:
                        return board_preview
                else:
                    return self.board    
            if self.player_turn and self.consecutive_move:
                return
            else: #all available valid moves
                moves = []
                for y,x in self.find_all(self.board, 2):                
                    if x >= 2 and y <= 3:
                        if self.board[y+1][x-1] == 1 and self.board[y+2][x-2] == 0:
                            moves.append([(y,x),(y+2,x-2)])
                    if x <= 3 and y <= 3:
                        if self.board[y+1][x+1] == 1 and self.board[y+2][x+2] == 0:
                            moves.append([(y,x),(y+2,x+2)])
                if moves == []:
                    for y,x in self.find_all(self.board, 2):                
                        if x >= 1 and y <= 4:
                            if self.board[y+1][x-1] == 0:
                                moves.append([(y,x),(y+1,x-1)])
                        if x <= 4 and y <= 4:
                            if self.board[y+1][x+1] == 0:
                                moves.append([(y,x),(y+1,x+1)])
                if moves == []:
                    self.game_is_finished(valid__ai_moves_empty= True)
                    return
                return moves
        


    def switch_turn(self, move: tuple[tuple[int, int], tuple[int, int]]):
        move = move
        if self.game_is_finished():
            return
        else:
            if self.player_turn:
                self.board[move[0][0]][move[0][1]] = 0
                self.board[move[1][0]][move[1][1]] = 1
                board_preview = [row.copy() for row in self.board]
                if self.game == 1:
                    if move[0][0]-2 == move[1][0]:
                        beaten_piece_X = (move[0][1] + move[1][1])//2
                        beaten_piece_Y = (move[0][0] + move[1][0])//2
                        self.board[beaten_piece_Y][beaten_piece_X] = 0
                        board_preview[beaten_piece_Y][beaten_piece_X] = 0
                        if move[1][1]>=2 and self.board[move[1][0]-1][move[1][1]-1] == 2 and self.board[move[1][0]-2][move[1][1]-2] == 0:
                            self.consecutive_move = True
                            board_preview[move[1][0]-2][move[1][1]-2] = 3
                        if move[1][1]<=3 and self.board[move[1][0]-1][move[1][1]+1] == 2 and self.board[move[1][0]-2][move[1][1]+2] == 0:
                            self.consecutive_move = True
                            board_preview[move[1][0]-2][move[1][1]+2] = 3
                        if any(3 in row for row in self.board) == True:
                            return board_preview
                        else:
                            self.player_turn = False
                            self.consecutive_move = False
                            self.switch_turn(self.ai.next_move(board_preview))
                            self.player_turn = True
                            return
                    else:
                        self.player_turn = False
                        self.consecutive_move = False
                        self.switch_turn(self.ai.next_move(board_preview))
                        self.player_turn = True
                        return
                else:
                    self.player_turn = False
                    self.consecutive_move = False
                    self.switch_turn(self.ai.next_move(board_preview))
                    self.player_turn = True
                    return
            else:
                self.board[move[0][0]][move[0][1]] = 0
                self.board[move[1][0]][move[1][1]] = 2
                board_preview = [row.copy() for row in self.board]
                if self.game == 1:
                    if move[0][0]+2 == move[1][0]:
                        moves = []
                        beaten_piece_X = (move[0][1] + move[1][1])//2
                        beaten_piece_Y = (move[0][0] + move[1][0])//2
                        self.board[beaten_piece_Y][beaten_piece_X] = 0
                        board_preview[beaten_piece_Y][beaten_piece_X] = 0
                        to_x, to_y = move[1]
                        if (to_y>=2 and to_x <= 3 and
                            self.board[to_x+1][to_y-1] == 1 and
                            self.board[to_x+2][to_y-2] == 0):
                            moves.append([(to_x,to_y),(to_x+2,to_y-2)])
                            self.consecutive_move = True
                        if (to_y<=3 and to_x <= 3 and
                            self.board[to_x+1][to_y+1] == 1 and
                            self.board[to_x+2][to_y+2] == 0):
                            moves.append([(to_x,to_y),(to_x+2,to_y+2)])
                            self.consecutive_move = True
                        if moves != []:
                            self.switch_turn(self.ai.next_move(board_preview, consecutive_moves = moves))
                        else:
                            self.player_turn = True
                            self.consecutive_move = False
                            self.game_is_finished()
                            return
                else:
                    self.player_turn = True
                    self.consecutive_move = False
                    self.game_is_finished()
                    return        

    def preview_move(self, board:list[list[int]], move:tuple[tuple[int,int], tuple[int,int]], player_moves:bool) -> list[list[int]]:
        ai_board = [row.copy() for row in board]
        if player_moves:
            ai_board[move[0][0]][move[0][1]] = 0
            ai_board[move[1][0]][move[1][1]] = 1
            if self.game == 1 and move[0][0] != move[1][0] -1:
                ai_board[(move[0][0] + move[1][0])//2][(move[0][1] + move[1][1])//2] = 0
        else:
            ai_board[move[0][0]][move[0][1]] = 0
            ai_board[move[1][0]][move[1][1]] = 2
            if self.game == 1 and move[0][0] != move[1][0] +1:
                ai_board[(move[0][0] + move[1][0])//2][(move[0][1] + move[1][1])//2] = 0    
        return ai_board

    def player_move_list(self, board:list[list[int]]) -> list[tuple[tuple[int,int], tuple[int,int]]]:
        player_moves = []
        board = board
        if self.game == 0:
                for y,x in self.find_all(board, 1):
                    if board[y-1][x] == 0:
                        player_moves.append([(y,x),(y-1,x)])
                    if x >= 1:
                        if board[y-1][x-1] == 2:
                            player_moves.append([(y,x),(y-1,x-1)])
                    if x <= 4:
                        if board[y-1][x+1] == 2:
                            player_moves.append([(y,x),(y-1,x+1)])
        else:
            for y,x in self.find_all(board, 1):                
                    if x >= 2:
                        if board[y-1][x-1] == 1 and board[y-2][x-2] == 0:
                            player_moves.append([(y,x),(y-2,x-2)])
                    if x <= 3:
                        if board[y-1][x+1] == 1 and board[y-2][x+2] == 0:
                            player_moves.append([(y,x),(y-2,x+2)])
                    if player_moves == []:
                        for y,x in self.find_all(board, 1):                
                            if x >= 1:
                                if board[y-1][x-1] == 0:
                                    player_moves.append([(y,x),(y-1,x-1)])
                            if x <= 4:
                                if board[y-1][x+1] == 0:
                                    player_moves.append([(y,x),(y-1,x+1)])
        return player_moves
    
    #checks to see if winning conditions are met
    def game_is_finished(self,*args, **kwargs):
        game_cancelled = kwargs.get('game_cancelled', False)
        valid_ai_moves_empty = kwargs.get('valid_ai_moves_empty', False)
        for column in self.board[0]:
            if column == 1:
                game_won = True
                database.database.add_leaderboard_entry(self.user, self.difficulty, self.game, game_won)
                if game_gui.game_gui:
                    game_gui.game_gui.end_game(game_won)
                return
        for column in self.board[5]:
            if column == 2:
                game_won = False
                database.database.add_leaderboard_entry(self.user, self.difficulty, self.game, game_won)
                if game_gui.game_gui:
                    game_gui.game_gui.end_game(game_won)
                return
        if self.player_turn:
            moves =[]
            if self.game == 0:
                for y,x in self.find_all(self.board, 1):
                    if self.board[y-1][x] == 0:
                        moves.append([(y,x),(y-1,x)])
                    if x >= 1:
                        if self.board[y-1][x-1] == 2:
                            moves.append([(y,x),(y-1,x-1)])
                    if x <= 4:
                        if self.board[y-1][x+1] == 2:
                            moves.append([(y,x),(y-1,x+1)])
                if moves == []:
                    game_won = False
                    database.database.add_leaderboard_entry(self.user, self.difficulty, self.game, game_won)
                    if game_gui.game_gui:
                        game_gui.game_gui.end_game(game_won)
                    return
            else:
                for y,x in self.find_all(self.board, 1):                
                    if x >= 2:
                        if self.board[y-1][x-1] == 1 and self.board[y-2][x-2] == 0:
                            moves.append([(y,x),(y-2,x-2)])
                    if x <= 3:
                        if self.board[y-1][x+1] == 1 and self.board[y-2][x+2] == 0:
                            moves.append([(y,x),(y-2,x+2)])
                    if moves == []:
                        for y,x in self.find_all(self.board, 1):                
                            if x >= 1:
                                if self.board[y-1][x-1] == 0:
                                    moves.append([(y,x),(y-1,x-1)])
                            if x <= 4:
                                if self.board[y-1][x+1] == 0:
                                    moves.append([(y,x),(y-1,x+1)])
                if moves == []:
                    game_won = False
                    database.database.add_leaderboard_entry(self.user, self.difficulty, self.game, game_won)
                    if game_gui.game_gui:
                        game_gui.game_gui.end_game(game_won)
                    return
        if valid_ai_moves_empty:
            game_won = True
            if game_gui.game_gui:
                game_gui.game_gui.end_game(game_won)
            database.database.add_leaderboard_entry(self.user, self.difficulty, self.game, game_won)
            return
        if game_cancelled:
            game_won = False
            database.database.add_leaderboard_entry(self.user, self.difficulty, self.game, game_won)
            return

game_logic: Game_Logic = Game_Logic()