import os
import random
import json
import time
from sty import Style, RgbFg, fg, bg
import millionaire.menu.menu as menu
import millionaire.util.util as util
operating_system = os.name
fg.purple = Style(RgbFg(148, 0, 211))
fg.orange = Style(RgbFg(255, 150, 50))
fg.green = Style(RgbFg(0, 255, 0))
bg.orange = bg(255, 150, 50)
languages = util.available_languages
language_dictionary = util.language_dictionary


def play():
    global game_language, question_lines_easy, question_lines_medium, question_lines_hard
    game_language = util.game_language
    global question_topics
    question_topics = util.question_topics
    global question_difficulty
    question_difficulty = util.question_difficulty
    player_name = input(language_dictionary[game_language].quiz.player_name_prompt)
    score = 0
    help_types = {"audience": True, "telephone": True, "halving": True}
    util.clear_screen()
    util.play_sound("start", 0)
    show_game_structure()
    if game_language == util.Language.HUNGARIAN.name:
        time.sleep(7)
    question_lines = []
    question_lines_easy = []
    question_lines_medium = []
    question_lines_hard = []
    if question_topics == util.Topics.ALL.name:
        for topic in util.Topics:
            if topic.name != util.Topics.ALL.name and question_difficulty != util.Difficulty.ALL.name:
                for level in util.Difficulty:
                    if question_difficulty == level.name:
                        for line in util.open_file(level.name, "r", ";",
                                                   "/text_files/topics/" + game_language + "/" + topic.name + "/" + level.name + "/"):
                            question_lines.append(line)
            else:
                if topic.name != util.Topics.ALL.name:
                    for line in util.open_file(util.Difficulty.EASY.name, "r", ";",
                                               "/text_files/topics/" + game_language + "/" + topic.name + "/" + util.Difficulty.EASY.name + "/"):
                        question_lines_easy.append(line)
                    for line in util.open_file(util.Difficulty.MEDIUM.name, "r", ";",
                                               "/text_files/topics/" + game_language + "/" + topic.name + "/" + util.Difficulty.MEDIUM.name + "/"):
                        question_lines_medium.append(line)
                    for line in util.open_file(util.Difficulty.HARD.name, "r", ";",
                                               "/text_files/topics/" + game_language + "/" + topic.name + "/" + util.Difficulty.HARD.name + "/"):
                        question_lines_hard.append(line)
    else:
        for level in util.Difficulty:
            if question_difficulty == level.name and level.name != util.Difficulty.ALL.name:
                for line in util.open_file(level.name, "r", ";",
                                           "/text_files/topics/" + game_language + "/" + question_topics + "/" + level.name + "/"):
                    question_lines.append(line)
            else:
                if level.name != util.Difficulty.ALL.name:
                    for line in util.open_file(util.Difficulty(level).name, "r", ";",
                                               "/text_files/topics/" + game_language + "/" + question_topics + "/" + level.name + "/"):
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
        print_question(question, shuffled_answers)
        play_music(i)
        answer = safe_input(
            language_dictionary[game_language].quiz.select_answer,
            ["a", "b", "c", "d", "h", "t"])
        util.clear_screen()
        print_question(question, shuffled_answers, answer, "orange")
        correct_answer_key = get_dictionary_key_by_value(shuffled_answers, question_lines[i][1])
        correct_answer_value = question_lines[i][1]
        util.stop_sound()
        while answer not in list(answers.keys()):
            if answer == "t":
                util.clear_screen()
                print_question(question, shuffled_answers)
                if util.game_language == util.Language.HUNGARIAN.name:
                    util.play_sound("music_off", 0)
                answer = safe_input(language_dictionary[game_language].quiz.select_answer_out,
                                    ["a", "b", "c", "d"])
                util.clear_screen()
                print_question(question, shuffled_answers, answer, "blue")
                util.play_sound("marked", 0)
                time.sleep(2)
                is_correct = check_answer(answer, correct_answer_key)
                if is_correct:
                    util.clear_screen()
                    print_question(question, shuffled_answers, answer, "green")
                    if i > 9:
                        print(bg.orange + show_prize(9) + bg.rs)
                        time.sleep(1)
                    elif i > 4:
                        print(bg.orange + show_prize(4) + bg.rs)
                        util.play_sound("won_hundred_bucks", 0)
                        time.sleep(1)
                    else:
                        print(fg.blue + language_dictionary[game_language].quiz.correct_answer_out + fg.rs)
                        util.play_sound("show_stop", 0)
                        time.sleep(1)
                else:
                    util.play_sound("bad_answer", 0)
                    util.clear_screen()
                    print_question(question, shuffled_answers, answer, "blue", correct_answer=correct_answer_key)
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
                util.clear_screen()
                print_question(question, shuffled_answers)
                help_functions = {"audience": audience_help, "telephone": telephone_help, "halving": halving}
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
                                print_question(question, shuffled_answers)
                            else:
                                list(help_functions.values())[x](question, shuffled_answers, correct_answer_value)
                            help_types[list(help_types)[x]] = False
                            break
                        else:
                            print(language_dictionary[game_language].quiz.help_disabled + list(help_types)[x] + " " +
                                  language_dictionary[game_language].quiz.help)
                answer = safe_input(
                    language_dictionary[game_language].quiz.select_answer,
                    ["a", "b", "c", "d", "h", "t"])
                time.sleep(2)
                util.clear_screen()
                print_question(question, shuffled_answers, answer, "orange")
        if game_language == util.Language.HUNGARIAN.name:
            play_marked_sound(answer)
        util.play_sound("marked", 0)
        is_correct = check_answer(answer, correct_answer_key)
        time.sleep(2)
        if is_correct:
            score += 1
            if i < 14:
                util.play_sound("correct_answer", 0)
                util.clear_screen()
                print_question(question, shuffled_answers, answer, "green")
                time.sleep(2)
                util.clear_screen()
                if len(question) % 2 == 0:
                    question = question + " "
                if i == 4:
                    print("\n" + " " * 20 + fg.yellow + language_dictionary[game_language].quiz.guaranteed_prize + show_prize(i) + fg.rs)
                    util.play_sound("won_hundred_bucks", 0)
                    print("-" * (len(question) + len(show_prize(i)) + 8))
                    print("|", bg.orange, fg.black, " " * (int(len(question) / 2)) + show_prize(i), fg.rs,
                          " " * (int(len(question) / 2)), bg.rs, "|")
                    print("-" * (len(question) + len(show_prize(i)) + 8))
                    time.sleep(3)
                elif i == 9:
                    print("\n" + " " * 20 + fg.yellow + language_dictionary[game_language].quiz.guaranteed_prize + show_prize(i) + fg.rs)
                    if util.game_language == util.Language.HUNGARIAN.name:
                        util.play_sound("now_comes_hard_part", 0)
                    print("-" * (len(question) + len(show_prize(i)) + 8))
                    print("|", bg.orange, fg.black, " " * (int(len(question) / 2)) + show_prize(i), fg.rs,
                          " " * (int(len(question) / 2)), bg.rs, "|")
                    print("-" * (len(question) + len(show_prize(i)) + 8))
                    time.sleep(3)
                else:
                    print("-" * (len(question)+len(show_prize(i))+8))
                    print("|",bg.orange,fg.black," " * (int(len(question)/2)) + show_prize(i),fg.rs, " " * (int(len(question)/2)),bg.rs, "|")
                    print("-" * (len(question)+len(show_prize(i))+8))
                    time.sleep(2)
            else:
                if util.game_language == util.Language.HUNGARIAN.name:
                    util.play_sound("great_logic", 0)
                time.sleep(1)
                util.clear_screen()
                print("\n" + " " * 20 + fg.purple + language_dictionary[game_language].quiz.won_prize + show_prize(i) + " !" + fg.rs)
                util.play_sound("winning_theme", 0)
                time.sleep(35)
                menu.return_prompt()
        else:
            util.play_sound("bad_answer", 0)
            util.clear_screen()
            print_question(question, shuffled_answers, answer, "orange", correct_answer=correct_answer_key)
            time.sleep(2)
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
    prizes = util.open_file("prizes_" + game_language, "r")
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
    call_text_files = ["mum_phone_" + game_language,
                       "dad_phone_" + game_language,
                       "teacher_phone_" + game_language,
                       "yoda_master_phone_" + game_language
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
            print(key.upper() + " : " + string_value + "% " + bg.orange + value*" " + bg.rs + " " + str(answers[key]))
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


def print_question(question: str, answers_: {}, selected="", color="", correct_answer=""):
    answer_values = list(answers_.values())
    len_first_answer = len(list(answers_.items())[0][1])
    len_second_answer = len(list(answers_.items())[1][1])
    len_third_answer = len(list(answers_.items())[2][1])
    len_fourth_answer = len(list(answers_.items())[3][1])
    longest_string = list(sorted(answers_.values(), key=len))[-1]
    len_separator = len(longest_string) * 2 + 30
    table_length = 0
    number_of_spaces = 0
    if len_separator > len(question) + 6:
        table_length = len_separator
        if table_length % 2 == 0:
            table_length += 1
        number_of_spaces = int((table_length/2)-9)
    else:
        table_length = int(len(question)) + 6
        if table_length % 2 == 0:
            table_length += 1
        number_of_spaces = int((table_length / 2) - 9)
    if selected != "":
        for i in answers_:
            if correct_answer != "" and i == correct_answer:
                answer_values[list(answers_).index(i)] = bg.green + fg.black + answers_[i] + fg.rs + bg.rs
            if i == selected:
                if color == "orange":
                    answer_values[list(answers_).index(i)] = bg.orange + fg.black + answers_[i] + fg.rs + bg.rs
                if color == "green":
                    answer_values[list(answers_).index(i)] = bg.green + fg.black + answers_[i] + fg.rs + bg.rs
                if color == "blue":
                    answer_values[list(answers_).index(i)] = bg.blue + fg.black + answers_[i] + fg.rs + bg.rs

    print("-" * (table_length))
    print("| " + question + " " * (table_length - len(question) - 3) + "|")
    print("-" * (table_length))
    print("\n")
    print("-" * table_length)
    print("| " + list(answers_.items())[0][0].upper(), ": ", answer_values[0],
          " " * (number_of_spaces - len_first_answer), "|",
          list(answers_.items())[1][0].upper(), ": ", answer_values[1],
          " " * (number_of_spaces - len_second_answer), "|")
    print("-" * table_length)
    print("| " + list(answers_.items())[2][0].upper(), ": ", answer_values[2],
          " " * (number_of_spaces - len_third_answer), "|",
          list(answers_.items())[3][0].upper(), ": ", answer_values[3],
          " " * (number_of_spaces - len_fourth_answer), "|")
    print("-" * table_length)


def show_game_structure():
    prizes = util.open_file("prizes_" + game_language, "r")
    if game_language == util.Language.HUNGARIAN.name:
        for i in range(len(prizes)):
            for j in range(len(prizes)):
                round_number = str(len(prizes) - j)
                if len(prizes) - j < 10:
                    round_number = " " + round_number
                if i == len(prizes) - j:
                    print(round_number + " " + bg.orange + fg.black + prizes[::-1][j][0] + fg.rs + bg.rs)
                else:
                    if j == 5 or j == 10 or j == 0:
                        print(round_number + " " + prizes[::-1][j][0])
                    else:
                        print(round_number + " " + fg.orange + prizes[::-1][j][0] + fg.rs)
            if game_language == util.Language.HUNGARIAN.name:
                time.sleep(0.3)
            if i != 15:
                util.clear_screen()
        time.sleep(3)
        helps = [" 50 : 50 ", "     \_] ", "  ☺ ☺ ☺  "]
        for i in range(3):
            for j in range(3):
                if i == j:
                    print(11 * "-")
                    print("|" + bg.orange + fg.black + helps[i] + fg.rs + bg.rs + "|")
                    print(11 * "-")

                else:
                    print(11 * "-")
                    print("|" + helps[j] + "|")
                    print(11 * "-")
            time.sleep(1)
            util.clear_screen()
        time.sleep(2)
        util.clear_screen()
    else:
        helps = [" 50 : 50 ", "     \_] ", "  ☺ ☺ ☺  "]
        separator = fg.blue + "|" + fg.rs
        print(fg.blue + 31*"-" + fg. rs)
        print(separator + helps[0] + separator + helps[1] + separator + helps[2] + separator)
        print(fg.blue + 31*"-" + fg. rs)
        for i in range(len(prizes)):
            round_number = str(len(prizes) - i)
            if len(prizes) - i < 10:
                round_number = " " + round_number
            if i == 5 or i == 10 or i == 0:
                print(round_number + " " + prizes[::-1][i][0])
            else:
                print(round_number + " " + fg.orange + prizes[::-1][i][0] + fg.rs)
        time.sleep(4)
        util.clear_screen()


def play_music(round: int):
    if round < 5:
        util.play_background_music(str(5), 0)
    else:
        util.play_background_music(str(round), 0)


def play_marked_sound(choise: str):
    sound_files = ["mark_" + choise,"mark_" + choise + "_1","mark_" + choise+ "_2"]
    util.play_sound(random.choice(sound_files), 0)
    time.sleep(1)