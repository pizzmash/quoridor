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
        self.p1_rb = PlayerRadioButton(self, "Player 1", borderwidth=2, relief="raised")
        self.p1_rb.grid(column=0, columnspan=2, padx=5, pady=5)
        # Player 2
        self.p2_rb = PlayerRadioButton(self, "Player 2", borderwidth=2, relief="raised")
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
        self.board_size = self.bs_sb.get()
        self.wall = self.wall_sb.get()
        self.players = [self.p1_rb.build(), self.p2_rb.build()]
        self.quit()


class PlayerRadioButton(tkinter.Frame):
    def __init__(self, master, text, borderwidth=0, relief="flat"):
        super().__init__(master, borderwidth=borderwidth, relief=relief)
        self.grid()
        label = tkinter.Label(self, text=text)
        self.var = tkinter.IntVar()
        self.var.set(0)
        r1 = tkinter.Radiobutton(self, value=0, variable=self.var, text="Human", command=self.update_eval_validation)
        r2 = tkinter.Radiobutton(self, value=1, variable=self.var, text="Random", command=self.update_eval_validation)
        r3 = tkinter.Radiobutton(self, value=2, variable=self.var, text="MiniMax", command=self.update_eval_validation)
        self.ef = EvalFrame(self)

        label.grid(row=0, column=0, columnspan=2)
        r1.grid(row=1, column=0, padx=5)
        r2.grid(row=2, column=0, padx=5)
        r3.grid(row=3, column=0, padx=5)
        self.ef.grid(row=1, column=1, rowspan=3, padx=5)

    def build(self):
        if self.var.get() == 0:
            return Human()
        elif self.var.get() == 1:
            return RandomBot()
        elif self.var.get() == 2:
            eval, depth = self.ef.build()
            return MiniMax(eval, depth)

    def update_eval_validation(self):
        if self.var.get() == 2:
            self.ef.active()
        else:
            self.ef.disable()


class EvalFrame(tkinter.Frame):
    def __init__(self, master, borderwidth=0, relief="flat"):
        super().__init__(master, borderwidth=borderwidth, relief=relief)
        self.grid()

        label = tkinter.Label(self, text="eval")
        label.grid()

        self.var = tkinter.IntVar()
        self.var.set(0)
        self.r1 = tkinter.Radiobutton(self, value=0, variable=self.var, text="DistanceEvaluation")
        self.r1.grid()

        self.depth_sb = SpinboxFrame(self, "depth", 2, 1, 5)
        self.depth_sb.grid()

        self.disable()

    def build(self):
        if self.var.get() == 0:
            eval = DistanceEvaluation()
        return eval, self.depth_sb.get()

    def disable(self):
        self.r1["state"] = "disable"
        self.depth_sb.disable()

    def active(self):
        self.r1["state"] = "active"
        self.depth_sb.active()


class SpinboxFrame(tkinter.Frame):
    def __init__(self, master, text, default, from_, to):
        super().__init__(master)
        self.grid()

        label = tkinter.Label(self, text=text)
        label.grid(row=0, column=0)

        self.var = tkinter.StringVar()
        self.var.set(default)
        self.spinbox = tkinter.Spinbox(self, textvariable=self.var, from_=from_, to=to, increment=1, width=2)
        self.spinbox.grid(row=0, column=1)

    def get(self):
        return int(self.var.get())

    def disable(self):
        self.spinbox["state"] = "disable"

    def active(self):
        self.spinbox["state"] = "normal"
