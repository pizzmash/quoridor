from enum import Enum


class Ditch:
    STATE = Enum('State', 'EMPTY, FILLED')

    def __init__(self, size):
        self.horizontal = [[self.STATE.EMPTY] * size for v in range(size-1)]
        self.vertical = [[self.STATE.EMPTY] * (size-1) for v in range(size)]
        self.xpt = [[self.STATE.EMPTY] * (size-1) for v in range(size-1)]

    def fill_horizontal(self, h, v):
        self.horizontal[v][h] = self.FILLED

    def fill_vertical(self, h, v):
        self.vertical[v][h] = self.FILLED
