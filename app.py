import tkinter
import threading
import copy

from board import Board
from human import Human
from evaluation import DistanceEvaluation
from minimax import MiniMax
from randombot import RandomBot
from boardcanvas import BoardCanvas, MoveStack


class App(tkinter.Frame):
    def __init__(self, master):
        self.width = 800
        self.height = 620
        super().__init__(master, width=self.width, height=self.height)
        self.pack()

        master.geometry("{}x{}".format(self.width, self.height))
        master.title("Quoridor")

        self.size = 9
        self.wall = 10
        self.board = Board(size=self.size, wall=self.wall)
        self.eval = DistanceEvaluation()
        self.move_stack = MoveStack()
        p1 = RandomBot()
        p2 = Human(self.move_stack)
        self.players = [p1, p2]
        # p2 = MiniMax(eval, depth=2)
        # p2 = RandomBot()
        # master.start()

        self.canvas = BoardCanvas(
            self, self.height, 10, self.board, [p1, p2], self.move_stack
        )
        self.canvas.place(width=self.height, height=self.height)

        self.thread = threading.Thread(target=self.game)
        self.thread.setDaemon(True)

    def game(self):
        self.canvas.draw()
        while True:
            while True:
                player = self.players[0] if self.board.order == self.board.ORDER.FIRST_HAND else self.players[1]
                board = copy.deepcopy(self.board)
                move = player.think(board)
                if move.launch(self.board):
                    break
            self.canvas.clear_piece()
            self.canvas.clear_wall()
            self.canvas.draw_pieces()
            self.canvas.draw_walls()
            if True in self.board.is_goaled():
                pass
                break

    def mainloop(self):
        self.thread.start()
        super().mainloop()
