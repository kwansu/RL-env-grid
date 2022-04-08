import numpy as np
from state import *


class Agent:
    def __init__(self, size, action_size=4, gamma=0.9):
        self.size = size
        self.action_size = action_size
        self.state_values = np.zeros(size)
        self.policy = np.ones((*size, self.action_size)) * (1 / self.action_size)
        self.actions = ["up", "down", "left", "right"]
        self.gamma = gamma

    def reset(self):
        self.policy = np.ones((*self.size, self.action_size)) * (1 / self.action_size)
        self.state_values = np.zeros(self.size)

    def evaluate_policy(self, states):
        copy = self.state_values.copy()
        row, col = self.state_values.shape
        for x in range(row):
            for y in range(col):
                if states[x, y].is_terminal:
                    continue
                new_v = 0
                for action, pa in zip(self.actions, self.policy[x, y]):
                    for pos, p in states[x, y].get_action_trans_prob(action).items():
                        new_v += pa * p * (states[pos].reward + self.gamma * copy[pos])
                self.state_values[x, y] = new_v

    def imporve_policy(self, states):
        row, col = self.state_values.shape
        for x in range(row):
            for y in range(col):
                max_q = float("-inf")
                for i, action in enumerate(self.actions):
                    q = 0
                    for pos, p in states[x, y].get_action_trans_prob(action).items():
                        q += p * (states[pos].reward + self.gamma * self.state_values[pos])
                    # q = sum(
                    #     [
                    #         p * (states[pos].reward + self.gamma * states[pos])
                    #         for pos, p in states[x, y].get__action_trans_prob(action)
                    #     ]
                    # )
                    if q > max_q:
                        max_q, max_count = q, 1
                        self.policy[x, y, :] = 0
                        self.policy[x, y, i] = 1
                    elif q == max_q:
                        max_count += 1
                        self.policy[x, y, i] = 1
                self.policy[x, y] /= max_count
