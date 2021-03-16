import random

from player import Player
from move import PieceMove


class RandomBot(Player):
    def __init__(self, all_random=False):
        self.all_random = all_random

    def think(self, board):
        moves = list(board.regal_move())
        if not self.all_random:
            move_type = random.randrange(2)
            if move_type == 0:
                moves = [move for move in moves if isinstance(move, PieceMove)]
            else:
                moves_ = [move for move in moves if not isinstance(move, PieceMove)]
                if len(moves_) == 0:
                    moves = [move for move in moves if isinstance(move, PieceMove)]
                else:
                    moves = moves_
        return random.choice(moves)
