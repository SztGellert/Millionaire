#!/usr/bin/python3

from quiz import quiz
from menu import menu


def main():
    menu.intro()
    menu.show_options()
    while True:
        chosen_option = menu.get_user_input()
        if chosen_option == "p":
            quiz.quiz()
            menu.show_options()
        if chosen_option == "h":
            menu.help()
            menu.show_options(1)
        if chosen_option == "c":
            menu.credits()
            menu.show_options(2)
        if chosen_option == "e":
            menu.exit()



if __name__ == "__main__":
    main()
