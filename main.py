from main_manager import MainManager
from state import *


if __name__ == "__main__":
    items = (State, Goal, Trap, Pusher)

    size = (10, 5)
    main_game = MainManager(size, items=items, is_render=True)
    main_game.run()
    main_game.shutdown()
