import msvcrt
import os
import sys
import time
import json
import keyboard
from sty import Style, RgbFg, fg, bg, rs
import millionaire.quiz_game.quiz_game as quiz
import millionaire.util.util as util
import millionaire.menu.helpers as helpers
import pygame

fg.purple = Style(RgbFg(148, 0, 211))
bg.orange = bg(255, 150, 50)
language_dictionary = util.language_dictionary
default_width = 40
screen_distance = 60
bg.dark_blue = bg(0, 0, 155)
bg.darkest_blue = bg(42, 45, 112)


def intro():
    if util.game_language == util.Language.HUNGARIAN.name:
        util.play_sound("intro", 0, dir="intro", volume=1)

    else:
        util.play_sound("intro", 0)

    bg.light_blue = bg(96, 180, 225)
    bg.deep_purple = bg(30, 0, 60)
    bg.blue = bg.darkest_blue

    text_count = 0

    first_text = language_dictionary[util.game_language].menu.side_title_first_part
    second_text = language_dictionary[util.game_language].menu.side_title_second_part
    millionaire_lines = language_dictionary[util.game_language].menu.millionaire_lines

    pixels_in_line = 0
    pixels_per_line = []

    diameter = 40

    # You must account for the loops being zero-based, but the quotient of the diameter / 2 being
    # one-based. If you use the exact radius, you will be short one column and one row.
    offset_radius = (diameter / 2) - 0.5
    util.clear_screen()

    points = list([] for sd in range(diameter))
    util.clear_screen()
    for i in range(diameter):
        for j in range(diameter):

            x = i - offset_radius
            y = j - offset_radius

            if x * x + y * y <= offset_radius * offset_radius + 1:
                line = 'X'
                end = '..'
                pixels_in_line += 1
            else:
                line = ' '
                end = '  '
            points[j].append(line + end)
        pixels_per_line.append(pixels_in_line)
        pixels_in_line = 0

    for point in range(len(points)):

        current_line = "".join(points[point])
        line = "".join(points[point])
        first_index = line.find("X")
        last_index = line.rfind(".")

        line2 = line[
                :first_index] + bg.light_blue + " " + bg.rs + bg.deep_purple + "       " + bg.rs + bg.white + " " + bg.blue + " " + bg.rs + bg.light_blue + "  " + bg.rs + line[
                                                                                                                                                                           first_index:last_index] + bg.light_blue + " " + bg.rs + bg.blue + " " + bg.rs + bg.white + " " + bg.rs + bg.deep_purple + "       " + bg.rs + bg.light_blue + "  " + bg.rs + bg.rs + line[
                                                                                                                                                                                                                                                                                                                                                                last_index:]

        color = bg.blue
        if point < 12:
            if point == 8:
                line2 = line[:first_index] + bg.light_blue + " " + bg.rs + bg.deep_purple + "   " + first_text[
                    -point] + "   " + bg.rs + bg.white + " " + bg.blue + " " + bg.rs + bg.light_blue + "  " + bg.rs + line[
                                                                                                                      first_index:last_index] + bg.blue + "    " + bg.rs + bg.light_blue + " " + bg.rs + bg.blue + " " + bg.rs + bg.white + " " + bg.rs + bg.deep_purple + "  " + \
                        second_text[point] + "    " + bg.rs + bg.light_blue + "  " + bg.rs + bg.rs + line[
                                                                                                     last_index:]
            elif point == 9:
                line2 = line[:first_index] + bg.light_blue + " " + bg.rs + bg.deep_purple + " " + first_text[
                    -point] + "   " + bg.rs + bg.white + " " + bg.blue + " " + bg.rs + bg.light_blue + "  " + bg.rs + line[
                                                                                                                      first_index:last_index] + bg.blue + "      " + bg.rs + bg.light_blue + " " + bg.rs + bg.blue + " " + bg.rs + bg.white + " " + bg.rs + bg.deep_purple + "  " + \
                        second_text[point] + "    " + bg.rs + bg.light_blue + "  " + bg.rs + bg.rs + line[
                                                                                                     last_index:]
            elif point == 11:
                line2 = line[:first_index] + bg.light_blue + " " + bg.rs + bg.deep_purple + "   " + first_text[
                    -point] + "   " + bg.rs + bg.white + " " + bg.blue + " " + bg.rs + bg.light_blue + "  " + bg.rs + line[
                                                                                                                      first_index:last_index] + bg.light_blue + " " + bg.rs + bg.blue + " " + bg.rs + bg.white + " " + bg.rs + bg.deep_purple + "  " + \
                        second_text[point] + "    " + bg.rs + bg.light_blue + "  " + bg.rs + bg.rs + line[
                                                                                                     last_index:]
            else:
                line2 = line[:first_index] + bg.light_blue + " " + bg.rs + bg.deep_purple + "   " + first_text[
                    -point] + "   " + bg.rs + bg.white + " " + bg.blue + " " + bg.rs + bg.light_blue + "  " + bg.rs + line[
                                                                                                                      first_index:last_index] + bg.blue + "   " + bg.rs + bg.light_blue + " " + bg.rs + bg.blue + " " + bg.rs + bg.white + " " + bg.rs + bg.deep_purple + "   " + \
                        second_text[point] + "   " + bg.rs + bg.light_blue + "  " + bg.rs + bg.rs + line[last_index:]
        if point == 15:
            millionaire_lines[0] = millionaire_lines[0].replace(" ", color + " " + bg.rs)
            line2 = line2[:115] + bg.rs + line2[115:125] + bg.rs + millionaire_lines[0] + line2[205:]
        if point == 16:
            millionaire_lines[1] = millionaire_lines[1].replace(" ", color + " " + bg.rs)
            line2 = line2[:115] + bg.rs + line2[115:125] + bg.rs + millionaire_lines[1] + line2[205:]
        if point == 17:
            millionaire_lines[2] = millionaire_lines[2].replace(" ", color + " " + bg.rs)
            line2 = line2[:115] + bg.rs + line2[115:125] + bg.rs + millionaire_lines[2] + line2[205:]
        if point == 18:
            millionaire_lines[3] = millionaire_lines[3].replace(" ", color + " " + bg.rs)
            line2 = line2[:115] + bg.rs + line2[115:125] + bg.rs + millionaire_lines[3] + line2[205:]
        if point == 19:
            millionaire_lines[4] = millionaire_lines[4].replace(" ", color + " " + bg.rs)
            line2 = line2[:115] + bg.rs + line2[115:125] + bg.rs + millionaire_lines[4] + line2[205:]
        if point == 20:
            millionaire_lines[5] = millionaire_lines[5].replace(" ", color + " " + bg.rs)
            line2 = line2[:115] + bg.rs + line2[115:125] + bg.rs + millionaire_lines[5] + line2[205:]
        if point == 21:
            millionaire_lines[6] = millionaire_lines[6].replace(" ", color + " " + bg.rs)
            line2 = line2[:115] + bg.rs + line2[115:125] + bg.rs + millionaire_lines[6] + line2[205:]
        if point == 22:
            millionaire_lines[7] = millionaire_lines[7].replace(" ", color + " " + bg.rs)
            line2 = line2[:115] + bg.rs + line2[115:125] + bg.rs + millionaire_lines[7] + line2[205:]
        if point == 23:
            millionaire_lines[8] = millionaire_lines[8].replace(" ", color + " " + bg.rs)
            line2 = line2[:115] + bg.rs + line2[115:125] + bg.rs + millionaire_lines[8] + line2[205:]
        if point == 24:
            millionaire_lines[9] = millionaire_lines[9].replace(" ", color + " " + bg.rs)
            line2 = line2[:115] + bg.rs + line2[115:125] + bg.rs + millionaire_lines[9] + line2[205:]
        if point == 25:
            millionaire_lines[10] = millionaire_lines[10].replace(" ", color + " " + bg.rs)
            line2 = line2[:115] + bg.rs + line2[115:125] + bg.rs + millionaire_lines[10] + line2[205:]
        if point > 25 and point < 37:
            if point == 30:
                line2 = line[:first_index] + bg.light_blue + " " + bg.rs + bg.deep_purple + "  " + first_text[
                    text_count] + " " + bg.rs + bg.white + " " + bg.blue + " " + bg.rs + bg.light_blue + "  " + bg.rs + line[
                                                                                                                        first_index:last_index] + bg.blue + "    " + bg.rs + bg.light_blue + " " + bg.rs + bg.blue + " " + bg.rs + bg.white + " " + bg.rs + bg.deep_purple + "   " + \
                        second_text[-text_count] + "     " + bg.rs + bg.light_blue + "  " + bg.rs + bg.rs + line[
                                                                                                            last_index:]
            elif point == 31:
                line2 = line[:first_index] + bg.light_blue + " " + bg.rs + bg.deep_purple + "    " + first_text[
                    text_count] + " " + bg.rs + bg.white + " " + bg.blue + " " + bg.rs + bg.light_blue + "  " + bg.rs + line[
                                                                                                                        first_index:last_index] + bg.blue + "" + bg.rs + bg.light_blue + " " + bg.rs + bg.blue + " " + bg.rs + bg.white + " " + bg.rs + bg.deep_purple + "   " + \
                        second_text[-text_count] + "     " + bg.rs + bg.light_blue + "  " + bg.rs + bg.rs + line[
                                                                                                            last_index:]
            else:
                line2 = line[:first_index] + bg.light_blue + " " + bg.rs + bg.deep_purple + "   " + first_text[
                    text_count] + "   " + bg.rs + bg.white + " " + bg.blue + " " + bg.rs + bg.light_blue + "  " + bg.rs + line[
                                                                                                                          first_index:last_index] + bg.blue + " " + bg.rs + bg.light_blue + " " + bg.rs + bg.blue + " " + bg.rs + bg.white + " " + bg.rs + bg.deep_purple + "   " + \
                        second_text[-text_count] + "   " + bg.rs + bg.light_blue + "  " + bg.rs + bg.rs + line[
                                                                                                          last_index:]
            text_count += 1
        line2 = line2.replace("X", bg.blue + " " + bg.rs)
        line2 = line2.replace(".", bg.blue + " " + bg.rs)
        line2 = line2.replace("X", bg.black + " " + bg.rs)
        line2 = line2.replace("|", bg.white + " " + bg.rs)

        line3 = "".join(line2)

        print(line3)

    timeout = 15
    start_time = time.time()
    inp = None

    print(screen_distance * "   " + language_dictionary[util.game_language].menu.skip_prompt)
    while True:
        # TODO: only works on win
        if msvcrt.kbhit():
            inp = msvcrt.getch()
            break
        elif time.time() - start_time > timeout:
            break

    if inp:
        util.stop_sound()
        return
    else:
        return


