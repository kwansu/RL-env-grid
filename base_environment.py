import time
import pygame
import threading
import numpy as np

from abc import *
from cell import *
from render_process import *


class BaseEnvironment(ABC):
    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def simulate(self, state, action):
        pass

    def __init__(
        self,
        row,
        col,
        key_queue,
        hotkey_funcs={},
        object_infos={},
        state_length=100,
        render=True,
        back_color=(128, 128, 128),
        item_back_color=(255, 255, 128),
        selected_back_color=(180, 70, 200),
    ):
        self.is_running = True
        self.state_length = state_length
        self.states = np.array(
            [[State(x, y, self.state_length) for y in range(col)] for x in range(row)]
        )
        self.window_size = (row * state_length, (col + 1) * state_length)
        self.state_shape = (row, col)
        self.actions = ("up", "down", "left", "right")

        self.render = render
        if render:
            self.back_color = back_color
            self.item_back_color = item_back_color
            self.selected_back_color = selected_back_color

            self.surface = None
            self.setup_render(key_queue, hotkey_funcs, object_infos)
            self.redraw()

    def draw_values(self, state_values):
        assert state_values.shape == self.state_shape
        for x in range(self.state_shape[0]):
            for y in range(self.state_shape[1]):
                self.draw_text(str(round(state_values[x, y], 2)), x, y)

    def draw_policy(self, policy):
        for x in range(self.state_shape[0]):
            for y in range(self.state_shape[1]):
                if self.states[x, y].type != "goal":
                    for i, p in enumerate(policy[x, y]):
                        sprite = self.sprites[self.actions[i]]
                        sprite.set_alpha(p * 255)
                        self.surface.blit(
                            sprite,
                            (x * self.state_length + 1, y * self.state_length + 1),
                        )

    def shutdown(self):
        if self.render and self.is_running:
            try:
                quit_pygame()
                self.render_thread.join(timeout=10)
            except Exception as e:
                print(e)
            else:
                print("render thread shutdown.")

    def redraw(self):
        if self.render:
            row, col = self.state_shape
            self.surface.fill(self.item_back_color)
            self.surface.fill(
                self.back_color,
                (0, 0, self.state_length * row, self.state_length * col),
            )
            pygame.display.flip()

            draw_grid(self.surface, row, col + 1)

            for line in self.states:
                for state in line:
                    if state.type:
                        state.draw(self.surface)

    def draw_text(self, text, x, y, color=(0, 0, 255)):
        self.states[x, y].redraw(self.surface, self.state_length - 1, self.back_color)
        text = self.font.render(text, True, color)
        w, h = text.get_size()
        x = (self.state_length - w) // 2 + x * self.state_length
        y = (self.state_length - h) // 2 + y * self.state_length
        self.surface.blit(text, (x, y))

    def setup_render(self, key_queue, hotkey_funcs, object_infos={}):
        pygame.font.init()
        self.font = pygame.font.SysFont("consolas", 15, True)

        self.render_thread = threading.Thread(
            target=render_process, args=(self, key_queue, hotkey_funcs)
        )
        self.render_thread.start()

        for _ in range(100):
            time.sleep(0.01)
            if self.surface:
                break
        else:
            raise Exception()

        in_size = (self.state_length - 2, self.state_length - 2)

        self.sprites = {
            key: pygame.transform.scale(pygame.image.load(path), in_size)
            for key, path in object_infos.items()
        }

    def quit_callback(self):
        self.is_running = False
