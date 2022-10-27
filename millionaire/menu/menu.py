import sys
import time
import keyboard
from util import util
from sty import Style, RgbFg, fg, bg

options = ["Play", "Help", "Credit", "Exit"]
fg.purple = Style(RgbFg(148, 0, 211))
select_msg = "Select Menu Option: "
return_msg = "Press ENTER to return to main menu..."
bg.orange = bg(255, 150, 50)


def intro():
    util.clear_screen()
    util.play_sound("loim_intro.wav", 0)
    time.sleep(2)
    file = (util.open_file("intro.txt", 'r'))
    for line_index in range(len(file)):
        if line_index == 3:
            print(fg.purple + file[line_index][0] + fg.rs)
            time.sleep(2)
        else:
            print(file[line_index][0])
        time.sleep(1)


def show_title():
    line_length = len(select_msg) + 3
    util.clear_screen()
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


def select_exit():
    sys.exit(0)


def select_help():
    util.clear_screen()
    file = (util.open_file("tutorial.txt", 'r'))
    for line in file:
        print(line[0])
    return_prompt()


def select_credits():
    util.clear_screen()
    file = (util.open_file("credits.txt", 'r'))
    for line in file:
        print(line[0])
    return_prompt()


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