def user_pressed_space():
    if util.operating_system == "posix":
        user_input = helpers.return_user_input_linux()
    else:
        user_input = helpers.return_user_input_windows()
    if user_input not in [b' ', '<SPACE>']:
        return

    util.stop_sound()
    return


def show_title():
    line_length = default_width + 3
    util.clear_screen()
    print(screen_distance * " " + "=" * line_length)
    print(screen_distance * " " + fg.purple + language_dictionary[util.game_language].menu.title_first_line + fg.rs)
    print(screen_distance * " " + "=" * line_length)
    print(screen_distance * " " + fg.yellow + "|" * line_length + fg.rs)
    print(screen_distance * " " + fg.purple + language_dictionary[util.game_language].menu.title_second_line + fg.rs)
    print(screen_distance * " " + fg.yellow + "|" * line_length + fg.rs)
    print(screen_distance * " " + "=" * line_length)
    print(screen_distance * " " + fg.purple + language_dictionary[util.game_language].menu.title_first_line + fg.rs)
    print(screen_distance * " " + "=" * line_length + "\n\n")


def show_options(options: list, max_options_length: int, chosen_option=0):
    show_title()
    fore_string = "|"
    after_string = "|"
    line_length = max_options_length
    option_length = max_options_length
    for i in range(len(options)):
        option = options[i]
        number_of_spaces = int((option_length - len(options[i]) - len(fore_string) - len(after_string)) / 2)
        if len(option) % 2 != 0:
            option = option + " "
        print(screen_distance * " " + "  " + "_" * line_length)
        if i == chosen_option:
            string_to_print = "  " + fore_string + bg.orange + number_of_spaces * " " + fg.black + option + fg.rs + number_of_spaces * " " + bg.rs + after_string
        else:
            string_to_print = "  " + fore_string + number_of_spaces * " " + option + number_of_spaces * " " + after_string
        print(screen_distance * " " + string_to_print)
        print(screen_distance * " " + "  " + "‾" * line_length + "\n")


