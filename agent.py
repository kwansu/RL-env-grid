import numpy as np
from states import *


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
                a = states[x, y]
                if a.is_terminal:
                    continue
                new_v = 0
                for action, ps in zip(self.actions, self.policy[x, y]):
                    for pos, p in states[x, y].get_transition_prob(action).items():
                        new_v += ps * p * (states[pos].reward + self.gamma * copy[pos])
                self.state_values[x, y] = new_v

    def imporve_policy(self):
        row, col = self.state_values.shape
        for x in range(row):
            for y in range(col):
                max_value = -1000.0
                for n, (dx, dy) in enumerate(self.actions.values()):
                    i = max(0, min(x + dx, row - 1))
                    j = max(0, min(y + dy, col - 1))
                    if self.state_values[i, j] > max_value:
                        max_value, max_count = self.state_values[i, j], 1
                        self.policy[x, y, :] = 0
                        self.policy[x, y, n] = 1
                    elif self.state_values[i, j] == max_value:
                        max_count += 1
                        self.policy[x, y, n] = 1
                self.policy[x, y] /= max_count
