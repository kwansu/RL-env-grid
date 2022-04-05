from glob import glob
from os.path import basename, splitext
from main_manager import MainManager


if __name__ == "__main__":
    img_dict = {splitext(basename(x))[0]: x for x in glob("sprites/*.png")}

    size = (10, 7)
    main_game = MainManager(size, img_dict=img_dict)
    main_game.run()
    main_game.shutdown()
