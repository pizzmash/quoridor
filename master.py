class Master:
    def __init__(self, board, players):
        self.board = board
        self.players = players

    def start(self):
        self.board.show()
        for player in self.players:
            player.register_board(self.board)
        while True:
            for player in self.players:
                player.think()
                self.board.show()
