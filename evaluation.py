from abc import ABCMeta, abstractmethod


class Evaluation(metaclass=ABCMeta):
    @abstractmethod
    def eval(self, board):
        raise NotImplementedError


class EachOtherGoalError(Exception):
    pass


class DistanceEvaluation(Evaluation):
    def eval(self, board):
        is_goaled = board.is_goaled()
        if is_goaled[0] and is_goaled[1]:
            raise EachOtherGoalError
        elif is_goaled[0]:
            return float('inf')
        elif is_goaled[1]:
            return -float('inf')
        else:
            distance = board.distance()
            walls = board.walls
            dd = distance[1] - distance[0]
            dw = walls[board.ORDER.FIRST_HAND] - walls[board.ORDER.SECOND_HAND]
            return dd * 0.75 + dw * 0.25
