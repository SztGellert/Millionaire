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
languages = ["en", "hu"]
lang = "en"
text = {}

def play():
    language_select = safe_input("Please select a language: 'e' for english and 'h' for hungarian:", ["0", "1"])
    text = util.init_language(languages[int(language_select)])
    lang = languages[int(language_select)]
    help_types = {"audience": True, "telephone": True, "halving": True}
    util.clear_screen()
    util.play_sound("lom.mp3", 0)
    time.sleep(2)
    question_file = 'questions_' + lang + ".txt"
    question_lines = util.open_file(question_file, "r")
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
            text[lang].quiz.select_answer,
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
                answer = safe_input(text[lang].quiz.select_answer_out,
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
                        print(fg.blue + text[lang].quiz.correct_answer_out + fg.rs)
                        util.play_sound("show_stop.mp3", 0)
                        time.sleep(1)
                else:
                    print(fg.red + text[lang].quiz.incorrect_answer + fg.rs)
                    util.play_sound("so_sorry.mp3", 0)
                    time.sleep(1)
                safe_input(text[lang].menu.return_prompt, ["enter"])
                util.clear_screen()
                return
            if answer == "h":
                util.clear_screen()
                print(question)
                for k in range(len(answer_list)):
                    print(list(answers.keys())[k] + ": " + answer_list[k])
                help_functions = {"audience": audience_help, "telephone": telephone_help, "halving": halving}
                chosen_help_type = safe_input(text[lang].quiz.help_selection,
                                              ["a", "t", "h"])
                for x in range(len(help_types)):
                    if chosen_help_type.lower() == list(help_types)[x][0]:
                        if help_types[list(help_types)[x]]:
                            if list(help_types)[x] == "halving":
                                shuffled_answers = list(help_functions.values())[x](question, shuffled_answers, correct_answer_value)
                                for a in range(len(answer_list)):
                                    answer_list[a] = list(shuffled_answers.values())[a]
                            else:
                                list(help_functions.values())[x](question, shuffled_answers, correct_answer_value)
                            help_types[list(help_types)[x]] = False
                            break
                        else:
                            print(text[lang].quiz.help_disabled + list(help_types)[x] + " " + text[lang].quiz.help)
                answer = safe_input(
                    text[lang].quiz.select_answer,
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
                    print(fg.yellow + text[lang].quiz.guaranteed_prize + show_prize(i) + fg.rs)
                    util.play_sound("won_hundred_bucks.mp3", 0)
                    time.sleep(1)
                elif i == 9:
                    print(fg.yellow + text[lang].quiz.guaranteed_prize + show_prize(i) + fg.rs)
                    util.play_sound("now_comes_hard_part.mp3", 0)
                    time.sleep(1)
                else:
                    print(fg.green + text[lang].quiz.correct_answer, + fg.rs)
                    util.clear_screen()
                    print(bg.orange + show_prize(i) + bg.rs)
                    time.sleep(2)
            else:
                util.play_sound("great_logic.mp3", 0)
                time.sleep(1)
                util.clear_screen()
                print(fg.purple + text[lang].quiz.won_prize + show_prize(i) + " !" + fg.rs)
                util.play_sound("winning_theme.mp3", 0)
                time.sleep(35)
                safe_input(text[lang].menu.return_prompt, ["enter"])
        else:
            print(fg.red + text[lang].quiz.incorrect_answer + fg.rs)
            safe_input(text[lang].menu.return_prompt, ["enter"])
            util.clear_screen()
            return
        util.clear_screen()

    return


def safe_input(input_text: str, allowed_list_of_letters: list) -> str:
    print(input_text)
    answer = keyboard.read_key()
    if answer not in allowed_list_of_letters:
        print(text[lang].quiz.allowed_letters_error + ' '.join(allowed_list_of_letters) + text[lang].quiz.allowed)
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
    prizes = util.open_file("prizes_" + lang + ".txt", "r")
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
    print(text[lang].quiz.call_duration, int(now - then), text[lang].quiz.call_seconds)
    util.stop_sound()


def telephone_help(question: str, answers: {}, correct_answer: str):
    phone = safe_input(text[lang].quiz.phone_prompt,
        ["m", "d", "t", "y"])
    call_text_files = ["mum_phone_" + lang + ".txt",
                       "dad_phone_" + lang + ".txt",
                       "teacher_phone_" + lang + ".txt",
                       "yoda_master_phone_" + lang + ".txt"
                       ]
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

