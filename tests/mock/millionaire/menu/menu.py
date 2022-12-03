# pylint: disable=<warning>


import time
import os
import json
from millionaire.util import util
from sty import Style, RgbFg, fg, bg
from millionaire.quiz_game.quiz_game import quiz_game
import keyboard

fg.purple = Style(RgbFg(148, 0, 211))
bg.orange = bg(255, 150, 50)
language_dictionary = util.language_dictionary
default_width = 40


def intro():
    util.clear_screen()
    if util.game_language == util.Language.HUNGARIAN.name:
        util.play_sound("intro.mp3", 0, volume=1)
    else:
        util.play_sound("intro.wav", 0)
    time.sleep(2)
    file = (util.open_file("intro_" + util.game_language, 'r'))
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
    print(fg.purple + language_dictionary[util.game_language].menu.title_first_line + fg.rs)
    print("=" * line_length)
    print(fg.yellow + "|" * line_length + fg.rs)
    print(fg.purple + language_dictionary[util.game_language].menu.title_second_line + fg.rs)
    print(fg.yellow + "|" * line_length + fg.rs)
    print("=" * line_length)
    print(fg.purple + language_dictionary[util.game_language].menu.title_first_line + fg.rs)
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
        if len(option) % 2 != 0:
            option = option + " "
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
    file = (util.open_file("credits_" + util.game_language, 'r'))
    for line in file:
        print(line[0])
    return_prompt()


def return_prompt():
    print(fg.red + "\n" + language_dictionary[util.game_language].menu.return_prompt + fg.rs)
    if util.operating_system == "posix":
        import getch
        user_input = getch.getch()
    else:
        import msvcrt
        user_input = msvcrt.getch()
    # escape
    if user_input == b'\x1b':
        return


def get_user_input(option_list: [], values_list: [], max_option_length: int, hotkey: str, start_index = 0, esc=True) -> str:
    i = start_index
    match hotkey:
        case "enter":
            user_input = b'\r'
        case "esc":
            user_input = b'\x1b'
        case "up":
            user_input = b'\x1b'
        case "down":
            user_input = b'\x1b'
        case default:
            user_input = b'\r'
    first_char = user_input
    # escape
    if first_char == b'\x1b':
        if esc == True:
            return values_list[-1]
        else:
            return values_list[start_index]    # enter
    if first_char == b'\r':
        return values_list[i]
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
            return values_list[i]
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
            return values_list[i]


