import tkinter

from board import Board
from human import Human
from master import Master
from evaluation import DistanceEvaluation
from minimax import MiniMax
from randombot import RandomBot
from app import App


def main():
    size = 7
    wall = 8
    board = Board(size=size, wall=wall)
    eval = DistanceEvaluation()
    p1 = RandomBot()
    p2 = RandomBot()
    master = Master(board, [p1, p2])
    # master.start()

    root = tkinter.Tk()
    app = App(root, 600, 10, board, [p1, p2])
    app.mainloop()


if __name__ == '__main__':
    main()
