import numpy as np

from encoder import Encoder
from move import PieceMove, HorizontalWallMove, VerticalWallMove


class SimpleEncoder(Encoder):
    def __init__(self, board_size):
        self.board_size = board_size

    def encode(self, board):
        board_matrix = np.zeros(self.shape()[0])
        for order, point in board.pieces.items():
            if order == board.order:
                board_matrix[0, point[0] * 2, point[1] * 2] = 1
            else:
                board_matrix[0, point[0] * 2, point[1] * 2] = 2
        for v, row in enumerate(board.ditch.horizontal):
            for h, state in enumerate(row):
                if state == board.ditch.STATE.FILLED:
                    board_matrix[0, v * 2 + 1, h * 2] = 3
        for v, row in enumerate(board.ditch.vertical):
            for h, state in enumerate(row):
                if state == board.ditch.STATE.FILLED:
                    board_matrix[0, v * 2, h * 2 + 1] = 3
        for v, row in enumerate(board.ditch.xpt):
            for h, state in enumerate(row):
                if state == board.ditch.STATE.FILLED:
                    board_matrix[0, v * 2 + 1, h * 2 + 1] = 3
        wall1 = board.walls[board.order]
        wall2 = board.walls[board.another_player()]
        # board_matrix = np.transpose(board_matrix, (1, 2, 0))
        return board_matrix, wall1, wall2

    def decode_move_index(self, index):
        if index < self.board_size * self.board_size:
            h = index % self.board_size
            v = index // self.board_size
            return PieceMove(h, v)
        elif index < self.board_size * self.board_size + (self.board_size - 1) ** 2:
            new_index = index - self.board_size * self.board_size
            h = new_index % (self.board_size - 1)
            v = new_index // (self.board_size - 1)
            return HorizontalWallMove(h, v)
        else:
            new_index = index - self.board_size * self.board_size
            new_index -= (self.board_size - 1) ** 2
            h = new_index % (self.board_size - 1)
            v = new_index // (self.board_size - 1)
            return VerticalWallMove(h, v)

    def num_points(self):
        num_points = self.board_size * self.board_size
        num_points += ((self.board_size - 1) ** 2) * 2
        return num_points

    def shape(self):
        return (1, self.board_size * 2 - 1, self.board_size * 2 - 1,), (1,), (1,)
