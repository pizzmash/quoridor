import copy


class Master:
    def __init__(self, board, players):
        self.board = board
        self.players = players

    def start(self):
        is_end = False
        self.board.show()
        while not is_end:
            for player in self.players:
                while True:
                    print(self.board.order)
                    board = copy.deepcopy(self.board)
                    if not player.think(board).launch(self.board):
                        print('不正な着手です．')
                    else:
                        break
                self.board.show()
                if True in self.board.is_goaled():
                    print(board.another_player(), 'の勝ちです．')
                    is_end = True
                    break
