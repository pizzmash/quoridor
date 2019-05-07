from analyzer import Analyzer


class GameMaster:
    def __init__(self, board, players):
        self.board = board
        self.players = players
        self.analyzer = Analyzer(self.board)
