import os
import cv2
import time
import pygame
import inspect
import threading
import numpy as np

from abc import *
from glob import glob
from os.path import basename, splitext

from state import *
from environment.render_process import *


class BaseEnvironment(ABC):
    @abstractmethod
    def reset(self):
        pass

    def __init__(
        self,
        row,
        col,
        key_queue=None,
        hotkey_funcs={},
        is_render=False,
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

        self.surface = None
        self.back_color = back_color
        self.item_back_color = item_back_color
        self.selected_back_color = selected_back_color

        sprite_path = os.path.dirname(os.path.abspath(__file__)) + "/sprite/*.png"
        img_dict = {splitext(basename(x))[0]: x for x in glob(sprite_path)}
        assert img_dict, sprite_path

        self.setup_render(img_dict, key_queue=key_queue, hotkey_funcs=hotkey_funcs)
        self._redraw()

    def shutdown(self):
        if self.is_running:
            try:
                quit_pygame()
                if self.render_thread:
                    self.render_thread.join(timeout=10)
            except Exception as e:
                print(e)
            else:
                print("render thread shutdown.")

    def get_image(self):
        view = pygame.surfarray.array3d(self.surface)
        view = view.transpose([1, 0, 2])
        img_bgr = cv2.cvtColor(view, cv2.COLOR_RGB2BGR)
        return img_bgr

    def _redraw(self):
        row, col = self.state_shape
        self.surface.fill(self.item_back_color)
        self.surface.fill(
            self.back_color, (0, 0, self.state_length * row, self.state_length * col),
        )
        pygame.display.flip()

        self._draw_grid()

        for line in self.states:
            for state in line:
                state.draw(self.surface, self.back_color)

    def _draw_grid(self):
        w, h = self.window_size
        for x in range(0, w, self.state_length):
            pygame.draw.line(self.surface, (0, 0, 0, 50), (x, 0), (x, h))
        for y in range(0, h, self.state_length):
            pygame.draw.line(self.surface, (0, 0, 0, 50), (0, y), (w, y))

    def setup_render(self, img_dict={}, key_queue=None, hotkey_funcs={}):
        pygame.font.init()
        self.font = pygame.font.SysFont("consolas", int(self.state_length * 0.18), True)

        if key_queue and hotkey_funcs:
            self.render_thread = threading.Thread(
                target=render_process, args=(self, key_queue, hotkey_funcs)
            )
            self.render_thread.start()
        else:
            pygame.init()
            self.surface = pygame.display.set_mode(self.window_size)

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

        module = __import__("state", fromlist=[None])
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