def select_exit():
    sys.exit(0)


def select_help():
    quiz.show_game_structure()
    util.clear_screen()
    file = (util.open_file("tutorial_" + str(util.game_language).lower(), 'r'))
    print("\n")
    for line in file:
        print("   " + line[0])
    print("\n")
    return_prompt()


def select_credits():
    util.clear_screen()
    file = (util.open_file("credits_" + str(util.game_language).lower(), 'r'))
    title_lines = language_dictionary[util.game_language].menu.credits_title_lines
    print("\n" + fg.purple + rs.italic)
    for line in title_lines:
        print(line)
    print("\n" + fg.rs)

    for line in file:
        print("   " + line[0])
    print("\n")
    return_prompt()


def select_scores():
    title_lines = language_dictionary[util.game_language].menu.scores_title_lines
    util.clear_screen()
    print("\n" + fg.purple + rs.italic)
    for line in title_lines:
        print(line)
    print("\n" + fg.rs)

    if os.path.isfile("scores.json"):
        f = open("scores.json")
        data = json.load(f)
        scores_sorted = sorted(data, key=lambda d: d['score'], reverse=True)
        len_val = 0
        len_player = 0
        index = 0
        for item in scores_sorted:
            i = 0
            for k, v in item.items():
                if i == 0:
                    if len(v) > len_player:
                        len_player = len(v)
                if i == 1:
                    index = list(
                        language_dictionary[util.Language.ENGLISH.name].menu.settings_menu_question_topics).index(
                        str(v).capitalize())
                    if len(language_dictionary[util.game_language].menu.settings_menu_question_topics[index]) > len_val:
                        len_val = len(language_dictionary[util.game_language].menu.settings_menu_question_topics[index])
                i += 1
        if len_val > len(language_dictionary[util.game_language].menu.scores[1]):
            score_space = len_val - len(language_dictionary[util.game_language].menu.scores[1])
        else:
            score_space = len(language_dictionary[util.game_language].menu.scores[1]) - len_val

        table_len = len(language_dictionary[util.game_language].menu.scores[0] +
                        language_dictionary[util.game_language].menu.scores[1] +
                        language_dictionary[util.game_language].menu.scores[2] +
                        language_dictionary[util.game_language].menu.scores[3]) + \
                    score_space + 24 - len(language_dictionary[util.game_language].menu.scores[3]) + 13
        print("   " + "_" * table_len)
        print("   " + "| " + fg.orange + language_dictionary[util.game_language].menu.scores[
            0] + fg.rs + " | " + fg.orange + language_dictionary[util.game_language].menu.scores[
                  1] + score_space * " " + fg.rs + " | " + fg.orange +
              language_dictionary[util.game_language].menu.scores[2] + fg.rs + " | " + fg.orange +
              language_dictionary[util.game_language].menu.scores[3] + (
                      24 - len(language_dictionary[util.game_language].menu.scores[3])) * " " + fg.rs + " |")
        print("   " + "‾" * table_len)
        print("   " + "—" * table_len)

        for item in scores_sorted:
            i = 0
            for k, v in item.items():
                if i == 0:
                    if len(v) > len_player:
                        print("   " + "| " + v + " " * (len(v) - len_player), end=" | ")
                    else:
                        print("   " + "| " + v + " " * (len_player - len(v)), end=" | ")
                if i == 1:
                    index = list(
                        language_dictionary[util.Language.ENGLISH.name].menu.settings_menu_question_topics).index(
                        str(v).capitalize())
                    print(
                        language_dictionary[util.game_language].menu.settings_menu_question_topics[index] +
                        (len_val - len(
                            language_dictionary[util.game_language].menu.settings_menu_question_topics[index])) * " ",
                        end=" | ")
                if i == 2:
                    print(
                        str(v) + " " * (len(language_dictionary[util.game_language].menu.scores[1]) - len(str(v)) + 1),
                        end=" | ")
                if i == 3:
                    print(v, end=" | ")

                i += 1
            print("\n" + "   " + "—" * table_len)
        f.close()
    else:
        print("\n\n   " + language_dictionary[util.game_language].menu.empty_scores)
    return_prompt()


