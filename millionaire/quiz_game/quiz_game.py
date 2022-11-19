import random
import os
from sty import Style, RgbFg, fg, bg
from util import util
import time
import json
from menu import menu

operating_system = os.name
fg.purple = Style(RgbFg(148, 0, 211))
fg.orange = Style(RgbFg(255, 150, 50))
fg.green = Style(RgbFg(0, 255, 0))
bg.orange = bg(255, 150, 50)
languages = util.available_languages
language_dictionary = util.language_dictionary
game_language = "en"
question_topics = "All "


def play():
    global game_language
    game_language = util.game_language
    global question_topics
    question_topics = util.question_topics
    global question_difficulty
    question_difficulty = util.question_difficulty
    player_name = input(language_dictionary[game_language].quiz.player_name_prompt)
    score = 0
    help_types = {"audience": True, "telephone": True, "halving": True}
    util.clear_screen()
    util.play_sound("lom.mp3", 0)
    time.sleep(2)
    question_file = 'questions_' + game_language + ".txt"
    question_lines = util.open_file(question_file, "r", ";")
    #if question_topics != language_dictionary[game_language].menu.settings_menu_question_topics[0]:
    #    populated = filter(lambda c: c[5] == str(question_topics).lower().strip(), question_lines)
    #    question_lines = list(populated)
    #if question_difficulty != "":
    levels = language_dictionary[game_language].menu.question_difficulty_levels
    #print(question_topics)
    #print(str(language_dictionary[game_language].menu.settings_menu_question_topics[0]).lower())
    if question_topics == "All " or "Mind":
        for a in levels:
            print(a)
            # populated = filter(lambda c: c[6] == a.lower().strip(), question_lines_)
            print(sum(1 for _ in filter(lambda c: c[6] == a.lower().strip(), question_lines)))
    for b in language_dictionary[game_language].menu.settings_menu_question_topics:
        populated1 = filter(lambda c: c[5] == b.lower().strip(), question_lines)
        question_lines_ = list(populated1)
        print(b)
        for a in levels:
            print(a)
            #populated = filter(lambda c: c[6] == a.lower().strip(), question_lines_)
            print(sum(1 for _ in filter(lambda c: c[6] == a.lower().strip(), question_lines_)))
    time.sleep(30)
    #question_lines = list(populated)
    random.shuffle(question_lines)
    for i in range(15):
        question = question_lines[i][0]
        print(question)
        answers = {"a": question_lines[i][1], "b": question_lines[i][2], "c": question_lines[i][3],
                   "d": question_lines[i][4]}
        answer_list = list(answers.values())
        random.shuffle(answer_list)
        shuffled_answers = dict(zip(answers, answer_list))
        for k in range(len(answer_list)):
            print(list(answers.keys())[k] + ": " + answer_list[k])
        answer = safe_input(
            language_dictionary[game_language].quiz.select_answer,
            ["a", "b", "c", "d", "h", "t"])
        correct_answer_key = get_dictionary_key_by_value(shuffled_answers, question_lines[i][1])
        correct_answer_value = question_lines[i][1]
        while answer not in list(answers.keys()):
            if answer == "t":
                util.clear_screen()
                print(question)
                for k in range(len(answer_list)):
                    print(list(answers.keys())[k] + ": " + answer_list[k])
                util.play_sound("music_off.mp3", 0)
                answer = safe_input(language_dictionary[game_language].quiz.select_answer_out,
                                    ["a", "b", "c", "d"])
                time.sleep(2)
                util.play_sound("marked.mp3", 0)
                time.sleep(2)
                is_correct = check_answer(answer, correct_answer_key)
                if is_correct:
                    util.clear_screen()
                    if i > 9:
                        print(bg.orange + show_prize(9) + bg.rs)
                        time.sleep(1)
                    elif i > 4:
                        print(bg.orange + show_prize(4) + bg.rs)
                        util.play_sound("won_hundred_bucks.mp3", 0)
                        time.sleep(1)
                    else:
                        print(fg.blue + language_dictionary[game_language].quiz.correct_answer_out + fg.rs)
                        util.play_sound("show_stop.mp3", 0)
                        time.sleep(1)
                else:
                    util.play_sound("bad_answer.mp3", 0)
                    print(fg.green + correct_answer_value + fg.rs)
                    print(fg.red + language_dictionary[game_language].quiz.incorrect_answer + fg.rs)
                    util.play_sound("so_sorry.mp3", 0)
                    time.sleep(1)
                menu.return_prompt()
                util.clear_screen()
                if score != 0:
                    write_content_to_file("scores.json", {"user": player_name, "topic": language_dictionary[game_language].menu.settings_menu_question_topics.index(question_topics), "score": score,
                                                          "time": time.ctime(time.time())})
                return
            if answer == "h":
                util.clear_screen()
                print(question)
                for k in range(len(answer_list)):
                    print(list(answers.keys())[k] + ": " + answer_list[k])
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
        util.play_sound("marked.mp3", 0)
        time.sleep(2)
        is_correct = check_answer(answer, correct_answer_key)
        time.sleep(2)
        if is_correct:
            score += 1
            if i < 14:
                util.play_sound("correct_answer.mp3", 0)
                if i == 4:
                    print(fg.yellow + language_dictionary[game_language].quiz.guaranteed_prize + show_prize(i) + fg.rs)
                    util.play_sound("won_hundred_bucks.mp3", 0)
                    time.sleep(1)
                elif i == 9:
                    print(fg.yellow + language_dictionary[game_language].quiz.guaranteed_prize + show_prize(i) + fg.rs)
                    util.play_sound("now_comes_hard_part.mp3", 0)
                    time.sleep(1)
                else:
                    print(fg.green + language_dictionary[game_language].quiz.correct_answer + fg.rs)
                    util.clear_screen()
                    print(bg.orange + show_prize(i) + bg.rs)
                    time.sleep(2)
            else:
                util.play_sound("great_logic.mp3", 0)
                time.sleep(1)
                util.clear_screen()
                print(fg.purple + language_dictionary[game_language].quiz.won_prize + show_prize(i) + " !" + fg.rs)
                util.play_sound("winning_theme.mp3", 0)
                time.sleep(35)
                menu.return_prompt()
        else:
            util.play_sound("bad_answer.mp3", 0)
            print(fg.green + correct_answer_value + fg.rs)
            print(fg.red + language_dictionary[game_language].quiz.incorrect_answer + fg.rs)
            menu.return_prompt()
            util.clear_screen()
            if score != 0:
                write_content_to_file("scores.json", {"user": player_name, "topic": language_dictionary[game_language].menu.settings_menu_question_topics.index(question_topics), "score": score, "time": time.ctime(time.time())})
            return
        util.clear_screen()

    write_content_to_file("scores.json", {"user": player_name, "topic": language_dictionary[game_language].menu.settings_menu_question_topics.index(question_topics), "score": score, "time": time.ctime(time.time())})
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
    prizes = util.open_file("prizes_" + game_language + ".txt", "r")
    return prizes[round_number][0]


