from abc import ABCMeta, abstractmethod


class Player(metaclass=ABCMeta):
    def register_board(self, board):
        self.board = board

    @abstractmethod
    def think(self):
        raise NotImplementedError
