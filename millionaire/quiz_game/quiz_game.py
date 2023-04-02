import os
import random
import json
import time
from sty import Style, RgbFg, fg, bg, rs
import millionaire.menu.menu as menu
import millionaire.util.util as util
import millionaire.menu.helpers as helpers
import threading

operating_system = os.name
fg.purple = Style(RgbFg(148, 0, 211))
fg.orange = Style(RgbFg(255, 150, 50))
fg.green = Style(RgbFg(0, 255, 0))
bg.orange = bg(255, 150, 50)
languages = util.available_languages
language_dictionary = util.language_dictionary
table_length = 113
game_levels = 15
screen_distance = 60
threads = []


def play():
    global base_threads
    global a_threads
    global b_threads
    global c_threads
    global d_threads
    global game_language, question_lines_easy, question_lines_medium, question_lines_hard
    game_language = util.game_language
    global question_topics
    question_topics = util.question_topics
    global question_difficulty
    question_difficulty = util.question_difficulty
    global help_types
    help_types = {"halving": True, "telephone": True, "audience": True}
    global random_sounds
    random_sounds = util.init_random_sounds()
    question_lines = []
    question_lines_easy = []
    question_lines_medium = []
    question_lines_hard = []
    if question_topics == util.Topics.ALL.name:
        for topic in util.Topics:
            if topic.name != util.Topics.ALL.name and question_difficulty != util.Difficulty.ALL.name:
                for level in util.Difficulty:
                    if question_difficulty == level.name:
                        for line in util.open_file(str(level.name).lower(), "r", ";",
                                                   "/text_files/topics/" + str(game_language).lower() + "/" + str(
                                                       topic.name).lower() + "/" + str(level.name).lower() + "/"):
                            question_lines.append(line)
            else:
                if topic.name != util.Topics.ALL.name:
                    for line in util.open_file(str(util.Difficulty.EASY.name).lower(), "r", ";",
                                               "/text_files/topics/" + str(game_language).lower() + "/" + str(
                                                   topic.name).lower() + "/" + str(
                                                   util.Difficulty.EASY.name).lower() + "/"):
                        question_lines_easy.append(line)
                    for line in util.open_file(str(util.Difficulty.MEDIUM.name).lower(), "r", ";",
                                               "/text_files/topics/" + str(game_language).lower() + "/" + str(
                                                   topic.name).lower() + "/" + str(
                                                   util.Difficulty.MEDIUM.name).lower() + "/"):
                        question_lines_medium.append(line)
                    for line in util.open_file(str(util.Difficulty.HARD.name).lower(), "r", ";",
                                               "/text_files/topics/" + str(game_language).lower() + "/" + str(
                                                   topic.name).lower() + "/" + str(
                                                   util.Difficulty.HARD.name).lower() + "/"):
                        question_lines_hard.append(line)
    else:
        for level in util.Difficulty:
            if question_difficulty == level.name and level.name != util.Difficulty.ALL.name:
                for line in util.open_file(str(level.name).lower(), "r", ";",
                                           "/text_files/topics/" + str(game_language).lower() + "/" + str(
                                               question_topics).lower() + "/" + str(level.name).lower() + "/"):
                    question_lines.append(line)
            else:
                if level.name != util.Difficulty.ALL.name:
                    for line in util.open_file(str(util.Difficulty(level).name).lower(), "r", ";",
                                               "/text_files/topics/" + str(game_language).lower() + "/" + str(
                                                   question_topics).lower() + "/" + str(level.name).lower() + "/"):
                        if level.name == util.Difficulty.EASY.name:
                            question_lines_easy.append(line)
                        if level.name == util.Difficulty.MEDIUM.name:
                            question_lines_medium.append(line)
                        if level.name == util.Difficulty.HARD.name:
                            question_lines_hard.append(line)
    random.shuffle(question_lines)
    random.shuffle(question_lines_easy)
    random.shuffle(question_lines_medium)
    random.shuffle(question_lines_hard)
    player_name = input(" " * screen_distance + language_dictionary[game_language].quiz.player_name_prompt)
    player = "player"
    if game_language == util.Language.HUNGARIAN.name:
        for name in os.listdir(util.get_data_path() + "/sound_files/" + str(game_language).lower() + "/players"):
            if player_name.lower() == name[:-4]:
                player = player_name
        util.play_sound("dear", 0, dir="intro", timer=True)
        util.play_sound(player, 0, dir="players", timer=True)
        millionaire_sounds = ["millionaire", "millionaire_1", "millionaire_2"]
        sound = random.choice(millionaire_sounds)
        util.play_sound(sound, 0, dir="intro", timer=True)
    score = 0
    util.clear_screen()
    if game_language == util.Language.ENGLISH:
        util.play_sound("start", 0)
    show_game_structure()
    for i in range(game_levels):
        init_threads(i)
        if question_difficulty == util.Difficulty.ALL.name:
            if i < 5:
                question_lines = question_lines_easy
            elif i < 10:
                question_lines = question_lines_medium
            else:
                question_lines = question_lines_hard
        question = question_lines[i][0]
        answers = {"a": question_lines[i][1], "b": question_lines[i][2], "c": question_lines[i][3],
                   "d": question_lines[i][4]}
        answer_list = list(answers.values())
        random.shuffle(answer_list)
        shuffled_answers = dict(zip(answers, answer_list))
        print_quiz_table("", {"a": "", "b": "", "c": "", "d": ""}, game_level=i, show_answers=False)
        if i in [0, 6, 8]:
            play_question_intro(i)
        if util.game_language == util.Language.HUNGARIAN.name and i < 14:
            play_question_prologue(i)
        util.clear_screen()
        print_quiz_table(question, {"a": "", "b": "", "c": "", "d": ""}, game_level=i, show_answers=False)
        play_music(i)
        time.sleep(2)
        answer_list_fill = ["","","",""]
        for j in range(4):
            util.clear_screen()
            answer_list_fill[j] = answer_list[j]
            print_quiz_table(question, {"a": answer_list_fill[0], "b": answer_list_fill[1], "c": answer_list_fill[2], "d": answer_list_fill[3]}, game_level=i)
            time.sleep(1)
        print("\n\n   " + fg.grey + language_dictionary[game_language].quiz.select_answer + fg.rs)
        correct_answer_key = get_dictionary_key_by_value(shuffled_answers, question_lines[i][1])
        correct_answer_value = question_lines[i][1]
        if util.game_language == util.Language.HUNGARIAN.name:
            thread_random(i, last_one="base")
        answer = handle_user_input(question, shuffled_answers, correct_answer_key, level=i)
        if answer == "esc":
            quit_quiz(score, player_name, question_topics)
            return
        util.pause_music()
        while answer not in list(answers.keys()):
            if answer == "esc":
                quit_quiz(score, player_name, question_topics)
                return
            if answer == "t":
                util.clear_screen()
                print_quiz_table(question, shuffled_answers, game_level=i)
                if util.game_language == util.Language.HUNGARIAN.name:
                    thread_random(score, working=False)
                    music_off_sounds = ["music_off", "lower_music"]
                    sound = random.choice(music_off_sounds)
                    if i > 8:
                        sound = "stop_at_finish"
                    util.play_sound(sound, 0, dir="out_of_game", timer=True)
                    util.stop_music()
                    out_of_game_sounds = ["and_then_out_of_game", "acknowledge_it_out_of_game", "out_of_game", "out_of_game_2", "out_of_game_say_letter"]
                    sound = random.choice(out_of_game_sounds)
                    util.play_sound(sound, 0, dir="out_of_game")
                print("\n\n  ", fg.grey + language_dictionary[game_language].quiz.select_answer_out + fg.rs)
                answer = handle_user_input(question, shuffled_answers, correct_answer_key, level=i, final_color="blue",
                                           out_of_game=True)
                if answer == "esc":
                    quit_quiz(score, player_name, question_topics)
                    return
                is_correct = check_answer(answer, correct_answer_key)
                if is_correct:
                    util.clear_screen()
                    print_quiz_table(question, shuffled_answers, answer, "green", "", game_level=i)
                    time.sleep(2)
                    if game_language == util.Language.HUNGARIAN.name:
                        util.play_sound("out_of_game_luck", 0, dir="out_of_game", timer=True)
                    if i > 0:
                        print_prizes_with_quizmaster(level=i - 1)
                    else:
                        print_prizes_with_quizmaster(level=i, nullprize=True)
                    print(fg.orange + "\n   " + language_dictionary[game_language].quiz.correct_answer_out + fg.rs)
                    util.play_sound("claps", 0, general=True, timer=True)
                else:
                    if game_language == util.Language.HUNGARIAN.name:
                        util.play_sound("good_to_stop", 0, dir="out_of_game", timer=True)
                    util.clear_screen()
                    print_quiz_table(question, shuffled_answers, answer, "blue", correct_answer=correct_answer_key,
                                     game_level=i)
                    time.sleep(2)
                    if i > 9:
                        print_prizes_with_quizmaster(9)
                    elif i > 4:
                        print_prizes_with_quizmaster(4)
                    else:
                        print_prizes_with_quizmaster(0, nullprize=True)
                    print(fg.red + "\n   " + language_dictionary[game_language].quiz.incorrect_answer + fg.rs)
                    if util.game_language == util.Language.HUNGARIAN.name:
                        sorry_sounds = ["so_sorry", "terribly_sorry"]
                        sound = random.choice(sorry_sounds)
                        util.play_sound(sound, 0, dir="out_of_game", timer=True)
                    time.sleep(1)
                    util.play_sound("claps", 0, general=True, timer=True)
                quit_quiz(score, player_name, question_topics)
                util.clear_screen()
                return

            if answer == "h" or "s":
                if list(help_types.values()).count(True) != 0:
                    if game_language == util.Language.HUNGARIAN.name:
                        util.pause_music()
                        thread_random(score, working=False)
                        play_help_sounds(help_types)
                        util.continue_music()
                    util.clear_screen()
                    print_quiz_table(question, shuffled_answers, game_level=i)
                    help_functions = {"halving": halving, "telephone": telephone_help, "audience": audience_help}
                    print("\n\n   " + fg.grey + language_dictionary[game_language].quiz.help_selection + fg.rs)
                    help_input = handle_user_input(question, shuffled_answers,  correct_answer_key, level=i, help=True)
                    if help_input == "esc":
                        quit_quiz(score, player_name, question_topics)
                        return
                    for x in range(len(help_types)):
                        if help_input == list(help_types)[x][0]:
                            if help_types[list(help_types)[x]]:
                                if list(help_types)[x] == "halving":
                                    shuffled_answers = list(help_functions.values())[x](question, shuffled_answers,
                                                                                        correct_answer_value)
                                    for a in range(len(answer_list)):
                                        answer_list[a] = list(shuffled_answers.values())[a]
                                    print_quiz_table(question, shuffled_answers, game_level=i)
                                    time.sleep(2)
                                    if util.game_language == util.Language.HUNGARIAN.name:
                                        after_halving_sounds = ["after_halving", "after_halving_2", "after_halving_3", "your_guess_stayed", "you_have_fifty_percent", "im_not_surprised"]
                                        sound = random.choice(after_halving_sounds)
                                        util.play_sound(sound, 0, dir="halving", timer=True)
                                elif list(help_types)[x] == "audience":
                                    audience_help(question, shuffled_answers, correct_answer_value, game_level=i)
                                else:
                                    list(help_functions.values())[x](question, shuffled_answers, correct_answer_value, player)
                                help_types[list(help_types)[x]] = False
                                break
                            else:
                                if list(help_types)[x] == "audience":
                                    print("  " + language_dictionary[game_language].quiz.audience_help_disabled)
                                elif list(help_types)[x] == "halving":
                                    print("  " + language_dictionary[game_language].quiz.halving_help_disabled)
                                else:
                                    print("  " + language_dictionary[game_language].quiz.phone_help_disabled)
                    play_music(i)
                    print("\n\n  ", fg.grey + language_dictionary[game_language].quiz.select_answer + fg.rs)
                    if help_input == "esc":
                        quit_quiz(score, player_name, question_topics)
                        return
                    answer = handle_user_input(question, shuffled_answers,  correct_answer_key, level=i)
                    time.sleep(2)
                    util.clear_screen()
                else:
                    play_help_sounds(help_types)
                    play_music(i)
                    util.clear_screen()
                    print_quiz_table(question, shuffled_answers, game_level=i)
                    print("\n\n   " + fg.grey + language_dictionary[game_language].quiz.helps_disabled + fg.rs)
                    print("\n\n   " + fg.grey + language_dictionary[game_language].quiz.select_answer + fg.rs)
                    answer = handle_user_input(question, shuffled_answers, correct_answer_key, level=i)
        is_correct = check_answer(answer, correct_answer_key)
        if is_correct:
            score += 1
            if i < 14:
                if i == 5:
                    util.play_sound("sixth_correct_answer", 0, general=True)
                else:
                    util.play_sound("correct_answer", 0, general=True)
                util.clear_screen()
                for k in range(4):
                    print_quiz_table(question, shuffled_answers, answer, "green", "", game_level=i)
                    time.sleep(0.12)
                    util.clear_screen()
                    print_quiz_table(question, shuffled_answers, answer, "orange", "", game_level=i)
                    time.sleep(0.12)
                    util.clear_screen()
                print_quiz_table(question, shuffled_answers, answer, "green", game_level=i)
                util.clear_screen()
                if len(question) % 2 == 0:
                    question = question + " "
                if util.game_language == util.Language.HUNGARIAN.name:
                    play_prize_sound(i)
                if i == 4:
                    print_prizes_with_quizmaster(i)
                    util.play_sound("won_hundred_bucks", 0, general=True)
                    time.sleep(7)
                elif i == 9:
                    print_prizes_with_quizmaster(i)
                    time.sleep(3)
                    if util.game_language == util.Language.HUNGARIAN.name:
                        util.play_sound("now_comes_hard_part", 0, dir="random")
                else:
                    print_prizes_with_quizmaster(i)
                    util.play_sound("claps", 0, general=True, timer=True)
                    time.sleep(2)
            else:
                if util.game_language == util.Language.HUNGARIAN.name:
                    util.play_sound("after_marking", 0, dir="lets_see")
                    time.sleep(4)
                    util.play_sound("great_logic", 0, dir="correct")
                    print_prizes_with_quizmaster(i)
                time.sleep(1)
                util.clear_screen()
                display_winning()
                quit_quiz(score, player_name, question_topics)
        else:
            thread_random(i, working=False)
            util.play_sound("bad_answer", 0, general=True)
            util.clear_screen()
            for k in range(4):
                print_quiz_table(question, shuffled_answers, answer, "orange", correct_answer=correct_answer_key, game_level=i)
                time.sleep(0.12)
                util.clear_screen()
                print_quiz_table(question, shuffled_answers,answer, "orange", game_level=i)
                time.sleep(0.12)
                util.clear_screen()
            print_quiz_table(question, shuffled_answers, answer, "orange", correct_answer=correct_answer_key,
                             game_level=i)
            time.sleep(2)
            if game_language == util.Language.HUNGARIAN.name:
                util.play_sound("so_sorry", 0, dir="out_of_game", timer = True)
                time.sleep(1)
                util.play_sound("claps", 0, general=True, timer=True)
            util.clear_screen()
            if i > 9:
                print_prizes_with_quizmaster(9)
            elif i > 4:
                print_prizes_with_quizmaster(4)
            else:
                print_prizes_with_quizmaster(0, nullprize=True)
            print("\n   " + fg.orange + language_dictionary[game_language].quiz.incorrect_answer + fg.rs)
            quit_quiz(score, player_name, question_topics)
            util.clear_screen()

            return
        util.clear_screen()
    quit_quiz(score, player_name, question_topics)

    return



