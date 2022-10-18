import random
import sys
import os
from sty import Style, RgbFg, fg, bg
import time
import pygame

operating_system = os.name
fg.purple = Style(RgbFg(148, 0, 211))
fg.orange = Style(RgbFg(255, 150, 50))
fg.green = Style(RgbFg(0, 255, 0))
bg.orange = bg(255, 150, 50)
help_types = {"audience": True, "telephone": True, "halving": True}


def intro():
    pygame.mixer.init()
    clear_screen(operating_system)
    play_sound("loim_intro.wav", 0)
    time.sleep(2)
    print(
        "This is the game of games..\nIn the arena..\nMr Steven Vágó is awaiting You!\n" + fg.purple + "Become the next Millionaire!\n" + fg.rs)
    time.sleep(5)


def play_sound(filename, starting_time):
    filepath = "./data/sound_files/"
    pygame.mixer.init()
    pygame.mixer.music.load(filepath + filename)
    pygame.mixer.music.set_volume(0.07)
    pygame.mixer.music.play(0, starting_time)


def open_file(filename, mode):
    file_path = "./data/text_files/" + filename
    with open(file_path, mode) as file:
        list_of_file = []
        for line in file:
            line = line.strip().split(',')
            list_of_file.append(line)
    return list_of_file


def safe_input(input_text, allowed_list_of_letters):
    answer = input(input_text)
    while answer not in allowed_list_of_letters:
        print("Error! Only letters: " + ' '.join(allowed_list_of_letters) + " allowed!")
        answer = input("Select the correct answer!")
    return answer


def print_phone_conversation(text, question, good_answer):
    play_sound("phone_ring.mp3", 0)
    time.sleep(2)
    play_sound("phone_call.mp3", 0)
    then = time.time()
    print(fg.orange + str(30 - int(time.time() - then)) + fg.rs)
    time.sleep(2)
    print(''.join(text[0]))
    print("\n" + ''.join(question))
    print(fg.orange + str(30 - int(time.time() - then)) + fg.rs)
    time.sleep(2)
    print(''.join(text[1]))
    print(fg.orange + str(30 - int(time.time() - then)) + fg.rs)
    time.sleep(2)
    print(fg.red + ''.join(text[2]) + fg.rs)
    print(fg.orange + str(30 - int(time.time() - then)) + fg.rs)
    time.sleep(2)
    print(''.join(text[3]))
    if text[2][0] == 'I call the Force for help!':
        print(''.join(text[4]))
        print(good_answer + "\n")
        print(''.join(text[5]))
    else:
        print(''.join(text[4]))
        print(good_answer + "\n")
    print(fg.orange + str(30 - int(time.time() - then)) + fg.rs)
    now = time.time()
    play_sound('phone_call.mp3', 30.0)
    time.sleep(3)
    print("Call Duration: ", int(now - then), " seconds\\ 30 a")
    pygame.mixer.music.stop()


def telephone_help(question, answers, correct_answer):
    phone = safe_input(
        "Who'd you like to call?\n"
        "for mum, press 'm'\n"
        "for dad press 'd'\n"
        "for old teacher from high school press 't'\n"
        "for Maester Yoda press 'y': ",
        ["m", "d", "t", "y"])
    call_list = ['m', 'd', 't', 'y']
    call_text_files = ["mum_phone.txt", "dad_phone.txt", "teacher_phone.txt", "yoda_master_phone.txt"]
    for letter in range(len(call_list)):
        if phone.lower() == call_list[letter]:
            text = (open_file(call_text_files[letter], 'r'))
            print_phone_conversation(text, question, correct_answer)


def halving(answers: {}, correct_answer: str):
    clear_screen(operating_system)
    time.sleep(2)
    play_sound("halving.mp3", 0)
    possibilities = ["a", "b", "c", "d"]
    possibilities.pop(list(answers).index(correct_answer))
    second = random.choice(possibilities)

    for i in answers:
        if i == correct_answer:
            print(i + ": " + answers[correct_answer])
        elif i == second:
            print(i + ": " + answers[second])
        else:
            print(i + ": ")


