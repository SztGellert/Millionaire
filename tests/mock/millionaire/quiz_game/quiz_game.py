import keyboard
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
prizes = ["5.000 Ft", "10.000 Ft", "25.000 Ft", "50.000 Ft", "100.000 Ft", "200.000 Ft", "300.000 Ft", "500.000 Ft",
          "800.000 Ft", "1.500.000 Ft", "3.000.000 Ft", "5.000.000 Ft", "10.000.000 Ft", "20.000.000 Ft",
          "40.000.000 Ft"]


def play(inputs: dict):
    out_of_game_inputs = inputs["out_of_game_answers"]
    game_inputs = inputs["game_answers"]
    audience_inputs = inputs["audience_answers"]
    halving_inputs = inputs["halving_answers"]
    phone_inputs = inputs["phone_answers"]
    return_inputs = inputs["return_prompt_answers"]
    help_types = {"audience": True, "halving": True, "phone": True}
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
        correct_answer_key = get_dictionary_key_by_value(shuffled_answers, question_lines[i][1])
        correct_answer_value = question_lines[i][1]
        if game_inputs[i] == "OK":
            answer = safe_input(
                "\nSelect the correct answer ('a','b','c','d'), 't' for guessing out of game or 'h' for help! ",
                ["a", "b", "c", "d", "h", "t"], correct_answer_key)
        else:
            answer = safe_input(
                "\nSelect the correct answer ('a','b','c','d'), 't' for guessing out of game or 'h' for help! ",
                ["a", "b", "c", "d", "h", "t"], game_inputs[i])
        while answer not in list(answers.keys()):
            if answer == "t":
                util.clear_screen()
                print(question)
                for k in range(len(answer_list)):
                    print(list(answers.keys())[k] + ": " + answer_list[k])
                util.play_sound("music_off.mp3", 0)
                if out_of_game_inputs[0] == "OK":
                    answer = safe_input("\nSelect the correct answer ('a','b','c','d') ! ",
                        ["a", "b", "c", "d"], correct_answer_key)
                else:
                    answer = safe_input("\nSelect the correct answer ('a','b','c','d') ! ",
                                        ["a", "b", "c", "d"], out_of_game_inputs[0])
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
                safe_input("press ENTER for main menu..", ["enter"], return_inputs[0])
                util.clear_screen()
                return
            if answer == "h":
                help_functions = {"audience": audience_help, "halving": halving, "telephone": telephone_help}
                help_inputs = [audience_inputs, halving_inputs, phone_inputs]
                chosen_help = str
                for x in range(len(help_types)):
                    if help_types[list(help_types)[x]] and (len(help_inputs[x]) > 0):
                        chosen_help = list(help_types)[x]
                chosen_input = ""
                chosen_help_values = []
                for help in help_inputs:
                    if len(help) > 0:
                        if chosen_help == "audience":
                            chosen_help_values = help_inputs[0]
                            chosen_input = "a"
                        if chosen_help == "halving":
                            chosen_help_values = help_inputs[1]
                            chosen_input = "h"
                        if chosen_help == "phone":
                            chosen_help_values = help_inputs[2]
                            chosen_input = "t"
                chosen_help_type = safe_input("Choose help: 'a' for audience, 'h' for halving, 't' for telephone! ",
                                              ["a", "h", "t"], chosen_input)
                for x in range(len(help_types)):
                    if chosen_help_type.lower() == list(help_types)[x][0]:
                        if help_types[list(help_types)[x]]:
                            if chosen_help == "halving":
                                shuffled_answers = list(help_functions.values())[x](question, shuffled_answers,
                                                                                    correct_answer_value)
                                for a in range(len(answer_list)):
                                    answer_list[a] = list(shuffled_answers.values())[a]
                            if chosen_help == "audience":
                                list(help_functions.values())[x](question, shuffled_answers, correct_answer_value)
                            if chosen_help == "phone":
                                list(help_functions.values())[x](question, shuffled_answers, correct_answer_value, chosen_help_values[1])
                            help_types[list(help_types)[x]] = False
                            break
                        else:
                            print("You have already used the " + list(help_types)[x] + " help!")
                if chosen_help != "phone":
                    if chosen_help_values[1] == "OK":
                        answer = safe_input(
                            "\nSelect the correct answer ('a','b','c','d'), 't' for guessing out of game or 'h' for help! ",
                            ["a", "b", "c", "d", "h", "t"], correct_answer_key)
                    else:
                        answer = safe_input(
                            "\nSelect the correct answer ('a','b','c','d'), 't' for guessing out of game or 'h' for help! ",
                            ["a", "b", "c", "d", "h", "t"], chosen_help_values[1])
                else:
                    if chosen_help_values[2] == "OK":
                        answer = safe_input(
                            "\nSelect the correct answer ('a','b','c','d'), 't' for guessing out of game or 'h' for help! ",
                            ["a", "b", "c", "d", "h", "t"], correct_answer_key)
                    else:
                        answer = safe_input(
                            "\nSelect the correct answer ('a','b','c','d'), 't' for guessing out of game or 'h' for help! ",
                            ["a", "b", "c", "d", "h", "t"], chosen_help_values[2])

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
                safe_input("press ENTER for main menu..", ["enter"], return_inputs[0])
        else:
            print(fg.red + "Bad answer! Better luck next time!" + fg.rs)
            safe_input("press ENTER for main menu..", ["enter"], return_inputs[0])
            util.clear_screen()
            return
        util.clear_screen()

    return


