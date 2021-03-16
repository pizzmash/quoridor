import random

from player import Player


class RandomBot(Player):
    def think(self, board):
        moves = list(board.regal_move())
        return random.choice(moves)
