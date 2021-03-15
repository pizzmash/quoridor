import tkinter


class App(tkinter.Frame):
    def __init__(self, master, side, margin, board):
        super().__init__(master)
        self.pack()

        master.geometry("{}x{}".format(side+margin*2, side+margin*2))
        master.title("title here")

        # キャンバス生成
        self.canvas = tkinter.Canvas(master, height=side+margin*2, width=side+margin*2)

        self.board = board
        self.side = side
        self.margin = margin

        # マスの幅と溝の幅の比
        self.rate = 5.
        # マスの幅
        self.mass_side = side / (board.size + (board.size + 1) / self.rate)
        # 溝の幅
        self.ditch_width = side / (board.size + (board.size + 1) / self.rate) / self.rate

        self.draw()

    def draw(self):
        self.canvas.create_rectangle(self.margin, self.margin, self.margin + self.side, self.margin + self.side, fill="burlywood1")
        self.canvas.bind("<Button-1>", self.canvas_click_listener)
        for v in range(self.board.size):
            for h in range(self.board.size):
                x, y = self.idx_to_mass_pos(h, v)
                self.canvas.create_rectangle(x, y, x + self.mass_side, y + self.mass_side, fill="burlywood1")
        self.canvas.pack()

    def idx_to_mass_pos(self, h, v):
        x = self.margin + (h + 1) * self.ditch_width + h * self.mass_side
        y = self.margin + (v + 1) * self.ditch_width + v * self.mass_side
        return x, y

    def pos_to_idx(self, x, y):
        if x <= self.margin or y <= self.margin \
                or x > self.margin + self.side \
                or y > self.margin + self.side:
            return -2
        h = (x - self.margin) / (self.mass_side + self.ditch_width)
        v = (y - self.margin) / (self.mass_side + self.ditch_width)
        is_h_wall = h - int(h) < 1 / (self.rate + 1)
        is_v_wall = v - int(v) < 1 / (self.rate + 1)
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
