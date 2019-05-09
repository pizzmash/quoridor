from board import Board
from human import Human
from master import Master
from evaluation import DistanceEvaluation
from minimax import MiniMax


def main():
    size = 9
    wall = 10
    board = Board(size=size, wall=wall)
    eval = DistanceEvaluation()
    p1 = MiniMax(eval, depth=2)
    # p1 = Human()
    p2 = MiniMax(eval, depth=2)
    master = Master(board, [p1, p2])
    master.start()


if __name__ == '__main__':
    main()
