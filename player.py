from abc import ABCMeta, abstractmethod


class Player(metaclass=ABCMeta):
    def __init__(self, board):
        self.board = board

    @abstractmethod
    def think(self):
        raise NotImplementedError
