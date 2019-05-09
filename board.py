import queue
import copy
from enum import Enum
from ditch import Ditch
from move import PieceMove, HorizontalWallMove, VerticalWallMove


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
        self.goal_v = {
            self.ORDER.FIRST_HAND: size-1,
            self.ORDER.SECOND_HAND: 0
        }
        self.ditch = Ditch(size)
        self.order = self.ORDER.FIRST_HAND

    def another_player(self, player=None):
        player = self.order if player is None else player
        if player == self.ORDER.FIRST_HAND:
            return self.ORDER.SECOND_HAND
        else:
            return self.ORDER.FIRST_HAND

    def turn(self):
        self.order = self.another_player()

    def movable_mass(self, player=None, from_h=None, from_v=None, is_jumping=False):
        player = self.order if player is None else player
        if from_h is None or from_v is None:
            from_v, from_h = self.pieces[player]
        mass = []
        dir = [[-1, 0], [0, -1], [0, 1], [1, 0]]
        for d in dir:
            h, v = from_h + d[1], from_v + d[0]
            is_regal_h = h >= 0 and h < self.size
            is_regal_v = v >= 0 and v < self.size
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
                    is_overlapped = \
                        [v, h] == self.pieces[self.another_player(player=player)]
                    if not is_jumping and is_overlapped:
                        # TODO: これだと相手が隣接しているところだったら方向を問わず跳べちゃう
                        mass += self.movable_mass(
                            player=self.another_player(player=player),
                            from_h=h,
                            from_v=v,
                            is_jumping=True
                        )
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
            if -1 in self.distance():
                print(self.distance())
                self.ditch.reset_horizontal(h, v)
                return False
            self.walls[self.order] -= 1
            self.turn()
            return True
        else:
            return False

    def put_vertical_wall(self, h, v):
        if self.walls[self.order] > 0 and self.ditch.fill_vertical(h, v):
            if -1 in self.distance():
                self.ditch.reset_vertical(h, v)
                return False
            self.walls[self.order] -= 1
            self.turn()
            return True
        else:
            return False

    def regal_move(self):
        result = []
        for m in self.movable_mass():
            result.append(PieceMove(h=m[1], v=m[0]))
        if self.walls[self.order] > 0:
            for v in range(self.size-1):
                for h in range(self.size-1):
                    if self.ditch.fill_horizontal(h, v):
                        if -1 not in self.distance():
                            result.append(HorizontalWallMove(h=h, v=v))
                        self.ditch.reset_horizontal(h, v)
                    if self.ditch.fill_vertical(h, v):
                        if -1 not in self.distance():
                            result.append(VerticalWallMove(h=h, v=v))
                        self.ditch.reset_vertical(h, v)
        return result

    def is_goaled(self):
        result = []
        for player in self.ORDER:
            if self.pieces[player][0] == self.goal_v[player]:
                result.append(True)
            else:
                result.append(False)
        return result

    def distance(self):
        result = []
        for player in self.ORDER:
            q = queue.Queue()
            is_visited = [[False] * self.size for i in range(self.size)]
            is_goaled = False
            q.put((self.pieces[player], 0))
            is_visited[self.pieces[player][0]][self.pieces[player][1]] = True
            while not q.empty():
                pos = q.get()
                mass = self.movable_mass(
                    player=player,
                    from_h=pos[0][1],
                    from_v=pos[0][0],
                )
                for m in copy.deepcopy(mass):
                    if is_visited[m[0]][m[1]]:
                        mass.remove(m)
                if self.goal_v[player] in [mass[i][0] for i in range(len(mass))]:
                    is_goaled = True
                    distance = pos[1]+1
                    break
                else:
                    for m in mass:
                        q.put((m, pos[1]+1))
                        is_visited[m[0]][m[1]] = True
            result.append(distance if is_goaled else -1)
        return result

    def show(self):
        print('+', end='')
        for h in range(self.size):
            print('-+', end='')
        print('')
        for v in range(self.size):
            print('|', end='')
            for h in range(self.size):
                if [v, h] == self.pieces[self.ORDER.FIRST_HAND]:
                    print('A', end='')
                elif [v, h] == self.pieces[self.ORDER.SECOND_HAND]:
                    print('B', end='')
                else:
                    print(' ', end='')
                if h < self.size - 1:
                    if self.ditch.vertical[v][h] == self.ditch.STATE.EMPTY:
                        print(' ', end='')
                    else:
                        print('|', end='')
                else:
                    print('|', end='')
            print('')
            print('+', end='')
            for h in range(self.size):
                if v < self.size - 1:
                    if self.ditch.horizontal[v][h] == self.ditch.STATE.EMPTY:
                        print(' ', end='')
                    else:
                        print('-', end='')
                else:
                    print('-', end='')
                print('+', end='')
            print('')