def select_settings():
    start_index = 0
    util.clear_screen()
    show_options(language_dictionary[util.game_language].menu.settings_menu_options, default_width)
    while True:
        chosen_option = get_user_input(language_dictionary[util.game_language].menu.settings_menu_options,
                                       language_dictionary[util.game_language].menu.settings_menu_options,
                                       default_width, start_index)
        if chosen_option == language_dictionary[util.game_language].menu.settings_menu_options[0]:
            langs = [language_dictionary[util.game_language].en, language_dictionary[util.game_language].hu]
            show_options(langs, 20, util.available_languages.index(util.game_language))
            chosen_lang_option = get_user_input(langs, util.available_languages, 20,
                                                util.available_languages.index(util.game_language), False)
            util.set_game_language(util.available_languages[util.available_languages.index(chosen_lang_option)])
            show_options(language_dictionary[util.game_language].menu.settings_menu_options, 40)
            start_index = 0
        elif chosen_option == language_dictionary[util.game_language].menu.settings_menu_options[1]:
            if util.system_volume:
                util.system_volume = False
            else:
                util.system_volume = True
            show_options(language_dictionary[util.game_language].menu.settings_menu_options, default_width,
                         chosen_option=1)
            start_index = 1
        elif chosen_option == language_dictionary[util.game_language].menu.settings_menu_options[2]:
            if os.name == "nt":
                keyboard.press('f11')
            start_index = 2
        elif chosen_option == language_dictionary[util.game_language].menu.settings_menu_options[3]:
            show_options(language_dictionary[util.game_language].menu.settings_menu_question_topics, default_width,
                         util.topics.index(util.question_topics))
            chosen_question_topic = get_user_input(
                language_dictionary[util.game_language].menu.settings_menu_question_topics, util.topics, default_width,
                util.topics.index(util.question_topics), False)
            util.set_question_topics(chosen_question_topic)
            show_options(language_dictionary[util.game_language].menu.settings_menu_options, 40, chosen_option=3)
            start_index = 3
        elif chosen_option == language_dictionary[util.game_language].menu.settings_menu_options[4]:
            if util.question_difficulty != util.Difficulty.ALL.name:
                show_options(language_dictionary[util.game_language].menu.question_difficulty_levels, 20,
                             util.difficulty_levels.index(util.question_difficulty))
                chosen_difficulty_option = get_user_input(
                    language_dictionary[util.game_language].menu.question_difficulty_levels, util.difficulty_levels, 20,
                    util.difficulty_levels.index(util.question_difficulty), False)
            else:
                show_options(language_dictionary[util.game_language].menu.question_difficulty_levels, 20)
                chosen_difficulty_option = get_user_input(
                    language_dictionary[util.game_language].menu.question_difficulty_levels, util.difficulty_levels, 20,
                    0, False)
            if chosen_difficulty_option != language_dictionary[util.game_language].menu.question_difficulty_levels[0]:
                util.set_question_difficulty(chosen_difficulty_option)
            else:
                util.set_question_difficulty(util.Difficulty.ALL.name)
            show_options(language_dictionary[util.game_language].menu.settings_menu_options, 40, chosen_option=4)
            start_index = 4
        elif chosen_option == language_dictionary[util.game_language].menu.settings_menu_options[5]:
            quizmaster_attitudes = language_dictionary[util.game_language].menu.quizmaster_attitudes
            show_options(language_dictionary[util.game_language].menu.quizmaster_attitudes, 20,
                         util.quizmaster_attitudes.index(util.quizmaster_attitude))
            chosen_attitude_option = get_user_input(quizmaster_attitudes, util.quizmaster_attitudes, 20,
                                                    util.quizmaster_attitudes.index(util.quizmaster_attitude), False)
            util.set_quizmaster_attitude(
                util.quizmaster_attitudes[util.quizmaster_attitudes.index(chosen_attitude_option)])
            show_options(language_dictionary[util.game_language].menu.settings_menu_options, 40, chosen_option=5)
            start_index = 5
        elif chosen_option == language_dictionary[util.game_language].menu.settings_menu_options[6]:
            util.init_settings(util.Language.ENGLISH.name, reset_settings=True)
            start_index = 6
        else:
            update_settings_file()
            return


