#!/usr/bin/python3

from quiz_game import quiz_game
from menu import menu
from util import util


def main():
    util.init()
    menu.intro()
    menu.show_options()
    while True:
        chosen_option = menu.get_user_input()
        if chosen_option == "p":
            quiz_game.play()
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
