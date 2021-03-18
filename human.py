from player import Player


class Human(Player):
    def __init__(self, move_stack):
        self.move_stack = move_stack

    def think(self, board):
        move = self.move_stack.pop()
        while move is None:
            move = self.move_stack.pop()
        return move
