import os
import random
import json
import time
from sty import Style, RgbFg, fg, bg
import millionaire.menu.menu as menu
import millionaire.util.util as util
import millionaire.menu.helpers as helpers

operating_system = os.name
fg.purple = Style(RgbFg(148, 0, 211))
fg.orange = Style(RgbFg(255, 150, 50))
fg.green = Style(RgbFg(0, 255, 0))
bg.orange = bg(255, 150, 50)
languages = util.available_languages
language_dictionary = util.language_dictionary
table_length = 113


def play():
    global game_language, question_lines_easy, question_lines_medium, question_lines_hard
    game_language = util.game_language
    global question_topics
    question_topics = util.question_topics
    global question_difficulty
    question_difficulty = util.question_difficulty
    player_name = input(language_dictionary[game_language].quiz.player_name_prompt)
    score = 0
    help_types = {"halving": True, "telephone": True, "audience": True}
    util.clear_screen()
    util.play_sound("start", 0)
    show_game_structure()
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
                                                   "/text_files/topics/" + str(game_language).lower() + "/" + str(topic.name).lower() + "/" + str(level.name).lower() + "/"):
                            question_lines.append(line)
            else:
                if topic.name != util.Topics.ALL.name:
                    for line in util.open_file(str(util.Difficulty.EASY.name).lower(), "r", ";",
                                               "/text_files/topics/" + str(game_language).lower() + "/" + str(topic.name).lower() + "/" + str(util.Difficulty.EASY.name).lower() + "/"):
                        question_lines_easy.append(line)
                    for line in util.open_file(str(util.Difficulty.MEDIUM.name).lower(), "r", ";",
                                               "/text_files/topics/" + str(game_language).lower() + "/" + str(topic.name).lower() + "/" + str(util.Difficulty.MEDIUM.name).lower() + "/"):
                        question_lines_medium.append(line)
                    for line in util.open_file(str(util.Difficulty.HARD.name).lower(), "r", ";",
                                               "/text_files/topics/" + str(game_language).lower() + "/" + str(topic.name).lower() + "/" + str(util.Difficulty.HARD.name).lower() + "/"):
                        question_lines_hard.append(line)
    else:
        for level in util.Difficulty:
            if question_difficulty == level.name and level.name != util.Difficulty.ALL.name:
                for line in util.open_file(str(level.name).lower(), "r", ";",
                                           "/text_files/topics/" + str(game_language).lower() + "/" + str(question_topics).lower() + "/" + str(level.name).lower() + "/"):
                    question_lines.append(line)
            else:
                if level.name != util.Difficulty.ALL.name:
                    for line in util.open_file(str(util.Difficulty(level).name).lower(), "r", ";",
                                               "/text_files/topics/" + str(game_language).lower() + "/" + str(question_topics).lower() + "/" + str(level.name).lower() + "/"):
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
    for i in range(15):
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
        if i == 0:
            time.sleep(4)
        print_quiz_table(question, shuffled_answers)
        play_music(i)
        if game_language == util.Language.HUNGARIAN.name:
            print("\n", language_dictionary[game_language].quiz.select_answer)
            answer = handle_user_input(question, shuffled_answers, i)
        else:
            answer = safe_input(
                language_dictionary[game_language].quiz.select_answer,
                ["a", "b", "c", "d", "h", "t"])
        correct_answer_key = get_dictionary_key_by_value(shuffled_answers, question_lines[i][1])
        correct_answer_value = question_lines[i][1]
        util.stop_sound()
        while answer not in list(answers.keys()):
            if answer == "t":
                util.clear_screen()
                print_quiz_table(question, shuffled_answers)
                if util.game_language == util.Language.HUNGARIAN.name:
                    util.play_sound("music_off", 0)
                if game_language == util.Language.HUNGARIAN.name:
                    print("\n", language_dictionary[game_language].quiz.select_answer_out)
                    answer = handle_user_input(question, shuffled_answers, i)
                else:
                    answer = safe_input(
                        language_dictionary[game_language].quiz.select_answer_out,
                        ["a", "b", "c", "d"])
                util.clear_screen()
                print_quiz_table(question, shuffled_answers, answer, "blue")
                util.play_sound("marked", 0)
                time.sleep(2)
                is_correct = check_answer(answer, correct_answer_key)
                if is_correct:
                    util.clear_screen()
                    print_quiz_table(question, shuffled_answers, answer, "green")
                    if i > 9:
                        print(bg.orange + show_prize(9) + bg.rs)
                        time.sleep(1)
                    elif i > 4:
                        print(bg.orange + show_prize(4) + bg.rs)
                        util.play_sound("won_hundred_bucks", 0)
                        time.sleep(7)
                    else:
                        print(fg.blue + language_dictionary[game_language].quiz.correct_answer_out + fg.rs)
                        util.play_sound("show_stop", 0)
                        time.sleep(1)
                else:
                    util.play_sound("bad_answer", 0)
                    util.clear_screen()
                    print_quiz_table(question, shuffled_answers, answer, "blue", correct_answer=correct_answer_key)
                    print(fg.red + language_dictionary[game_language].quiz.incorrect_answer + fg.rs)
                    if util.game_language == util.Language.HUNGARIAN.name:
                        util.play_sound("so_sorry", 0)
                    time.sleep(1)
                menu.return_prompt()
                util.clear_screen()
                if score != 0:
                    write_content_to_file("scores.json", {"user": player_name, "topic": question_topics, "score": score,
                                                          "time": time.ctime(time.time())})
                return
            if answer == "h":
                if list(help_types.values()).count(True) == len(
                        help_types) and game_language == util.Language.HUNGARIAN.name:
                    util.play_sound("still_have_all_helps", 0)
                util.clear_screen()
                print_quiz_table(question, shuffled_answers)
                help_functions = {"halving": halving, "telephone": telephone_help, "audience": audience_help}
                chosen_help_type = safe_input(language_dictionary[game_language].quiz.help_selection,
                                              ["a", "t", "h"])
                for x in range(len(help_types)):
                    if chosen_help_type.lower() == list(help_types)[x][0]:
                        if help_types[list(help_types)[x]]:
                            if list(help_types)[x] == "halving":
                                shuffled_answers = list(help_functions.values())[x](question, shuffled_answers,
                                                                                    correct_answer_value)
                                for a in range(len(answer_list)):
                                    answer_list[a] = list(shuffled_answers.values())[a]
                                print_quiz_table(question, shuffled_answers)
                            else:
                                list(help_functions.values())[x](question, shuffled_answers, correct_answer_value)
                            help_types[list(help_types)[x]] = False
                            break
                        else:
                            print(language_dictionary[game_language].quiz.help_disabled + list(help_types)[x] + " " +
                                  language_dictionary[game_language].quiz.help)
                if game_language == util.Language.HUNGARIAN.name:
                    print("\n", language_dictionary[game_language].quiz.select_answer)
                    answer = handle_user_input(question, shuffled_answers, i)
                else:
                    answer = safe_input(
                        language_dictionary[game_language].quiz.select_answer,
                        ["a", "b", "c", "d", "h", "t"])
                time.sleep(2)
        util.clear_screen()
        print_quiz_table(question, shuffled_answers, answer, "orange")
        util.play_sound("marked", 0)
        is_correct = check_answer(answer, correct_answer_key)
        time.sleep(2)
        if is_correct:
            score += 1
            if i < 14:
                util.play_sound("correct_answer", 0)
                util.clear_screen()
                print_quiz_table(question, shuffled_answers, answer, "green")
                time.sleep(2)
                util.clear_screen()
                if len(question) % 2 == 0:
                    question = question + " "
                if i == 4:
                    print("\n" + " " * 20 + fg.yellow + language_dictionary[
                        game_language].quiz.guaranteed_prize + show_prize(i) + fg.rs)
                    util.play_sound("won_hundred_bucks", 0)
                    print("-" * (len(question) + len(show_prize(i)) + 8))
                    print("|", bg.orange, fg.black, " " * (int(len(question) / 2)) + show_prize(i), fg.rs,
                          " " * (int(len(question) / 2)), bg.rs, "|")
                    print("-" * (len(question) + len(show_prize(i)) + 8))
                    time.sleep(7)
                elif i == 9:
                    print("\n" + " " * 20 + fg.yellow + language_dictionary[
                        game_language].quiz.guaranteed_prize + show_prize(i) + fg.rs)
                    if util.game_language == util.Language.HUNGARIAN.name:
                        util.play_sound("now_comes_hard_part", 0)
                    print("-" * (len(question) + len(show_prize(i)) + 8))
                    print("|", bg.orange, fg.black, " " * (int(len(question) / 2)) + show_prize(i), fg.rs,
                          " " * (int(len(question) / 2)), bg.rs, "|")
                    print("-" * (len(question) + len(show_prize(i)) + 8))
                    time.sleep(3)
                else:
                    print("-" * (len(question) + len(show_prize(i)) + 8))
                    print("|", bg.orange, fg.black, " " * (int(len(question) / 2)) + show_prize(i), fg.rs,
                          " " * (int(len(question) / 2)), bg.rs, "|")
                    print("-" * (len(question) + len(show_prize(i)) + 8))
                    time.sleep(2)
            else:
                if util.game_language == util.Language.HUNGARIAN.name:
                    util.play_sound("after_marking", 0)
                    time.sleep(4)
                    util.play_sound("great_logic", 0)
                time.sleep(1)
                util.clear_screen()
                print("\n" + " " * 20 + fg.purple + language_dictionary[game_language].quiz.won_prize + show_prize(
                    i) + " !" + fg.rs)
                util.play_sound("winning_theme", 0)
                time.sleep(35)
                menu.return_prompt()
        else:
            util.play_sound("bad_answer", 0)
            util.clear_screen()
            print_quiz_table(question, shuffled_answers, answer, "orange", correct_answer=correct_answer_key)
            time.sleep(2)
            if game_language == util.Language.HUNGARIAN.name:
                util.play_sound("so_sorry", 0)
                time.sleep(1)
            print(fg.red + language_dictionary[game_language].quiz.incorrect_answer + fg.rs)
            menu.return_prompt()
            util.clear_screen()
            if score != 0:
                write_content_to_file("scores.json", {"user": player_name, "topic": question_topics, "score": score,
                                                      "time": time.ctime(time.time())})
            return
        util.clear_screen()

    write_content_to_file("scores.json", {"user": player_name, "topic": question_topics, "score": score,
                                          "time": time.ctime(time.time())})
    return


