from player import Player
import copy
from tqdm import tqdm


class MiniMax(Player):
    def __init__(self, eval, depth=3, depth_sort=2):
        self.eval = eval
        self.depth = depth
        self.depth_sort = depth_sort

    def think(self, board):
        move, val = self.search(
            board,
            depth=self.depth,
            depth_sort=self.depth_sort
        )
        return move

    def sorted_move(self, board):
        dict = {}
        moves = list(board.regal_move())
        vir = copy.deepcopy(board)
        for move in moves:
            move.launch(vir)
            dict[move] = self.eval.eval(vir)
        mag = -1 if board.order == board.ORDER.FIRST_HAND else 1
        dict = sorted(dict.items(), key=lambda x: mag * x[1])
        return [x[0] for x in dict]

    def search(self, board, depth, depth_sort, alpha=None, beta=None):
        result = None
        if True in board.is_goaled():
            return None, self.eval.eval(board)
        elif depth <= 0:
            return None, self.eval.eval(board)
        is_end = False
        if depth_sort > 0:
            moves = lambda: self.sorted_move(board)
        else:
            moves = board.regal_move
        for move in tqdm(moves()):
            vir = copy.deepcopy(board)
            move.launch(vir)
            _, val = self.search(
                board=vir,
                depth=depth-1,
                depth_sort=depth_sort-1,
                alpha=alpha,
                beta=beta
            )
            if board.order == board.ORDER.FIRST_HAND:
                if alpha is None or val > alpha:
                    result = move
                    alpha = val
            else:
                if beta is None or val < beta:
                    result = move
                    beta = val
            if alpha is not None and beta is not None and alpha >= beta:
                break
        if board.order == vir.ORDER.FIRST_HAND:
            return result, alpha
        else:
            return result, beta