def display_winning():
    util.play_sound("winning_theme", 0, general=True)
    print("\n" + " " * 20 + fg.purple + language_dictionary[game_language].quiz.won_prize + show_prize(
        14) + " !" + fg.rs)
    for i in range(22):
        win_color = bg.blue
        if i % 2 == 0:
            win_color = bg.yellow
        util.clear_screen()

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
        #util.clear_screen()

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

            color = win_color
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
                            second_text[point] + "   " + bg.rs + bg.light_blue + "  " + bg.rs + bg.rs + line[
                                                                                                        last_index:]
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
            line2 = line2.replace("X", win_color + " " + bg.rs)
            line2 = line2.replace(".", win_color + " " + bg.rs)
            line2 = line2.replace("X", bg.black + " " + bg.rs)
            line2 = line2.replace("|", bg.white + " " + bg.rs)

            line3 = "".join(line2)

            print(line3)

        print("\n\n\n" + " " * 53 + fg.purple + language_dictionary[game_language].quiz.won_prize + show_prize(
            14) + " !" + fg.rs)

        time.sleep(1)
    #time.sleep(35)

def play_prize_sound(level: int):
    if level in [4, 7, 9, 11, 12]:
        util.play_sound("level_" + str(level), 0, dir="prize")


def thread_random(level: int, selected="", last_one="", working=True):
    global base_threads
    global a_threads
    global b_threads
    global c_threads
    global d_threads
    global threads

    if working == True:
        if last_one == "a":
            for thread in a_threads:
                thread.cancel()
        elif last_one == "b":
            for thread in b_threads:
                thread.cancel()
        elif last_one == "c":
            for thread in c_threads:
                thread.cancel()
        elif last_one == "d":
            for thread in d_threads:
                thread.cancel()
        elif last_one == "base":
            pass
        else:
            for thread in base_threads:
                thread.cancel()

        if selected == "a":
            for thread in a_threads:
                if not thread.finished.is_set():
                    thread.start()

                else:
                    a_threads = []
                    threads[1] = []
                    for i in range (4):
                        a_threads.append(threading.Timer(15.0 * (i+1), play_random_quizmaster_sound, args=(level,)))
                    for thread_ in a_threads:
                        thread_.start()
                    threads[1] = a_threads
                    return
        elif selected == "b":
            for thread in b_threads:
                if not thread.finished.is_set():
                    thread.start()
                else:
                    b_threads = []
                    threads[2] = []

                    for i in range(4):
                        b_threads.append(threading.Timer(15.0 * (i + 1), play_random_quizmaster_sound, args=(level,)))
                    for thread_ in b_threads:
                        thread_.start()
                    threads[2] = b_threads

                    return
        elif selected == "c":
            for thread in c_threads:
                if not thread.finished.is_set():
                    thread.start()

                else:
                    c_threads = []
                    threads[3] = []

                    for i in range(4):
                        c_threads.append(threading.Timer(15.0 * (i + 1), play_random_quizmaster_sound, args=(level,)))
                    for thread_ in c_threads:
                        thread_.start()
                    threads[3] = c_threads

                    return
        elif selected == "d":
            for thread in d_threads:
                if not thread.finished.is_set():
                    thread.start()
                else:
                    d_threads = []
                    threads[4] = []

                    for i in range(4):
                        d_threads.append(threading.Timer(15.0 * (i + 1), play_random_quizmaster_sound, args=(level,)))
                    for thread_ in d_threads:
                        thread_.start()
                    threads[4] = d_threads

                    return
        else:
            for thread in base_threads:
                if not thread.finished.is_set():
                    thread.start()
                else:
                    base_threads = []
                    threads[0] = []
                    for i in range(4):
                        base_threads.append(threading.Timer(15.0 * (i + 1), play_random_quizmaster_sound, args=(level,)))
                    for thread_ in base_threads:
                        thread_.start()
                    threads[0] = base_threads
                    return

    else:
        for list in threads:
            for thread in list:
                    thread.cancel()