def safe_input(input_text: str, allowed_list_of_letters: list) -> str:
    answer = input(input_text)
    if answer not in allowed_list_of_letters:
        print(language_dictionary[game_language].quiz.allowed_letters_error + ' '.join(allowed_list_of_letters) +
              language_dictionary[game_language].quiz.allowed)
    while answer not in allowed_list_of_letters:
        answer = input(input_text)
    time.sleep(1)

    return answer


def get_dictionary_key_by_value(dictionary: {}, value: str) -> str:
    for choice, answerValue in dict.items(dictionary):
        if answerValue == value:
            return choice


def check_answer(answer: str, correct_answer: str) -> bool:
    return answer == correct_answer


def show_prize(round_number: int) -> str:
    prizes = util.open_file("prizes_" + str(game_language).lower(), "r")
    return prizes[round_number][0]


def print_phone_conversation(text: list, question: str, answers: {}, good_answer: str):
    util.play_sound("phone_ring", 0)
    time.sleep(2)
    util.play_sound("phone_call", 0)
    then = time.time()
    for i in range(len(text)):
        print(fg.orange + str(30 - int(time.time() - then)) + fg.rs)
        time.sleep(2)
        if i == 0:
            print(text[i][0] + " " + question + " " + ",".join(list(answers.values())))
        elif i == len(text) - 1:
            print(text[i][0] + " " + good_answer.upper())
        else:
            print(text[i][0])
    print(fg.orange + str(30 - int(time.time() - then)) + fg.rs)
    now = time.time()
    util.play_sound('phone_call', 30.0)
    time.sleep(3)
    print(language_dictionary[game_language].quiz.call_duration, int(now - then),
          language_dictionary[game_language].quiz.call_seconds)
    util.stop_sound()