def update_settings_file():
    filename = "settings.json"
    content = {"language": util.game_language, "topic": util.question_topics, "difficulty": util.question_difficulty,
               "volume": util.system_volume, "quizmaster_attitude": util.quizmaster_attitude}
    with open(filename, "w", encoding="UTF-8") as outfile:
        json.dump(content, outfile)


def return_prompt():
    esc_keys = [b'\x1b', '<ESC>']
    print(fg.grey + "\n\n   " + language_dictionary[util.game_language].menu.return_prompt + fg.rs)
    if util.operating_system == "posix":
        user_input = helpers.return_user_input_linux()
    else:
        user_input = helpers.return_user_input_windows()
    while user_input not in esc_keys:
        if util.operating_system == "posix":
            user_input = helpers.return_user_input_linux()
        else:
            user_input = helpers.return_user_input_windows()
        if user_input in esc_keys:
            return


def get_user_input(option_list: [], values_list: [], max_option_length: int, start_index=0, esc=True) -> str:
    i = start_index
    while True:
        if util.operating_system == "posix":
            user_input = helpers.return_user_input_linux()
        else:
            user_input = helpers.return_user_input_windows()
        first_char = user_input
        # escape
        if first_char == b'\x1b' or first_char == '<ESC>':
            if esc == True:
                return values_list[-1]
            else:
                return values_list[start_index]
        # enter
        if first_char == b'\r' or first_char == '<Ctrl-j>':
            return values_list[i]
        # up
        if first_char == b'H' or first_char == '<UP>':
            if i == 0:
                i = len(option_list) - 1
                show_options(option_list, max_option_length, len(option_list) - 1)
            else:
                i -= 1
                show_options(option_list, max_option_length, i)
            # enter
            if user_input == b'\r' or user_input == '<Ctrl-j>':
                return values_list[i]
        # down
        if first_char == b'P' or first_char == '<DOWN>':
            if i == len(option_list) - 1:
                i = 0
                show_options(option_list, max_option_length)
            else:
                i += 1
                show_options(option_list, max_option_length, i)
            # enter
            if user_input == b'\r' or user_input == '<Ctrl-j>':
                return values_list[i]


