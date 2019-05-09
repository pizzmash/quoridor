import copy


class Master:
    def __init__(self, board, players):
        self.board = board
        self.players = players

    def start(self):
        self.board.show()
        while True:
            for player in self.players:
                while True:
                    board = copy.deepcopy(self.board)
                    if not player.think(board).launch(self.board):
                        print('それ不正だよ')
                    else:
                        break
                self.board.show()
