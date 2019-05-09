from human import Human
import copy


class MiniMax(Human):
    def __init__(self, eval, depth=3):
        self.eval = eval
        self.depth = depth

    def think(self, board):
        self.is_first_hand = board.order == board.ORDER.FIRST_HAND
        return self.think(board, depth=self.depth)[0]

    def think(self, board, depth, alpha=None, beta=None):
        if True in board.is_goaled():
            return None, self.eval.eval(board)
        elif depth <= 0:
            return None, self.eval.eval(board)
        for move in board.regal_move():
            vir = move.launch(copy.deepcopy(board))
            _, val = self.think(board=vir, depth=depth-1, alpha=alpha, beta=beta)
            if board.order == board.ORDER.FIRST_HAND:
                if alpha is None or val > alpha:
                    result = move
                    alpha = val
            else:
                if beta is None or val < beta:
                    result = move
                    beta = val
            if alpha is not None and beta is not None and alpha > beta:
                break
        if board.order == vir.ORDER.FIRST_HAND:
            return result, alpha
        else:
            return result, beta
