from main_manager import MainManager
from state import *


if __name__ == "__main__":
    items = (State, Goal, Trap, Pusher, Swamp)

    size = (10, 5)
    main_game = MainManager(size, items=items, enable_multi_thread=False)
    main_game.run()
    main_game.shutdown()