def safe_input(input_text: str, allowed_list_of_letters: list, hotkey: str) -> str:
    print(input_text)
    keyboard.press_and_release(hotkey)
    answer = hotkey
    if answer not in allowed_list_of_letters:
        print("Error! Only letters: " + ' '.join(allowed_list_of_letters) + " allowed!")
    while answer not in allowed_list_of_letters:
        answer = keyboard.read_key()
    if answer != "enter":
        print(answer)
    time.sleep(1)

    return answer


def get_dictionary_key_by_value(dictionary: {}, value: str) -> str:
    for choice, answerValue in dict.items(dictionary):
        if answerValue == value:
            return choice


def check_answer(answer: str, correct_answer: str) -> bool:
    return answer == correct_answer


def show_prize(round_number: int) -> str:
    return prizes[round_number]


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
    print("Call Duration: ", int(now - then), " seconds\\ 30s")
    util.stop_sound()


def telephone_help(question: str, answers: {}, correct_answer: str, hotkey: str):
    phone = safe_input(
        "Who'd you like to call?\n"
        "for mum, press 'm'\n"
        "for dad press 'd'\n"
        "for old teacher from high school press 't'\n"
        "for Maester Yoda press 'y': ",
        ["m", "d", "t", "y"], hotkey)
    call_text_files = ["mum_phone.txt", "dad_phone.txt", "teacher_phone.txt", "yoda_master_phone.txt"]
    for i in range(len(call_text_files)):
        if phone.lower() == call_text_files[i][0]:
            text = (util.open_file(call_text_files[i], 'r'))
            print_phone_conversation(text, question, answers, correct_answer)


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
        for k in range(len(chances)):
            if str(answers[answers_list[k]]) != "":
                print(str(answers_list[k]) + " : " + str(answers[answers_list[k]]) + " || " + str(chances[k]) + "%")
            else:
                print(str(answers_list[k]) + " : ")
        time.sleep(1)
        if i != len(answers_list) - 1:
            util.clear_screen()


def get_chances(answers: {}, correct_value: str) -> list:
    answers_list = list(answers.keys())
    chances_dict = {}
    correct_answer = get_dictionary_key_by_value(answers, correct_value)
    chances_dict[correct_answer] = random.randrange(40, 89)
    answers_list.pop(answers_list.index(correct_answer))
    for k in range(len(answers_list)):
        if k == len(answers_list)-1:
            chances_dict[answers_list[k]] = 100 - sum(chances_dict.values())
        else:
            chances_dict[answers_list[k]] = random.randrange(0, 100 - sum(chances_dict.values()))
    chances = sorted(chances_dict.values(), reverse=True)

    return chances
