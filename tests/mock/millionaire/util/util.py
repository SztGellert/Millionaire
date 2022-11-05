import json
import os
import pathlib
from collections import namedtuple

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame

operating_system = os.name
language_dictionary = {}
available_languages = ["en", "hu"]
game_language = available_languages[0]


def init():
    pygame.mixer.init()


def init_language(selected_lang: str) -> dict:
    for lang in available_languages:
        lang_dict = read_json_dict(selected_lang)
        language_dictionary.update({lang: custom_dictionary_decoder(lang_dict)})
        """
        print("\nPrinting nested dictionary as a key-value pair\n")
        for i in data['people1']:
            print("Name:", i['name'])
            print("Website:", i['website'])
            print("From:", i['from'])
            print()
            """
    return language_dictionary


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
    with open(file_path, mode, encoding="UTF-8") as file:
        list_of_file = []
        for line in file:
            line = line.strip().split(',')
            list_of_file.append(line)
    return list_of_file


def stop_sound():
    pygame.mixer.music.stop()


def read_json_dict(file_name: str) -> {}:
    file_path = get_data_path() + "/language_files/" + file_name + ".json"
    with open(file_path, encoding="UTF-8") as json_file:
        data = json.load(json_file)

        return data


def custom_dictionary_decoder(dict1):
    for key, value in dict1.items():
        if type(value) is dict:
            dict1[key] = custom_dictionary_decoder(value)
    return namedtuple('X', dict1.keys())(*dict1.values())