from player import Player
from move import PieceMove, HorizontalWallMove, VerticalWallMove


class Human(Player):
    def think(self):
        print('1: 動く\n2: 横の壁\n3: 縦の壁')
        mode = int(input())
        if mode == 1:
            print('どこに？')
            print(self.board.movable_mass())
            v, h = [int(i) for i in input().split()]
            move = PieceMove(h, v)
        elif mode == 2:
            print('どこに？')
            v, h = [int(i) for i in input().split()]
            move = HorizontalWallMove(h, v)
        elif mode == 3:
            print('どこに？')
            v, h = [int(i) for i in input().split()]
            move = VerticalWallMove(h, v)
        move.launch(self.board)
