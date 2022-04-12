import pygame
from random import random


class Cell:
    l = 0.0
    max_x, max_y = 0, 0
    sprite = None

    def __init__(self, x, y):
        self.pos = (x, y)
        self.top_left = (x * self.l + 1, y * self.l + 1)
        self.back_color = None

    def draw(self, surface):
        surface.blit(self.sprite, self.top_left)

    def redraw(self, surface, back_color):
        pygame.draw.rect(surface, back_color, self.top_left + (self.l - 2, self.l - 2))
        if self.sprite:
            surface.blit(self.sprite, self.top_left)

    @staticmethod
    def fix_pos(x, y):
        return max(min(x, Cell.max_x), 0), max(min(y, Cell.max_y), 0)


class State(Cell):
    render_policy = False
    render_value = False
    policy_sprites = None

    def __init__(self, x, y, is_terminal=False):
        super().__init__(x, y)
        self.is_terminal = is_terminal
        self.reward = -1
        self.value = None
        self.policy = [0.0] * 4
        self.text_top_left = None

    def copy_info(self, state):
        self.pos = state.pos
        self.top_left = state.top_left

    def draw(self, surface, back_color):
        self.redraw(surface, back_color)
        if not self.is_terminal:
            if self.render_value and self.text_top_left:
                surface.blit(self.value, self.text_top_left)
            if self.render_policy:
                for sprite, p in zip(self.policy_sprites, self.policy):
                    sprite.set_alpha(p * 255)
                    surface.blit(sprite, self.top_left)

    def set_value(self, text, font, color=(0, 0, 255)):
        self.value = font.render(text, True, color)
        w, h = self.value.get_size()
        x = (self.l - w) // 2 + self.pos[0] * self.l
        y = (self.l - h) // 2 + self.pos[1] * self.l
        self.text_top_left = (x, y)

    def set_policy(self, policy):
        self.policy = policy.copy()

    def get_action_trans_prob(self, action):
        x, y = self.pos
        if action == "up":
            y -= 1
        elif action == "down":
            y += 1
        elif action == "left":
            x -= 1
        else:
            x += 1
        return {self.fix_pos(x, y): 1.0}


class Goal(State):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_terminal = True
        self.reward = 20


class Trap(State):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_terminal = True
        self.reward = -20


class Pusher(State):
    def get_action_trans_prob(self, action):
        x, y = self.pos
        if action == "up":
            y = 0
        elif action == "down":
            y = self.max_y
        elif action == "left":
            x = 0
        else:
            x = self.max_x
        return {(x, y): 1.0}


class Swamp(State):
    def get_action_trans_prob(self, action):
        x, y = self.pos
        p1 = x + 1, y
        p2 = x - 1, y
        p3 = x, y + 1
        p4 = x, y - 1

        return {
            self.fix_pos(*p1): 0.25,
            self.fix_pos(*p2): 0.25,
            self.fix_pos(*p3): 0.25,
            self.fix_pos(*p4): 0.25,
        }
