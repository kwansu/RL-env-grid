from main_manager import MainManager


if __name__ == "__main__":
    object_infos = {
        "player": "sprites/player.png",
        "goal": "sprites/goal.png",
        "up": "sprites/arrow_up.png",
        "down": "sprites/arrow_down.png",
        "left": "sprites/arrow_left.png",
        "right": "sprites/arrow_right.png",
        "left_item": "sprites/left_item.png",
        "right_item": "sprites/right_item.png",
    }

    main_game = MainManager(object_infos=object_infos)
    main_game.run()
    main_game.shutdown()