def play_random_quizmaster_sound(level: int):
    util.pause_music()
    global random_sounds
    sound_file = random.choice(random_sounds)
    util.play_sound_object(sound_file)
    util.continue_music()


def play_question_prologue(level: int):
    sounds_list = [
        ["here_is_the_first_question_one", "here_is_the_first_question_two", "here_is_the_first_question_three"],
        ["here_is_the_second_question_one"],
        ["here_is_the_third_question_one", "here_is_the_third_question_two", "here_is_the_third_question_three"],
        ["here_is_the_fourth_question_one", "here_is_the_fourth_question_two", "here_is_the_fourth_question_three"],
        ["here_is_the_fifth_question_one", "here_is_the_fifth_question_two", "here_is_the_fifth_question_three"],
        ["here_is_the_sixth_question_one", "here_is_the_sixth_question_two", "here_is_the_sixth_question_three", "here_is_the_sixth_question_four", "here_is_the_sixth_question_five", "here_is_the_sixth_question_six"],
        ["here_is_the_seventh_question_one", "here_is_the_seventh_question_two", "here_is_the_seventh_question_three", "here_is_the_seventh_question_four"],
        ["here_is_the_eighths_question_one", "here_is_the_eighthsquestion_two", "here_is_the_eighths_question_three", "here_is_the_eighths_question_four", "here_is_the_eighths_question_five", "here_is_the_eighths_question_six"],
        ["here_is_the_nineth_question_one", "here_is_the_nineth_question_two", "here_is_the_nineth_question_three"],
        ["here_is_the_tenth_question_one", "here_is_the_tenth_question_two", "here_is_the_tenth_question_three"],
        ["here_is_the_eleventh_question_one", "here_is_the_eleventh_question_two", "here_is_the_eleventh_question_three"],
        ["here_is_the_twelfth_question_one", "here_is_the_twelfth_question_two", "here_is_the_twelfth_question_three", "here_is_the_twelfth_question_four"],
        ["here_is_the_thirteenth_question_one", "here_is_the_thirteenth_question_two"],
        ["here_is_the_fourteenth_question_one"]
    ]

    if level == 7:
        if list(help_types.values()).count(True) == len(
                help_types)-2 and help_types["telephone"]:
            sounds_list[7].append("here_is_the_eighths_question_with_phone")
    if level == 8:
        if list(help_types.values()).count(True) == len(
                help_types)-1:
            sounds_list[8].append("here_is_the_nineth_question_two_with_two_helps")
        if list(help_types.values()).count(True) == len(
                help_types):
            sounds_list[8].append("here_is_the_nineth_question_with_three_helps")

    sound_file = random.choice(sounds_list[level])
    util.play_sound(sound_file, 0, dir="question_prologue", timer=True)

    chance = random.randrange(0, 10)
    if chance > 7:
        if level == 3:
                util.play_sound("at_4", 0, dir="question_prologue", timer=True)
        elif level == 4:
                util.play_sound("at_5", 0, dir="question_prologue", timer=True)
        elif level == 5:
                util.play_sound("at_6", 0, dir="question_prologue", timer=True)
        elif level == 6:
                util.play_sound("at_7", 0, dir="question_prologue", timer=True)
        elif level == 7:
                util.play_sound("at_8", 0, dir="question_prologue", timer=True)
        elif level == 8:
            util.play_sound("at_9", 0, dir="question_prologue", timer=True)
        elif level == 9:
                util.play_sound("at_10", 0, dir="question_prologue", timer=True)
        elif level == 10:
                util.play_sound("at_11", 0, dir="question_prologue", timer=True)
        elif level == 11:
                util.play_sound("at_12", 0, dir="question_prologue", timer=True)
        elif level == 12:
                util.play_sound("at_13", 0, dir="question_prologue", timer=True)
        else:
            pass


def play_question_intro(level: int):
    sound_file = ""
    if level == 0:
        sound_file = "before_question"
    if level == 6:
        sound_file = "before_seventh_question"
    elif level == 8:
        sound_file = "before_nineth_question"

    util.play_sound(sound_file, 0, timer=True, general=True)


def play_help_sounds(help_types: {}):
    sound_file = ""
    help_assets = ["you_still_have_help","you_have_helps_if_unsure","you_still_have_helps_dont_worry"]

    if list(help_types.values()).count(True) == len(
            help_types):
        all_help_sounds = ["you_still_have_three_helps", "still_have_all_helps", "yet_having_three_helps", "still_have_three_helps_2", "still_have_3_lifelines"]
        sound_file = random.choice(all_help_sounds)
    elif list(help_types.values()).count(True) == len(
            help_types)-1:
        two_help_sounds = ["and_still_have_two_helps", "still_have_two_helps_i_take_it"]
        if help_types["telephone"] and help_types["audience"]:
            two_help_sounds.append("you_still_have_two_helps_phone_audience")
        sound_file = random.choice(two_help_sounds)
    elif list(help_types.values()).count(True) == len(
            help_types)-2:
        help_assets.append("you_waste_a_lot")
        if help_types["telephone"]:
            phone_left_sounds = ["you_have_a_phone_help_left",  "you_have_a_phone_but_make_you_mad"]
            for sound in phone_left_sounds:
                help_assets.append(sound)
        else:
            one_help_sounds = ["oh_god_got_one_help", "you_still_have_one_help", "whatever_you_say_theres_1_help"]
            for sound in one_help_sounds:
                help_assets.append(sound)
        sound_file = random.choice(help_assets)
    else:
        no_help_sounds = ["no_more_helps", "without_help", "sorry_no_more_helps", "since_lost_helps", "fighting_without_helps", "but_no_more_helps"]
        sound_file = random.choice(no_help_sounds)

    util.play_sound(sound_file, 0, dir="help", timer=True)