def select_settings():
    start_index = 0
    util.clear_screen()
    show_options(language_dictionary[util.game_language].menu.settings_menu_options, default_width)
    while True:
        chosen_option = get_user_input(language_dictionary[util.game_language].menu.settings_menu_options, language_dictionary[util.game_language].menu.settings_menu_options, default_width, start_index)
        if chosen_option == language_dictionary[util.game_language].menu.settings_menu_options[0]:
            langs = [language_dictionary[util.game_language].en, language_dictionary[util.game_language].hu]
            show_options(langs, 20, util.available_languages.index(util.game_language))
            chosen_lang_option = get_user_input(langs, util.available_languages, 20, util.available_languages.index(util.game_language), False)
            util.set_game_language(util.available_languages[util.available_languages.index(chosen_lang_option)])
            show_options(language_dictionary[util.game_language].menu.settings_menu_options, 40)
            start_index = 0
        elif chosen_option == language_dictionary[util.game_language].menu.settings_menu_options[1]:
            if util.system_volume:
                util.system_volume = False
            else:
                util.system_volume = True
            show_options(language_dictionary[util.game_language].menu.settings_menu_options, default_width, chosen_option=1)
            start_index = 1
        elif chosen_option == language_dictionary[util.game_language].menu.settings_menu_options[2]:
            keyboard.press('f11')
            start_index = 2
        elif chosen_option == language_dictionary[util.game_language].menu.settings_menu_options[3]:
            show_options(language_dictionary[util.game_language].menu.settings_menu_question_topics, default_width,  util.topics.index(util.question_topics))
            chosen_question_topic = get_user_input(language_dictionary[util.game_language].menu.settings_menu_question_topics, util.topics, default_width, util.topics.index(util.question_topics), False)
            util.set_question_topics(chosen_question_topic)
            show_options(language_dictionary[util.game_language].menu.settings_menu_options, 40, chosen_option=3)
            start_index = 3
        elif chosen_option == language_dictionary[util.game_language].menu.settings_menu_options[4]:
            if util.question_difficulty != util.Difficulty.ALL.name:
                show_options(language_dictionary[util.game_language].menu.question_difficulty_levels, 20, util.difficulty_levels.index(util.question_difficulty))
                chosen_difficulty_option = get_user_input(language_dictionary[util.game_language].menu.question_difficulty_levels, util.difficulty_levels, 20, util.difficulty_levels.index(util.question_difficulty), False)
            else:
                show_options(language_dictionary[util.game_language].menu.question_difficulty_levels, 20)
                chosen_difficulty_option = get_user_input(language_dictionary[util.game_language].menu.question_difficulty_levels, util.difficulty_levels, 20, 0, False)
            if chosen_difficulty_option != language_dictionary[util.game_language].menu.question_difficulty_levels[0]:
                util.set_question_difficulty(chosen_difficulty_option)
            else:
                util.set_question_difficulty(util.Difficulty.ALL.name)
            show_options(language_dictionary[util.game_language].menu.settings_menu_options, 40, chosen_option=4)
            start_index = 4
        elif chosen_option == language_dictionary[util.game_language].menu.settings_menu_options[5]:
            util.init_settings(util.Language.ENGLISH.name, reset_settings=True)
            start_index = 5
        else:
            update_settings_file()
            return


def handle_main_menu():
    start_index = 0
    options_length = default_width
    show_options(language_dictionary[util.game_language].menu.main_menu_options, options_length)
    while True:
        chosen_option = get_user_input(language_dictionary[util.game_language].menu.main_menu_options, language_dictionary[util.game_language].menu.main_menu_options, options_length, start_index)
        if chosen_option == language_dictionary[util.game_language].menu.main_menu_options[0]:
            quiz_game.play()
            show_options(language_dictionary[util.game_language].menu.main_menu_options, options_length)
            start_index = 0
        if chosen_option == language_dictionary[util.game_language].menu.main_menu_options[1]:
            select_help()
            show_options(language_dictionary[util.game_language].menu.main_menu_options, options_length, chosen_option=1)
            start_index = 1
        if chosen_option == language_dictionary[util.game_language].menu.main_menu_options[2]:
            select_settings()
            show_options(language_dictionary[util.game_language].menu.main_menu_options, options_length, chosen_option=2)
            start_index = 2
        if chosen_option == language_dictionary[util.game_language].menu.main_menu_options[3]:
            select_credits()
            show_options(language_dictionary[util.game_language].menu.main_menu_options, options_length, chosen_option=3)
            start_index = 3
        if chosen_option == language_dictionary[util.game_language].menu.main_menu_options[4]:
            select_scores()
            show_options(language_dictionary[util.game_language].menu.main_menu_options, options_length, chosen_option=4)
            start_index = 4
        if chosen_option == language_dictionary[util.game_language].menu.main_menu_options[5]:
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
                if i == 1:
                    print(language_dictionary[util.game_language].menu.scores[i], ":", language_dictionary[util.game_language].menu.settings_menu_question_topics[v], end=" ")
                else:
                    print(language_dictionary[util.game_language].menu.scores[i], ":", v, end=" ")
                i += 1
            print("\n")
            print("-" * 100)
        f.close()
    else:
        print(language_dictionary[util.game_language].menu.empty_scores)
    return_prompt()


def update_settings_file():
    filename = "settings.json"
    content = {"language": util.game_language, "topic": util.question_topics, "difficulty": util.question_difficulty, "volume": util.system_volume}
    with open(filename, "w", encoding="UTF-8") as outfile:
        json.dump(content, outfile)
