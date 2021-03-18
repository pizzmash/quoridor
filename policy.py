import numpy as np

from player import Player
from simpleencoder import SimpleEncoder
from move import PieceMove, HorizontalWallMove, VerticalWallMove
import kerasutil


class Policy(Player):
    def __init__(self, model, encoder):
        self.model = model
        self.encoder = encoder

    def clip_probs(self, probs):
        min_p = 1e-5
        max_p = 1 - min_p
        clipped_probs = np.clip(probs, min_p, max_p)
        clipped_probs = clipped_probs / np.sum(clipped_probs)
        return clipped_probs

    def think(self, board):
        board_tensor, wall1, wall2 = self.encoder.encode(board)
        X = np.array([board_tensor])
        Y = np.array([wall1])
        Z = np.array([wall2])
        move_probs = self.model.predict([X, Y, Z])[0]

        move_probs = self.clip_probs(move_probs)

        num_moves = self.encoder.num_points()
        candidates = np.arange(num_moves)
        ranked_moves = np.random.choice(
            candidates, num_moves, replace=False, p=move_probs)

        for move_idx in ranked_moves:
            move = self.encoder.decode_move_index(move_idx)
            if move.launch(board):
                break

        if self.collector is not None:
            self.collector.record_decision(
                state=board_tensor, wall1=wall1, wall2=wall2, action=move_idx
            )
        return move

    def set_collector(self, collector):
        self.collector = collector

    def serialize(self, h5file):
        h5file.create_group("encoder")
        h5file['encoder'].attrs['board_size'] = self.encoder.board_size
        h5file.create_group("model")
        kerasutil.save_model_to_hdf5_group(self.model, h5file['model'])


def load_policy_agent(h5file):
    model = kerasutil.load_model_from_hdf5_group(h5file['model'])
    board_size = h5file["encoder"].attrs['board_size']
    encoder = SimpleEncoder(board_size=board_size)
    return Policy(model, encoder)