def fastest_finger_first():
    global game_language, question_lines_easy, question_lines_medium, question_lines_hard
    game_language = util.game_language
    global question_topics
    question_topics = util.question_topics
    global question_difficulty
    question_difficulty = util.question_difficulty
    global help_types
    help_types = {"halving": True, "telephone": True, "audience": True}
    question_lines = []
    question_lines_easy = []
    question_lines_medium = []
    question_lines_hard = []
    for line in util.open_file("questions", "r", ";",
                               "/text_files/fastest_fingers_first/" + str(game_language).lower() + "/"):
        question_lines.append(line)
    random.shuffle(question_lines)
    player_name = input(" " * screen_distance + language_dictionary[game_language].quiz.player_name_prompt)
    score = 0
    total_answer = ""
    util.clear_screen()
    if game_language == util.Language.ENGLISH:
        util.play_sound("start", 0)
    question = question_lines[0][0]
    answers = {"a": question_lines[0][1], "b": question_lines[0][2], "c": question_lines[0][3],
               "d": question_lines[0][4]}
    answer_list = list(answers.values())
    random.shuffle(answer_list)
    # shuffled_answers = dict(zip(answers, answer_list))
    shuffled_answers = answers
    print_quizmaster()
    if game_language == util.Language.HUNGARIAN.name:
        util.play_sound("lets_look_at_the_fastest_fingers_question", 0, dir="fastest_fingers")
        time.sleep(2)
    start = time.time()
    util.clear_screen()
    print_fastest_fingers_table(question, shuffled_answers, game_level=0, quizmaster=True, prizes=False)
    util.play_sound("fastest_fingers_first", 0, general=True)
    print("\n\n   " + fg.grey + language_dictionary[game_language].quiz.select_answer_out + fg.rs)
    for i in range(4):
        answer = handle_fastest_fingers_first_input(question, shuffled_answers, 0, total_answer)
        if answer == "esc":
            quit_fastest_fingers()
            return
        total_answer += answer
    correct_answer_keys = question_lines[0][5]
    util.clear_screen()
    end = time.time()
    is_correct = check_answer(total_answer, correct_answer_keys)
    util.stop_sound()
    print_fastest_fingers_table(question, answers, total_answer, "orange", game_level=0, quizmaster=True, prizes=False)
    if game_language == util.Language.HUNGARIAN.name:
        if os.path.isfile("./data/sound_files/hungarian/fastest_fingers" + correct_answer_keys + ".wav"):
            util.play_sound(correct_answer_keys, 0)
        time.sleep(1)
        util.play_sound("lets_see_who_is_correct", 0, dir="fastest_fingers")
    time.sleep(2)
    if is_correct:
        util.play_sound("fastest_fingers_correct", 0, general=True)
        util.clear_screen()
        if len(question) % 2 == 0:
            question = question + " "
        print_prizes_with_quizmaster(0, False, special_text="♦ " + player_name + " : " + str(end - start)[:5] + " ♦",
                                     bg_color=bg.green)
        time.sleep(2)
        util.play_sound("fastest_fingers_win", 0, general=True)
    else:
        util.play_sound("fastest_fingers_bad", 0, general=True)
        util.clear_screen()
        print("\n   " + fg.orange + language_dictionary[game_language].quiz.incorrect_answer + fg.rs)
        quit_fastest_fingers()
        return

    quit_fastest_fingers()

    return

def init_threads(level: int):
    global base_threads
    global a_threads
    global b_threads
    global c_threads
    global d_threads
    global threads

    if level > 0:
        thread_random(level, working=False)
    threads = []

    for i in range(5):
        options = []
        for j in range(4):
            options.append(threading.Timer(15.0 * (j+1), play_random_quizmaster_sound, args =  (level,)))
        threads.append(options)

    base_threads = threads[0]
    a_threads = threads[1]
    b_threads = threads[2]
    c_threads = threads[3]
    d_threads = threads[4]


def get_dictionary_key_by_value(dictionary: {}, value: str) -> str:
    for choice, answerValue in dict.items(dictionary):
        if answerValue == value:
            return choice


def check_answer(answer: str, correct_answer: str) -> bool:
    return answer == correct_answer


def show_prize(round_number: int) -> str:
    prizes = util.open_file("prizes_" + str(game_language).lower(), "r")
    return prizes[round_number][0]


def halving(question: str, answers: {}, correct_answer: str) -> dict:
    if util.game_language == util.Language.HUNGARIAN.name:
        before_halving_sounds = ["before_halving", "before_halving_2", "before_halving_3", "before_halving_4",
                                "before_halving_5", "before_halving_6", "halv", "lets_even_half", "lets_halv", "lets_see_which_two", "lets_take_two",
                                 "lets_take_two_1", "lets_take_two_2", "lets_take_two_3", "two_of_four"]
        sound = random.choice(before_halving_sounds)
        util.play_sound(sound, 0, dir="halving", timer=True)
    time.sleep(2)
    util.clear_screen()
    util.play_sound("halving", 0, general=True)
    halved_answers = calculate_halved_answers(answers, correct_answer)
    return halved_answers


def calculate_halved_answers(answers: {}, correct_answer: str) -> {}:
    halved_answers = {}
    correct_value = get_dictionary_key_by_value(answers, correct_answer)
    second_answer = random.choice([x for x in answers if x != correct_value])
    for i in answers:
        if answers[i] == correct_answer:
            halved_answers[i] = answers[i]
        elif i == second_answer:
            halved_answers[i] = answers[second_answer]
        else:
            halved_answers[i] = ""

    return halved_answers


def get_chances(answers: {}, correct_value: str) -> dict:
    answers_list = list(answers.keys())
    chances_dict = {}
    correct_answer = get_dictionary_key_by_value(answers, correct_value)
    chances_dict[correct_answer] = random.randrange(40, 89)
    answers_list.pop(answers_list.index(correct_answer))
    if list(answers.values()).count("") == 2:
        for k in range(len(list(answers.keys())) - 1):
            if list(answers.values())[k] != "":
                chances_dict[answers_list[k]] = 100 - sum(chances_dict.values())
            else:
                chances_dict[answers_list[k]] = 0
        return chances_dict

    for k in range(len(answers_list)):
        if k == len(answers_list) - 1:
            chances_dict[answers_list[k]] = 100 - sum(chances_dict.values())
        else:
            chances_dict[answers_list[k]] = random.randrange(0, 100 - sum(chances_dict.values()))

    return chances_dict


def write_content_to_file(filename: str, content: {}):
    if os.path.isfile(filename):
        with open(filename, 'r+') as file:
            file_data = json.load(file)
            file_data.append(content)
            file.seek(0)
            json.dump(file_data, file)

    else:
        with open(filename, "w", encoding="UTF-8") as outfile:
            json.dump([content], outfile)


def divide_question(question: str) -> list:
    question_parts = []
    basic_question_length = 109
    if len(question) >= basic_question_length:
        for i in range(int(len(question) / basic_question_length) + 1):
            index = basic_question_length * i
            question_parts.append(question[index:basic_question_length * (i + 1)])

    return question_parts


def divide_answer(answer: str, number_of_parts: float) -> list:
    answer_parts = []
    basic_question_length = 109
    basic_answer_length = int((basic_question_length / 2) - 5)
    for i in range(int(number_of_parts) + 1):
        if len(answer[i:basic_answer_length * (i + 1)]) > 0:
            index = basic_answer_length * i
            answer_parts.append(answer[index:basic_answer_length * (i + 1)])
        else:
            answer_parts.append("")
    return answer_parts