def print_phone_conversation(text: list, question: str, answers: {}, good_answer: str):
    util.play_sound("phone_ring.mp3", 0)
    time.sleep(2)
    util.play_sound("phone_call.mp3", 0)
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
    util.play_sound('phone_call.mp3', 30.0)
    time.sleep(3)
    print(language_dictionary[game_language].quiz.call_duration, int(now - then),
          language_dictionary[game_language].quiz.call_seconds)
    util.stop_sound()


def telephone_help(question: str, answers: {}, correct_answer: str):
    time.sleep(10)
    phone = safe_input(language_dictionary[game_language].quiz.phone_prompt,
                       ["m", "d", "t", "y"])
    call_text_files = ["mum_phone_" + game_language + ".txt",
                       "dad_phone_" + game_language + ".txt",
                       "teacher_phone_" + game_language + ".txt",
                       "yoda_master_phone_" + game_language + ".txt"
                       ]
    for i in range(len(call_text_files)):
        if phone.lower() == call_text_files[i][0]:
            conversation = (util.open_file(call_text_files[i], 'r', separator=";"))
            print_phone_conversation(conversation, question, answers, correct_answer)


def halving(question: str, answers: {}, correct_answer: str) -> dict:
    util.play_sound("lets_take_two.mp3", 0)
    util.clear_screen()
    time.sleep(2)
    util.play_sound("halving.mp3", 0)
    print(question)
    halved_answers = calculate_halved_answers(answers, correct_answer)
    for i in halved_answers:
        print(i + ": " + halved_answers[i])
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
    util.play_sound("push_your_buttons.mp3", 0)
    time.sleep(3)
    util.clear_screen()
    answers_list = list(answers.keys())
    for i in range(len(answers_list)):
        print(question)
        chances = get_chances(answers, correct_value)
        for key, value in sorted(chances.items()):
            print(key + " : " + str(answers[key]) + " || " + str(value) + "%")
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
