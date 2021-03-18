class Encoder:
    def encode(self, board):
        raise NotImplementedError()

    def encode_move(self, move):
        raise NotImplementedError()

    def decode_move_index(self, index):
        raise NotImplementedError()

    def num_points(self):
        raise NotImplementedError()

    def shape(self):
        raise NotImplementedError()