def print_quiz_table(question: str, answers_: {}, selected="", color="", correct_answer="", game_level=0,
                     quizmaster=True, prizes=True, show_answers=True):
    colors_ = {
        "orange":  bg.orange,
        "green":   bg.green,
        "blue":    bg.blue ,
        "li_grey": bg.da_grey,
    }

    global table_length
    basic_question_length = 109
    answer_values = list(answers_.values())
    longest_string = list(sorted(answers_.values(), key=len))[-1]
    spaces_after_question = table_length - len(question) - 3
    if len(question) > basic_question_length:
        question_list = divide_question(question)
        question = ""
        for i in range(len(question_list)):
            if i < len(question_list) - 1:
                spaces_after_question = table_length - (len(question_list[i])) - 4
                question = question + question_list[i] + spaces_after_question * " " + "    ►\n ◄  "
            else:
                question = question + question_list[i]
                spaces_after_question = table_length - (len(question_list[i])) - 3
        number_of_spaces = int((table_length / 2) - 6)
    else:
        number_of_spaces = int((table_length / 2) - 6)
    if quizmaster:
        if prizes:
            print_quizmaster_with_prizes(game_level)
        else:
            print_quizmaster()
    print("  /" + "‾" * (table_length) + "\\")
    print(" ◄  " + question + " " * spaces_after_question + "   ►")
    print("  \\" + "_" * (table_length) + "/")
    print("\n")
    if show_answers:
        if len(longest_string) > number_of_spaces:
            print("   " + "_" * (number_of_spaces + 4) + "     " + "_" * (number_of_spaces + 4))
            number_of_spaces = number_of_spaces + 7
            number_of_parts = len(longest_string) / number_of_spaces
            if type(number_of_parts) == float:
                number_of_parts += 1
            answer_list_a = divide_answer(answer_values[0], number_of_parts)
            answer_list_b = divide_answer(answer_values[1], number_of_parts)
            answer_list_c = divide_answer(answer_values[2], number_of_parts)
            answer_list_d = divide_answer(answer_values[3], number_of_parts)
            answers_lists = [answer_list_a, answer_list_b, answer_list_c, answer_list_d]
            longest_string_divided = int(number_of_parts)
            answer = ""
            index = 0
            for i in range(4):
                if i == 0 or i == 2:
                    first_bgcolor = ""
                    second_bgcolor = ""

                    for j in range(longest_string_divided + 1):
                        symbol = "♦"
                        first_symbol_color = fg.orange
                        first_char_color = fg.orange
                        second_symbol_color = fg.orange
                        second_char_color = fg.orange
                        if j == 0:
                            first_string = list(answers_.items())[i][j].upper() + ": " + fg.rs + answers_lists[index][j]
                            second_string =  list(answers_.items())[i + 1][j].upper() + ": " + fg.rs + \
                                            answers_lists[index + 1][j]
                            len_first_string = len("♦" + list(answers_.items())[i][j].upper() + ": "  + answers_lists[index][j])
                            len_second_string = len("♦" + list(answers_.items())[i + 1][j].upper() + ": "  + answers_lists[index + 1][j])
                        else:
                            first_string = " " * 4 + fg.rs + answers_lists[index][j]
                            second_string = " " * 4 + fg.rs + answers_lists[index + 1][j]
                            len_first_string = len(" " * 4 + answers_lists[index][j])
                            len_second_string = len(" " * 4 + answers_lists[index + 1][j])
                            symbol = ""
                            first_symbol_color = ""
                            first_char_color = ""
                            second_symbol_color = ""
                            second_char_color =  ""
                        first_spaces = number_of_spaces - len_first_string - 3
                        second_spaces = number_of_spaces - len_second_string - 3
                        first_string = first_string + " " * first_spaces
                        second_string = second_string + " " * second_spaces
                        if selected != "":
                            for answer_ in answers_:
                                if correct_answer != "" and correct_answer == list(answers_.keys())[index]:
                                    first_symbol_color = fg.white
                                    first_char_color = fg.black
                                    first_bgcolor = bg.green
                                if correct_answer != "" and correct_answer == list(answers_.keys())[index + 1]:
                                    second_bgcolor = bg.green
                                    second_symbol_color = fg.white
                                    second_char_color = fg.black

                                if list(answers_.keys())[index] == selected:
                                    for bg_color in colors_:
                                        if color == bg_color:
                                            first_symbol_color = fg.white
                                            first_char_color = fg.black
                                            first_bgcolor = colors_[color]

                                            first_string = first_string
                                if list(answers_.keys())[index + 1] == selected:
                                    for bg_color in colors_:
                                        if color == bg_color:
                                            second_symbol_color = fg.white
                                            second_char_color = fg.black
                                            second_bgcolor = colors_[color]

                                            second_string = second_string

                        answer = answer + " ◄|" + first_bgcolor + first_symbol_color + symbol + fg.rs + first_char_color + first_string + fg.rs + bg.rs + \
                                 "|►━◄|" + second_bgcolor + second_symbol_color + symbol + fg.rs + second_char_color  + second_string + fg.rs + bg.rs + "|►"
                        if j < longest_string_divided:
                            answer = answer + "\n"
                if i == 0:
                    answer = answer + "\n" + "   " + "‾" * (number_of_spaces - 3) + "     " + "‾" * (number_of_spaces - 3) + \
                             "\n" + "   " + "_" * (number_of_spaces - 3) + "     " + "_" * (number_of_spaces - 3) + "\n"
                index += 1
            print(answer)
            print("   " + "‾" * (number_of_spaces - 3) + "     " + "‾" * (number_of_spaces - 3))
        else:
            print("   " + "_" * (number_of_spaces + 4) + "     " + "_" * (number_of_spaces + 4))
            if selected != "":
                index = 0
                for i in answers_:
                    if i == selected:
                        for bg_color in colors_:
                            if color == bg_color:
                                answer_values[list(answers_).index(i)] = colors_[color] +  "♦" + fg.black + \
                                                                         list(answers_.items())[index][
                                                                             0].upper() + ": " + fg.rs + answers_[i] + " " * (
                                                                                 number_of_spaces - len(
                                                                             list(answers_.items())[index][
                                                                                 1])) + bg.rs
                    elif correct_answer != "" and i == correct_answer:
                        answer_values[list(answers_).index(i)] = bg.green  + "♦" + fg.black + list(answers_.items())[index][
                            0].upper() + ": " + fg.rs + answers_[i] + " " * (number_of_spaces - len(
                            list(answers_.items())[index][1])) + bg.rs
                    else:
                        answer_values[list(answers_).index(i)] = fg.orange + "♦"  + list(answers_.items())[index][0].upper() + ": " + fg.rs + \
                                                                 answers_[
                                                                     i] + " " * (number_of_spaces - len(
                            list(answers_.items())[index][1]))
                    index += 1
            else:
                for i in range(len(answers_)):
                    answer_values[i] = fg.orange + "♦" + list(answers_.items())[i][0].upper() + ": " + fg.rs + answer_values[i] + " " * (
                            number_of_spaces - len(list(answers_.items())[i][1]))

            print(" ◄|" + answer_values[0] + "|►━◄|" + answer_values[1] + "|►")
            print("   " + "‾" * (number_of_spaces + 4) + "     " + "‾" * (number_of_spaces + 4))
            print("   " + "_" * (number_of_spaces + 4) + "     " + "_" * (number_of_spaces + 4))
            print(" ◄|" + answer_values[2] + "|►━◄|" + answer_values[3] + "|►")
            print("   " + "‾" * (number_of_spaces + 4) + "     " + "‾" * (number_of_spaces + 4))


def print_fastest_fingers_table(question: str, answers_: {}, selected="", color="", correct_answer="", game_level=0,
                                quizmaster=True, prizes=True):
    colors_ = {
        "orange": bg.orange,
        "green": bg.green,
        "blue": bg.blue,
        "li_grey": bg.li_grey,
    }
    global table_length
    basic_question_length = 109
    answer_values = list(answers_.values())
    longest_string = list(sorted(answers_.values(), key=len))[-1]
    spaces_after_question = table_length - len(question) - 3
    if len(question) > basic_question_length:
        question_list = divide_question(question)
        question = ""
        for i in range(len(question_list)):
            if i < len(question_list) - 1:
                spaces_after_question = table_length - (len(question_list[i])) - 4
                question = question + question_list[i] + spaces_after_question * " " + "    ►\n ◄  "
            else:
                question = question + question_list[i]
                spaces_after_question = table_length - (len(question_list[i])) - 3
        number_of_spaces = int((table_length / 2) - 6)
    else:
        number_of_spaces = int((table_length / 2) - 6)
    if quizmaster:
        if prizes:
            print_quizmaster_with_prizes(game_level)
        else:
            print_quizmaster()
    print("  /" + "‾" * (table_length) + "\\")
    print(" ◄  " + question + " " * spaces_after_question + "   ►")
    print("  \\" + "_" * (table_length) + "/")
    print("\n")
    if len(longest_string) > number_of_spaces:
        print("   " + "_" * (number_of_spaces + 3) + "     " + "_" * (number_of_spaces + 5))
        number_of_spaces = number_of_spaces + 7
        number_of_parts = len(longest_string) / number_of_spaces
        if type(number_of_parts) == float:
            number_of_parts += 1
        answer_list_a = divide_answer(answer_values[0], number_of_parts)
        answer_list_b = divide_answer(answer_values[1], number_of_parts)
        answer_list_c = divide_answer(answer_values[2], number_of_parts)
        answer_list_d = divide_answer(answer_values[3], number_of_parts)
        answers_lists = [answer_list_a, answer_list_b, answer_list_c, answer_list_d]
        longest_string_divided = int(number_of_parts)
        answer = ""
        index = 0
        for i in range(4):
            if i == 0 or i == 2:
                for j in range(longest_string_divided + 1):
                    if j == 0:
                        first_string = " " + list(answers_.items())[i][j].upper() + ": " + answers_lists[index][j]
                        second_string = " " + list(answers_.items())[i + 1][j].upper() + ": " + \
                                        answers_lists[index + 1][j]
                    else:
                        first_string = " " * 3 + answers_lists[index][j]
                        second_string = " " * 3 + answers_lists[index + 1][j]
                    first_spaces = number_of_spaces - len(first_string) - 4
                    second_spaces = number_of_spaces - len(second_string) - 4
                    first_string = first_string + " " * first_spaces
                    second_string = second_string + " " * second_spaces
                    if selected != "":
                        for answer_ in answers_:
                            if correct_answer != "" and correct_answer == list(answers_.keys())[index]:
                                first_string = bg.green + fg.black + first_string + fg.rs + bg.rs
                            if correct_answer != "" and correct_answer == list(answers_.keys())[index + 1]:
                                second_string = bg.green + fg.black + second_string + fg.rs + bg.rs
                            if list(answers_.keys())[index] == selected or list(answers_.keys())[index] in selected:
                                if list(answers_.keys())[index] in selected:
                                    first_string = str(selected.index(list(answers_.items())[index][
                                                                          0]) + 1) + ": " + first_string
                                for bg_color in colors_:
                                    if color == bg_color:
                                        first_string = colors_[color] + fg.black + first_string + fg.rs + bg.rs
                            if list(answers_.keys())[index + 1] == selected and list(answers_.keys())[
                                index] in selected:
                                if list(answers_.keys())[index] in selected:
                                    second_string = str(selected.index(list(answers_.items())[index][
                                                                           0]) + 1) + ": " + first_string
                                for bg_color in colors_:
                                    if color == bg_color:
                                        second_string = colors_[color] + fg.black + second_string + fg.rs + bg.rs
                    answer = answer + " ◄|" + first_string + "|►━◄|" + second_string + "  |►"
                    if j < longest_string_divided:
                        answer = answer + "\n"
            if i == 0:
                answer = answer + "\n" + "   " + "‾" * (number_of_spaces - 4) + "     " + "‾" * (number_of_spaces - 2) + \
                         "\n" + "   " + "_" * (number_of_spaces - 4) + "     " + "_" * (number_of_spaces - 2) + "\n"
            index += 1
        print(answer)
        print("   " + "‾" * (number_of_spaces - 4) + "     " + "‾" * (number_of_spaces - 2))
    else:
        print("   " + "_" * (number_of_spaces + 4) + "     " + "_" * (number_of_spaces + 4))
        if selected != "":
            index = 0
            for i in answers_:
                if i == selected or list(answers_.keys())[index] in selected:
                    for bg_color in colors_:
                        if color == bg_color:
                            answer_values[list(answers_).index(i)] = colors_[color] + fg.black + " " + str(
                                selected.index(list(answers_.items())[index][
                                                   0]) + 1) + ": " + answers_[i] + " " * (number_of_spaces - len(
                                list(answers_.items())[index][1])) + fg.rs + bg.rs
                elif correct_answer != "" and i == correct_answer:
                    answer_values[list(answers_).index(i)] = bg.green + fg.black + " " + str(
                        selected.index(list(answers_.items())[index][
                                           0]) + 1) + ": " + answers_[i] + " " * (number_of_spaces - len(
                        list(answers_.items())[index][1])) + fg.rs + bg.rs
                else:
                    answer_values[list(answers_).index(i)] = " " + list(answers_.items())[index][0].upper() + ": " + \
                                                             answers_[i] + " " * (number_of_spaces - len(
                        list(answers_.items())[index][1]))
                index += 1
        else:
            for i in range(len(answers_)):
                answer_values[i] = " " + list(answers_.items())[i][0].upper() + ": " + answer_values[i] + " " * (
                        number_of_spaces - len(list(answers_.items())[i][1]))

        print(" ◄|" + answer_values[0] + "|►━◄|" + answer_values[1] + "|►")
        print("   " + "‾" * (number_of_spaces + 4) + "     " + "‾" * (number_of_spaces + 4))
        print("   " + "_" * (number_of_spaces + 4) + "     " + "_" * (number_of_spaces + 4))
        print(" ◄|" + answer_values[2] + "|►━◄|" + answer_values[3] + "|►")
        print("   " + "‾" * (number_of_spaces + 4) + "     " + "‾" * (number_of_spaces + 4))


