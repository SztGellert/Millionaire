#!/usr/bin/python3
from tests.mock.millionaire.menu import menu
from tests.mock.millionaire.util import util

def main(menu_inputs: list, game_inputs: dict):
    util.init()
    menu.intro()
    menu.handle_main_menu(menu_inputs, game_inputs)


if __name__ == "__main__":
    main([], {})