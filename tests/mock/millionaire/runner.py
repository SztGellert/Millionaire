#!/usr/bin/python3
import os, sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../millionaire')
from quiz_game import quiz_game
from menu import menu
from util import util


def main(menu_inputs: list, game_inputs: dict):
    util.init()
    menu.intro()
    menu.show_options()
    while menu_inputs:
        chosen_option = menu_inputs[0]
        if chosen_option == "p":
            quiz_game.play(game_inputs)
            menu.show_options()
        if chosen_option == "h":
            menu.select_help()
            menu.show_options(1)
        if chosen_option == "c":
            menu.select_credits()
            menu.show_options(2)
        if chosen_option == "e":
            menu.select_exit()


if __name__ == "__main__":
    main()
