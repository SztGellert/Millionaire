import time
import os
import json
from util import util
from sty import Style, RgbFg, fg, bg
from quiz_game import quiz_game

default_width = 40
fg.purple = Style(RgbFg(148, 0, 211))
bg.orange = bg(255, 150, 50)
game_language = "en"
language_dictionary = util.language_dictionary



def intro():
    util.clear_screen()
    util.play_sound("loim_intro.wav", 0)
    time.sleep(2)
    file = (util.open_file("intro.txt", 'r'))
    for line_index in range(len(file)):
        if line_index == 3:
            print(fg.purple + file[line_index][0] + fg.rs)
            time.sleep(2)
        else:
            print(file[line_index][0])
        time.sleep(1)


def show_title():
    line_length = default_width + 3
    util.clear_screen()
    print("=" * line_length)
    print(fg.purple + language_dictionary[game_language].menu.title_first_line + fg.rs)
    print("=" * line_length)
    print(fg.yellow + "|" * line_length + fg.rs)
    print(fg.purple + language_dictionary[game_language].menu.title_second_line + fg.rs)
    print(fg.yellow + "|" * line_length + fg.rs)
    print("=" * line_length)
    print(fg.purple + language_dictionary[game_language].menu.title_first_line + fg.rs)
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
    return


def select_help():
    util.clear_screen()
    file = (util.open_file("tutorial_" + util.game_language + ".txt", 'r'))
    for line in file:
        print(line[0])
    return_prompt()


def select_credits():
    util.clear_screen()
    file = (util.open_file("credits_" + util.game_language + ".txt", 'r'))
    for line in file:
        print(line[0])
    return_prompt()


def return_prompt():
    print(fg.red + "\n" + language_dictionary[game_language].menu.return_prompt + fg.rs)
    if util.operating_system == "posix":
        import getch
        user_input = getch.getch()
    else:
        import msvcrt
        user_input = msvcrt.getch()
    # escape
    if user_input == b'\x1b':
        return


def get_user_input(option_list: [], max_option_length: int,  hotkey: str) -> str:
    i = 0
    first_char = ""
    if util.operating_system == "posix":
        import getch
        user_input = getch.getch()
    else:
        import msvcrt
        user_input = msvcrt.getch()
    while True:
        print(hotkey)
        if hotkey == "enter":
            first_char = b'\r'
        if hotkey == "esc":
            first_char = b'\x1b'
        if hotkey == "up":
            first_char = b'H'
        if hotkey == "down":
            first_char = b'P'
        # escape
        if first_char == b'\x1b':
            return option_list[-1]
        # enter
        if first_char == b'\r':
            return option_list[i]
        # up
        if first_char == b'H':
            if i == 0:
                i = len(option_list) - 1
                show_options(option_list, max_option_length, len(option_list) - 1)
            else:
                i -= 1
                show_options(option_list, max_option_length, i)
            # enter
            if user_input == b'\r':
                return option_list[i]
        # down
        if first_char == b'P':
            if i == len(option_list) - 1:
                i = 0
                show_options(option_list, max_option_length)
            else:
                i += 1
                show_options(option_list, max_option_length, i)
            # enter
            if user_input == b'\r':
                return option_list[i]


def select_settings():
    util.clear_screen()
    show_options(language_dictionary[game_language].menu.settings_menu_options, 40)
    while True:
        chosen_option = get_user_input(language_dictionary[game_language].menu.settings_menu_options, 40)
        if chosen_option == language_dictionary[game_language].menu.settings_menu_options[0]:
            show_options([language_dictionary[game_language].en, language_dictionary[game_language].hu], 20)
            langs = [language_dictionary[game_language].en, language_dictionary[game_language].hu]
            chosen_lang_option = get_user_input(langs, 20)
            util.init_language(util.available_languages[langs.index(chosen_lang_option)])
            show_options(language_dictionary[game_language].menu.settings_menu_options, 40)
        if chosen_option == language_dictionary[game_language].menu.settings_menu_options[-2]:
            show_options(language_dictionary[game_language].menu.settings_menu_question_topics, 20)
            chosen_question_topic = get_user_input(language_dictionary[game_language].menu.settings_menu_question_topics, 20)
            if chosen_question_topic != language_dictionary[game_language].menu.settings_menu_question_topics[0]:
                util.init_question_topics(chosen_question_topic)
            show_options(language_dictionary[game_language].menu.settings_menu_options, 40)
        if chosen_option == language_dictionary[game_language].menu.settings_menu_options[-1]:
            return


def handle_main_menu(input_: str, game_inputs: {}):
    options_length = default_width
    show_options(language_dictionary[game_language].menu.main_menu_options, options_length)
    while True:
        chosen_option = get_user_input(language_dictionary[game_language].menu.main_menu_options, options_length, input_)
        if chosen_option == language_dictionary[game_language].menu.main_menu_options[0]:
            quiz_game.play(game_inputs)
            show_options(language_dictionary[game_language].menu.main_menu_options, options_length)
        if chosen_option == language_dictionary[game_language].menu.main_menu_options[1]:
            select_help()
            show_options(language_dictionary[game_language].menu.main_menu_options, options_length, 1)
        if chosen_option == language_dictionary[game_language].menu.main_menu_options[2]:
            select_settings()
            show_options(language_dictionary[game_language].menu.main_menu_options, options_length, 2)
        if chosen_option == language_dictionary[game_language].menu.main_menu_options[3]:
            select_credits()
            show_options(language_dictionary[game_language].menu.main_menu_options, options_length, 3)
        if chosen_option == language_dictionary[game_language].menu.main_menu_options[4]:
            select_scores()
            show_options(language_dictionary[game_language].menu.main_menu_options, options_length, 4)
        if chosen_option == language_dictionary[game_language].menu.main_menu_options[4]:
            select_exit()


def select_scores():
    util.clear_screen()
    if os.path.isfile("scores.json"):
        f = open("scores.json")
        data = json.load(f)
        scores_sorted = sorted(data, key=lambda d: d['score'], reverse=True)
        print("-" * 100)
        for item in scores_sorted:
            i = 0
            for k, v in item.items():
                print(language_dictionary[game_language].menu.scores[i], ":", v, end=" ")
                i += 1
            print("\n")
            print("-" * 100)
        f.close()
    else:
        print(language_dictionary[game_language].menu.empty_scores)
    return_prompt()
