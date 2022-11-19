import json
import os
import pathlib
from collections import namedtuple

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame

operating_system = os.name
available_languages = ["en", "hu"]
game_language = available_languages[0]
language_dictionary = {}
question_topics = "All "
question_difficulty = ""


def init():
    pygame.mixer.init()
    init_settings(available_languages[0])


def init_settings(selected_lang: str):
    global game_language
    global question_topics
    global language_dictionary
    global question_difficulty

    if os.path.isfile("settings.json"):
        file_path = "settings.json"
        with open(file_path, encoding="UTF-8") as json_file:
            data = json.load(json_file)
            global game_language
            game_language = data["language"]
            question_difficulty = data["difficulty"]
            for lang in available_languages:
                lang_dict = read_json_dict(lang)
                language_dictionary.update({lang: custom_dictionary_decoder(lang_dict)})
            lang_dict = read_json_dict(game_language)
            language_dictionary.update({game_language: custom_dictionary_decoder(lang_dict)})
            question_topics = data["topic"]
    else:
        for lang in available_languages:
            lang_dict = read_json_dict(selected_lang)
            language_dictionary.update({lang: custom_dictionary_decoder(lang_dict)})
            game_language = selected_lang
            question_topics = language_dictionary[game_language].menu.settings_menu_question_topics[0]


def init_question_topics(selected_topic: str):
    global question_topics
    question_topics = selected_topic


def clear_screen():
    if operating_system == "posix":
        os.system('clear')
    else:
        os.system('cls')


def play_sound(filename, starting_time, volume=0.07):
    file_path = get_data_path() + "/sound_files/" + filename
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(0, starting_time)


def get_data_path() -> str:
    if operating_system == "posix":
        path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
        data_path = path + "/data"
    else:
        data_path = "../data"

    return data_path


def open_file(filename: str, mode: str, separator=",") -> list:
    file_path = get_data_path() + "/text_files/" + filename
    with open(file_path, mode, encoding="UTF-8") as file:
        list_of_file = []
        for line in file:
            line = line.strip().split(separator)
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


def set_question_topics(selected_topic: str):
    global question_topics
    question_topics = selected_topic


def set_question_difficulty(level: str):
    global question_difficulty
    question_difficulty = level


def set_game_language(selected_lang: str):
    global game_language
    global question_topics
    for lang in available_languages:
        lang_dict = read_json_dict(selected_lang)
        language_dictionary.update({lang: custom_dictionary_decoder(lang_dict)})
        game_language = selected_lang
        question_topics = language_dictionary[game_language].menu.settings_menu_question_topics[0]
