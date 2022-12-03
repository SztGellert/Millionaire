#!/usr/bin/python3

from millionaire.quiz_game import quiz_game
from millionaire.menu import menu
from millionaire.util import util


def main():
    util.init()
    menu.intro()
    menu.handle_main_menu()


if __name__ == "__main__":
    main()
