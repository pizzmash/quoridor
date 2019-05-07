from enum import Enum


class Ditch:
    STATE = Enum('State', 'EMPTY, FILLED')

    def __init__(self, size):
        self.horizontal = [[self.STATE.EMPTY] * size for v in range(size-1)]
        self.vertical = [[self.STATE.EMPTY] * (size-1) for v in range(size)]
        self.xpt = [[self.STATE.EMPTY] * (size-1) for v in range(size-1)]

    def is_fillable(self, h, v):
        return self.xpt[v][h] == self.STATE.EMPTY

    def fill_horizontal(self, h, v):
        if self.is_fillable(h, v):
            self.horizontal[v][h] = self.FILLED
            self.horizontal[v][h+1] = self.FILLED
            return True
        else:
            return False

    def fill_vertical(self, h, v):
        if self.is_fillable(h, v):
            self.vertical[v][h] = self.FILLED
            self.vertical[v+1][h] = self.FILLED
            return True
        else:
            return False