class MenuOption(pygame.sprite.Sprite):

    def __init__(self, type, text, order, base_height):
        super().__init__()

        x_pos = 400
        y_pos = base_height + (order * 35)

        self.frame = pygame.image.load('./data/graphics/option.png').convert_alpha()
        font = pygame.font.SysFont('Sans', 25)
        self.type = type
        self.text = font.render(text, True, (255, 255, 255))
        self.image = self.frame
        self.image.blit(self.text, [30, 0])
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    def get_is_active(self):
        if hasattr(self, 'is_active'):
            return self.is_active
        else:
            return True

    def set_is_active(self):
        self.is_active = True

    def unset_is_active(self):
        self.is_active = False

    def player_input(self):
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint((pygame.mouse.get_pos())):
            print(self.type)
            if self.type == "play":
                quiz.play()
            if self.type == "exit":
                pygame.quit()
                exit()
            if self.type == "options":
                print("YES")
                global options
                options = True
                print(options)
            if self.type == "Language selection":
                global lang_selection
                lang_selection = True
            if self.type in [util.Language.HUNGARIAN.name, util.Language.ENGLISH.name]:
                util.set_game_language(self.type)
            if self.type == "Back":
                options = False

    def update(self):
        self.player_input()


def main():
    pygame.init()
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
    pygame.time.set_timer(pygame.USEREVENT + 2, 1000)

    global screen
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Runner')
    global clock
    clock = pygame.time.Clock()
    global sky_surface

    sky_surface = pygame.image.load('./data/graphics/background_.png').convert_alpha()
    settings_option_group = pygame.sprite.Group()
    sprite_group = ['play', "intro", "credits", "options", "exit"]
    menu_option_group = pygame.sprite.Group()
    texts = ["Play", "Intro", "Credits", "Options", "Exit"]
    main_menu_base_y = 445
    for index in range(len(sprite_group)):
        menu_option_group.add(MenuOption(sprite_group[index], texts[index], index, main_menu_base_y))
    settings = ["Language selection", "Disable/Enable Sound",
                "Question types",
                "Question difficulty",
                "Quizmaster attitude",
                "Restore Settings",
                "Back"]
    settings_menu_base_y = 245

    for index in range(len(settings)):
        settings_option_group.add(MenuOption(settings[index], settings[index], index, settings_menu_base_y))
    langs = util.available_languages
    lang_group = pygame.sprite.Group()

    for index in range(len(langs)):
        lang_group.add(MenuOption(langs[index], langs[index], index, main_menu_base_y))
    global options, lang_selection
    options = False
    lang_selection = False
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(sky_surface, (0, -20))
        if options:

            if lang_selection:
                screen.fill((0, 0, 0))

                lang_group.draw(screen)
                lang_group.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    lang_selection = False

            else:
                screen.fill((0, 0, 0))

                settings_option_group.draw(screen)
                settings_option_group.update()

        else:
            screen.fill((0, 0, 0))
            screen.blit(sky_surface, (0, -20))

            menu_option_group.draw(screen)
            menu_option_group.update()

        pygame.display.update()
        clock.tick(60)


