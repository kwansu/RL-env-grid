import queue
import pygame

from states import *
from agent import Agent
from environment.grid_world import GridWorld


class MainManager:
    def __init__(self, grid_size=(6, 6), img_dict=None, items=[], is_render=True):
        key_funcs = [
            (f"K_{s[4:].upper()}", s) if len(s) > 5 else (f"K_{s[4:]}", s)
            for s in dir(self)
            if s[:4] == "put_"
        ]

        keys = dir(pygame)
        key_funcs = {
            getattr(pygame, k): getattr(self, v) for k, v in key_funcs if k in keys
        }
        key_funcs[pygame.BUTTON_LEFT] = self.put_mouse

        self.key_queue = queue.Queue() if is_render else None

        self.agent = Agent(grid_size)
        self.env = GridWorld(
            *grid_size,
            items=items,
            key_queue=self.key_queue,
            hotkey_funcs=key_funcs,
            img_dict=img_dict,
            is_render=is_render,
            # state_length=30,
        )

    def shutdown(self):
        self.env.shutdown()

    def put_mouse(self, pos):
        self.env.click_pos(pos)

    def put_a(self, key):
        self.env.reset()

    def put_space(self, key):
        State.render_value = True
        self.agent.evaluate_policy(self.env.states)
        self.env.draw_values(self.agent.state_values)

    def put_t(self, key):
        State.render_policy = True
        self.agent.imporve_policy(self.env.states)
        self.env.draw_policy(self.agent.policy)

    def put_r(self, key):
        self.agent.reset()
        self.env.reset()

    def run(self):
        if not self.env.is_render:
            return

        while self.env.is_running:
            self.key_put_procedure()

        self.shutdown()

    def key_put_procedure(self):
        while not self.key_queue.empty():
            func, arg = self.key_queue.get()
            func(arg)
