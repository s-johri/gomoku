from gomoku import Player, RandomPlayer
from process import gomoku
from main import AIPlayer 

opp = AIPlayer('O')
player = Player('X')

#gomoku(player, opp)
gomoku(opp, player)
