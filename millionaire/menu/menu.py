import os
import pathlib
import sys
import time
import keyboard
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame
from sty import Style, RgbFg, fg, bg

operating_system = os.name
options = ["Play", "Help", "Credit", "Exit"]
fg.purple = Style(RgbFg(148, 0, 211))
select_msg = "Select Menu Option: "
return_msg = "Press ENTER to return to main menu..."
bg.orange = bg(255, 150, 50)


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



def show_options(chosen_option=0):
    show_title()
    fore_string = "| "
    after_string = " |"
    line_length = len(select_msg)
    option_length = len(select_msg)
    for i in range(len(options)):
        option = options[i]
        number_of_spaces = int((option_length - len(options[i]) - len(fore_string) - len(after_string)) / 2)
        print("  " + "-" * line_length)
        if i == chosen_option:
            string_to_print = "  " + fore_string + bg.orange + number_of_spaces * " " + fg.black + option + fg.rs + number_of_spaces * " " + bg.rs + after_string
        else:
            string_to_print = "  " + fore_string + number_of_spaces * " " + option + number_of_spaces * " " + after_string
        print(string_to_print)
    print("  " + "-" * line_length + "\n")


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
    print(fg.red + "\n" + return_msg + fg.rs)
    if keyboard.read_key() == "enter":
        return


def get_user_input() -> str:
    i = 0
    while True:
        if keyboard.read_key() == "enter":
            return options[i][0].lower()
        if keyboard.read_key() == 'down':
            if i == 3:
                i = 0
                show_options()
            else:
                i += 1
                show_options(i)
            if keyboard.read_key() == "enter":
                return options[i][0].lower()
        if keyboard.read_key() == 'up':
            if i == 0:
                i = 3
                show_options(3)
            else:
                i -= 1
                show_options(i)
            if keyboard.read_key() == "enter":
                return options[i][0].lower()
