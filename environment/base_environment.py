import time
import pygame
import inspect
import threading
import numpy as np


from abc import *
from states import *
from environment.render_process import *


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
        img_dict={},
        state_length=100,
        back_color=(128, 128, 128),
        item_back_color=(255, 255, 128),
        selected_back_color=(180, 70, 200),
    ):
        self.is_running = True
        self.state_length = state_length
        Cell.l = self.state_length
        Cell.max_x, Cell.max_y = row - 1, col - 1
        self.states = np.array([[State(x, y) for y in range(col)] for x in range(row)])
        self.window_size = (row * state_length, (col + 1) * state_length)
        self.state_shape = (row, col)
        self.actions = ("up", "down", "left", "right")

        self.back_color = back_color
        self.item_back_color = item_back_color
        self.selected_back_color = selected_back_color

        self.surface = None
        self.setup_render(key_queue, hotkey_funcs, img_dict)
        self.redraw()

    def shutdown(self):
        if self.is_running:
            try:
                quit_pygame()
                self.render_thread.join(timeout=10)
            except Exception as e:
                print(e)
            else:
                print("render thread shutdown.")

    def redraw(self):
        row, col = self.state_shape
        self.surface.fill(self.item_back_color)
        self.surface.fill(
            self.back_color, (0, 0, self.state_length * row, self.state_length * col),
        )
        pygame.display.flip()

        self.draw_grid()

        for line in self.states:
            for state in line:
                if state.sprite:
                    state.draw(self.surface, self.back_color)

    def draw_grid(self):
        w, h = self.window_size
        for x in range(0, w, self.state_length):
            pygame.draw.line(self.surface, (0, 0, 0, 50), (x, 0), (x, h))
        for y in range(0, h, self.state_length):
            pygame.draw.line(self.surface, (0, 0, 0, 50), (0, y), (w, y))

    def setup_render(self, key_queue, hotkey_funcs, img_dict={}):
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
            for key, path in img_dict.items()
        }

        module = __import__("states", fromlist=[None])
        for class_name, _class in inspect.getmembers(module, inspect.isclass):
            class_name = class_name.lower()
            if class_name in self.sprites.keys():
                _class.sprite = self.sprites[class_name]

        State.policy_sprites = [
            self.sprites["up"],
            self.sprites["down"],
            self.sprites["left"],
            self.sprites["right"],
        ]

    def quit_callback(self):
        self.is_running = False
