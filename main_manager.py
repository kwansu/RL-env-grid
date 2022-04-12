import time
import queue
import pygame

from state import *
from agent import Agent
from environment.grid_world import GridWorld


class MainManager:
    def __init__(self, grid_size=(6, 6), enable_multi_thread=False, **kwargs):
        self.enable_multi_thread = enable_multi_thread
        if enable_multi_thread:
            self.key_queue = queue.Queue()
            kwargs["key_queue"] = self.key_queue
            kwargs["hotkey_funcs"] = self.get_hotkey()

        self.agent = Agent(grid_size)
        self.env = GridWorld(*grid_size, **kwargs)

    def shutdown(self):
        self.env.shutdown()

    def put_mouse(self, pos):
        self.env.click_pos(pos)

    def put_a(self, key):
        State.render_policy = not State.render_policy
        self.env.redraw()

    def put_s(self, key):
        State.render_value = not State.render_value
        self.env.redraw()

    def put_space(self, key):
        self.agent.evaluate_policy(self.env.states)
        self.env.draw_values(self.agent.state_values)

    def put_t(self, key):
        self.agent.imporve_policy(self.env.states)
        self.env.draw_policy(self.agent.policy)

    def put_r(self, key):
        self.agent.reset()
        self.env.reset()

    def put_up(self, key):
        self.env.step("up")

    def put_down(self, key):
        self.env.step("down")

    def put_left(self, key):
        self.env.step("left")

    def put_right(self, key):
        self.env.step("right")
        
    def put_h(self, key):
        self.env.enable_agent_render = not self.env.enable_agent_render
        self.env.draw_agent()

    def get_hotkey(self):
        hotkey_dict = [
            (f"K_{s[4:].upper()}", s) if len(s) > 5 else (f"K_{s[4:]}", s)
            for s in dir(self)
            if s[:4] == "put_"
        ]

        keys = dir(pygame)
        hotkey_dict = {
            getattr(pygame, k): getattr(self, v) for k, v in hotkey_dict if k in keys
        }
        hotkey_dict[pygame.BUTTON_LEFT] = self.put_mouse
        return hotkey_dict

    def key_put_procedure(self):
        while not self.key_queue.empty():
            func, arg = self.key_queue.get()
            func(arg)

    def run(self):
        if self.enable_multi_thread:
            while self.env.is_running:
                self.key_put_procedure()
        else:
            self.render_process()
            
        self.shutdown()
    
    def render_process(self):
        is_running = True
        hotkey_dict = self.get_hotkey()

        try:
            while is_running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print("running = False")
                        is_running = False
                        self.env.quit_callback()

                    if event.type == pygame.KEYDOWN:
                        if event.key in hotkey_dict.keys():
                            hotkey_dict[event.key](event.key)

                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button in hotkey_dict.keys():
                            hotkey_dict[event.button](event.pos)

                pygame.display.update()
                time.sleep(0.01)
        finally:
            pygame.quit()
