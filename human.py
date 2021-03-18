from player import Player


class Human(Player):
    def __init__(self, move_stack=None):
        self.move_stack = move_stack

    def think(self, board):
        if self.move_stack is None:
            return None
        move = self.move_stack.pop()
        while move is None:
            move = self.move_stack.pop()
        return move
