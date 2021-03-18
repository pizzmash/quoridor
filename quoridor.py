import tkinter

from board import Board
from human import Human
from master import Master
from evaluation import DistanceEvaluation
from minimax import MiniMax
from randombot import RandomBot
from boardcanvas import BoardCanvas, MoveStack


def main():
    size = 9
    wall = 10
    board = Board(size=size, wall=wall)
    eval = DistanceEvaluation()
    move_stack = MoveStack()
    p1 = RandomBot()
    p2 = Human(move_stack)
    # p2 = MiniMax(eval, depth=2)
    # p2 = RandomBot()
    master = Master(board, [p1, p2])
    # master.start()

    root = tkinter.Tk()
    canvas = BoardCanvas(root, 600, 10, board, [p1, p2], move_stack)
    canvas.mainloop()


if __name__ == '__main__':
    main()