def telephone_help(question: str, answers: {}, correct_answer: str):
    phone = safe_input(language_dictionary[game_language].quiz.phone_prompt,
                       ["m", "d", "t", "y"])
    call_text_files = ["mum_phone_" + str(game_language).lower(),
                       "dad_phone_" + str(game_language).lower(),
                       "teacher_phone_" + str(game_language).lower(),
                       "yoda_master_phone_" + str(game_language).lower()
                       ]
    for i in range(len(call_text_files)):
        if phone.lower() == call_text_files[i][0]:
            conversation = (util.open_file(call_text_files[i], 'r', separator=";"))
            print_phone_conversation(conversation, question, answers, correct_answer)


def halving(question: str, answers: {}, correct_answer: str) -> dict:
    if util.game_language == util.Language.HUNGARIAN.name:
        util.play_sound("lets_take_two", 0)
    util.clear_screen()
    time.sleep(2)
    util.play_sound("halving", 0)
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


def audience_help(question: str, answers: {}, correct_value: str):
    if util.game_language == util.Language.HUNGARIAN.name:
        util.play_sound("push_your_buttons", 0)
        time.sleep(3)
    else:
        util.play_sound("audience", 0)
    util.clear_screen()
    answers_list = list(answers.keys())
    for i in range(len(answers_list)):
        print(question)
        chances = get_chances(answers, correct_value)
        print("\n")
        for key, value in sorted(chances.items()):
            string_value = str(value)
            if len(string_value) == 1:
                string_value = string_value + " "
            print(key.upper() + " : " + string_value + "% " + bg.orange + value * " " + bg.rs + " " + str(answers[key]))
            print("\n")
        time.sleep(1)
        if i != len(answers_list) - 1:
            util.clear_screen()


