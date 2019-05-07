from enum import Enum
from abc import ABCMeta, abstractmethod


class Move(metaclass=ABCMeta):
    def __init__(self, board, player):
        self.board = board
        self.player = player

    @abstractmethod
    def launch():
        raise NotImplementedError


class PieceMove(Move):
    def __init__(self, board, player, h, v):
        super(PieceMove, self).__init__(board, player)
        self.h = h
        self.v = v

    def launch(self):
        return self.board.move_piece(self.h, self.v)


class HorizontalWallMove(Move):
    def __init__(self, board, player, h, v):
        super(HorizontalWallMove, self).__init__(board, player)
        self.h = h
        self.v = v

    def launch(self):
        return self.board.put_horizontal_wall(self.h, self.v)


class VerticalWallMove(Move):
    def __init__(self, board, player, h, v):
        super(VerticalWallMove, self).__init__(board, player)
        self.h = h
        self.v = v

    def launch(self):
        return self.board.put_vertical_wall(self.h, self.v)