"""
def stop_game_and_guess_out_of_game(answer, Help_available, table_line_length, prices, prices1, prices2, counter, current_line, answers, choises, shuffled_line, question):
    if answer.lower() == "s":
        clear_screen(operating_system)
        play_sound("data/sound_files/zene_le.mp3", 0)
        print_lists(Help_available, table_line_length)
        quiz_table(table_line_length, choises, question, shuffled_line)
        answer = safe_input("\nSelect the correct answer (a,b,c,d)! ", ["a", "b", "c", "d"])
        marking(answer, current_line, answers, choises, table_line_length, shuffled_line, question, Help_available)
        clear_screen(operating_system)
        print_lists(Help_available, table_line_length)
        print("  "+bg.black+"/"+"‾"*(table_line_length-6)+"\\"+bg.rs)
        width = table_line_length
        if counter == 0:
            won_prize = "0 Ft."
            len_table = len("‾"*(table_line_length-6-len(won_prize)))
        else:
            won_prize = prices[counter-1]
            len_table = len("‾"*(table_line_length-len(prices2[counter-1])))
        print("-"+bg.black+"‹"+fg.orange+''.join(won_prize.center((width-4), ' '))+fg.rs+"›"+bg.rs+"-")
        print("  "+bg.black+"\\"+"_"*(table_line_length-6)+"/"+bg.rs)
        time.sleep(3)
        sys.exit(0)
"""


def clear_screen(os_sys: str):
    if os_sys == "posix":
        os.system('clear')
    else:
        os.system('cls')


def get_dictionary_key_by_value(dictionary: {}, value: str):
    for choice, answerValue in dict.items(dictionary):
        if answerValue == value:
            return choice


def show_price(round_number: int):
    prices = ["5.000 Ft", "10.000 Ft", "25.000 Ft", "50.000 Ft", "100.000 Ft", "200.000 Ft", "300.000 Ft", "500.000 Ft",
              "800.000 Ft", "1.500.000 Ft", "3.000.000 Ft", "5.000.000 Ft", "10.000.000 Ft", "20.000.000 Ft",
              "40.000.000 Ft"]
    return prices[round_number]


def quiz():
    clear_screen(operating_system)
    for i in range(15):
        question_lines = open_file('questions.txt', "r")
        random.shuffle(question_lines)
        print(question_lines[i][0])
        answers = {"a": question_lines[i][1], "b": question_lines[i][2], "c": question_lines[i][3],
                   "d": question_lines[i][4]}
        answer_list = list(answers.values())
        random.shuffle(answer_list)
        shuffled_answers = dict(zip(answers, answer_list))
        for k in range(len(answer_list)):
            print(list(answers.keys())[k] + ": " + answer_list[k])
        answer = safe_input("\nSelect the correct answer ('a','b','c','d') or 'h' for help! ",
                            ["a", "b", "c", "d", "h"])
        correct_answer = get_dictionary_key_by_value(shuffled_answers, question_lines[i][1])

        if answer == "h":
            show_help_types(question_lines[i][0], shuffled_answers, correct_answer)
            answer = safe_input("\nSelect the correct answer ('a','b','c','d') ! ",
                                ["a", "b", "c", "d"])
            # is_correct = check_answer(answer, correct_answer)
            time.sleep(2)
            clear_screen(operating_system)

        play_sound("marked.mp3", 0)
        time.sleep(2)
        is_correct = check_answer(answer, correct_answer)
        if is_correct:
            if i < 14:
                play_sound("correct_answer.mp3", 0)
                if i == 4:
                    print(fg.yellow + "You have guaranteed 100.000 Ft" + fg.rs)
                    time.sleep(1)
                elif i == 9:
                    print(fg.yellow + "You have guaranteed 1.500.000 Ft" + fg.rs)
                    time.sleep(1)
                else:
                    print(fg.green + "Well Done!" + fg.rs)
                    clear_screen(operating_system)
                    print(bg.orange + show_price(i) + bg.rs)
                    time.sleep(2)
            else:
                play_sound("great_logic.mp3", 0)
                time.sleep(1)
                clear_screen(operating_system)
                print(fg.purple + "Congratulations! You have won 40 000 000 Ft!" + fg.rs)
                play_sound("winning_theme.mp3", 0)
                time.sleep(35)
                sys.exit(0)
        else:
            print(fg.red + "Bad answer! Better luck next time!" + fg.rs)
            if safe_input("Would you like to play again? ('y'/'n')", ['y', 'n']) == 'y':
                clear_screen(operating_system)
                quiz()
            else:
                sys.exit(0)
        clear_screen(operating_system)


