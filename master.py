class Master:
    def __init__(self, board, players):
        self.board = board
        self.players = players

    def start(self):
        self.board.show()
        order = self.board.order
        for player in self.players:
            player.register_board(self.board)
        while True:
            for player in self.players:
                while True:
                    player.think()
                    if self.board.order != order:
                        order = self.board.order
                        break
                    else:
                        print('それ不正だよ')
                self.board.show()
