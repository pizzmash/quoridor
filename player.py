from abc import ABCMeta, abstractmethod


class Player(metaclass=ABCMeta):
    @abstractmethod
    def think(self, board):
        raise NotImplementedError