def get_chances(answers: {}, correct_value: str) -> dict:
    answers_list = list(answers.keys())
    chances_dict = {}
    correct_answer = get_dictionary_key_by_value(answers, correct_value)
    chances_dict[correct_answer] = random.randrange(40, 89)
    answers_list.pop(answers_list.index(correct_answer))
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


def divide_answer(answer: str, number_of_parts: int) -> list:
    answer_parts = []
    basic_question_length = 109
    basic_answer_length = int((basic_question_length / 2) - 5)
    for i in range(number_of_parts + 1):
        if len(answer[i:basic_answer_length * (i + 1)]) > 0:
            index = basic_answer_length * i
            answer_parts.append(answer[index:basic_answer_length * (i + 1)])
        else:
            answer_parts.append("")

    return answer_parts


def print_quiz_table(question: str, answers_: {}, selected="", color="", correct_answer=""):
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
                question = question + question_list[i] + spaces_after_question * " " + " |\n| "
            else:
                question = question + question_list[i]
                spaces_after_question = table_length - (len(question_list[i])) - 3
        number_of_spaces = int((table_length / 2) - 6)
    else:
        number_of_spaces = int((table_length / 2) - 6)

    print("-" * (table_length))
    print("| " + question + " " * spaces_after_question + "|")
    print("-" * (table_length))
    print("\n")
    print("-" * table_length)
    if len(longest_string) > number_of_spaces:
        number_of_spaces = number_of_spaces + 7
        number_of_parts = int(len(longest_string) / number_of_spaces)
        answer_list_a = divide_answer(answer_values[0], number_of_parts)
        answer_list_b = divide_answer(answer_values[1], number_of_parts)
        answer_list_c = divide_answer(answer_values[2], number_of_parts)
        answer_list_d = divide_answer(answer_values[3], number_of_parts)
        answers_lists = [answer_list_a, answer_list_b, answer_list_c, answer_list_d]
        longest_string_divided = int(len(longest_string) / number_of_spaces)
        answer = ""
        index = 0
        for i in range(4):
            if i == 0 or i == 2:
                for j in range(longest_string_divided + 1):
                    if j == 0:
                        first_string = list(answers_.items())[i][j].upper() + ": " + answers_lists[index][j]
                        second_string = list(answers_.items())[i + 1][j].upper() + ": " + answers_lists[index + 1][j]
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
                            if list(answers_.keys())[index] == selected:
                                if color == "orange":
                                    first_string = bg.orange + fg.black + first_string + fg.rs + bg.rs
                                if color == "green":
                                    first_string = bg.green + fg.black + first_string + fg.rs + bg.rs
                                if color == "blue":
                                    first_string = bg.blue + fg.black + first_string + fg.rs + bg.rs
                            if list(answers_.keys())[index + 1] == selected:
                                if color == "orange":
                                    second_string = bg.orange + fg.black + second_string + fg.rs + bg.rs
                                if color == "green":
                                    second_string = bg.green + fg.black + second_string + fg.rs + bg.rs
                                if color == "blue":
                                    second_string = bg.blue + fg.black + second_string + fg.rs + bg.rs
                    answer = answer + "| " + first_string + " | " + second_string + " |"
                    if j < longest_string_divided:
                        answer = answer + "\n"
            if i == 0:
                answer = answer + "\n" + "-" * table_length + "\n"
            index += 1
        print(answer)
    else:
        if selected != "":
            index = 0
            for i in answers_:
                if i == selected:
                    if color == "orange":
                        answer_values[list(answers_).index(i)] = bg.orange + fg.black + list(answers_.items())[index][
                            0].upper() + ": " + answers_[i] + " " * (number_of_spaces - len(
                            list(answers_.items())[index][1])) + fg.rs + bg.rs
                    if color == "green":
                        answer_values[list(answers_).index(i)] = bg.green + fg.black + list(answers_.items())[index][
                            0].upper() + ": " + answers_[i] + " " * (number_of_spaces - len(
                            list(answers_.items())[index][1])) + fg.rs + bg.rs
                    if color == "blue":
                        answer_values[list(answers_).index(i)] = bg.blue + fg.black + list(answers_.items())[index][
                            0].upper() + ": " + answers_[i] + " " * (number_of_spaces - len(
                            list(answers_.items())[index][1])) + fg.rs + bg.rs
                elif correct_answer != "" and i == correct_answer:
                    answer_values[list(answers_).index(i)] = bg.green + fg.black + list(answers_.items())[index][
                        0].upper() + ": " + answers_[i] + " " * (number_of_spaces - len(
                        list(answers_.items())[index][1])) + fg.rs + bg.rs
                else:
                    answer_values[list(answers_).index(i)] = list(answers_.items())[index][0].upper() + ": " + answers_[
                        i] + " " * (number_of_spaces - len(list(answers_.items())[index][1]))
                index += 1
        else:
            for i in range(len(answers_)):
                answer_values[i] = list(answers_.items())[i][0].upper() + ": " + answer_values[i] + " " * (
                            number_of_spaces - len(list(answers_.items())[i][1]))

        print("| " + answer_values[0] + " | " + answer_values[1] + " |")
        print("-" * table_length)
        print("| " + answer_values[2] + " | " + answer_values[3] + " |")
    print("-" * table_length)


