from enum import Enum
from ditch import Ditch


class Board:
    ORDER = Enum('Order', 'FIRST_HAND, SECOND_HAND')

    def __init__(self, size=7, wall=8):
        self.size = size
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

    def movable_mass(self, from_h=None, from_v=None):
        if from_h is None or from_v is None:
            from_v, from_h = self.pieces[self.order]
        mass = []
        dir = [[-1, 0], [0, -1], [0, 1], [1, 0]]
        for d in dir:
            h, v = from_h + d[1], from_v + d[0]
            is_regal_h = h >= 0 and h + d[1] < self.size
            is_regal_v = v + d[0] >= 0 and v + d[0] < self.size
            if is_regal_h and is_regal_v:
                if d[0] == 0:
                    ditch = self.ditch.vertical
                else:
                    ditch = self.ditch.horizontal
                if -1 in d:
                    ditch_pos_h, ditch_pos_v = from_h + d[1], from_v + d[0]
                else:
                    ditch_pos_h, ditch_pos_v = from_h, from_v
                if ditch[ditch_pos_v][ditch_pos_h] == self.ditch.STATE.EMPTY:
                    if [v, h] == self.pieces[self.another_player()]:
                        # TODO: これだと相手が隣接しているところだったら方向を問わず跳べちゃう
                        mass += self.movable_mass(h, v)
                    else:
                        mass += [[v, h]]
        try:
            mass.remove([from_v, from_h])
        except ValueError:
            pass
        return mass

    def move_piece(self, h, v):
        if [v, h] in self.movable_mass():
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
