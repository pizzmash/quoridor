from ditch import Ditch


class Board:
    def __init__(self, size=7, wall=8):
        self.pieces = ([0, (int)(size/2)], [size-1, (int)(size/2)])
        self.walls = [wall, wall]
        self.ditch = Ditch(size)