def handle_main_menu():
    start_index = 0
    options_length = default_width
    show_options(language_dictionary[util.game_language].menu.main_menu_options, options_length)
    while True:
        chosen_option = get_user_input(language_dictionary[util.game_language].menu.main_menu_options,
                                       language_dictionary[util.game_language].menu.main_menu_options, options_length,
                                       start_index)
        if chosen_option == language_dictionary[util.game_language].menu.main_menu_options[0]:
            quiz.play()
            show_options(language_dictionary[util.game_language].menu.main_menu_options, options_length)
            start_index = 0
        if chosen_option == language_dictionary[util.game_language].menu.main_menu_options[1]:
            quiz.fastest_finger_first()
            show_options(language_dictionary[util.game_language].menu.main_menu_options, options_length,
                         chosen_option=1)
            start_index = 1
        if chosen_option == language_dictionary[util.game_language].menu.main_menu_options[2]:
            select_help()
            show_options(language_dictionary[util.game_language].menu.main_menu_options, options_length,
                         chosen_option=2)
            start_index = 2
        if chosen_option == language_dictionary[util.game_language].menu.main_menu_options[3]:
            select_settings()
            show_options(language_dictionary[util.game_language].menu.main_menu_options, options_length,
                         chosen_option=3)
            start_index = 3
        if chosen_option == language_dictionary[util.game_language].menu.main_menu_options[4]:
            select_credits()
            show_options(language_dictionary[util.game_language].menu.main_menu_options, options_length,
                         chosen_option=4)
            start_index = 4
        if chosen_option == language_dictionary[util.game_language].menu.main_menu_options[5]:
            select_scores()
            show_options(language_dictionary[util.game_language].menu.main_menu_options, options_length,
                         chosen_option=5)
            start_index = 5
        if chosen_option == language_dictionary[util.game_language].menu.main_menu_options[6]:
            select_exit()
