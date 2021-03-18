import numpy as np
import copy
import h5py
from keras.layers import Input, Dense, Activation, concatenate
from keras.models import Model

from simpleencoder import SimpleEncoder
from layers import layers
from policy import Policy
from experience import ExperienceBuffer, ExperienceCollector, combine_experience
from board import Board


def simulate_game(board_size, wall, players):
    board = Board(size=board_size, wall=wall)
    while True not in board.is_goaled():
        player = players[0] if board.order == board.ORDER.FIRST_HAND else players[1]
        vir = copy.deepcopy(board)
        move = player.think(vir)
        move.launch(board)
    return 0 if board.is_goaled()[0] else 1


def main():
    board_size = 7
    wall = 8

    encoder = SimpleEncoder(board_size=board_size)
    input1 = Input(shape=encoder.shape()[0])
    input2 = Input(shape=encoder.shape()[1])
    input3 = Input(shape=encoder.shape()[2])
    x = input1
    for layer in layers(encoder.shape()[0]):
        x = layer(x)
    x = Model(inputs=input1, outputs=x)
    y = Model(inputs=input2, outputs=input2)
    z = Model(inputs=input3, outputs=input3)

    combined = concatenate([x.output, y.output, z.output])

    u = Dense(encoder.num_points())(combined)
    u = Activation("softmax")(u)

    model = Model(inputs=[x.input, y.input, z.input], outputs=u)

    agent1 = Policy(model, encoder)
    agent2 = Policy(model, encoder)
    collector1 = ExperienceCollector()
    collector2 = ExperienceCollector()
    agent1.set_collector(collector1)
    agent2.set_collector(collector2)

    num_games = 2

    for i in range(num_games):
        print("start")
        collector1.begin_episode()
        collector2.begin_episode()

        winner = simulate_game(board_size, wall, [agent1, agent2])
        if winner == 0:
            collector1.complete_episode(reward=1)
            collector2.complete_episode(reward=-1)
        else:
            collector1.complete_episode(reward=-1)
            collector2.complete_episode(reward=1)

    experience = combine_experience([collector1, collector2])
    with h5py.File("experience.hdf5", 'w') as experience_outf:
        experience.serialize(experience_outf)



if __name__ == main():
    main()