def print_quizmaster_with_prizes(level: int):
    prizes = util.open_file("prizes_" + str(game_language).lower(), "r")[::-1]
    prizes_ = util.open_file("prizes_" + str(game_language).lower(), "r")[::-1]
    index = 0
    len_al = 45
    helps = [" 50 : 50 ", "   \_] ", "   ☺ ☺ ☺   "]
    helps_ = [" 50 : 50 ", "   \_] ", "   ☺ ☺ ☺   "]
    i = 0
    for key, value in help_types.items():
        if not value:
            helps_[i] = fg.red + helps[i] + fg.rs
        i += 1
    help_length = len(helps[0] + helps[1] + helps[2]) + 2
    print(" " * 87 + " " + help_length * "_")
    print(" " * 87 + "|" + (help_length - 2) * " " + "  |")
    print(" " * 87 + "|" + helps_[0] + helps_[1] + helps_[2] + "  |")
    print(" " * 87 + "|" + help_length * "_" + "|")

    for line in util.open_file("quizmaster", "r", ";", "/text_files/", strip=False):
        if index < len(prizes):
            missing_space = len_al - len(line[0])
            round_number = str(len(prizes) - index)
            if len(prizes) - index < 10:
                round_number = " " + round_number
            box_space = len(round_number + " ♦ " + prizes[index][0]) + 1
            if len(prizes) - index == level + 1:
                prizes_[index][0] = bg.orange + fg.black + prizes[index][0] + fg.rs + bg.rs
            if len(prizes) - index <= level:
                if len(prizes) - index in [5, 10, 15]:
                    print(line[0] + " " * missing_space + "| " + round_number + " ♦ " + prizes_[index][
                        0] + fg.rs + " " * (help_length - box_space) + "|")
                else:
                    print(line[0] + " " * missing_space + "| " + round_number + " ♦ " + fg.orange + prizes_[index][
                        0] + fg.rs + " " * (help_length - box_space) + "|")
            else:
                if len(prizes) - index in [5, 10, 15]:
                    print(line[0] + " " * missing_space + "| " + round_number + "   " + prizes_[index][0] + " " * (
                            help_length - box_space) + "|")
                else:
                    print(line[0] + " " * missing_space + "| " + round_number + "   " + fg.orange + prizes_[index][
                        0] + fg.rs + " " * (help_length - box_space) + "|")
        elif index == len(prizes):
            print(line[0] + " " * (missing_space + 3) + help_length * "‾")
        else:
            print(line[0])
        index += 1


def print_quizmaster():
    for line in util.open_file("quizmaster", "r", ";", "/text_files/", strip=False):
        print(line[0])


def audience_help(question, answers: {}, correct_value: str, game_level):
    if util.game_language == util.Language.HUNGARIAN.name:
        options = []
        for key in answers:
            if answers[key] != "":
                options.append(key)
        if options == ["a", "b"]:
            prolouge = "audience_a_b"
        elif options == ["a", "c"]:
            prolouge = "audience_a_b"
        elif options == ["c", "d"]:
            prolouge = "audience_c_d"
        else:
            audience_prolouges = ["audience_isnt_calm", "then_ask_audience",
                                  "no_audience", "audience_intro","audience_intro_1", "audience_intro_2", "audience_intro_3", "audience_intro_4",
                                  "audience_intro_5", "audience_intro_6"]
            prolouge = random.choice(audience_prolouges)
        util.play_sound(prolouge, 0, dir="audience", timer=True)
    len_al = 45
    percent_color = bg(200, 35, 254)
    answers_list = list(answers.keys())
    if util.game_language == util.Language.HUNGARIAN.name:
        util.play_sound("push_your_buttons", 0, dir="audience")
        time.sleep(2)
    else:
        util.play_sound("audience", 0, general=True)
    util.clear_screen()
    len_window = 21

    for i in range(len(answers_list)):
        answers_list = list(answers.keys())
        chances = get_chances(answers, correct_value)
        string_value = ""
        values = []
        for key, value in sorted(chances.items()):
            values.append(round(value / 10))
            next_value = str(value)
            if len(next_value) == 1:
                next_value = next_value + " "
            string_value = string_value + " " + next_value + "% "
        index = 0
        for line in util.open_file("quizmaster", "r", ";", "/text_files/", strip=False):
            percentages = ""
            missing_space = len_al - len(line[0])
            if index == 0:
                print(line[0] + " " * (missing_space + 1) + "_" * (len_window - 1))
            elif index == 1:
                print(line[0] + " " * missing_space + "|" + string_value + "|")
            elif index == 2:
                print(line[0] + " " * missing_space + "|" + (len_window - 1) * " " + "|")
            else:
                if index < 13:
                    for j in range(10):
                        if j == (index - 3):
                            if values[0] >= 10 - j:
                                percentages = percentages + percent_color + "   " + bg.rs + "  "
                            else:
                                percentages = percentages + "     "
                            if values[1] >= 10 - j:
                                percentages = percentages + percent_color + "   " + bg.rs + "  "
                            else:
                                percentages = percentages + "     "
                            if values[2] >= 10 - j:
                                percentages = percentages + percent_color + "   " + bg.rs + "  "
                            else:
                                percentages = percentages + "     "
                            if values[3] >= 10 - j:
                                percentages = percentages + percent_color + "   " + bg.rs
                            else:
                                percentages = percentages + "   "
                    print(line[0] + " " * (missing_space) + "| " + percentages + " |")
                elif index == 13:
                    print(line[0] + " " * (
                        missing_space) + "|" + fg.orange + rs.dim_bold + "  A ♦  B ♦  C ♦  D " + fg.rs + " |")
                elif index == 14:
                    print(line[0] + " " * (missing_space + 1) + "‾" * (len_window - 1))
                else:
                    print(line[0])
            index += 1
        print_quiz_table(question, answers, game_level=game_level, quizmaster=False)
        time.sleep(1)
        if i < len(answers_list) - 1:
            util.clear_screen()
            i += 1
        else:
            util.play_sound("audience_end", 0, general=True)
            time.sleep(1)
            if util.game_language == util.Language.HUNGARIAN.name:
                audience_after_sounds = ["after_audience", "after_audience_2", "audience_false", "you_disagree_audience", "weights_a_lot", "believe_audience", "audience_random"]
                after_sound = random.choice(audience_after_sounds)
                util.play_sound(after_sound, 0, dir="audience", timer=True)


