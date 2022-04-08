from glob import glob
from os.path import basename, splitext
from main_manager import MainManager
from state import *


if __name__ == "__main__":
    img_dict = {splitext(basename(x))[0]: x for x in glob("sprites/*.png")}
    items = (State, Goal, Trap, Pusher)

    size = (10, 5)
    main_game = MainManager(size, img_dict=img_dict, items=items)
    main_game.run()
    main_game.shutdown()
