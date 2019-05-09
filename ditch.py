from enum import Enum


class Ditch:
    STATE = Enum('State', 'EMPTY, FILLED')

    def __init__(self, size):
        self.horizontal = [[self.STATE.EMPTY] * size for v in range(size-1)]
        self.vertical = [[self.STATE.EMPTY] * (size-1) for v in range(size)]
        self.xpt = [[self.STATE.EMPTY] * (size-1) for v in range(size-1)]

    def is_fillable_horizontal(self, h, v):
        is_empty_1 = self.horizontal[v][h] == self.STATE.EMPTY
        is_empty_2 = self.horizontal[v][h+1] == self.STATE.EMPTY
        is_empty_3 = self.xpt[v][h] == self.STATE.EMPTY
        return is_empty_1 and is_empty_2 and is_empty_3

    def is_fillable_vertical(self, h, v):
        is_empty_1 = self.vertical[v][h] == self.STATE.EMPTY
        is_empty_2 = self.vertical[v+1][h] == self.STATE.EMPTY
        is_empty_3 = self.xpt[v][h] == self.STATE.EMPTY
        return is_empty_1 and is_empty_2 and is_empty_3

    def fill_horizontal(self, h, v):
        if self.is_fillable_horizontal(h, v):
            self.horizontal[v][h] = self.STATE.FILLED
            self.horizontal[v][h+1] = self.STATE.FILLED
            self.xpt[v][h] = self.STATE.FILLED
            return True
        else:
            return False

    def reset_horizontal(self, h, v):
        self.horizontal[v][h] = self.STATE.EMPTY
        self.horizontal[v][h+1] = self.STATE.EMPTY
        self.xpt[v][h] = self.STATE.EMPTY

    def fill_vertical(self, h, v):
        if self.is_fillable_vertical(h, v):
            self.vertical[v][h] = self.STATE.FILLED
            self.vertical[v+1][h] = self.STATE.FILLED
            self.xpt[v][h] = self.STATE.FILLED
            return True
        else:
            return False

    def reset_vertical(self, h, v):
        self.vertical[v][h] = self.STATE.EMPTY
        self.vertical[v+1][h] = self.STATE.EMPTY
        self.xpt[v][h] = self.STATE.EMPTY
