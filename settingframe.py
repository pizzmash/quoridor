import tkinter

from human import Human
from randombot import RandomBot
from minimax import MiniMax
from boardcanvas import MoveStack
from evaluation import DistanceEvaluation


class SettingFrame(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()

        # Player 1
        self.p1_rb = PlayerRadioButton(self, "Player 1")
        self.p1_rb.grid(column=0, columnspan=2, padx=5, pady=5)
        # Player 2
        self.p2_rb = PlayerRadioButton(self, "Player 2")
        self.p2_rb.grid(column=0, columnspan=2, padx=5, pady=5)
        # board size
        self.bs_sb = SpinboxFrame(self, "board size", 9, 3, 15)
        self.bs_sb.grid(row=2, padx=5, pady=5)
        # walls
        self.wall_sb = SpinboxFrame(self, "walls", 10, 0, 20)
        self.wall_sb.grid(row=2, column=1, padx=5, pady=5)
        # NewGame
        self.button = tkinter.Button(self, text="new game", command=self.build)
        self.button.grid(column=0, columnspan=2, padx=5, pady=5)

    def build(self):
        self.board_size = int(self.bs_sb.var.get())
        self.wall = int(self.wall_sb.var.get())
        self.players = [self.p1_rb.build(), self.p2_rb.build()]
        self.quit()


class PlayerRadioButton(tkinter.Frame):
    def __init__(self, master, text):
        super().__init__(master)
        self.grid()
        label = tkinter.Label(self, text=text)
        self.var = tkinter.IntVar()
        self.var.set(0)
        r1 = tkinter.Radiobutton(self, value=0, variable=self.var, text="Human")
        r2 = tkinter.Radiobutton(self, value=1, variable=self.var, text="Random")
        r3 = tkinter.Radiobutton(self, value=2, variable=self.var, text="MiniMax")
        self.ef = EvalFrame(self)

        label.grid(row=0, column=0, columnspan=2)
        r1.grid(row=1, column=0)
        r2.grid(row=2, column=0)
        r3.grid(row=3, column=0)
        self.ef.grid(row=1, column=1, rowspan=3)

    def build(self):
        if self.var.get() == 0:
            return Human()
        elif self.var.get() == 1:
            return RandomBot()
        elif self.var.get() == 2:
            return MiniMax(self.ef.build(), depth=2)


class EvalFrame(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()

        label = tkinter.Label(self, text="eval")
        self.var = tkinter.StringVar()
        listbox = tkinter.Listbox(self, listvariable=self.var, height=3, width=15)
        listbox.insert(tkinter.END, 'DistanceEvaluation')
        label.grid()
        listbox.grid(padx=10)

    def build(self):
        if self.var.get() == 'DistanceEvaluation':
            return DistanceEvaluation()


class SpinboxFrame(tkinter.Frame):
    def __init__(self, master, text, default, from_, to):
        super().__init__(master)
        self.grid()

        label = tkinter.Label(self, text=text)
        label.grid(row=0, column=0)

        self.var = tkinter.StringVar()
        self.var.set(default)
        spinbox = tkinter.Spinbox(self, textvariable=self.var, from_=from_, to=to, increment=1, width=2)
        spinbox.grid(row=0, column=1)
