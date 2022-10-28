import copy
import random
import sys
import os
from sty import Style, RgbFg, fg, bg
from util import util
import time


operating_system = os.name
fg.purple = Style(RgbFg(148, 0, 211))
fg.orange = Style(RgbFg(255, 150, 50))
fg.green = Style(RgbFg(0, 255, 0))
bg.orange = bg(255, 150, 50)
help_types = {"audience": False, "telephone": False, "halving": False}
prizes = ["5.000 Ft", "10.000 Ft", "25.000 Ft", "50.000 Ft", "100.000 Ft", "200.000 Ft", "300.000 Ft", "500.000 Ft",
          "800.000 Ft", "1.500.000 Ft", "3.000.000 Ft", "5.000.000 Ft", "10.000.000 Ft", "20.000.000 Ft",
          "40.000.000 Ft"]


def play():
    help_types["audience"] = True
    help_types["telephone"] = True
    help_types["halving"] = True
    util.clear_screen()
    util.play_sound("lom.mp3", 0)
    time.sleep(2)
    question_lines = util.open_file('questions.txt', "r")
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
            "\nSelect the correct answer ('a','b','c','d'), 't' for guessing out of game or 'h' for help! ",
            ["a", "b", "c", "d", "h", "t"])
        correct_answer_key = get_dictionary_key_by_value(shuffled_answers, question_lines[i][1])
        correct_answer_value = question_lines[i][1]
        while answer not in list(answers.keys()):
            if answer == "t":
                util.play_sound("music_off.mp3", 0)
                answer = safe_input("\nSelect the correct answer ('a','b','c','d') ! ",
                                    ["a", "b", "c", "d"])
                time.sleep(2)
                util.clear_screen()
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
                        print(fg.blue + "Correct answer! Better luck next time!" + fg.rs)
                        util.play_sound("show_stop.mp3", 0)
                        time.sleep(1)
                else:
                    print(fg.red + "Bad answer! Better luck next time!" + fg.rs)
                    util.play_sound("so_sorry.mp3", 0)
                    time.sleep(1)
                if safe_input("Would you like to play again? ('y'/'n')", ['y', 'n']) == 'y':
                    util.clear_screen()
                    play()
                else:
                    sys.exit(0)
            if answer == "h":
                help_functions = {"audience": audience_help, "telephone": telephone_help, "halving": halving}
                chosen_help_type = safe_input("Choose help: 'a' for audience, 't' for telephone, 'h' for halving! ",
                                              ["a", "t", "h"])
                for x in range(len(help_types)):
                    if chosen_help_type.lower() == list(help_types)[x][0]:
                        if help_types[list(help_types)[x]]:
                            list(help_functions.values())[x](question, shuffled_answers, correct_answer_value)
                            help_types[x] = False
                            break
                        else:
                            print("You have already used the " + help_types[x] + " help!")
                answer = safe_input(
                    "\nSelect the correct answer ('a','b','c','d'), 't' for guessing out of game or 'h' for help! ",
                    ["a", "b", "c", "d", "h", "t"])
                time.sleep(2)
                util.clear_screen()
        util.play_sound("marked.mp3", 0)
        time.sleep(2)
        is_correct = check_answer(answer, correct_answer_key)
        time.sleep(2)
        if is_correct:
            if i < 14:
                util.play_sound("correct_answer.mp3", 0)
                if i == 4:
                    print(fg.yellow + "You have guaranteed 100.000 Ft" + fg.rs)
                    util.play_sound("won_hundred_bucks.mp3", 0)
                    time.sleep(1)
                elif i == 9:
                    print(fg.yellow + "You have guaranteed 1.500.000 Ft" + fg.rs)
                    util.play_sound("now_comes_hard_part.mp3", 0)
                    time.sleep(1)
                else:
                    print(fg.green + "Well Done!" + fg.rs)
                    util.clear_screen()
                    print(bg.orange + show_prize(i) + bg.rs)
                    time.sleep(2)
            else:
                util.play_sound("great_logic.mp3", 0)
                time.sleep(1)
                util.clear_screen()
                print(fg.purple + "Congratulations! You have won 40 000 000 Ft!" + fg.rs)
                util.play_sound("winning_theme.mp3", 0)
                time.sleep(35)
                sys.exit(0)
        else:
            print(fg.red + "Bad answer! Better luck next time!" + fg.rs)
            input("press ENTER for main menu..")
            util.clear_screen()
            return
        util.clear_screen()


def safe_input(input_text, allowed_list_of_letters):
    answer = input(input_text)
    while answer not in allowed_list_of_letters:
        print("Error! Only letters: " + ' '.join(allowed_list_of_letters) + " allowed!")
        answer = input("Select the correct answer!")
    return answer


def get_dictionary_key_by_value(dictionary: {}, value: str):
    for choice, answerValue in dict.items(dictionary):
        if answerValue == value:
            return choice


def check_answer(answer: str, correct_answer: str):
    return answer == correct_answer


def show_prize(round_number: int):
    return prizes[round_number]


def print_phone_conversation(text, question, answers, good_answer):
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
    print("Call Duration: ", int(now - then), " seconds\\ 30s")
    util.stop_sound()


def telephone_help(question, answers, correct_answer):
    phone = safe_input(
        "Who'd you like to call?\n"
        "for mum, press 'm'\n"
        "for dad press 'd'\n"
        "for old teacher from high school press 't'\n"
        "for Maester Yoda press 'y': ",
        ["m", "d", "t", "y"])
    call_text_files = ["mum_phone.txt", "dad_phone.txt", "teacher_phone.txt", "yoda_master_phone.txt"]
    for i in range(len(call_text_files)):
        if phone.lower() == call_text_files[i][0]:
            text = (util.open_file(call_text_files[i], 'r'))
            print_phone_conversation(text, question, answers, correct_answer)


def halving(question: str, answers: {}, correct_answer: str):
    util.play_sound("lets_take_two.mp3", 0)
    util.clear_screen()
    time.sleep(2)
    util.play_sound("halving.mp3", 0)
    correct_value = get_dictionary_key_by_value(answers, correct_answer)
    second_answer = random.choice([x for x in answers if x != correct_value])
    print(question)
    for i in answers:
        if answers[i] == correct_answer:
            print(i + ": " + answers[i])
        elif i == second_answer:
            print(i + ": " + answers[second_answer])
        else:
            print(i + ": ")


def audience_help(question, answers, correct_value):
    util.play_sound("push_your_buttons.mp3", 0)
    time.sleep(3)
    util.clear_screen()
    answers_list = list(answers.keys())
    for i in range(len(answers_list)):
        print(question)
        chances = sorted(get_chances(), reverse=True)
        for k in range(len(answers_list)):
            if answers[answers_list[k]] == correct_value:
                print(str(answers_list[k]) + " : " + str(answers[answers_list[k]]) + " || " + str(chances[0]) + "%")
            else:
                print(str(answers_list[k]) + " : " + str(answers[answers_list[k]]) + " || " + str(chances[0]) + "%")
            chances.pop(0)
        time.sleep(1)
        if i != len(answers_list)-1:
            util.clear_screen()


def get_chances() -> list:
    percents = [random.randrange(40, 89)]
    for i in range(3):
        percents.append(random.randrange(0, 100 - sum(percents)))

    return percents
