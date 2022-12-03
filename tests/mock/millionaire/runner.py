#!/usr/bin/python3

from menu import menu
from util import util


def main(menu_inputs: list, game_inputs: dict):
    util.init()
    menu.intro()
    for i in range(len(menu_inputs)):
        menu.handle_main_menu(menu_inputs[i], game_inputs)


if __name__ == "__main__":
    main()