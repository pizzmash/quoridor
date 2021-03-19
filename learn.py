import numpy as np
import copy
import h5py
from tqdm import tqdm
from keras.layers import Input, Dense, Activation, concatenate
from keras.models import Model

from simpleencoder import SimpleEncoder
from layers import layers
from policy import Policy, load_policy_agent
from experience import ExperienceBuffer, ExperienceCollector, combine_experience, load_experience
from board import Board
from evaluation import DistanceEvaluation
from minimax import MiniMax
from randombot import RandomBot


def simulate_game(board_size, wall, players):
    board = Board(size=board_size, wall=wall)
    while True not in board.is_goaled():
        player = players[0] if board.order == board.ORDER.FIRST_HAND else players[1]
        vir = copy.deepcopy(board)
        move = player.think(vir)
        move.launch(board)
    return 0 if board.is_goaled()[0] else 1


def compere_agent(num_games, board_size, wall, players):
    wins = 0
    losses = 0
    for i in tqdm(range(num_games)):
        if i % 2 == 0:
            ps = players
            order = 0
        else:
            ps = [players[1], players[0]]
            order = 1
        result = simulate_game(board_size, wall, ps)
        if result == order:
            wins += 1
        else:
            losses += 1
    print('Agent 1 record: {}/{}'.format(wins, wins + losses))


def main():
    board_size = 5
    wall = 6

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

    policy_fn = "policy.hdf5"
    updated_agent_filename = "policy.hdf5"

    collector1 = ExperienceCollector()
    collector2 = ExperienceCollector()

    for piyo in range(100):

        if piyo > 0:
            agent1 = load_policy_agent(h5py.File(policy_fn))
            agent2 = load_policy_agent(h5py.File(policy_fn))
        else:
            agent1 = Policy(model, encoder)
            agent2 = Policy(model, encoder)
        agent1.set_collector(collector1)
        agent2.set_collector(collector2)

        num_games = 5

        for i in tqdm(range(num_games)):
            collector1.begin_episode()
            collector2.begin_episode()

            winner = simulate_game(board_size, wall, [agent1, agent2])
            if winner == 0:
                collector1.complete_episode(reward=1)
                collector2.complete_episode(reward=-1)
            else:
                collector1.complete_episode(reward=-1)
                collector2.complete_episode(reward=1)

        exp_filename = "experience.hdf5"

        experience = combine_experience([collector1, collector2])
        with h5py.File(exp_filename, 'w') as experience_outf:
            experience.serialize(experience_outf)

        learning_agent_filename = policy_fn

        if piyo > 0:
            learning_agent = load_policy_agent(h5py.File(learning_agent_filename))
        else:
            learning_agent = Policy(model, encoder)
        exp_buffer = load_experience(h5py.File(exp_filename))
        learning_agent.train(
            exp_buffer,
            lr=0.01,
            # clipnorm=learning_agent.clip_probs,
            batch_size=16
        )
        with h5py.File(updated_agent_filename, 'w') as updated_agent_outf:
            learning_agent.serialize(updated_agent_outf)
        if piyo > 0 and piyo % 10 == 0:
            compere_agent(100, board_size, wall, [learning_agent, agent1])


if __name__ == main():
    main()
