import ai as ai
import game_gui as game_gui

class Game_Logic:

    player_turn: bool
    user: int
    game: int
    difficulty: int
    board: list[list[int]]
    consecutive_turn_count= 0

    def start(self, active_user, active_game, active_difficulty):
        self.player_turn = True
        self.user = active_user
        self.game = active_game
        self.difficulty = active_difficulty
        # testing boards
        if self.game == 0:
            self.board = [[2,2,2,2,2,2],
                          [0,0,0,0,0,0],
                          [0,0,0,0,0,0],
                          [0,0,0,0,0,0],
                          [0,0,0,0,0,0],
                          [1,1,1,1,1,1]]
        elif self.game == 1:
            self.board = [[0,2,0,2,0,2],
                          [2,0,2,0,2,0],
                          [0,0,0,0,0,0],
                          [0,0,0,0,0,0],
                          [0,1,0,1,0,1],
                          [1,0,1,0,1,0]]
        
        #send boardinfo to gui
            
    def find_all(self, matrix, element): #helperfunction for get_valid_moves ai version
        yield from ((row_no, col_no)   #Iterate through all row, column indexes in a 2D Matrix where matrix[row][col] == element
            for row_no, row in enumerate(matrix)  
            for col_no, matrix_element in enumerate(row)  
            if matrix_element == element)  
            
    #checks and returns valid move possibilities, for a single piece for the player, all pieces for the AI
    def get_valid_moves(self, *args, **kwargs):

        chosen_piece = kwargs.get('chosen_piece', None)
        player_turn = kwargs.get('player_turn', False)
        if chosen_piece != None:
            posY = chosen_piece[0]
            posX = chosen_piece[1]
        board_preview = self.board
        if self.game_is_finished():
            return
        else:
            if self.game == 0:     
                if player_turn: #valid moves for single selected piece by player
                    if self.board[posY-1][posX] == 0:
                        board_preview[posY-1][posX] = 3
                    if posX >= 1:
                        if self.board[posY-1][posX-1] == 2:
                            board_preview[posY-1][posX-1] = 3
                    if posX <= 4:
                        if self.board[posY-1][posX+1] == 2:
                            board_preview[posY-1][posX+1] = 3
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
                    print(moves)
                    return moves
            elif self.game == 1:
                if player_turn: #valid moves for single selected piece by player            
                    if posX >= 2:
                        if self.board[posY-1][posX-1] == 2 and self.board[posY-2][posX-2] == 0:
                            board_preview[posY-2][posX-2] = 3
                    if posX <= 3:
                        if self.board[posY-1][posX+1] == 2 and self.board[posY-2][posX+2] == 0:
                            board_preview[posY-2][posX+2] = 3
                    if any(3 in row for row in self.board) == False:
                        if posX >= 1:
                            if self.board[posY-1][posX-1] == 0:
                                board_preview[posY-1][posX-1] = 3
                        if posX <= 4:
                            if self.board[posY-1][posX+1] == 0:
                                board_preview[posY-1][posX+1] = 3
                        return board_preview
                    else:
                        return board_preview
                else: #all available valid moves
                    moves = []
                    for y,x in self.find_all(self.board, 2):                
                        if x >= 2:
                            if self.board[y+1][x-1] == 1 and self.board[y+2][x-2] == 0:
                                moves.append([(y,x),(y+2,x-2)])
                        if x <= 3:
                            if self.board[y+1][x+1] == 1 and self.board[y+2][x+2] == 0:
                                moves.append([(y,x),(y+2,x+2)])
                    if moves == []:
                        for y,x in self.find_all(self.board, 2):                
                            if x >= 1:
                                if self.board[y+1][x-1] == 0:
                                    moves.append([(y,x),(y+1,x-1)])
                            if x <= 4:
                                if self.board[y+1][x+1] == 0:
                                    moves.append([(y,x),(y+1,x+1)])
                        return moves
                    else:
                        return moves
            


    def switch_turn(self, move: tuple[tuple[int]]):
        move = move
        if self.player_turn:
            self.board[move[0][0]][move[0][1]] = 0
            self.board[move[1][0]][move[1][1]] = 1
            if self.game == 1:
                if move[0][0]+2 == move[1][0]:
                    beaten_piece_X = (move[0][1] + move[1][1])/2
                    beaten_piece_Y = (move[0][0] + move[1][0])/2
                    self.board[beaten_piece_Y][beaten_piece_X] = 0
                    if move[1][1]>=2 and self.board[move[1][0]-1][move[1][1]-1] == 2 and self.board[move[1][0]-2][move[1][1]-2] == 0:
                        self.board[move[1][0]-2][move[1][1]-2] = 3
                        self.consecutive_turn_count +=1
                        game_gui.playerAlertOrWhatever(self.board) #placeholder for telling the human player that it's still his turn, sending only the next jump as move
                    elif move[1][1]<=3 and self.board[move[1][0]-1][move[1][1]+1] == 2 and self.board[move[1][0]-2][move[1][1]+2] == 0:
                        self.board[move[1][0]-2][move[1][1]+2] = 3
                        self.consecutive_turn_count +=1
                        game_gui.playerAlertOrWhatever(self.board)  #placeholder for telling the human player that it's still his turn, sending only the next jump as move
                                                                    #must become impossible to change piece (via gui or restriction in logic?)                
                    else:
                        self.consecutive_turn_count = 0
                        ai.kickoffai #tell ai to go
        else:
            self.board[move[0][0]][move[0][1]] = 0
            self.board[move[1][0]][move[1][1]] = 2
            if self.game == 1:
                if move[0][0] +2 == move[1][0]:
                    beaten_piece_X = (move[0][1] + move[1][1])/2
                    beaten_piece_Y = (move[0][0] + move[1][0])/2
                    self.board[beaten_piece_Y][beaten_piece_X] = 0
                    if move[1][1]>=2 and self.board[move[1][0]-1][move[1][1]-1] == 2 and self.board[move[1][0]-2][move[1][1]-2] == 0:
                        self.board[move[1][0]-2][move[1][1]-2] = 3
                        self.consecutive_turn_count +=1
                        game_gui.playerAlertOrWhatever(self.board) #placeholder for telling the human player that it's still his turn, sending only the next jump as move
                    if move[1][1]<=3 and self.board[move[1][0]-1][move[1][1]+1] == 2 and self.board[move[1][0]-2][move[1][1]+2] == 0:
                        self.board[move[1][0]-2][move[1][1]+2] = 3
                        self.consecutive_turn_count +=1
                        game_gui.playerAlertOrWhatever(self.board) #placeholder for telling the human player that it's still his turn, sending only the next jump as move            
                    else:
                        self.consecutive_turn_count = 0
                        ai.kickoffai #tell ai to go



    #checks to see if winning conditions are met
    def game_is_finished(self,*args, **kwargs):
        game_cancelled = kwargs.get('game_cancelled', False)
        valid_moves_empty = kwargs.get('valid_moves_empty', False)
        for column in self.board[0]:
            if column == 1:
                print("placeholder, send win bool")
                game_won = True
                #game_gui.gameover(game_won)
                # SQL befehl mit daten  
                #fancy schmancy info to gui that game is over and lost, loss into database
                return
        for column in self.board[5]:
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

game_logic: Game_Logic = Game_Logic()