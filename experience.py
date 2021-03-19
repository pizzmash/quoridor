import numpy as np


class ExperienceBuffer:
    def __init__(self, states, walls1, walls2, actions, rewards):
        self.states = states
        self.walls1 = walls1
        self.walls2 = walls2
        self.actions = actions
        self.rewards = rewards

    def serialize(self, h5file):
        h5file.create_group('experience')
        h5file['experience'].create_dataset('states', data=self.states)
        h5file['experience'].create_dataset('walls1', data=self.walls1)
        h5file['experience'].create_dataset('walls2', data=self.walls2)
        h5file['experience'].create_dataset('actions', data=self.actions)
        h5file['experience'].create_dataset('rewards', data=self.rewards)


class ExperienceCollector:
    def __init__(self):
        self.states = []
        self.walls1 = []
        self.walls2 = []
        self.actions = []
        self.rewards = []
        self.current_episode_states = []
        self.current_episode_walls1 = []
        self.current_episode_walls2 = []
        self.current_episode_actions = []

    def begin_episode(self):
        self.current_episode_states = []
        self.current_episode_walls1 = []
        self.current_episode_walls2 = []
        self.current_episode_actions = []

    def record_decision(self, state, wall1, wall2, action):
        self.current_episode_states.append(state)
        self.current_episode_walls1.append(wall1)
        self.current_episode_walls2.append(wall2)
        self.current_episode_actions.append(action)

    def complete_episode(self, reward):
        num_states = len(self.current_episode_states)
        self.states += self.current_episode_states
        self.walls1 += self.current_episode_walls1
        self.walls2 += self.current_episode_walls2
        self.actions += self.current_episode_actions
        self.rewards += [reward for _ in range(num_states)]

        self.begin_episode()

    def to_buffer(self):
        return ExperienceBuffer(
            states=np.array(self.states),
            walls1=np.array(self.walls1),
            walls2=np.array(self.walls2),
            actions=np.array(self.actions),
            rewards=np.array(self.rewards)
        )


def combine_experience(collectors):
    combined_states = np.concatenate([np.array(c.states) for c in collectors])
    combined_walls1 = np.concatenate([np.array(c.walls1) for c in collectors])
    combined_walls2 = np.concatenate([np.array(c.walls2) for c in collectors])
    combined_actions = np.concatenate([np.array(c.actions) for c in collectors])
    combined_rewards = np.concatenate([np.array(c.rewards) for c in collectors])

    return ExperienceBuffer(
        combined_states,
        combined_walls1,
        combined_walls2,
        combined_actions,
        combined_rewards)


def load_experience(h5file):
    return ExperienceBuffer(
        states=np.array(h5file['experience']['states']),
        walls1=np.array(h5file['experience']['walls1']),
        walls2=np.array(h5file['experience']['walls2']),
        actions=np.array(h5file['experience']['actions']),
        rewards=np.array(h5file['experience']['rewards'])
    )

def prepare_experience_data(experience, board_size):
    experience_size = experience.actions.shape[0]
    target_vectors = np.zeros(
        (experience_size, board_size * board_size + ((board_size - 1) ** 2) * 2)
    )
    for i in range(experience_size):
        action = experience.actions[i]
        reward = experience.rewards[i]
        target_vectors[i][action] = reward
    return target_vectors