def telephone_help(question: str, answers: {}, correct_answer: str, player_name: str):
    if util.game_language == util.Language.HUNGARIAN.name:
        before_phone_sounds = ["if_you_want_phone_then_i_agree",  "i_didnt_want_to_advise_phone", "we_dont_phone", "phone_broke", "we_dont_phone_two"]
        before_sound = random.choice(before_phone_sounds)
        util.play_sound(before_sound, 0, dir="phone", timer=True)
    print("\n   " + language_dictionary[game_language].quiz.phone_prompt)
    phone = handle_user_input(question, answers,  correct_answer, help=True)
    call_text_files = ["mum_phone_" + str(game_language).lower(),
                       "dad_phone_" + str(game_language).lower(),
                       "teacher_phone_" + str(game_language).lower(),
                       "yoda_master_phone_" + str(game_language).lower()
                       ]
    conversation = ""
    if util.game_language == util.Language.HUNGARIAN.name:
        dial_sound = "colleagues_are_dialing"
        util.play_sound(dial_sound, 0, dir="phone", timer=True)
    for i in range(len(call_text_files)):
        if phone.lower() == call_text_files[i][0]:
            conversation = (util.open_file(call_text_files[i], 'r', separator=";"))
            if phone.lower() == "t":
                util.play_sound("teacher_first_part", 0, dir="phone", timer=True)
                util.play_sound(player_name, 0, dir="players", timer=True)
                util.play_sound("teacher_second_part", 0, dir="phone", timer=True)

            else:
                util.play_sound("phone_ring", 0, general=True)
                time.sleep(2)
            util.play_sound("phone_call", 0, general=True)
    len_al = 45
    util.clear_screen()
    len_window = 5
    then = time.time()
    text = ""
    now = 0.0
    for i in range(30):
        index = 0
        for line in util.open_file("quizmaster", "r", ";", "/text_files/", strip=False):

            missing_space = len_al - len(line[0])
            if index == 0:
                print("\n\n\n\n" + line[0] + " " * (missing_space + 1) + "_" * (len_window - 1))
            elif index == 1:
                print(line[0] + " " * missing_space + "|" + (len_window - 1) * " " + "|")
            else:
                if index == 2:
                    now = time.time()
                    print(line[0] + " " * (missing_space) + "| " + fg.orange + str(30 - int(now - then)) + fg.rs + " |")
                    print(line[0] + " " * (missing_space) + "|" + "_" * (len_window - 1) + "|")
                else:
                    print(line[0])
            index += 1
        print_quiz_table(question, answers, quizmaster=False)
        if i == 0:
            text = "  " + text + "\n" + "   " + conversation[0][0] + " \n" + "   " + question + " " + ", ".join(
                list(answers.values()))
        elif i == len(conversation) - 1:
            if phone == "y":
                text = "  " + text + "\n" + "   " + conversation[5][0] + " " + correct_answer.upper()
            else:
                text = "  " + text + "\n" + "   " + conversation[4][0] + " " + correct_answer.upper()
            print(text)
            break
        elif i == len(conversation) - 2:
            time.sleep(2)
            text = text + "\n" + "   " + conversation[i][0]
        else:
            text = text + "\n" + "   " + conversation[i][0]
        print(text)
        time.sleep(2)
        if i < 30:
            util.clear_screen()
            i += 1
    util.play_sound('phone_call_ends', 0, general=True)
    time.sleep(5)
    if util.game_language == util.Language.HUNGARIAN.name:
        after_sound = "over_30_secs"
        util.play_sound(after_sound, 0, dir="phone", timer=True)
    print("\n   " + language_dictionary[game_language].quiz.call_duration, int(now - then),
          language_dictionary[game_language].quiz.call_seconds)
    util.stop_sound()


def print_prizes_with_quizmaster(level: int, nullprize=False, special_text="", bg_color=bg.blue):
    prizes = util.open_file("prizes_" + str(game_language).lower(), "r")
    util.clear_screen()
    global table_length
    decor_str = " ♦ "
    prize = decor_str + prizes[level][0] + decor_str
    if nullprize == True:
        if util.game_language == util.Language.HUNGARIAN.name:
            prize = "0 Ft"
        if util.game_language == util.Language.ENGLISH.name:
            prize = "£0"
    if special_text != "":
        prize = special_text
    prize_length = len(prize)
    number_of_spaces = int((table_length - prize_length) / 2)
    if prize_length % 2 == 0:
        prize = prize + " "
    for i in range(4):
        print("\r")
    for line in util.open_file("quizmaster", "r", ";", "/text_files/", strip=False):
        print(line[0])
    print("  /" + bg_color + "‾" * (table_length) + bg.rs + "\\")
    print(" ◄ " + bg_color + fg.orange + number_of_spaces * " " + prize + fg.rs + " " * number_of_spaces + bg.rs + " ►")
    print("  \\" + bg_color +  "_" * (table_length) +  bg.rs +"/")


def show_game_structure():
    import time, msvcrt
    # TODO: only works on win
    timeout = 2
    startTime = time.time()
    inp = None
    print(language_dictionary[util.game_language].quiz.skip_prompt)
    while True:
        if msvcrt.kbhit():
            global game_language
            inp = msvcrt.getch()
            break
        elif time.time() - startTime > timeout:
            break
    util.clear_screen()
    if inp:
        return

    game_language = util.game_language
    prizes = util.open_file("prizes_" + str(game_language).lower(), "r")
    if game_language == util.Language.HUNGARIAN.name:
        util.play_sound("prizes_description", 0, dir="intro")
        print_helps()
        print("\n\n")
        for i in range(len(prizes)):
            for j in range(len(prizes)):
                round_number = str(len(prizes) - j)
                if len(prizes) - j < 10:
                    round_number = " " + round_number
                if i == len(prizes) - j - 1:
                    print(round_number + " ♦ " + bg.orange + fg.black + prizes[::-1][j][0] + fg.rs + bg.rs)
                else:
                    if j == 5 or j == 10 or j == 0:
                        print(round_number + " ♦ " + prizes[::-1][j][0])
                    else:
                        print(round_number + " ♦ " + fg.orange + prizes[::-1][j][0] + fg.rs)
            if os.name == "nt":
                time.sleep(0.3)
            else:
                time.sleep(0.4)
            if i != 14:
                util.clear_screen()
                print_helps()
                print("\n\n")
        if os.name == "posix":
            time.sleep(2)
        else:
            time.sleep(0.7)
        util.clear_screen()
        print_helps()
        print("\n\n")
        for a in range(2):
            for b in range(len(prizes)):
                round_number = str(len(prizes) - b)
                if len(prizes) - b < 10:
                    round_number = " " + round_number
                if a == 0 and b == 10 or a == 1 and b == 5:
                    print(round_number + " ♦ " + bg.orange + fg.black + prizes[::-1][b][0] + fg.rs + bg.rs)
                else:
                    if b == 0 or b == 5 or b == 10:
                        print(round_number + " ♦ " + prizes[::-1][b][0])
                    else:
                        print(round_number + " ♦ " + fg.orange + prizes[::-1][b][0] + fg.rs)
            time.sleep(1)
            if a == 1 and os.name == "nt":
                time.sleep(0.4)
            util.clear_screen()
            print_helps()
            print("\n\n")
        util.play_sound("help_modules", 0, dir="intro")
        util.clear_screen()
        list_helps()
        time.sleep(3)
        util.clear_screen()
        print_helps()
        print("\n\n")
        print_prizes()
        util.play_sound("prologue_end", 0,  dir="intro", timer=True)
        util.clear_screen()
    else:
        print_helps()
        print("\n\n")
        print_prizes()
        time.sleep(4)
        util.clear_screen()


def print_helps(helps=None):
    if helps is None:
        helps = [" 50 : 50 ", "     \_] ", "  ☺ ☺ ☺  "]
    separator = fg.blue + "|" + fg.rs
    print(fg.blue + 31 * "-" + fg.rs)
    print(separator + helps[0] + separator + helps[1] + separator + helps[2] + separator)
    print(fg.blue + 31 * "-" + fg.rs)


def list_helps():
    halving_ = " 50 : 50 "
    telephone_ = "     \_] "
    audience_ = "  ☺ ☺ ☺  "
    helps_ = [[bg.orange + fg.black + halving_ + fg.rs + bg.rs, telephone_, audience_],
              [halving_, bg.orange + fg.black + telephone_ + fg.rs + bg.rs, audience_],
              [halving_, telephone_, bg.orange + fg.black + "  ☻ ☻ ☻  " + fg.rs + bg.rs]]

    for help_ in helps_:
        print_helps(help_)
        print("\n\n")
        print_prizes()
        if helps_.index(help_) < 2:
            time.sleep(1.3)
            util.clear_screen()


