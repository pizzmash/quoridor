import tkinter
import threading
import copy

from board import Board
from human import Human
from evaluation import DistanceEvaluation
from minimax import MiniMax
from randombot import RandomBot
from boardcanvas import BoardCanvas, MoveStack
from settingframe import SettingFrame


class App(tkinter.Frame):
    def __init__(self, master, board_size, wall, players):
        self.width = 800
        self.height = 620
        super().__init__(master)
        master.title("Quoridor")
        self.grid()
        self.setup(board_size, wall, players)
        

    def setup(self, board_size, wall, players):
        self.board = Board(size=board_size, wall=wall)
        if isinstance(players[0], Human) or isinstance(players[1], Human):
            self.move_stack = MoveStack()
            for i in range(2):
                if isinstance(players[i], Human):
                    players[i].move_stack = self.move_stack
        else:
            self.move_stack = None
        self.players = players

        # canvs
        self.canvas = BoardCanvas(
            self, self.height, 10, self.board, self.players, self.move_stack
        )
        self.canvas.grid(row=0, column=0, rowspan=3)
        self.canvas.draw()

        self.thread = threading.Thread(target=self.game)
        self.thread.setDaemon(True)
        self.thread.start()

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
        super().mainloop()
