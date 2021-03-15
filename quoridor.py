import tkinter

from board import Board
from human import Human
from master import Master
from evaluation import DistanceEvaluation
from minimax import MiniMax
from app import App


def main():
    size = 7
    wall = 8
    board = Board(size=size, wall=wall)
    eval = DistanceEvaluation()
    p1 = MiniMax(eval, depth=3)
    p2 = MiniMax(eval, depth=3)
    master = Master(board, [p1, p2])
    # master.start()

    root = tkinter.Tk()
    app = App(root, 600, 10, board)
    app.mainloop()


if __name__ == '__main__':
    main()
