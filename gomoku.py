# The script provides a Gomoku Board class and a Player class
#
# 
import random

class Board:
    """ a data type for a Connect Five board with arbitrary dimensions
    """   
    
    def __init__(self,height=10,width=10):
        self.height = height
        self.width = width
        self.slots = [[' ']*width for r in range(height)]

    def __repr__(self):
        """ Returns a string representation of a Board object.
        """
        s = ''         # begin with an empty string

        # add one row of slots at a time to s
        for row in range(self.height):
            s += '|'   # one vertical bar at the start of the row
            for col in range(self.width):
                s += self.slots[row][col] + '|'
            
            s += ' ' + str(row%10) + '\n'

        s += "-"*(self.width*2+3)+"\n"
        for c in range(self.width):
            s+=' '+str(c%10)
        s += '\n'
        return s       
            
    def can_add_to(self, row, col):
        """ returns True if you can add a checker to the specified position 
            (row, col) in the called Board object, and False otherwise.
            input: row, col are integers
        """
        if col < 0 or col >= self.width \
            or row < 0 or row >= self.height:
            return False
        elif self.slots[row][col] != ' ':
            return False
        else:
            return True 
        
    def add_checker(self, checker, row, col):
        """ adds the specified checker (either 'X' or 'O') to the
            column with the specified index col in the called Board.
            inputs: checker is either 'X' or 'O'
                    col is a valid column index
        """
        assert(checker == 'X' or checker == 'O')
        
        if self.can_add_to(row, col):
            self.slots[row][col] = checker
            
    def reset(self):
        self.slots = [[' ']*self.width for r in range(self.height)]

    def is_full(self):
        for r in range(self.height):
            if ' ' in self.slots[r]:
                return False
        return True
           
    def is_win_for(self, checker, r, c):
        """ Checks for if the specified checker added to position x, y will 
            lead to a win
        """
        assert(checker == 'X' or checker == 'O')
        return self.is_horizontal_win(checker,r,c) \
            or self.is_vertical_win(checker,r,c) \
            or self.is_diagonal1_win(checker,r,c) \
            or self.is_diagonal2_win(checker,r,c)
    
    def is_horizontal_win(self, checker, r, c):
        cnt = 0
        
        for i in range(5):
            # Check if the next four columns in this row
            # contain the specified checker.
            if c+i < self.width and self.slots[r][c+i] == checker:
                cnt += 1
            else:
                break
        
        if cnt == 5:
            return True
        else:
            # check towards left           
            for i in range(1, 6-cnt):
                if c-i >= 0 and self.slots[r][c-i] == checker:
                    cnt += 1
                else:
                    break
               
            if cnt == 5:
                return True  
            
        return False
                        
    def is_vertical_win(self, checker, r, c):
        cnt = 0
        for i in range(5):
            # Check if the next four rows in this col
            # contain the specified checker.            
            if r+i < self.width and self.slots[r+i][c] == checker:
                cnt += 1
            else:
                break
        
        if cnt == 5:
            return True
        else:
            # check upwards
            for i in range(1, 6-cnt):
                if r-i >= 0 and self.slots[r-i][c] == checker:
                    cnt += 1
                else:
                    break
            
            if cnt == 5:
                return True  
            
        return False

    def is_diagonal1_win(self, checker, r, c):
        cnt = 0
        for i in range(5):
            if r+i < self.height and c+i < self.width and \
                self.slots[r+i][c+i] == checker:                    
                cnt += 1
            else:
                break
        if cnt == 5:
            return True
        else:
            for i in range(1, 6-cnt):
                if r-i >= 0 and c-i >= 0 and \
                    self.slots[r-i][c-i] == checker:
                        cnt += 1
                else:
                    break
                
            if cnt == 5:
                return True  
        
        return False    

    def is_diagonal2_win(self, checker, r, c):
        cnt = 0
        for i in range(5):
            if r-i >= 0 and c+i < self.width and \
                self.slots[r-i][c+i] == checker:
                cnt += 1
            else:
                break
            
        if cnt == 5:
            return True
        else:
            for i in range(1, 6-cnt):
                if r+i < self.height and c-i >= 0 and \
                    self.slots[r+i][c-i] == checker:
                    cnt += 1
                else:
                    break
                
            if cnt == 5:
                return True  
        
        return False 

class Player:
    def __init__(self,checker):
        assert(checker == 'X' or checker == 'O')
        self.checker = checker
        self.num_moves = 0

    def __repr__(self):
        return "Player: "+self.checker
    
    def opponent_checker(self):
        if self.checker == 'X':
            return 'O'
        else:
            return 'X'

    def next_move(self, board):
        """ gets and returns the called Player's next move for a game on
            the specified Board object. The method ensures that the move
            is valid for the specified Board -- asking repeatedly if
            necessary until the human player enters a valid move.
            input: board is a Board object for the game that the called
                     Player is playing.
        """
        self.num_moves += 1
        
        while True:
            pos_str = input('Enter a position: ')
            pos_lst = pos_str.split()                
            if board.can_add_to(int(pos_lst[0]), int(pos_lst[1])):
                return int(pos_lst[0]), int(pos_lst[1])
            else:
                print('Try again!')

                
class RandomPlayer(Player):
    """ a subclass of Player that chooses at random
        from the available position.
    """
    def next_move(self, board):
        """ returns the called RandomPlayer's next move for a game on
            the specified Board object. The method chooses at random
            from the columns that are not yet full, and we assume 
            that there is at least one such column.
            input: board is a Board object for the game that the called
                   Player is playing.
        """
        assert(board.is_full() == False)
        self.num_moves += 1
        open_pos = []
        for row in range(board.height):
            for col in range(board.width):
                if board.can_add_to(row, col):
                    open_pos.append((row, col))
        
        return random.choice(open_pos)