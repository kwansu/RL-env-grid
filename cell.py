import pygame


class Cell:
    def __init__(self, x, y, length):
        self.pos = (x, y)
        self.top_left = (x * length + 1, y * length + 1)
        self.type = None
        self.sprite = None

    def draw(self, surface):
        surface.blit(self.sprite, self.top_left)

    def redraw(self, surface, length, back_color):
        pygame.draw.rect(surface, back_color, self.top_left + (length, length))
        if self.sprite:
            surface.blit(self.sprite, self.top_left)


class State(Cell):
    def __init__(self, x, y, length):
        super().__init__(x, y, length)
        self.reward = -1

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
    def __init__(self, x, y, length, move, sprite):
        super().__init__(x, y, length)
        self.sprite = sprite
        self.move = move

    def step(self, action):
        x, y = self.pos
        x += self.move[0] * 100
        y += self.move[1] * 100
        return x, y


class PuserUp(Puser):
    def __init__(self, x, y, length, sprite=None):
        super().__init__(x, y, length, (0, -1), sprite)


class PuserDown(Puser):
    def __init__(self, x, y, length, sprite=None):
        super().__init__(x, y, length, (0, 1), sprite)


class PuserLeft(Puser):
    def __init__(self, x, y, length, sprite=None):
        super().__init__(x, y, length, (-1, 0), sprite)


class PuserRight(Puser):
    def __init__(self, x, y, length, sprite=None):
        super().__init__(x, y, length, (1, 0), sprite)
