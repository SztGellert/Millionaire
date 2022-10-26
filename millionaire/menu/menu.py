import os
import pathlib
import sys
import time

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame
from sty import Style, RgbFg, fg, bg
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

operating_system = os.name
options = ["Play", "Help", "Credit", "Exit"]
fg.purple = Style(RgbFg(148, 0, 211))
select_msg = "Select Menu Option: "
return_msg = "Press ENTER to return to main menu..."


def intro():
    pygame.mixer.init()
    clear_screen()
    play_sound("loim_intro.wav", 0)
    time.sleep(2)
    file = (open_file("intro.txt", 'r'))
    for line_index in range(len(file)):
        if line_index == 3:
            print(fg.purple + file[line_index][0] + fg.rs)
            time.sleep(2)
        else:
            print(file[line_index][0])
        time.sleep(1)


def show_title():
    line_length = len(select_msg) + 3
    clear_screen()
    print("=" * line_length)
    print(fg.purple + " ♦ WHO WANTS TO BE A ♦" + fg.rs)
    print("=" * line_length)
    print(fg.yellow + "|" * line_length + fg.rs)
    print(fg.purple + " M I L L I O N A I R E" + fg.rs)
    print(fg.yellow + "|" * line_length + fg.rs)
    print("=" * line_length)
    print(fg.purple + " ♦ WHO WANTS TO BE A ♦" + fg.rs)
    print("=" * line_length + "\n\n")


def show_options():
    i = 1
    fore_string = "| "
    after_string = " |"
    line_length = len(select_msg) + 3
    option_length = len(select_msg)
    for option in options:
        number_of_spaces = int((option_length - len(option) - len(fore_string) - len(after_string)) / 2)
        print("-" * line_length)
        string_to_print = fore_string + "[" + option[
            0] + "]" + number_of_spaces * " " + option + number_of_spaces * " " + after_string
        print(string_to_print)
        i += 1
    print("-" * line_length + "\n")


def get_user_input():
    input_text = "\n" + select_msg
    allowed_characters = ["p", "h", "c", "e"]
    choise = input(input_text)
    while choise not in allowed_characters:
        print("Error! Only options: " + ' '.join(allowed_characters) + " allowed!")
        choise = input("Select an option from the list above!")

    return choise


def exit():
    sys.exit(0)


def clear_screen():
    if operating_system == "posix":
        os.system('clear')
    else:
        os.system('cls')


def play_sound(filename, starting_time):
    file_path = get_data_path() + "/sound_files/" + filename
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(0.07)
    pygame.mixer.music.play(0, starting_time)


def get_data_path() -> str:
    if operating_system == "posix":
        path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
        data_path = path + "/data"
    else:
        data_path = "../data"

    return data_path


def help():
    clear_screen()
    file = (open_file("tutorial.txt", 'r'))
    for line in file:
        print(line[0])
    return_prompt()


def credits():
    clear_screen()
    file = (open_file("credits.txt", 'r'))
    for line in file:
        print(line[0])
    return_prompt()


def open_file(filename, mode):
    file_path = get_data_path() + "/text_files/" + filename
    with open(file_path, mode) as file:
        list_of_file = []
        for line in file:
            line = line.strip().split(',')
            list_of_file.append(line)
    return list_of_file


def return_prompt():
    input_text = fg.red + "\n" + return_msg + fg.rs
    input(input_text)
    clear_screen()
