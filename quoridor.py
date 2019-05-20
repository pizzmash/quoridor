from board import Board
from human import Human
from master import Master
from evaluation import DistanceEvaluation
from minimax import MiniMax


def main():
    size = 7
    wall = 8
    board = Board(size=size, wall=wall)
    eval = DistanceEvaluation()
    p1 = MiniMax(eval, depth=3)
    p2 = MiniMax(eval, depth=3)
    master = Master(board, [p1, p2])
    master.start()


if __name__ == '__main__':
    main()
