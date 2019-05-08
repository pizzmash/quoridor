from enum import Enum
from ditch import Ditch


class Board:
    ORDER = Enum('Order', 'FIRST_HAND, SECOND_HAND')

    def __init__(self, size=7, wall=8):
        self.pieces = {
            self.ORDER.FIRST_HAND: [0, (int)(size/2)],
            self.ORDER.SECOND_HAND: [size-1, (int)(size/2)]
        }
        self.walls = {
            self.ORDER.FIRST_HAND: wall,
            self.ORDER.SECOND_HAND: wall
        }
        self.ditch = Ditch(size)
        self.order = self.ORDER.FIRST_HAND

    def another_player(self):
        if self.order == self.ORDER.FIRST_HAND:
            return self.ORDER.SECOND_HAND
        else:
            return self.ORDER.FIRST_HAND

    def turn(self):
        self.order = self.another_player()

    def is_movable(self, player, h, v):
        """
        TODO: playerが[v, h]に移動できるか？
        ↓相手の駒と重なっていないか？
        is_overlapped = [v, h] == self.pieces[self.another_player]
        """
        return True

    def move_piece(self, h, v):
        if self.is_movable(self.order, h, v):
            self.pieces[self.order] = [v, h]
            self.turn()
            return True
        else:
            return False

    def put_horizontal_wall(self, h, v):
        if self.walls[self.order] > 0 and self.ditch.fill_horizontal(h, v):
            self.walls[self.order] -= 1
            self.turn()
            return True
        else:
            return False

    def put_vertical_wall(self, h, v):
        if self.walls[self.order] > 0 and self.ditch.fill_vertical(h, v):
            self.walls[self.order] -= 1
            self.turn()
            return True
        else:
            return False
