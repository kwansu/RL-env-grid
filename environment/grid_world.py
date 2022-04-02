import numpy as np
from environment.base_environment import *


class GridWorld(BaseEnvironment):
    def __init__(self, row, col, *args):
        super().__init__(row, col, *args)
        start_pos=(0, 0)
        self.agent_pos = np.ones(2, dtype=int)
        self.enable_agent_render = True
        self.moves = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
        self.moves = {k: np.array(v) for k, v in self.moves.items()}

        self.start_pos = np.array(start_pos, dtype=int)

        self.selected_cell = None

        self.controls = tuple(Cell(x, col, self.state_length) for x in range(row))
        self.controls[0].sprite = self.sprites["left_item"]
        self.controls[-1].sprite = self.sprites["right_item"]
        self.items = (None, "goal")

        self.start_item_index = 0
        self.max_start_item_index = max(1, len(self.items) - row + 1)
        self.update_item()

        self.reset()

    def reset(self):
        self.agent_pos = self.start_pos
        if self.render:
            self.redraw()
            for cell in self.controls:
                if cell.sprite:
                    cell.draw(self.surface)

            if self.enable_agent_render:
                self.surface.blit(
                    self.sprites["player"], self.agent_pos * self.state_length
                )
        return tuple(self.agent_pos)

    def simulate(self, state, action):
        if not isinstance(state, State):
            state = self.states[state]
            state.step(action)
        return 

    def update_item(self):
        for item, cell in zip(self.items[self.start_item_index :], self.controls[1:]):
            cell.type = item
            cell.sprite = self.sprites[item] if item else None
        if self.selected_cell:
            self.selected_cell.redraw(
                self.surface, self.state_length, self.item_back_color
            )
            self.selected_cell = None

    def play_one_step(self, action):
        self.states[self.agent_pos].redraw(
            self.surface, self.state_length - 1, self.back_color
        )
        self.agent_pos += self.moves[action]
        self.agent_pos.clip(
            0, (self.state_shape[0] - 1, self.state_shape[1] - 1), out=self.agent_pos
        )

        self.surface.blit(self.sprites["agent"], self.agent_pos * self.state_length)
        next_state = tuple(self.agent_pos)
        state: state = self.states[self.agent_pos]
        terminal = state.type == "goal"
        reward = state.reward

        return next_state, reward, terminal

    def click_pos(self, pos):
        if pos > (0, 0) and pos < self.window_size:
            x, y = map(lambda x: x // self.state_length, pos)
            if y >= self.state_shape[1]:
                self.select_item(x)
            else:
                self.change_state(self.states[x, y])

    def change_state(self, state):
        if self.selected_cell:
            state.type = self.selected_cell.type
            state.sprite = self.sprites[state.type] if state.type else None
            state.redraw(self.surface, self.state_length-1, self.back_color)

    def select_item(self, x):
        if x == 0:
            self.start_item_index = min(
                max(self.start_item_index - 1, 0), self.max_start_item_index
            )
            self.update_item()
        elif x == self.state_shape[1] - 1:
            self.start_item_index = min(
                max(self.start_item_index + 1, 0), self.max_start_item_index
            )
            self.update_item()
        else:
            if self.selected_cell:
                self.selected_cell.redraw(
                    self.surface, self.state_length, self.item_back_color
                )
            self.selected_cell = self.controls[self.start_item_index + x]
            if self.selected_cell:
                self.selected_cell.redraw(
                    self.surface, self.state_length, self.selected_back_color
                )
