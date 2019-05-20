from human import Human
import copy
from tqdm import tqdm


class MiniMax(Human):
    def __init__(self, eval, depth=3):
        self.eval = eval
        self.depth = depth

    def think(self, board):
        dict = {}
        moves = list(board.regal_move())
        vir = copy.deepcopy(board)
        for move in moves:
            move.launch(vir)
            dict[move] = self.eval.eval(vir)
        mag = -1 if board.order == board.ORDER.FIRST_HAND else 1
        dict = sorted(dict.items(), key=lambda x: mag * x[1])
        moves = [x[0] for x in dict]
        move, val = self.search(board, depth=self.depth, moves=moves)
        return move

    def search(self, board, depth, moves=None, alpha=None, beta=None):
        result = None
        if True in board.is_goaled():
            return None, self.eval.eval(board)
        elif depth <= 0:
            return None, self.eval.eval(board)
        is_end = False
        if moves is None:
            regal_move = board.regal_move
        else:
            regal_move = lambda: moves
        for move in tqdm(regal_move()):
            vir = copy.deepcopy(board)
            move.launch(vir)
            _, val = self.search(board=vir, depth=depth-1, alpha=alpha, beta=beta)
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
