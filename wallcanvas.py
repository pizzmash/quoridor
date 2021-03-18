import tkinter


class WallCanbas(tkinter.Canvas):
    def __init__(self, master, wall, width, height, wall_width, wall_length):
        super().__init__(master, height=height, width=width, background="burlywood1")
        self.width = width
        self.height = height
        self.wall = wall
        self.current_wall = wall
        self.wall_width = wall_width
        self.wall_length = wall_length

    def draw(self):
        margin_x = (self.width - self.wall * self.wall_width) / (self.wall + 1.)
        margin_y = (self.height - self.wall_length) / 2.
        for i in range(self.wall):
            start_x = (margin_x + self.wall_width) * (i + 1) - self.wall_width / 2.
            self.create_rectangle(
                start_x,
                margin_y,
                start_x + self.wall_width,
                margin_y + self.wall_length,
                fill = "burlywood4",
                tag="wall_{}".format(i)
            )

    def use(self):
        self.current_wall -= 1
        self.delete("wall_{}".format(self.current_wall))
