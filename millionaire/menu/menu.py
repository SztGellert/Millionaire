import random
import sys
import time
import keyboard
from util import util
from sty import Style, RgbFg, fg, bg

from quiz_game import quiz_game

main_menu_options = ["Play", "Help", "Settings", "Credit", "Exit"]
fg.purple = Style(RgbFg(148, 0, 211))
bg.orange = bg(255, 150, 50)
game_language = "en"
language_dictionary = util.language_dictionary
settings_menu_options = ["Language selection",
                         "Sound Volume selection",
                         "Default colour theme selection",
                         "Display size",
                         "Question types",
                         "Back"
                         ]


def intro():
    util.clear_screen()
    util.play_sound("loim_intro.wav", 0)
    time.sleep(2)
    file = (util.open_file("intro_" + game_language + ".txt", 'r'))
    for line_index in range(len(file)):
        if line_index == 3:
            print(fg.purple + file[line_index][0] + fg.rs)
            time.sleep(2)
        else:
            print(file[line_index][0])
        time.sleep(1)


def show_title():
    line_length = 43
    util.clear_screen()
    print("=" * line_length)
    print(fg.purple + " ♦ WHO WANTS TO BE A ♦" + fg.rs)
    print("=" * line_length)
    print(fg.yellow + "|" * line_length + fg.rs)
    print(fg.purple + " M I L L I O N A I R E" + fg.rs)
    print(fg.yellow + "|" * line_length + fg.rs)
    print("=" * line_length)
    print(fg.purple + " ♦ WHO WANTS TO BE A ♦" + fg.rs)
    print("=" * line_length + "\n\n")


def show_options(options: list, max_options_length: int, chosen_option=0):
    show_title()
    fore_string = "| "
    after_string = " |"
    line_length = max_options_length
    option_length = max_options_length
    for i in range(len(options)):
        option = options[i]
        number_of_spaces = int((option_length - len(options[i]) - len(fore_string) - len(after_string)) / 2)
        print("  " + "-" * line_length)
        if i == chosen_option:
            string_to_print = "  " + fore_string + bg.orange + number_of_spaces * " " + fg.black + option + fg.rs + number_of_spaces * " " + bg.rs + after_string
        else:
            string_to_print = "  " + fore_string + number_of_spaces * " " + option + number_of_spaces * " " + after_string
        print(string_to_print)
    print("  " + "-" * line_length + "\n")


def select_exit():
    sys.exit(0)


def select_help():
    util.clear_screen()
    file = (util.open_file("tutorial" + util.game_language + ".txt", 'r'))
    for line in file:
        print(line[0])
    return_prompt()


def select_credits():
    util.clear_screen()
    file = (util.open_file("credits_" + util.game_language + ".txt", 'r'))
    for line in file:
        print(line[0])
    return_prompt()


def select_settings():
    util.clear_screen()
    show_options(settings_menu_options, 40)
    while True:
        chosen_option = get_user_input(settings_menu_options, 40)
        if chosen_option == "Language selection":
            show_options(util.available_languages, 20)
            chosen_lang_option = get_user_input(util.available_languages, 20)
            lang_ = ""
            if chosen_lang_option == util.available_languages[0]:
                lang_ = util.available_languages[0]
            if chosen_lang_option == util.available_languages[1]:
                lang_ = util.available_languages[1]
            util.init_language(lang_)
            if chosen_lang_option:
                show_options(settings_menu_options, 40)
        if chosen_option == "Back":
            return


def return_prompt():
    print(fg.red + "\n" + language_dictionary[game_language].menu.return_prompt + fg.rs)
    if keyboard.read_key() == "enter":
        return


def get_user_input(option_list: [], max_option_length: int) -> str:
    i = 0
    while True:
        if keyboard.read_key() == "enter":
            return option_list[i]
        if keyboard.read_key() == 'down':
            if i == len(option_list) - 1:
                i = 0
                show_options(option_list, max_option_length)
            else:
                i += 1
                show_options(option_list, max_option_length, i)
            if keyboard.read_key() == "enter":
                return option_list[i]
        if keyboard.read_key() == 'up':
            if i == 0:
                i = len(option_list) - 1
                show_options(option_list, max_option_length, len(option_list) - 1)
            else:
                i -= 1
                show_options(option_list, max_option_length, i)
            if keyboard.read_key() == "enter":
                return option_list[i]


def handle_main_menu():
    options_length = 40
    show_options(main_menu_options, options_length)
    while True:
        chosen_option = get_user_input(main_menu_options, options_length)
        if chosen_option == "Play":
            quiz_game.play()
            show_options(main_menu_options, options_length)
        if chosen_option == "Help":
            select_help()
            show_options(main_menu_options, options_length, 1)
        if chosen_option == "Settings":
            select_settings()
            show_options(main_menu_options, options_length, 2)
        if chosen_option == "Credit":
            select_credits()
            show_options(main_menu_options, options_length, 3)
        if chosen_option == "Exit":
            select_exit()
