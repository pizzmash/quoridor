import tkinter
import threading
import copy

from move import PieceMove, HorizontalWallMove, VerticalWallMove


class MoveStack:
    def __init__(self):
        self.lock = threading.Lock()
        self.move = None
        self.valid = False

    def update(self, move):
        self.lock.acquire()
        self.move = move
        self.valid = True
        self.lock.release()
        return True

    def pop(self):
        self.lock.acquire()
        if not self.valid:
            self.lock.release()
            return None
        move = self.move
        self.valid = False
        self.lock.release()
        return move


class BoardCanvas(tkinter.Canvas):
    def __init__(self, master, side, margin, board, players, move_stack=None):
        # キャンバス生成
        # self.canvas = tkinter.Canvas(master, height=side+margin*2, width=side+margin*2)
        super().__init__(master, height=side+margin*2, width=side+margin*2)
        self.bind("<Button-1>", self.click_listener)
        self.bind("<Motion>", self.motion_listener)


        self.board = board
        self.players = players
        self.side = side
        self.margin = margin

        self.piece_colors = ["red", "blue"]

        # マスの幅と溝の幅の比
        self.mass_ditch_width_rate = 5.
        # コマの幅とマスの幅の比
        self.piece_mass_width_rate = 0.8
        # マスの幅
        self.mass_side = side / (board.size + (board.size + 1) / self.mass_ditch_width_rate)
        # 溝の幅
        self.ditch_width = side / (board.size + (board.size + 1) / self.mass_ditch_width_rate) / self.mass_ditch_width_rate

        self.move_stack = move_stack

    def draw_board(self):
        self.create_rectangle(
            self.margin,
            self.margin,
            self.margin + self.side,
            self.margin + self.side,
            fill="burlywood1"
        )
        for v in range(self.board.size):
            for h in range(self.board.size):
                x, y = self.idx_to_mass_pos(h, v)
                self.create_rectangle(
                    x,
                    y,
                    x + self.mass_side,
                    y + self.mass_side,
                    fill="burlywood1"
                )

    def draw_piece(self, h, v, color, tag="piece"):
        mass_margin = (1. - self.piece_mass_width_rate) / 2. * self.mass_side
        x, y = self.idx_to_mass_pos(h, v)
        self.create_oval(
            x + mass_margin,
            y + mass_margin,
            x + mass_margin + self.mass_side * self.piece_mass_width_rate,
            y + mass_margin + self.mass_side * self.piece_mass_width_rate,
            fill=color,
            tag=tag
        )

    def draw_pieces(self):
        for i, order in enumerate(self.board.ORDER):
            v, h = self.board.pieces[order]
            self.draw_piece(h, v, self.piece_colors[i])

    def draw_vertical_wall(self, h, v, color, tag="wall"):
        x, y = self.idx_to_vertical_wall_pos(h, v)
        self.create_rectangle(
            x,
            y,
            x + self.ditch_width,
            y + self.mass_side,
            fill=color,
            tag=tag
        )

    def draw_horizontal_wall(self, h, v, color, tag="wall"):
        x, y = self.idx_to_horizontal_wall_pos(h, v)
        self.create_rectangle(
            x,
            y,
            x + self.mass_side,
            y + self.ditch_width,
            fill=color,
            tag=tag
        )

    def draw_xpt_wall(self, h, v, color, tag="wall"):
        x, y = self.idx_to_cross_ponit_pos(h, v)
        self.create_rectangle(
            x,
            y,
            x + self.ditch_width,
            y + self.ditch_width,
            fill=color,
            tag=tag
        )

    def draw_walls(self):
        for v in range(self.board.size):
            for h in range(self.board.size):
                if h < self.board.size - 1:
                    if self.board.ditch.vertical[v][h] \
                            == self.board.ditch.STATE.FILLED:
                        self.draw_vertical_wall(h, v, "burlywood4")
                if v < self.board.size - 1:
                    if self.board.ditch.horizontal[v][h] \
                            == self.board.ditch.STATE.FILLED:
                        self.draw_horizontal_wall(h, v, "burlywood4")
                if v < self.board.size - 1 and h < self.board.size - 1:
                    if self.board.ditch.xpt[v][h] \
                            == self.board.ditch.STATE.FILLED:
                        self.draw_xpt_wall(h, v, "burlywood4")

    def draw(self):
        self.draw_board()
        self.draw_pieces()
        self.draw_walls()

    def clear(self):
        self.delete("all")

    def clear_piece(self):
        self.delete("piece")

    def clear_wall(self):
        self.delete("wall")

    def idx_to_mass_pos(self, h, v):
        x = self.margin + (h + 1) * self.ditch_width + h * self.mass_side
        y = self.margin + (v + 1) * self.ditch_width + v * self.mass_side
        return x, y

    def idx_to_horizontal_wall_pos(self, h, v):
        x = self.margin + (h + 1) * self.ditch_width + h * self.mass_side
        y = self.margin + (v + 1) * self.ditch_width + (v + 1) * self.mass_side
        return x, y

    def idx_to_vertical_wall_pos(self, h, v):
        x = self.margin + (h + 1) * self.ditch_width + (h + 1) * self.mass_side
        y = self.margin + (v + 1) * self.ditch_width + v * self.mass_side
        return x, y

    def idx_to_cross_ponit_pos(self, h, v):
        x = self.margin + (h + 1) * self.ditch_width + (h + 1) * self.mass_side
        y = self.margin + (v + 1) * self.ditch_width + (v + 1) * self.mass_side
        return x, y

    def pos_to_move(self, x, y):
        if x <= self.margin or y <= self.margin \
                or x > self.margin + self.side \
                or y > self.margin + self.side:
            return None
        h = (x - self.margin) / (self.mass_side + self.ditch_width)
        v = (y - self.margin) / (self.mass_side + self.ditch_width)
        is_h_wall = v - int(v) < 1 / (self.mass_ditch_width_rate + 1)
        is_v_wall = h - int(h) < 1 / (self.mass_ditch_width_rate + 1)
        h = int(h)
        v = int(v)
        if is_h_wall and is_v_wall:
            return None
        elif is_h_wall:
            v -= 1
            if 0 <= h < self.board.size and 0 <= v < self.board.size:
                if h == self.board.size - 1:
                    return HorizontalWallMove(h - 1, v)
                else:
                    return HorizontalWallMove(h, v)
            else:
                return None
        elif is_v_wall:
            h -= 1
            if 0 <= h < self.board.size and 0 <= v < self.board.size:
                if v == self.board.size - 1:
                    return VerticalWallMove(h, v - 1)
                else:
                    return VerticalWallMove(h, v)
            else:
                return None
        else:
            return PieceMove(h, v)

    def click_listener(self, event):
        move = self.pos_to_move(event.x, event.y)
        if self.move_stack is not None:
            if move is not None:
                self.move_stack.update(move)

    def motion_listener(self, event):
        color = "black"
        tag = "candidate"
        self.delete(tag)
        move = self.pos_to_move(event.x, event.y)
        if move is not None:
            board = copy.deepcopy(self.board)
            valid = move.launch(board)
            if not valid:
                return
            if isinstance(move, HorizontalWallMove):
                self.draw_horizontal_wall(move.h, move.v, color, tag)
                self.draw_horizontal_wall(move.h + 1, move.v, color, tag)
                self.draw_xpt_wall(move.h, move.v, color, tag)
            elif isinstance(move, VerticalWallMove):
                self.draw_vertical_wall(move.h, move.v, color, tag)
                self.draw_vertical_wall(move.h, move.v + 1, color, tag)
                self.draw_xpt_wall(move.h, move.v, color, tag)
            elif isinstance(move, PieceMove):
                self.draw_piece(move.h, move.v, color, tag)
