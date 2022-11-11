#!/usr/bin/python3

from quiz_game import quiz_game
from menu import menu
from util import util


def main():
    util.init()
    #menu.intro()
    menu.handle_main_menu()


if __name__ == "__main__":
    main()
