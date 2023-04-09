#!/usr/bin/python3

from millionaire.menu import menu
from millionaire.util import util
from millionaire.quiz_game import quiz_game


def main():
    util.init()
 #   menu.intro()
#    menu.handle_main_menu()
    quiz_game.play()

if __name__ == "__main__":
    main()
