import time
import pygame


def render_process(env, key_queue, hotkey_dict={}):
    is_running = True

    pygame.init()
    env.surface = pygame.display.set_mode(env.window_size)
    print(*env.state_shape)

    if not key_queue:
        return

    try:
        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("running = False")
                    is_running = False
                    env._quit_callback()

                if event.type == pygame.KEYDOWN:
                    if event.key in hotkey_dict.keys():
                        key_queue.put((hotkey_dict[event.key], event.key))

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button in hotkey_dict.keys():
                        key_queue.put((hotkey_dict[event.button], event.pos))

            pygame.display.update()
            time.sleep(0.01)
    finally:
        pygame.quit()


def quit_pygame():
    quit_event = pygame.event.Event(pygame.QUIT)
    pygame.event.post(quit_event)
