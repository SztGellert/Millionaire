import os
import pathlib

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
os.environ['SDL_AUDIODRIVER'] = 'dsp'
import pygame

operating_system = os.name


def init():
    pygame.mixer.init()


def clear_screen():
    if operating_system == "posix":
        os.system('clear')
    else:
        os.system('cls')


def play_sound(filename, starting_time):
    file_path = get_data_path() + "/sound_files/" + filename
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


def open_file(filename: str, mode: str) -> list:
    file_path = get_data_path() + "/text_files/" + filename
    with open(file_path, mode) as file:
        list_of_file = []
        for line in file:
            line = line.strip().split(',')
            list_of_file.append(line)
    return list_of_file


def stop_sound():
    pygame.mixer.music.stop()