def print_prizes():
    game_language = util.game_language
    prizes = util.open_file("prizes_" + str(game_language).lower(), "r")
    for i in range(len(prizes)):
        round_number = str(len(prizes) - i)
        if len(prizes) - i < 10:
            round_number = " " + round_number
        if i == 5 or i == 10 or i == 0:
            print(round_number + " " + prizes[::-1][i][0])
        else:
            print(round_number + " " + fg.orange + prizes[::-1][i][0] + fg.rs)


def play_music(round: int):
    if round < 5:
        util.play_background_music(str(5), 0)
    else:
        util.play_background_music(str(round), 0)


def play_marked_sound(choise: str, level: int, last_one=""):
    sounds = []

    for answer in ["a", "b", "c", "d"]:
        if choise == answer:
            if choise == last_one and level > 0:
                sounds.append("mark_" + choise + "_again")
            else:
                sounds.append("mark_" + choise)
                sounds.append("mark_" + choise + "_1")
                sounds.append("mark_" + choise + "_2")
                if choise == "b":
                    sounds.append("poke_b")
                if choise in ["b", "d"]:
                    sounds.append("mark_" + choise + "_3")
                    sounds.append("mark_" + choise + "_4")

    sound = random.choice(sounds)
    util.play_sound(sound, 0, dir="mark", timer=True)

    sounds = []
    if level == 7:
        sounds = ["lets_see_500", "lets_see_500_1"]
    elif level == 8:
        sounds = ["lets_see_800", "lets_see_800_2"]
    elif level == 10:
        sounds = ["lets_see_3_million", "lets_see_3_million_2", "lets_see_3_million_3"]
    elif level == 13:
        sounds = ["lets_see_10_million"]
    else:
        sounds = ["lets_see"]
        for i in range(24):
            sounds.append("lets_see_" + str(i + 1))

    sound = random.choice(sounds)
    util.play_sound(sound, 0, dir="lets_see", timer=True)


def get_sound_list(attitude: str) -> {}:
    correct_sounds = ["you_must_mark", "you_came_for_money", "dont_sigh_yet", "hurry_up", "dont_let_me_speak", "dont_listen_to_me", "whatever_you_say_wow", "that_was_fast", "what_you_say_will_be", "watch_out_more_im_not_always_evil", "you_may_feel_im_hurrying", "final_or"]
    bad_sounds = ["you_mark_anyways", "i_wont_help_more", "calm", "look_at_my_eyes", "dont_want_to_say_dummy", "nooo", "dont_be_impatient", "so_you_gonna_poke", "but_i_helped_you"]
    other_sounds = ['be_careful_is_it_final', "in_this_show_i_have_to_ask_is_it_final", "i_must_ask_is_it_final", "final_or_final",
                    "take_that_as_final", "last_one_final", "take_the_risk", "i_dont_help_more_if_you_wish_we_mark", "pay_attention_to_the_quizmaster", "so_what_to_do",
                    "you_see_clueless"]

    if attitude == util.QuizMasterAttitude.FRIENDLY.name:
        for i in range(2):
            correct_sounds.append(other_sounds[i])
            bad_sounds.append(other_sounds[i])
        return {"correct_sounds" : correct_sounds, "bad_sounds": bad_sounds}
    elif attitude == util.QuizMasterAttitude.NEUTRAL.name:
        for sound in other_sounds:
            correct_sounds.append(sound)
            bad_sounds.append(sound)
        return {"correct_sounds" : correct_sounds, "bad_sounds": bad_sounds}
    elif attitude == util.QuizMasterAttitude.HOSTILE.name:
        return {"correct_sounds" : other_sounds, "bad_sounds": other_sounds}
    else:
        return {"correct_sounds" : [], "bad_sounds": []}


def handle_user_input(question: str, answers: dict, correct_answer: str, level=0, final_color="orange", out_of_game=False,
                      help=False) -> str:
    select_text = language_dictionary[game_language].quiz.select_answer
    last_input = ""
    sound_dir = ""
    if util.game_language == util.Language.HUNGARIAN.name:
        sound_list_dict = get_sound_list(util.quizmaster_attitude)
        bad_sounds = sound_list_dict['bad_sounds']
        correct_sounds = sound_list_dict['correct_sounds']

    if out_of_game:
        select_text = language_dictionary[game_language].quiz.select_answer_out

    while True:
        user_input = get_user_input()
        if not help:
            user_inputs = [[b'a', "a"], [b'b', "b"], [b'c', "c"], [b'd', "d"]]
            for input_ in user_inputs:
                if user_input == input_[0] or user_input == input_[1]:
                    if util.game_language == util.Language.HUNGARIAN.name:
                        sound_dir = "random"
                        thread_random(level, selected=input_[1], last_one=last_input)
                        if util.quizmaster_attitude != util.QuizMasterAttitude.NONE.name:
                            if input_[1] == correct_answer:
                                selected_sound = random.choice(correct_sounds)
                            else:
                                selected_sound = random.choice(bad_sounds)
                    util.clear_screen()
                    print_quiz_table(question, answers, game_level=level, selected=input_[1], color="li_grey")
                    print("\n\n   " + fg.grey + select_text + fg.rs)
                    if not out_of_game:
                        util.pause_music()
                    if util.game_language == util.Language.HUNGARIAN.name and util.quizmaster_attitude != util.QuizMasterAttitude.NONE.name:
                        if selected_sound.find("mark") != -1 or selected_sound.find("final") != -1:
                            sound_dir ="mark"
                        util.play_sound(selected_sound, 0, dir=sound_dir)
                    if not out_of_game:
                        util.continue_music()
                    last_input = input_[1]
                    while True:
                        user_input = get_user_input()
                        util.stop_sound()
                        if user_input == b'\r' or user_input == '<Ctrl-j>':
                            thread_random(level, working=False)
                            util.clear_screen()
                            print_quiz_table(question, answers, input_[1], final_color, game_level=level)
                            if not out_of_game:
                                util.pause_music()
                            if util.game_language == util.Language.HUNGARIAN.name and not out_of_game:
                                play_marked_sound(input_[1], level, last_one=last_input)
                            return input_[1]
                        if user_input not in input_:
                            break

            if not out_of_game:
                if user_input == b'h' or user_input == "h":
                    return "h"
                if user_input == b's' or user_input == "s":
                    return "h"
                if user_input == b'k' or user_input == "k":
                    return "t"
                if user_input == b't' or user_input == "t":
                    return "t"
            if user_input == b'\x1b' or user_input == '<ESC>':
                return "esc"

        else:
            if user_input == b'a' or user_input == "a":
                return "a"
            if user_input == b'd' or user_input == "d":
                return "d"
            if user_input == b'f' or user_input == "f":
                return "h"
            if user_input == b'm' or user_input == "m":
                return "m"
            if user_input == b'p' or user_input == "p":
                return "d"
            if user_input == b't' or user_input == "t":
                return "t"
            if user_input == b'k' or user_input == "k":
                return "a"
            if user_input == b'h' or user_input == "h":
                return "h"
            if user_input == b's' or user_input == "s":
                return "h"
            if user_input == b'y' or user_input == "y":
                return "y"
            if user_input == b'\x1b' or user_input == '<ESC>':
                return "esc"


def handle_fastest_fingers_first_input(question: str, answers: dict, level: int, selected: str,
                                       final_color="orange") -> str:
    select_text = language_dictionary[game_language].quiz.select_answer_out
    while True:
        user_input = get_user_input()
        user_inputs = [[b'a', "a"], [b'b', "b"], [b'c', "c"], [b'd', "d"]]

        for input_ in user_inputs:
            if user_input == input_[0] or user_input == input_[1]:
                util.clear_screen()
                print_fastest_fingers_table(question, answers, selected + input_[1], final_color, game_level=level,
                                            quizmaster=True, prizes=False)
                print("\n\n   " + fg.grey + select_text + fg.rs)
                return input_[1]

        if user_input == b'\x1b' or user_input == '<ESC>':
            return "esc"


def get_user_input() -> bytes:
    if util.operating_system == "posix":
        user_input = helpers.return_user_input_linux()
    else:
        user_input = helpers.return_user_input_windows()

    return user_input


def quit_quiz(score: int, name, topic):
    thread_random(score, working=False)
    util.play_sound("time_end_horn", 0, general=True, timer=True)
    util.stop_music()
    if game_language == util.Language.HUNGARIAN.name:
        exit_sounds = ["exit_epilogue", "delay", "what_a_game_it_was", "how_ugly_sound_it_has"]
        if score < 5:
            exit_sounds.append("this_not_ended_well")
        sound = random.choice(exit_sounds)
        util.play_sound(sound, 0, dir="out_of_game")
    if score > 0:
        write_content_to_file("scores.json",
                              {"user": name, "topic": topic, "score": score, "time": time.ctime(time.time())})
    menu.return_prompt()
    util.stop_sound()


def quit_fastest_fingers():
    menu.return_prompt()
    util.stop_sound()