def show_game_structure():
    prizes = util.open_file("prizes_" + str(game_language).lower(), "r")
    if game_language == util.Language.HUNGARIAN.name:
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
            if os.name == "POSIX":
                time.sleep(0.3)
            else:
                time.sleep(0.4)
            if i != 14:
                util.clear_screen()
                print_helps()
                print("\n\n")
        if os.name != "POSIX":
            time.sleep(2)
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
            util.clear_screen()
            print_helps()
            print("\n\n")
        util.clear_screen()
        list_helps()
        util.clear_screen()
        print_helps()
        print("\n\n")
        print_prizes()
        time.sleep(8)
        util.clear_screen()
    else:
        helps = [" 50 : 50 ", "     \_] ", "  ☺ ☺ ☺  "]
        separator = fg.blue + "|" + fg.rs
        print(fg.blue + 31 * "-" + fg.rs)
        print(separator + helps[0] + separator + helps[1] + separator + helps[2] + separator)
        print(fg.blue + 31 * "-" + fg.rs)
        print("\n\n")
        print_prizes()
        time.sleep(4)
        util.clear_screen()


def print_helps():
    helps = [" 50 : 50 ", "     \_] ", "  ☺ ☺ ☺  "]
    separator = fg.blue + "|" + fg.rs
    print(fg.blue + 31 * "-" + fg.rs)
    print(separator + helps[0] + separator + helps[1] + separator + helps[2] + separator)
    print(fg.blue + 31 * "-" + fg.rs)


def list_helps():
    helps = [" 50 : 50 ", "     \_] ", "  ☺ ☺ ☺  "]
    separator = fg.blue + "|" + fg.rs
    print(fg.blue + 31 * "-" + fg.rs)
    print(separator + bg.orange + fg.black + helps[0] + fg.rs + bg.rs + separator + helps[1] + separator + helps[
        2] + separator)
    print(fg.blue + 31 * "-" + fg.rs)
    print("\n\n")
    print_prizes()
    time.sleep(1.3)
    util.clear_screen()
    print(fg.blue + 31 * "-" + fg.rs)
    print(separator + helps[0] + separator + bg.orange + fg.black + helps[1] + fg.rs + bg.rs + separator + helps[
        2] + separator)
    print(fg.blue + 31 * "-" + fg.rs)
    print("\n\n")
    print_prizes()
    time.sleep(1.3)
    util.clear_screen()
    print(fg.blue + 31 * "-" + fg.rs)
    print(separator + helps[0] + separator + helps[
        1] + separator + bg.orange + fg.black + "  ☻ ☻ ☻  " + fg.rs + bg.rs + separator)
    print(fg.blue + 31 * "-" + fg.rs)
    print("\n\n")
    print_prizes()
    time.sleep(1.3)


