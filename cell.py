import pygame


class Cell:
    l = 0.0

    def __init__(self, x, y):
        self.pos = (x, y)
        self.top_left = (x * self.l + 1, y * self.l + 1)
        self.type = None
        self.sprite = None
        self.back_color = None

    def draw(self, surface):
        surface.blit(self.sprite, self.top_left)

    def redraw(self, surface, back_color):
        pygame.draw.rect(surface, back_color, self.top_left + (self.l - 2, self.l - 2))
        if self.sprite:
            surface.blit(self.sprite, self.top_left)


class State(Cell):
    render_policy = False
    render_value = False
    policy_sprites = None

    def __init__(self, x, y):
        super().__init__(x, y)
        self.reward = -1
        self.value = None
        self.policy = [0.0] * 4

    def draw(self, surface, back_color):
        self.redraw(surface, back_color)
        if self.render_value:
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

    def step(self, action):
        x, y = self.pos
        if action == "up":
            y -= 1
        elif action == "down":
            y += 1
        elif action == "left":
            x -= 1
        else:
            x += 1
        return x, y


class Puser(State):
    def __init__(self, x, y, move, sprite):
        super().__init__(x, y)
        self.sprite = sprite
        self.move = move

    def step(self, action):
        x, y = self.pos
        x += self.move[0] * 100
        y += self.move[1] * 100
        return x, y


class PuserUp(Puser):
    def __init__(self, x, y, sprite=None):
        super().__init__(x, y, (0, -1), sprite)


class PuserDown(Puser):
    def __init__(self, x, y, sprite=None):
        super().__init__(x, y, (0, 1), sprite)


class PuserLeft(Puser):
    def __init__(self, x, y, sprite=None):
        super().__init__(x, y, (-1, 0), sprite)


class PuserRight(Puser):
    def __init__(self, x, y, sprite=None):
        super().__init__(x, y, (1, 0), sprite)
