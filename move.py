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
        pass


class HorizontalWallMove(Move):
    def __init__(self, board, player, h, v):
        super(HorizontalWallMove, self).__init__(board, player)
        self.h = h
        self.v = v

    def launch(self):
        pass


class VerticalWallMove(Move):
    def __init__(self, board, player, h, v):
        super(VerticalWallMove, self).__init__(board, player)
        self.h = h
        self.v = v

    def launch(self):
        pass
