from player import Player
from move import PieceMove, HorizontalWallMove, VerticalWallMove


class Human(Player):
    def think(self):
        print('1: 動く\n2: 横の壁\n 3: 縦の壁')
        mode = int(input())
        print('どこに？')
        v, h = [int(i) for i in input().split()]
        if mode == 1:
            move = PieceMove(h, v)
        elif mode == 2:
            move = HorizontalWallMove(h, v)
        elif mode == 3:
            move = VerticalWallMove(h, v)
        move.launch()