def check_answer(answer: str, correct_answer: str):
    return answer == correct_answer


def show_help_types(question: str, answers: {}, correct_answer: str):
    chosen_help = safe_input("Choose help: 'a' for audience, 't' for telephone, 'h' for halving! ", ["a", "t", "h"])
    if chosen_help.lower() == "a":
        if help_types["audience"]:
            # clear_screen(operating_system)
            audience_help(correct_answer)
            # audience_help(answers, current_line, question, table_line_length, choises, shuffled_line,
            #               Help_available)
            help_types["audience"] = False
        else:
            print("You have already used the audience's help!")

    if chosen_help.lower() == "t":
        if help_types["telephone"]:
            telephone_help(question, answers, correct_answer)
            help_types["telephone"] = False
        else:
            print("You have already used the telephone help!")

    if chosen_help.lower() == "h":
        if help_types["halving"]:
            halving(answers, correct_answer)
            help_types["halving"] = False
            # print_lists(Help_available, table_line_length, 'vago_helping.txt')
            # quiz_table(table_line_length, choises, question, shuffled_line)
        else:
            print("You have already used the halving help!")


def audience_help(correct_answer: str):
    play_sound("kozonseg.mp3", 0)
    answers_list = ["a", "b", "c", "d"]
    chances = get_chances()
    chances.sort(reverse=True)
    answers = {}
    for i in range(4):
        if answers_list[i] == correct_answer and chances[i] == correct_answer:
            answers[answers_list[i]] = chances[0]
        else:
            answers[answers_list[i]] = chances[i]
    time.sleep(1)
    for i in answers:
        print(i + " : " + str(answers[i]) + "%")
    time.sleep(1)


def get_chances() -> list:
    percents = []
    percents.append(random.randrange(40, 89))
    percents.append(random.randrange(0, 100 - percents[0]))
    percents.append(random.randrange(0, 100 - sum(percents[0:2])))
    percents.append(100 - sum(percents[0:3]))
    return percents

    """"
    Code for confirmation dialog & stopping 
    
    list_of_are_you_sure_sound_files = ["./sound_files/vegleges.mp3", "./sound_files/vegleges2.mp3", "./sound_files/vegleges3.mp3", "./sound_files/vegleges4.mp3", "./sound_files/vegyem_veglegesnek.mp3"]
    are_you_sure_sound = choose_random_from_list(list_of_are_you_sure_sound_files)
   
    play_sound(are_you_sure_sound, 0)
    time.sleep(1)
    answer = safe_input("Are you sure? ", ["a", "b", "c", "d", "s"])
    
    stop_game_and_guess_out_of_game(answer, Help_available, table_line_length, prices, prices1, prices2, counter,current_line, answers, choises, shuffled_line, question)
    
    answer=marking(answer, current_line, answers, choises, table_line_length, shuffled_line, question, Help_available)[1]
    
    clear_screen(operating_system)
    print_lists(Help_available, table_line_length)
    quiz_table(table_line_length, choises, question, shuffled_line)
    play_sound("./sound_files/marked.mp3", 0)
    time.sleep(4)

    """
