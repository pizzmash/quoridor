from abc import ABCMeta, abstractmethod


class Move(metaclass=ABCMeta):
    @abstractmethod
    def launch(self, board):
        raise NotImplementedError


class PieceMove(Move):
    def __init__(self, h, v):
        self.h = h
        self.v = v

    def launch(self, board):
        return board.move_piece(self.h, self.v)


class HorizontalWallMove(Move):
    def __init__(self, h, v):
        self.h = h
        self.v = v

    def launch(self, board):
        return board.put_horizontal_wall(self.h, self.v)


class VerticalWallMove(Move):
    def __init__(self, h, v):
        self.h = h
        self.v = v

    def launch(self, board):
        return board.put_vertical_wall(self.h, self.v)
