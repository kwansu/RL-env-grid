import numpy as np
from environment.base_environment import *


class GridWorld(BaseEnvironment):
    def __init__(self, row, col, items, **kwargs):
        super().__init__(row, col, **kwargs)
        start_pos = (0, 0)
        self.agent_pos = np.ones(2, dtype=int)
        self.enable_agent_render = False

        self.start_pos = np.array(start_pos, dtype=int)

        self.selected_idx = None

        self.controls = [State(x, col) for x in range(row)]
        self.controls[0].sprite = self.sprites["left_item"]
        self.controls[-1].sprite = self.sprites["right_item"]
        self.items = tuple([state(0, 0) for state in items])

        self.start_item = 0
        self.max_item = max(0, len(self.items) - row + 2)
        self._update_item()

        self.reset()

    def reset(self):
        self.agent_pos = self.start_pos
        self._redraw()
        for state in self.controls:
            if state.sprite:
                state.draw(self.surface, self.item_back_color)

        if self.enable_agent_render:
            self.surface.blit(
                self.sprites["player"], self.agent_pos * self.state_length
            )
        return tuple(self.agent_pos)

    def change_state(self, pos, state_type):
        self.states[pos] = state_type(*pos)
        self.states[pos].redraw(self.surface, self.back_color)

    def click_pos(self, pos):
        if pos > (0, 0) and pos < self.window_size:
            x, y = map(lambda x: x // self.state_length, pos)
            if y >= self.state_shape[1]:
                self._select_item(x)
            else:
                self.change_state((x, y), type(self.controls[self.selected_idx]))

    def _update_item(self):
        for item, i in zip(
            self.items[self.start_item :], range(1, len(self.controls) - 1)
        ):
            item.copy_info(self.controls[i])
            self.controls[i] = item
            self.controls[i].redraw(self.surface, self.item_back_color)

        if self.selected_idx:
            self.controls[self.selected_idx].redraw(self.surface, self.item_back_color)
            self.selected_idx = None

    def _select_item(self, x):
        if x == 0:
            self.start_item = min(max(self.start_item - 1, 0), self.max_item)
            self._update_item()
        elif x == self.state_shape[0] - 1:
            self.start_item = min(max(self.start_item + 1, 0), self.max_item)
            self._update_item()
        else:
            if self.selected_idx:
                self.controls[self.selected_idx].redraw(
                    self.surface, self.item_back_color
                )
            self.selected_idx = self.start_item + x
            if self.selected_idx:
                self.controls[self.selected_idx].redraw(
                    self.surface, self.selected_back_color
                )

    def draw_values(self, state_values):
        assert state_values.shape == self.state_shape
        self.set_render_value(True)

        for o, v in zip(np.nditer(self.states, ["refs_ok"]), np.nditer(state_values)):
            state = o.item()
            state.set_value(str(np.round(v, 3)), self.font)
            state.draw(self.surface, self.back_color)

    def draw_policy(self, policy):
        assert policy.shape[:2] == self.state_shape
        self.set_render_policy(True)

        for x in range(self.state_shape[0]):
            for y in range(self.state_shape[1]):
                state = self.states[x, y]
                if not state.is_terminal:
                    state.set_policy(policy[x, y])
                    state.draw(self.surface, self.back_color)

    def set_render_value(self, enable):
        State.render_value = enable

    def set_render_policy(self, enable):
        State.render_policy = enable
