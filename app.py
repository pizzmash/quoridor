import tkinter
import threading
import copy


class App(tkinter.Frame):
    def __init__(self, master, side, margin, board, players):
        super().__init__(master)
        self.pack()

        master.geometry("{}x{}".format(side+margin*2, side+margin*2))
        master.title("title here")

        # キャンバス生成
        self.canvas = tkinter.Canvas(master, height=side+margin*2, width=side+margin*2)
        self.canvas.bind("<Button-1>", self.canvas_click_listener)
        self.canvas.pack()

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

        self.thread = threading.Thread(target=self.game)

    def draw_board(self):
        self.canvas.create_rectangle(
            self.margin,
            self.margin,
            self.margin + self.side,
            self.margin + self.side,
            fill="burlywood1"
        )
        for v in range(self.board.size):
            for h in range(self.board.size):
                x, y = self.idx_to_mass_pos(h, v)
                self.canvas.create_rectangle(
                    x,
                    y,
                    x + self.mass_side,
                    y + self.mass_side,
                    fill="burlywood1"
                )

    def draw_piece(self):
        mass_margin = (1. - self.piece_mass_width_rate) / 2. * self.mass_side
        for i, order in enumerate(self.board.ORDER):
            v, h = self.board.pieces[order]
            x, y = self.idx_to_mass_pos(h, v)
            self.canvas.create_oval(
                x + mass_margin,
                y + mass_margin,
                x + mass_margin + self.mass_side * self.piece_mass_width_rate,
                y + mass_margin + self.mass_side * self.piece_mass_width_rate,
                fill=self.piece_colors[i],
                tag="piece"
            )

    def draw_wall(self):
        for v in range(self.board.size):
            for h in range(self.board.size):
                if h < self.board.size - 1:
                    if self.board.ditch.vertical[v][h] \
                            == self.board.ditch.STATE.FILLED:
                        x, y = self.idx_to_vertical_wall_pos(h, v)
                        self.canvas.create_rectangle(
                            x,
                            y,
                            x + self.ditch_width,
                            y + self.mass_side,
                            fill="burlywood4",
                            tag="wall"
                        )
                if v < self.board.size - 1:
                    if self.board.ditch.horizontal[v][h] \
                            == self.board.ditch.STATE.FILLED:
                        x, y = self.idx_to_horizontal_wall_pos(h, v)
                        self.canvas.create_rectangle(
                            x,
                            y,
                            x + self.mass_side,
                            y + self.ditch_width,
                            fill="burlywood4",
                            tag="wall"
                        )
                if v < self.board.size - 1 and h < self.board.size - 1:
                    if self.board.ditch.xpt[v][h] \
                            == self.board.ditch.STATE.FILLED:
                        x, y = self.idx_to_cross_ponit_pos(h, v)
                        self.canvas.create_rectangle(
                            x,
                            y,
                            x + self.ditch_width,
                            y + self.ditch_width,
                            fill="burlywood4",
                            tag="wall"
                        )

    def draw(self):
        self.draw_board()
        self.draw_piece()
        self.draw_wall()

    def clear(self):
        self.canvas.delete("all")

    def clear_piece(self):
        self.canvas.delete("piece")

    def clear_wall(self):
        self.canvas.delete("wall")

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

    def pos_to_idx(self, x, y):
        if x <= self.margin or y <= self.margin \
                or x > self.margin + self.side \
                or y > self.margin + self.side:
            return -2
        h = (x - self.margin) / (self.mass_side + self.ditch_width)
        v = (y - self.margin) / (self.mass_side + self.ditch_width)
        is_h_wall = h - int(h) < 1 / (self.mass_ditch_width_rate + 1)
        is_v_wall = v - int(v) < 1 / (self.mass_ditch_width_rate + 1)
        if is_h_wall and is_v_wall:
            return -1
        elif is_h_wall:
            return 2, int(h) - 1, int(v)
        elif is_v_wall:
            return 3, int(h), int(v) - 1
        else:
            return 1, int(h), int(v)

    def canvas_click_listener(self, event):
        pos_info = self.pos_to_idx(event.x, event.y)
        if pos_info == -2:
            print("out of range")
        elif pos_info == -1:
            print("ditch x ditch!")
        else:
            print(pos_info[0], pos_info[1], pos_info[2])

    def game(self):
        self.draw()
        while getattr(self.thread, "run", True):
            while True:
                player = self.players[0] if self.board.order == self.board.ORDER.FIRST_HAND else self.players[1]
                board = copy.deepcopy(self.board)
                move = player.think(board)
                if move.launch(self.board):
                    break
            self.clear_piece()
            self.clear_wall()
            self.draw_piece()
            self.draw_wall()
            if True in self.board.is_goaled():
                pass
                break

    def mainloop(self):
        self.thread.start()
        super().mainloop()
        self.thread.run = False
        self.thread.join()
