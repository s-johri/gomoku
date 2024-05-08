# Implement an AI Player for Gomoku
# A Random Player is provided for you

from gomoku import Player, Board
import math
import numpy as np
import copy
import time

class AIPlayer(Player):
    """ a subclass of Player that looks ahead some number of moves and 
    strategically determines its best next move.
    """
    
    previous_board = Board(10,10)
  
    @staticmethod
    def get_evaluation_range(board, counter):
        #Compute range window size
        if counter >= 2:
            #print("Large evaluation range")
            rowS = 0
            rowE = board.height
            colS = 0
            colE = board.width
        else:
            #print("Small evaluation range")
            rowS = 3
            rowE = board.height-3
            colS = 3
            colE = board.width-3
        return int(rowS), int(rowE), int(colS), int(colE)


    def next_move(self, board):
        """ returns the called AIPlayer's next move for a game on
            the specified Board object. 
            input: board is a Board object for the game that the called
                     Player is playing.
            return: row, col are the coordinated of a vacant location on the board 
        """
        start = time.time()
        self.num_moves += 1
        assert(board.is_full() == False)
    
        counter = self.num_moves
        rowS, rowE, colS, colE = self.get_evaluation_range(board, counter)
        
        if counter >= 3:
            last_opp_move_row = 0
            last_opp_move_col = 0
            for row in range(board.height):
                for col in range(board.width): 
                    if self.previous_board.can_add_to(row, col) != board.can_add_to(row, col):
                        last_opp_move_row = row
                        last_opp_move_col = col
                        break
                if last_opp_move_row != 0:
                    break
                
        #Find all the open position (without a marker X or O)
        open_pos_priority_1 = []
        open_pos_priority_2 = []
        open_pos_no_priority = []
        for row in range(rowS,rowE+1):
            for col in range(colS,colE+1):
                if board.can_add_to(row, col):
                    #priority if close to opp last move
                    if counter >= 3:
                        flag_priority_1 = False
                        if last_opp_move_row == row-1 and last_opp_move_col == col-1:
                            flag_priority_1 = True
                        elif last_opp_move_row == row-1 and last_opp_move_col == col:
                            flag_priority_1 = True
                        elif last_opp_move_row == row-1 and last_opp_move_col == col+1:
                            flag_priority_1 = True
                        elif last_opp_move_row == row and last_opp_move_col == col-1:
                            flag_priority_1 = True
                        elif last_opp_move_row == row and last_opp_move_col == col+1:
                            flag_priority_1 = True
                        elif last_opp_move_row == row+1 and last_opp_move_col == col-1:
                            flag_priority_1 = True
                        elif last_opp_move_row == row+1 and last_opp_move_col == col:
                            flag_priority_1 = True
                        elif last_opp_move_row == row+1 and last_opp_move_col == col+1:
                            flag_priority_1 = True
                        if flag_priority_1:
                            open_pos_priority_1.append((row, col))
                            continue
                    #priority if one neighboor has a checker
                    flag_priority_2 = False
                    if row-1 >= 0 and col-1 >= 0 and not board.can_add_to(row-1, col-1):
                        flag_priority_2 = True
                    elif row-1 >= 0  and not board.can_add_to(row-1, col) :
                        flag_priority_2 = True
                    elif row-1 >= 0 and col+1 <= 9 and not board.can_add_to(row-1, col+1) :
                        flag_priority_2 = True
                    elif col-1 >= 0 and not board.can_add_to(row, col-1) :
                        flag_priority_2 = True
                    elif col+1 <= 9 and not board.can_add_to(row, col+1) :
                        flag_priority_2 = True
                    elif row+1 <= 9 and col-1 >= 0 and not board.can_add_to(row+1, col-1) :
                        flag_priority_2 = True
                    elif row+1 <= 9 and not board.can_add_to(row+1, col) :
                        flag_priority_2 = True
                    elif row+1 <= 9 and col+1 <= 9 and not board.can_add_to(row+1, col+1) :
                        flag_priority_2 = True
                    if flag_priority_2:
                        open_pos_priority_2.append((row, col))
                    else:
                        open_pos_no_priority.append((row, col))
                        
        #Shuffle for best performances
        np.random.shuffle(open_pos_no_priority)
        np.random.shuffle(open_pos_priority_2)
        np.random.shuffle(open_pos_priority_1)
        open_pos = []
        if len(open_pos_priority_1) == 0 and len(open_pos_priority_2) == 0:
            open_pos = open_pos_no_priority
        else:
            if counter >= 3:
                open_pos = open_pos_priority_1 + open_pos_priority_2
            else:
                open_pos = open_pos_priority_2
        
        maxEval = -math.inf
        bestMove = ()
        depth = 2
        if len(open_pos) == 1:
            bestMove = open_pos[0]
        else:
            for move in open_pos:
                val = self.minimax(self, self.checker, move, board, depth, -math.inf, math.inf, True, open_pos)
                if val > maxEval:
                    maxEval = val
                    bestMove = move
                #print("*********Evaluating move: ", move, " -score = ", val)
                if time.time() - start >= 5.0:
                    #print("Break timeout during evaluation of move: ", move)
                    break
        #print("best move: ", bestMove, "-score ",maxEval) 
        
        if counter >= 2:
            self.previous_board = copy.deepcopy(board)
            self.previous_board.add_checker(self.checker, bestMove[0], bestMove[1])
        
        return bestMove

      
    def minimax(self, player, ch, move, board, depth, alpha, beta, isMaximizing, pos_move):
        
        new_board = copy.deepcopy(board)
        new_board.add_checker(ch, move[0], move[1])
        new_pos_move = pos_move.copy()
        del pos_move
        new_pos_move.remove(move)
        
        win = new_board.is_win_for(ch, move[0], move[1])
        if depth == 0 or win:
            if win:
                if ch == player.opponent_checker():
                    return -100000 #Direct loss
                else:
                    return 100000 #Direct win
            else: #depth=0
                return self.static_eval(new_board, ch, player.opponent_checker())
        
        #MAXIMIZING        
        if isMaximizing:
            maxEval = -math.inf
            for child_move in new_pos_move:
                pos_value = min(move[0], board.height - move[0]) * min(move[1], board.width - move[1]) / 10.0
                val = self.minimax(player, player.opponent_checker(), child_move, new_board, depth - 1, alpha, beta, False, new_pos_move)
                if val >= 0:
                    val += pos_value
                maxEval = max(maxEval, val)
                alpha = max(alpha, val)
                if beta <= alpha:
                    break
            return maxEval
        
        #MINIMIZING
        else:
            minEval = math.inf
            for child_move in new_pos_move:
                val = self.minimax(player, player.checker, child_move, new_board, depth - 1, alpha, beta, True, new_pos_move)
                minEval = min(minEval, val)
                beta = min(beta, val)
                if beta <= alpha:
                    break
            return minEval
         
        
    @staticmethod  
    def static_eval(board, checker, opp_checker):
        
        #Do not consider diagonals with less than 4 element (useless for evaluation)
        rows = [''.join(board.slots[row]) for row in range(board.height)]
        columns = [''.join([row[col] for row in rows]) for col in range(board.width)]
        a = np.array(board.slots)
        diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1]) if len(a[::-1,:].diagonal(i)) > 4]
        diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1) if len(a.diagonal(i)) > 4)
        diagonals = [''.join(n.tolist()) for n in diags]
        
        #10 rows, 10 cols, 11*2 diagonals = tot 42 elements to consider for evaluation 
        l = rows + columns + diagonals
        score = 0
        
        #PENALTIES IN ORDER OF IMPORTANCE 
        for comp in l:
            #PRIORITY 1: Combination for which the opponent win in the next move (with depth 2 the opponent has the next move here)
            flag_p1 = False
            if comp.find(' '+opp_checker*4+' ') != -1: #'XXXX'
                score -= 30000 
                flag_p1 = True
            elif comp.find(opp_checker*4+' ') != -1: #XXXX'
                score -= 30000
                flag_p1 = True
            elif comp.find(' '+opp_checker*4) != -1: #'XXXX
                score -= 30000
                flag_p1 = True
            elif comp.find(opp_checker*2+' '+opp_checker*2) != -1: #XX'XX
                score -= 20000
                flag_p1 = True
            elif comp.find(opp_checker+' '+opp_checker*3) != -1: #X'XXX
                score -= 20000
                flag_p1 = True
            elif comp.find(opp_checker*3+' '+opp_checker) != -1: #XXX'X
                score -= 20000
                flag_p1 = True
            #if flag_p1:
                #score -= 20000 #Loss next move
                #break #save performance
            
            #PRIORITY 2: the opponent win in 2 moves 
            flag_p2 = False
            if comp.find(' '+opp_checker*2+' '+opp_checker+' ') != -1: #'XX'X'
                flag_p2 = True 
            elif comp.find(' '+opp_checker+' '+opp_checker*2+' ') != -1: #'X'XX'
                flag_p2 = True
            elif comp.find(' '+opp_checker*3+' '+' ') != -1: #'XXX''
                flag_p2 = True
            elif comp.find('  '+opp_checker*3+' ') != -1: #''XXX'
                flag_p2 = True
            elif comp.find(' '+opp_checker*3+' ') != -1: #'XXX'
                score -= 100
            elif comp.find(opp_checker*3+' '+' ') != -1: #XXX''
                score -= 100
            elif comp.find(' '+' '+opp_checker*3) != -1: #''XXX
                score -= 100
            #AGAINST PRIORITY 2: I win in my next move
            if comp.find(' '+checker*4+' ') != -1: #'XXXX' 
                score += 1000
            elif comp.find(checker*4+' ') != -1: #XXXX'
                score += 500
            elif comp.find(' '+checker*4) != -1: #'XXXX
                score += 500
            elif comp.find(checker*2+' '+checker*2) != -1: #XX'XX
                score += 500
            elif comp.find(checker+' '+checker*3) != -1: #X'XXX
                score += 500
            elif comp.find(checker*3+' '+checker) != -1: #XXX'X
                score += 500
            else:
                if flag_p2: #need a win for me in my next move to balance
                    score -= 10000 #priority 2 is effective against me
            
            #NO PRIORITY THREATS: add simple points 
            #OPPONENT 
            if comp.find(' '+opp_checker*2+' '+' ') != -1: #'XX''
                score -= 25
            elif comp.find(' '+' '+opp_checker*2+' ') != -1: #''XX'
                score -= 25
            elif comp.find(opp_checker*2+' '+' '+' ') != -1: #XX'''
                score -= 25
            elif comp.find(' '+' '+' '+opp_checker*2) != -1: #'''XX
                score -= 25
            if comp.find(' '+opp_checker+' '+opp_checker+' ') != -1: #'X'X'
                score -= 25
            elif comp.find(opp_checker+' '+opp_checker+' '+' ') != -1: #X'X''
                score -= 25
            elif comp.find(' '+' '+opp_checker+' '+opp_checker) != -1: #''X'X
                score -= 25
            #ME
            if comp.find(' '+checker*2+' '+checker+' ') != -1: #'XX'X'
                score += 30
            elif comp.find(' '+checker+' '+checker*2+' ') != -1: #'X'XX'
                score += 30 
            elif comp.find(' '+checker+' '+checker+' ') != -1: #'X'X'
                score += 10
            elif comp.find(checker+' '+checker+' '+' ') != -1: #X'X''
                score += 10
            elif comp.find(' '+' '+checker+' '+checker) != -1: #''X'X
                score += 10
            elif comp.find(' '+checker*2+' '+' ') != -1: #'XX''
                score += 15
            elif comp.find(' '+' '+checker*2+' ') != -1: #''XX'
                score += 15
            elif comp.find(checker*2+' '+' '+' ') != -1: #XX'''
                score += 15
            elif comp.find(' '+' '+' '+checker*2) != -1: #'''XX
                score += 15
            if comp.find(' '+checker*3+' '+' ') != -1: #'XXX''
                score += 30
            elif comp.find(' '+' '+checker*3+' ') != -1: #''XXX'
                score += 30 
            elif comp.find(checker*3+' '+' ') != -1: #XXX''
                score += 30 
            elif comp.find(' '+' '+checker*3) != -1: #''XXX
                score += 30
            
        return score
    