def print_prizes():
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


def play_marked_sound(choise: str, level: int):
    sound_files = ["mark_" + choise, "mark_" + choise + "_1", "mark_" + choise + "_2"]
    if level == 4:
        util.play_sound("mark_500", 0)
        time.sleep(6)
    else:
        util.play_sound(random.choice(sound_files), 0)
        time.sleep(1)


def handle_user_input(question: str, answers: dict, level: int) -> str:
    final_sounds = ["final", "final_1", "final_2", "final_3", "final_4", "final_5"]
    lets_see_sounds = ["lets_mark", "lets_see", "lets_see_1", "lets_see_2", "lets_see_3"]
    while True:
        user_input = get_user_input()
        if user_input == b'a' or user_input == "a":
            selected_final_sound = random.choice(final_sounds)
            selected_lets_see_sound = random.choice(lets_see_sounds)
            util.play_sound(selected_final_sound, 0)
            util.clear_screen()
            print_quiz_table(question, answers)
            print("\n" + language_dictionary[game_language].quiz.select_answer + language_dictionary[
                game_language].quiz.selected_answer + "A")
            while True:
                user_input = get_user_input()
                if user_input == b'\r' or user_input == '<Ctrl-j>':
                    play_marked_sound("a", level)
                    util.play_sound(selected_lets_see_sound, 0)
                    time.sleep(3)
                    return "a"
                else:
                    break
        if user_input == b'b' or user_input == "b":
            selected_final_sound = random.choice(final_sounds)
            selected_lets_see_sound = random.choice(lets_see_sounds)
            util.play_sound(selected_final_sound, 0)
            util.clear_screen()
            print_quiz_table(question, answers)
            print("\n " + language_dictionary[game_language].quiz.select_answer + language_dictionary[
                game_language].quiz.selected_answer + "B")
            while True:
                user_input = get_user_input()
                if user_input == b'\r' or user_input == '<Ctrl-j>':
                    play_marked_sound("b", level)
                    util.play_sound(selected_lets_see_sound, 0)
                    time.sleep(3)
                    return "b"
                else:
                    break
        if user_input == b'c' or user_input == "c":
            selected_final_sound = random.choice(final_sounds)
            selected_lets_see_sound = random.choice(lets_see_sounds)
            util.play_sound(selected_final_sound, 0)
            util.clear_screen()
            print_quiz_table(question, answers)
            print("\n " + language_dictionary[game_language].quiz.select_answer + language_dictionary[
                game_language].quiz.selected_answer + "C")
            while True:
                user_input = get_user_input()
                if user_input == b'\r' or user_input == '<Ctrl-j>':
                    play_marked_sound("c", level)
                    util.play_sound(selected_lets_see_sound, 0)
                    time.sleep(3)
                    return "c"
                else:
                    break
        if user_input == b'd' or user_input == "d":
            selected_final_sound = random.choice(final_sounds)
            selected_lets_see_sound = random.choice(lets_see_sounds)
            util.play_sound(selected_final_sound, 0)
            util.clear_screen()
            print_quiz_table(question, answers)
            print("\n " + language_dictionary[game_language].quiz.select_answer + language_dictionary[
                game_language].quiz.selected_answer + "D")
            while True:
                user_input = get_user_input()
                if user_input == b'\r' or user_input == '<Ctrl-j>':
                    play_marked_sound("d", level)
                    util.play_sound(selected_lets_see_sound, 0)
                    time.sleep(3)
                    return "d"
                else:
                    break
        if user_input == b't' or user_input == "t":
            return "t"
        if user_input == b'h' or user_input == "h":
            return "h"


def get_user_input() -> bytes:
    if util.operating_system == "posix":
        user_input = helpers.return_user_input_linux()
    else:
        user_input = helpers.return_user_input_windows()

    return user_input
