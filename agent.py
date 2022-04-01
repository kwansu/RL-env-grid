import numpy as np


class Agent:
    def __init__(self, size):
        self.size = size
        self.action_size = 4
        self.state_values = np.zeros(size)
        self.policy = np.ones((*size, self.action_size)) * (1 / self.action_size)
        self.actions = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}

    def reset(self):
        self.policy = np.ones((*self.size, self.action_size)) * (1 / self.action_size)
        self.state_values = np.zeros(self.size)

    def evaluate_policy(self, states):
        copy = self.state_values.copy()
        row, col = self.state_values.shape
        for x in range(row):
            for y in range(col):
                if states[x][y].type == "goal":
                    continue
                updated_score = 0
                for (dx, dy), p in zip(self.actions.values(), self.policy[x, y]):
                    i = max(0, min(x + dx, row - 1))
                    j = max(0, min(y + dy, col - 1))
                    updated_score += copy[i, j] * p - 1
                self.state_values[x, y] = updated_score / 4

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
