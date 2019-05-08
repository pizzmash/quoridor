from board import Board
from human import Human
from master import Master


def main():
    size = 5
    board = Board(size=size)
    p1 = Human()
    p2 = Human()
    master = Master(board, [p1, p2])
    master.start()


if __name__ == '__main__':
    main()
