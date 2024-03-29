import copy
import json
import os
import random
import time
from math import sin, cos, radians

import pygame
import requests

import millionaire.util.util as util
import millionaire.menu.menu as menu

languages = util.available_languages
language_dictionary = util.language_dictionary
game_levels = 15
threads = []
help_types = {"halving": True, "telephone": True, "audience": True}


class TableElement(pygame.sprite.Sprite):

    def __init__(self, type, text):
        super().__init__()
        self.text_size = 33
        self.text_x = 110
        self.text_y = 20

        self.base_text = text
        self.correct_option: pygame.Surface

        # size 33 max 24 length text y 20 cd:15
        # size 25 max 32 length text y 25 cd:20
        # size 18 max 44 length y 30 cd: 25

        self.is_active = self.get_is_active()
        if type not in ["question", "prize"]:
            if not self.is_active:
                text = ""
            if len(text) > 32:
                self.text_size = 18
                self.text_y = 30
            elif len(text) > 24:
                self.text_size = 25
                self.text_y = 25
            else:
                self.text_size = 33
                self.text_y = 20

        if type == "a":
            self.text_x = 165

            self.frame = pygame.image.load('./data/graphics/option_a.png').convert_alpha()
            self.selected_option = pygame.image.load('./data/graphics/option_a_marked.png').convert_alpha()
            self.pre_marked_option = pygame.image.load('./data/graphics/option_a_pre_marked.png').convert_alpha()

            x_pos = 342
            y_pos = 643

        elif type == "b":
            self.text_x += 5

            self.frame = pygame.image.load('./data/graphics/option_b.png').convert_alpha()
            self.selected_option = pygame.image.load('./data/graphics/option_b_marked.png').convert_alpha()
            self.pre_marked_option = pygame.image.load('./data/graphics/option_b_pre_marked.png').convert_alpha()

            x_pos = 1021
            y_pos = 644

        elif type == "c":
            self.text_x = 165
            self.text_y = self.text_y - 5

            self.frame = pygame.image.load('./data/graphics/option_c.png').convert_alpha()
            self.selected_option = pygame.image.load('./data/graphics/option_c_marked.png').convert_alpha()
            self.pre_marked_option = pygame.image.load('./data/graphics/option_c_pre_marked.png').convert_alpha()

            x_pos = 342
            y_pos = 719

        elif type == "d":
            self.text_x = 120
            self.text_y = self.text_y - 5

            self.frame = pygame.image.load('./data/graphics/option_d.png').convert_alpha()
            self.selected_option = pygame.image.load('./data/graphics/option_d_marked.png').convert_alpha()
            self.pre_marked_option = pygame.image.load('./data/graphics/option_d_pre_marked.png').convert_alpha()

            x_pos = 1022
            y_pos = 719

        else:

            if type == "prize":
                self.frame = pygame.image.load('./data/graphics/prize_.png').convert_alpha()
                x_pos = 683
                y_pos = 555

            else:
                self.frame = pygame.image.load('./data/graphics/question.png').convert_alpha()
                x_pos = 683
                y_pos = 555

        font = pygame.font.SysFont('Sans', self.text_size)
        color = (255, 255, 255)
        if type == "prize":
            self.text_size = 33
            font = pygame.font.SysFont('Sans', self.text_size, bold=True)
            color = (245, 148, 41)

        self.text = font.render(text, True, color)

        self.type = type
        self.image = self.frame
        if type == "prize":
            width = 1366

            font = pygame.font.SysFont('Sans', 56, bold=True)

            self.text_1 = font.render(text, True, color)
            text_rect_1 = self.text_1.get_rect(center=(width / 2, 48))
            self.image.blit(self.text_1, text_rect_1)
        if type == "question":
            self.text_y = 8
            width = 1366
            delimiter = 86
            if len(text) > delimiter:
                if len(text) > 2 * delimiter:
                    font = pygame.font.SysFont('Sans', 18)
                    delimiter = 110

                # draw text
                # font = pygame.font.Font(None, 25)
                # text = font.render("You win!", True, BLACK)
                # text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                # screen.blit(text, text_rect
                self.text_1 = font.render(text[:delimiter], True, color)
                text_rect_1 = self.text_1.get_rect(center=(width / 2, 35))
                self.image.blit(self.text_1, text_rect_1)

                self.text_2 = font.render(text[delimiter:], True, color)
                text_rect_2 = self.text_2.get_rect(center=(width / 2, 70))
                self.image.blit(self.text_2, text_rect_2)

            else:
                # self.text_size = 18
                text_rect = self.text.get_rect(center=(width / 2, 45))

                self.image.blit(self.text, text_rect)
            self.rect = self.image.get_rect(center=(x_pos, y_pos))

        if type not in ["question", "prize"]:
            self.image.blit(self.text, [self.text_x, self.text_y])
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    def get_is_active(self):
        if hasattr(self, 'is_active'):
            return self.is_active
        else:
            return True

    def set_is_active(self):
        self.is_active = True

    def unset_is_active(self):
        self.is_active = False

    def player_input(self):
        if pygame.mouse.get_pressed()[0] and self.type != 'question':
            self.animation_state()

    def update(self, selected_, correct, type_="select"):
        global selected
        global type

        self.is_active = self.get_is_active()
        if not self.is_active:
            self.kill()
        if type_ == "select":
            if selected_ == self.type:
                self.image = self.selected_option
                self.image.blit(self.text, [self.text_x, self.text_y])

        elif type_ == "mark":
            if correct == self.type:
                self.correct_option = pygame.image.load(
                    './data/graphics/option_' + self.type + '_won.png').convert_alpha()
                self.image = self.correct_option
                self.image.blit(self.text, [self.text_x, self.text_y])
        elif type_ == "pre_marked":
            if selected_ == self.type:
                self.image = self.pre_marked_option
                self.image.blit(self.text, [self.text_x, self.text_y])
                type = "select"
                selected = ""
        else:

            if type_ == "fastest_fingers_select":
                global fastest_fingers_result
                global fastest_fingers_mark_event
                if self.type != "question" and selected != "":
                    if self.type == selected and self.type not in fastest_fingers_result:
                        self.image = self.selected_option
                        fastest_fingers_result += selected
                        font = pygame.font.SysFont('Sans', self.text_size)
                        color = (255, 255, 255)
                        self.text = font.render(str(len(fastest_fingers_result)) + ": " + self.base_text, True, color)
                        self.image.blit(self.text, [self.text_x, self.text_y])
                    if len(fastest_fingers_result) == 4:
                        fastest_fingers_mark_event = pygame.USEREVENT + 1
                        type = "fastest_fingers_mark"

    def animation_state(self):
        self.image = self.selected_option


class Prizes(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.frame = pygame.image.load('./data/graphics/question_0_prize.png').convert_alpha()
        x_pos = 1150
        y_pos = 380

        self.image = self.frame
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    def update(self):
        global game_level
        global prize_table_seconds

        if prize_table_seconds > 3:
            self.image = pygame.image.load('./data/graphics/question_' + str(game_level) + '_prize.png').convert_alpha()
        else:
            self.image = pygame.image.load(
                './data/graphics/question_' + str(game_level + 1) + '_prize.png').convert_alpha()

    def animation_state(self):
        pass


class Help(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        font = pygame.font.SysFont('Sans', 25)
        self.correct_option = pygame.image.load('./data/graphics/option_correct.png').convert_alpha()

        self.selected_option = pygame.image.load('./data/graphics/option_marked.png').convert_alpha()

        if type == "halving":
            self.frame = pygame.image.load('./data/graphics/halving.png').convert_alpha()
            x_pos = 1003
            y_pos = 80

        elif type == "telephone":
            self.frame = pygame.image.load('./data/graphics/telephone.png').convert_alpha()
            x_pos = 1121
            y_pos = 80

        elif type == "teacher":
            self.frame = pygame.image.load('./data/graphics/teacher.png').convert_alpha()
            x_pos = 1121
            y_pos = 160
            self.is_dialed = False

        elif type == "chewbacca":
            self.frame = pygame.image.load('./data/graphics/chewbacca.png').convert_alpha()
            x_pos = 1003
            y_pos = 160
            self.is_dialed = False
        elif type == "clock":
            self.frame = pygame.image.load('./data/graphics/clock.png').convert_alpha()
            x_pos = 1121
            y_pos = 180
        elif type == "audience_table":
            self.frame = pygame.image.load('./data/graphics/audience_table.png').convert_alpha()
            x_pos = 1130
            y_pos = 290
        elif type == "random":
            self.frame = pygame.image.load('./data/graphics/random.png').convert_alpha()
            x_pos = 1240
            y_pos = 160
            self.is_dialed = False

        else:
            self.frame = pygame.image.load('./data/graphics/audience.png').convert_alpha()
            x_pos = 1240
            y_pos = 80
            self.is_consumed = False

        self.type = type
        self.image = self.frame
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    def player_input(self, correct_answer: ""):
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint((pygame.mouse.get_pos())):
            global help_types
            global help_group
            if self.type == "halving":
                self.halving(correct_answer)
                help_types[self.type] = False
            elif self.type == "telephone":
                self.phone_prologue()
                global phone_select
                phone_select = True

            elif self.type in ["teacher", "chewbacca", "random"]:
                global dial_event
                global intro_duration
                if not self.is_dialed:
                    dial_event = pygame.USEREVENT + 5
                    self.is_dialed = True
                if dial_event != 0:
                    self.phone_dial()
                    intro_duration = self.phone_intro()
            elif self.type == "audience":
                global audience_intro_duration
                global audience_intro_event
                if self.is_consumed == False:
                    audience_intro_event = pygame.USEREVENT + 7
                    audience_intro_duration = self.audience_prologue()
                    self.is_consumed = True
            else:
                pass

    def update(self, correct_answer: ""):

        global help_types
        global phone_event
        global help_group
        global phone_intro_event
        global intro_duration

        first_line = [(22, 32), (98, 82)]
        second_line = [(100, 30), (30, 82)]
        width = 11
        color = (207, 16, 26)

        if self.type not in ["teacher", "chewbacca", "random", "clock", "audience_table"]:
            if help_types["halving"] == False and self.type == "halving":
                pygame.draw.line(self.image, color, first_line[0], first_line[1], width=width)
                pygame.draw.line(self.image, color, second_line[0], second_line[1], width=width)
            if help_types["telephone"] == False and self.type == "telephone":
                pygame.draw.line(self.image, color, first_line[0], first_line[1], width=width)
                pygame.draw.line(self.image, color, second_line[0], second_line[1], width=width)

            if help_types["audience"] == False and self.type == "audience":
                pygame.draw.line(self.image, color, first_line[0], first_line[1], width=width)
                pygame.draw.line(self.image, color, second_line[0], second_line[1], width=width)

            if help_types[self.type]:
                self.player_input(correct_answer)
                if self.type == "audience":
                    if audience_event != 0:
                        if util.game_language == util.Language.HUNGARIAN.name:
                            self.audience_start()
                        else:
                            self.audience()
                        help_types["audience"] = False

        else:
            if self.type == "clock":
                if phone_event == 0:
                    self.kill()
            elif self.type == "audience_table":
                pass
            else:
                if help_types["telephone"]:
                    self.player_input(correct_answer)

                    if phone_intro_event == 0 and self.is_dialed and intro_duration <= 0:
                        for ob in help_group.sprites():
                            if ob.type in ["teacher", "chewbacca", "random"]:
                                help_group.remove(ob)
                        print(phone_intro_event)
                        self.phone()
                        phone_select = False
                        help_types["telephone"] = False
                        global type
                        type = "pre_marked"
                        global selected
                        selected = correct_answer
                        chance = random.randint(0, 10)
                        answers = ["a", "b", "c", "d"]
                        answers.remove(correct_answer)
                        if chance == 0:
                            selected = random.choice(answers)

    def halving(self, correct_answer):
        global obstacle_group
        choises = ["a", "b", "c", "d"]
        choises.remove(correct_answer)
        choises.remove(random.choice(choises))
        for ob in obstacle_group.sprites():
            if ob.type in choises:
                ob.unset_is_active()
        halving_before_sounds()
        global after_halving_event
        after_halving_event = pygame.USEREVENT + 1

    def audience_prologue(self):
        global help_group
        if util.game_language == util.Language.HUNGARIAN.name:
            options = []
            for ob in help_group.sprites():
                options.append(ob.type)
            if options == ["a", "b"]:
                prolouge = "audience_a_b"
            elif options == ["a", "c"]:
                prolouge = "audience_a_b"
            elif options == ["c", "d"]:
                prolouge = "audience_c_d"
            else:
                audience_prolouges = ["audience_isnt_calm", "then_ask_audience",
                                      "no_audience", "audience_intro", "audience_intro_1", "audience_intro_2",
                                      "audience_intro_3", "audience_intro_4",
                                      "audience_intro_5", "audience_intro_6"]
                prolouge = random.choice(audience_prolouges)
            util.play_sound(prolouge, 0, dir="audience")
            return util.get_sound_length(prolouge, dir="audience")
        else:
            return 0

    def audience_start(self):
        if util.game_language == util.Language.HUNGARIAN.name:
            util.play_sound("push_your_buttons", 0, dir="audience")
            time.sleep(2)

    def phone_prologue(self):
        global player_in_game
        if util.game_language == util.Language.HUNGARIAN.name:
            before_phone_sounds = ["if_you_want_phone_then_i_agree", "i_didnt_want_to_advise_phone", "we_dont_phone",
                                   "phone_broke", "we_dont_phone_two"]
            before_sound = random.choice(before_phone_sounds)
            util.play_sound(before_sound, 0, dir="phone", timer=True)

    def phone_dial(self):
        global dial_seconds
        if util.game_language == util.Language.HUNGARIAN.name:
            dial_sound = "colleagues_are_dialing"
            util.play_sound(dial_sound, 0, dir="phone", timer=True)
            dial_seconds = util.get_sound_length(dial_sound, dir="phone")

    def phone_intro(self) -> int:
        target = self.type
        if util.game_language == util.Language.HUNGARIAN.name:

            if target == "teacher":
                util.play_sound("teacher_intro", 0, dir="phone")
                return util.get_sound_length("teacher_intro", dir="phone")
            if target == "chewbacca":
                util.play_sound("chewbacca_intro", 0, dir="phone")
                return util.get_sound_length("chewbacca_intro", dir="phone")
            if target == "random":
                util.play_sound("weekly_seven_intro", 0, dir="phone")
                return util.get_sound_length("weekly_seven_intro", dir="phone")
        else:
            return 0

    def phone(self):
        global call_duration
        if util.game_language == util.Language.HUNGARIAN.name:

            if self.type == "teacher":
                util.play_sound("teacher", 0, dir="phone")
                call_duration = util.get_sound_length("teacher", dir="phone")
            if self.type == "chewbacca":
                util.play_sound("chewbacca", 0, dir="phone")
                call_duration = util.get_sound_length("chewbacca", dir="phone")
                util.play_background_sound("phone_call", 0, general=True)
            if self.type == "random":
                util.play_sound("weekly_seven", 0, dir="phone")
                call_duration = util.get_sound_length("weekly_seven", dir="phone")
        else:
            call_duration = 15
            util.play_background_sound("phone_call", 0, general=True)

    def audience(self):
        util.play_sound("audience", 0, general=True)


class MenuOption(pygame.sprite.Sprite):

    def __init__(self, type, order, base_height):
        super().__init__()

        x_pos = 685
        y_pos = base_height + (order * 35)

        self.frame = pygame.image.load('./data/graphics/option.png').convert_alpha()
        self.font = pygame.font.SysFont('Sans', 25)
        self.type = type
        self.text_color = (255, 255, 255)

        if type == "resume":
            text = language_dictionary[util.game_language].quiz.menu[order]
        elif type == "out_of_game":
            text = language_dictionary[util.game_language].quiz.menu[order]
        elif type == "exit":
            text = language_dictionary[util.game_language].quiz.menu[order]
        elif type == "settings":
            text = language_dictionary[util.game_language].quiz.menu[order]
        elif type == "quizmaster_attitude_option":
            text = language_dictionary[util.game_language].menu.quizmaster_attitudes[order]
        elif type == "language_option":
            text = [language_dictionary[util.game_language].en, language_dictionary[util.game_language].hu][order]
        else:
            text = ""

        self.name = text
        self.text = self.font.render(text, True, (255, 255, 255))
        self.image = self.frame
        self.image.blit(self.text, [30, 0])
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.lang = util.game_language
        self.order = order

    def get_is_active(self):
        if hasattr(self, 'is_active'):
            return self.is_active
        else:
            return True

    def set_is_active(self):
        self.is_active = True

    def unset_is_active(self):
        self.is_active = False

    def player_input(self):

        if self.rect.collidepoint((pygame.mouse.get_pos())):
            self.image = pygame.image.load('./data/graphics/option_marked.png').convert_alpha()
            self.image.blit(self.text, [30, 0])
        else:
            self.image = pygame.image.load('./data/graphics/option.png').convert_alpha()
            self.image.blit(self.text, [30, 0])

        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint((pygame.mouse.get_pos())):
            global game_active
            if self.name == language_dictionary[util.game_language].quiz.menu[0]:
                game_active = True
            if self.name == language_dictionary[util.game_language].quiz.menu[1]:
                menu.options = True
            if self.name == language_dictionary[util.game_language].quiz.menu[2]:
                global out_of_game
                out_of_game = True
                game_active = True
            if self.name == language_dictionary[util.game_language].quiz.menu[-1]:
                global exit_game
                exit_game = True

    def update(self):
        if self.lang != util.game_language:
            if self.type == "resume":
                text = language_dictionary[util.game_language].quiz.menu[self.order]
            elif self.type == "settings":
                text = language_dictionary[util.game_language].quiz.menu[self.order]
            elif self.type == "out_of_game":
                text = language_dictionary[util.game_language].quiz.menu[self.order]
            elif self.type == "exit":
                text = language_dictionary[util.game_language].quiz.menu[self.order]
            else:
                text = ""

            self.text = self.font.render(text, True, (255, 255, 255))
            self.lang = util.game_language
            self.name = text

        self.player_input()


class FastestFingersResult(pygame.sprite.Sprite):

    def __init__(self, type, text, order):
        super().__init__()

        x_pos = 1023
        y_pos = 482

        y_pos = y_pos + (order * 68)

        self.frame = pygame.image.load('./data/graphics/fastest_' + type + '.png').convert_alpha()
        self.font = pygame.font.SysFont('Sans', 33)
        self.type = type
        self.text_color = (255, 255, 255)

        self.name = text
        self.text = self.font.render(text, True, (255, 255, 255))
        self.image = self.frame
        self.image.blit(self.text, [110, 15])
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.lang = util.game_language
        self.order = order

    def get_is_active(self):
        if hasattr(self, 'is_active'):
            return self.is_active
        else:
            return True

    def set_is_active(self):
        self.is_active = True

    def unset_is_active(self):
        self.is_active = False

    def update(self):
        pass


def play_random_quizmaster_sound(level: int):
    util.pause_music()
    global random_sounds
    sound_file = random.choice(random_sounds)
    util.play_sound_object(sound_file)
    util.continue_music()


def get_dictionary_key_by_value(dictionary: {}, value: str) -> str:
    for choice, answerValue in dict.items(dictionary):
        if answerValue == value:
            return choice


def answer_out_of_game(level):
    util.pause_music()
    if util.game_language == util.Language.HUNGARIAN.name:
        music_off_sounds = ["music_off", "lower_music"]
        sound = random.choice(music_off_sounds)
        if level > 8:
            sound = "stop_at_finish"
        util.play_sound(sound, 0, dir="out_of_game", timer=True)
        util.stop_music()
        out_of_game_sounds = ["and_then_out_of_game", "acknowledge_it_out_of_game", "out_of_game",
                              "out_of_game_2", "out_of_game_say_letter"]
        sound = random.choice(out_of_game_sounds)
        util.play_sound(sound, 0, dir="out_of_game")


def play():
    global game_language
    global question_lines
    global correct_answer_key
    global game_active
    global base_threads
    global a_threads
    global b_threads
    global c_threads
    global d_threads
    global game_language, question_lines_easy, question_lines_medium, question_lines_hard
    game_language = util.game_language
    global question_topics
    question_topics = util.question_topics
    global question_difficulty
    question_difficulty = util.question_difficulty
    global help_types
    help_types = {"halving": True, "telephone": True, "audience": True}
    global help_group
    help_group = pygame.sprite.Group()
    global random_sounds
    random_sounds = util.init_random_sounds()

    topic = question_topics
    difficulty = question_difficulty
    if question_topics == util.Topics.ALL.name:
        topic = ""
    if question_difficulty == util.Difficulty.ALL.name:
        difficulty = ""

    exceptions = json.dumps({"easyQuestions": util.easy_question_exceptions,
                             "mediumQuestions": util.medium_question_exceptions,
                             "hardQuestions": util.hard_question_exceptions})
    global data
    data = requests.post(
        'https://yi4tfqk2xmyzsgt72ojur5bk6q0mjtnw.lambda-url.eu-north-1.on.aws?topic=' + topic.lower() + '&difficulty=' + difficulty.lower(),
        data=exceptions,
        headers={"Content-Type": "application/json"})

    if data.status_code == 200:

        if data.json()['exception']['resetEasyFilter']:
            util.easy_question_exceptions = []
        if data.json()['exception']['resetMediumFilter']:
            util.medium_question_exceptions = []
        if data.json()['exception']['resetHardFilter']:
            util.hard_question_exceptions = []

        question_lines = []
        data = data.json()['questions']

        for i in range(15):
            question_lines.append(
                [data[i][game_language[:2].lower()]['text'], data[i][game_language[:2].lower()]['answers'][0],
                 data[i][game_language[:2].lower()]['answers'][1],
                 data[i][game_language[:2].lower()]['answers'][2], data[i][game_language[:2].lower()]['answers'][3]])

        if len(question_lines) != 15:
            return

        game_active = True
        pygame.init()
        global screen
        # screen = pygame.display.set_mode((1024, 768))
        # pygame.FULLSCREEN
        if util.full_screen:
            screen = pygame.display.set_mode((1366, 768), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((1366, 768))

        pygame.display.set_caption(language_dictionary[util.game_language].title)
        millioniareIcon = pygame.image.load('./data/graphics/loim.png')
        pygame.display.set_icon(millioniareIcon)
        global clock
        clock = pygame.time.Clock()
        global test_font
        test_font = pygame.font.Font(pygame.font.get_default_font(), 50)

        global prizes_table
        prizes_table = pygame.sprite.GroupSingle()
        global in_game_menu_bg
        in_game_menu_bg = pygame.image.load('./data/graphics/in_game_menu_bg.jpg').convert_alpha()

        game_levels = 15
        level = 0
        answers = {"a": question_lines[level][1], "b": question_lines[level][2], "c": question_lines[level][3],
                   "d": question_lines[level][4]}
        answer_list = list(answers.values())
        random.shuffle(answer_list)
        shuffled_answers = dict(zip(answers, answer_list))
        global player, player_in_game
        player = "player"
        player_in_game = "player"
        # DEBUG COMMENT HERE

        start_game()
        if game_language == util.Language.HUNGARIAN.name:
            for name in os.listdir(util.get_data_path() + "/sound_files/" + str(game_language).lower() + "/players"):
                if player.lower() == name[:-4]:
                    player_in_game = player.lower()
            util.play_sound("dear", 0, dir="intro", timer=True)
            util.play_sound(player_in_game, 0, dir="players", timer=True)
            millionaire_sounds = ["millionaire", "millionaire_1", "millionaire_2"]
            sound = random.choice(millionaire_sounds)
            util.play_sound(sound, 0, dir="intro", timer=True)

        global game_level
        score = 0
        is_active = True
        end = False
        for i in range(game_levels):
            game_level = i

            if data[i]["difficulty"] == "easy":
                util.easy_question_exceptions.append(data[i]["id"])
            elif data[i]["difficulty"] == "medium":
                util.medium_question_exceptions.append(data[i]["id"])
            else:
                util.hard_question_exceptions.append(data[i]["id"])
            menu.update_settings_file()

            if i > 0 and is_active:
                score += 1
            if i == 14:
                end = True
            if i < game_levels:
                if is_active:
                    is_active = game_loop(i, question_lines)
                else:
                    break

        quit_quiz(score, player, question_topics, end)

    return


def start_game():
    global player
    player = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    return
                elif event.key == pygame.K_BACKSPACE:
                    player = player[:-1]
                elif event.key == pygame.K_SPACE:
                    player += " "
                elif event.key in [337, 252, 233, 225, 369, 246, 243, 237, 250]:
                    player += event.unicode
                else:
                    for i in range(pygame.K_a, pygame.K_z + 1):
                        if event.key == i:
                            player += pygame.key.name(event.key)
            else:
                pass

            display_ = pygame.sprite.GroupSingle()
            display_.add(TableElement('question',
                                      f'{language_dictionary[util.game_language].quiz.player_name_prompt} {player.title()}'))
            display_.draw(screen)

        pygame.display.update()
        clock.tick(60)


def game_loop(level: int, question_array: {}):
    global in_game_bg
    if level < 5:
        in_game_bg = pygame.image.load('./data/graphics/bg_easy.jpg').convert_alpha()
    elif level < 9:
        in_game_bg = pygame.image.load('./data/graphics/bg_medium.jpg').convert_alpha()
    else:
        in_game_bg = pygame.image.load('./data/graphics/bg_hard.jpg').convert_alpha()

    global out_of_game
    out_of_game = False
    last_input = ""
    global random_sounds
    global game_active
    global after_halving_event

    question = question_array[level][0]
    answers = {"a": question_array[level][1], "b": question_array[level][2], "c": question_array[level][3],
               "d": question_array[level][4]}
    answer_list = list(answers.values())
    random.shuffle(answer_list)
    shuffled_answers = dict(zip(answers, answer_list))

    # DEBUG COMMENT HERE

    if level in [0, 6, 8]:
        play_question_intro(level)
    if util.game_language == util.Language.HUNGARIAN.name and level < 14:
        play_question_prologue(level)
        play_music(level)
    global question_lines
    correct_answer_key = get_dictionary_key_by_value(shuffled_answers, question_lines[level][1])
    dbclock = pygame.time.Clock()
    DOUBLECLICKTIME = 500

    pygame.time.set_timer(pygame.USEREVENT, 1000)  # SELECT EVENT
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  # AFTER HALVING EVENT
    pygame.time.set_timer(pygame.USEREVENT + 2, 1000)  # MARK EVENT
    pygame.time.set_timer(pygame.USEREVENT + 3, 1000)  # PHONE EVENT
    pygame.time.set_timer(pygame.USEREVENT + 4, 1000)  # AUDIENCE EVENT
    pygame.time.set_timer(pygame.USEREVENT + 5, 1000)  # DIAL EVENT
    pygame.time.set_timer(pygame.USEREVENT + 6, 1000)  # PHONE INTRO EVENT
    pygame.time.set_timer(pygame.USEREVENT + 7, 1000)  # AUDIENCE INTRO EVENT
    pygame.time.set_timer(pygame.USEREVENT + 8, 1000)  # PRIZE EVENT
    pygame.time.set_timer(pygame.USEREVENT + 9, 1000)  # PRIZE TABLE EVENT
    pygame.time.set_timer(pygame.USEREVENT + 10, 15000)  # random sound event

    global counter
    counter = 3
    sprite_group = ['question', "a", "b", "c", "d"]
    global selected
    selected = ""
    global type
    type = "select"
    texts = [question, answer_list[0], answer_list[1], answer_list[2], answer_list[3]]
    global obstacle_group
    obstacle_group = pygame.sprite.Group()
    for index in range(len(sprite_group)):
        obstacle_group.add(TableElement(sprite_group[index], texts[index]))
    global help_group

    help_sprites = ['halving', "telephone", "audience"]
    for index in range(len(help_sprites)):
        help_group.add(Help(help_sprites[index]))
    halving_time = 6
    global after_halving_event
    after_halving_event = 0
    mark_seconds = 5
    global mark_event
    mark_event = 0

    global phone_selection_event
    phone_selection_event = 0
    global phone_select
    phone_select = False
    global phone_event
    phone_event = 0
    phone_seconds = 30
    global call_duration
    call_duration = 0
    global audience_event
    audience_event = 0
    audience_text = ""
    if util.game_language == util.Language.HUNGARIAN.name:
        audience_seconds = 7
    else:
        audience_seconds = 4
    audience_res = {}
    global dial_event
    global dial_seconds
    dial_event = 0
    dial_seconds = 2
    global phone_intro_event
    global intro_duration
    phone_intro_event = 0
    intro_duration = 0
    clock_added = False
    audience_table_added = False
    global audience_intro_event
    audience_intro_event = 0
    global audience_intro_duration
    audience_intro_duration = 0
    prize_group = pygame.sprite.GroupSingle()
    if level < 14:
        prize_seconds = 5
    else:
        prize_seconds = 45
    prize_event = 0
    menu_group = pygame.sprite.Group()
    menu_group.add(MenuOption("resume", 0, 300))
    menu_group.add(MenuOption("out_of_game", 1, 300))
    menu_group.add(MenuOption("settings", 2, 300))
    menu_group.add(MenuOption("exit", 3, 300))

    prizes_table.add(Prizes())

    settings_group = []

    for option in language_dictionary[util.game_language].menu.ingame_settings_menu_options:
        settings_group.append(option)

    settings_option_group = menu.sprite_group_init(settings_group,
                                                   "ingame_settings_menu_option", 300)
    lang_group = menu.sprite_group_init(util.available_languages, "ingame_language_option", 300)

    global exit_game
    exit_game = False
    global options
    options = False

    global settings_init
    settings_init = False

    out_of_game_started = False
    global prize_table_event
    prize_table_event = pygame.USEREVENT + 9
    global prize_table_seconds

    prize_table_seconds = 5

    random_sound_event = pygame.USEREVENT + 10

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_active = False
            elif event.type == pygame.USEREVENT and selected != "" and type == "select":
                if audience_event != 0:
                    audience_event = 0
                    for ob in help_group.sprites():
                        if ob.type == "audience_table":
                            help_group.remove(ob)
                counter -= 1
                if counter < 1:
                    play_select_sounds(level, selected, last_input, out_of_game)
                    type = "mark"
            elif event.type == mark_event:
                mark_seconds -= 1
            elif event.type == after_halving_event:
                halving_time -= 1
                if halving_time < 1:
                    after_halving_sounds = ["after_halving", "after_halving_2", "after_halving_3",
                                            "your_guess_stayed", "you_have_fifty_percent",
                                            "im_not_surprised"]
                    sound = random.choice(after_halving_sounds)
                    if util.game_language == util.Language.HUNGARIAN.name:
                        util.play_sound(sound, 0, dir="halving")
                    after_halving_event = 0
            elif event.type == phone_event:

                if len(help_group) == 3 and not clock_added:
                    help_group.add(Help("clock"))
                    clock_added = True
                if phone_seconds > 0 and phone_seconds > 30 - call_duration:
                    phone_seconds -= 1
                else:
                    util.stop_music()
                    util.play_sound("phone_call_return", 0, general=True)
                    phone_event = 0


            elif event.type == dial_event:
                if audience_event != 0:
                    audience_event = 0
                    for ob in help_group.sprites():
                        if ob.type == "audience_table":
                            help_group.remove(ob)
                if dial_seconds > 0:
                    dial_seconds -= 1
                if dial_seconds < 1 and phone_event == 0:
                    phone_intro_event = pygame.USEREVENT + 6
                    dial_event = 0

            elif event.type == phone_intro_event:
                if intro_duration > 0:
                    intro_duration -= 1

                else:
                    phone_event = pygame.USEREVENT + 3
                    phone_intro_event = 0
            elif event.type == audience_intro_event:
                if audience_intro_duration > 0:
                    audience_intro_duration -= 1
                if audience_intro_duration < 1:
                    audience_event = pygame.USEREVENT + 4
                    audience_intro_event = 0
            elif event.type == audience_event:
                if audience_seconds > 0:
                    audience_seconds -= 1

                    answer_keys = ["a", "b", "c", "d"]
                    audience_res = {}
                    first = random.randrange(40, 89)
                    audience_res[correct_answer_key] = first
                    answer_keys.remove(correct_answer_key)
                    if len(obstacle_group) == 5:

                        second = random.randrange(0, 100 - sum(audience_res.values()))
                        next = random.choice(answer_keys)
                        audience_res[next] = second
                        answer_keys.remove(next)

                        third = random.randrange(0, 100 - sum(audience_res.values()))
                        next = random.choice(answer_keys)
                        audience_res[next] = third
                        answer_keys.remove(next)
                        fourth = 100 - sum(audience_res.values())
                        next = answer_keys[0]
                        audience_res[next] = fourth
                        answer_keys.remove(next)
                    else:
                        for ob in obstacle_group.sprites():
                            if ob.type != correct_answer_key:
                                next = ob.type
                        fourth = 100 - sum(audience_res.values())
                        audience_res[next] = fourth

                    audience_res = dict(sorted(audience_res.items()))
                    answer_keys = ["a", "b", "c", "d"]
                    audience_text = ""
                    for key in answer_keys:
                        if key in audience_res:
                            audience_text += f"{audience_res[key]}% "
                        else:
                            audience_text += "   "

                elif audience_seconds == 0:
                    util.play_sound("audience_end", 0, general=True, timer=True)
                    if util.game_language == util.Language.HUNGARIAN.name:
                        audience_after_sounds = ["after_audience", "after_audience_2", "audience_false",
                                                 "you_disagree_audience", "weights_a_lot", "believe_audience",
                                                 "audience_random"]
                        after_sound = random.choice(audience_after_sounds)
                        util.play_sound(after_sound, 0, dir="audience", timer=True)
                    audience_seconds = -1
                else:
                    pass

            elif event.type == prize_event:
                if prize_seconds > 0:
                    prize_seconds -= 1

            elif event.type == prize_table_event:
                if prize_table_seconds > 0:
                    prize_table_seconds -= 1
                if prize_table_seconds == 0:
                    prize_table_event = 0

            else:
                if event.type == random_sound_event:
                    event_list = [phone_event, audience_event, after_halving_event, phone_selection_event, mark_event,
                                  prize_event, dial_event, phone_intro_event, audience_intro_event]
                    active_events = list(filter(lambda x: x > 0, event_list))
                    if len(active_events) == 0:

                        if util.get_sound_channel_availability and util.game_language == util.Language.HUNGARIAN.name and random_sounds:
                            play_random_quizmaster_sound(level)

            if game_active:
                if event.type == pygame.MOUSEBUTTONDOWN and selected == "":
                    if dbclock.tick() < DOUBLECLICKTIME:
                        for ob in obstacle_group.sprites():
                            if ob.type != 'question':
                                if ob.rect.collidepoint(event.pos) and pygame.mouse.get_pressed()[0]:
                                    selected = ob.type
                    else:
                        util.stop_sound()
                        last_input = ""
                        sound_dir = ""
                        if util.game_language == util.Language.HUNGARIAN.name:
                            sound_list_dict = get_sound_list(util.quizmaster_attitude)
                            bad_sounds = sound_list_dict['bad_sounds']
                            correct_sounds = sound_list_dict['correct_sounds']

                        if util.game_language == util.Language.HUNGARIAN.name:
                            sound_dir = "random"
                        for ob in obstacle_group.sprites():
                            if ob.type != 'question':
                                if ob.rect.collidepoint(event.pos) and pygame.mouse.get_pressed()[0]:
                                    clicked_option = ob.type
                                    if util.quizmaster_attitude != util.QuizMasterAttitude.NONE.name and util.game_language == util.Language.HUNGARIAN.name:
                                        if clicked_option == correct_answer_key:
                                            selected_sound = random.choice(correct_sounds)
                                        else:
                                            selected_sound = random.choice(bad_sounds)
                                        # if not out_of_game:
                                        #    util.pause_music()
                                        if util.game_language == util.Language.HUNGARIAN.name and util.quizmaster_attitude != util.QuizMasterAttitude.NONE.name:
                                            if selected_sound.find("mark") != -1 or selected_sound.find("final") != -1:
                                                sound_dir = "mark"
                                        util.play_sound(selected_sound, 0, dir=sound_dir)

            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_active = False
        if game_active:
            util.continue_music()
            global game_language
            if game_language != util.game_language:
                game_language = util.game_language
                question_lines = []
                for i in range(15):
                    question_lines.append(
                        [data[i][util.game_language[:2].lower()]['text'],
                         data[i][game_language[:2].lower()]['answers'][0],
                         data[i][game_language[:2].lower()]['answers'][1],
                         data[i][game_language[:2].lower()]['answers'][2],
                         data[i][game_language[:2].lower()]['answers'][3]])
                question = question_lines[level][0]
                answers = {"a": question_lines[level][1], "b": question_lines[level][2], "c": question_lines[level][3],
                           "d": question_lines[level][4]}
                answer_list = list(answers.values())
                random.shuffle(answer_list)
                shuffled_answers = dict(zip(answers, answer_list))
                texts = [question, answer_list[0], answer_list[1], answer_list[2], answer_list[3]]
                correct_answer_key = get_dictionary_key_by_value(shuffled_answers, question_lines[level][1])
                obstacle_group = pygame.sprite.Group()
                for index in range(len(sprite_group)):
                    obstacle_group.add(TableElement(sprite_group[index], texts[index]))
                obstacle_group.update(selected, correct_answer_key, type)
                menu_group.update()

            if out_of_game and not out_of_game_started:
                answer_out_of_game(level)
                out_of_game_started = True

            screen.blit(in_game_bg, (0, 0))
            if prize_table_event != 0:
                prizes_table.draw(screen)
                prizes_table.update()
                help_group.draw(screen)
                help_group.update(correct_answer_key)
            else:
                if phone_select:
                    help_group.add(Help("teacher"))
                    help_group.add(Help("chewbacca"))
                    help_group.add(Help("random"))
                    phone_select = False
                if audience_event and not audience_table_added:
                    help_group.add(Help("audience_table"))
                    audience_table_added = True

                if type == "mark":
                    if mark_seconds < 1:
                        if selected == correct_answer_key:
                            if level < 14:
                                if prize_seconds == 3 and len(prize_group) == 0:
                                    if not out_of_game:
                                        play_correct_sounds(level)
                                    prize_group.add(TableElement("prize", get_prize(level)))
                                if prize_event != 0:
                                    if prize_seconds == 0:
                                        if out_of_game:
                                            if game_language == util.Language.HUNGARIAN.name:
                                                util.play_sound("out_of_game_luck", 0, dir="out_of_game", timer=True)
                                            util.play_sound("claps", 0, general=True, timer=True)
                                            return False
                                        else:
                                            return True
                            else:
                                if prize_seconds == 33 and len(prize_group) == 0:
                                    if not out_of_game:
                                        play_correct_sounds(level)
                                    prize_group.add(TableElement("prize", get_prize(level)))
                                if prize_event != 0:
                                    if prize_seconds == 0:
                                        if out_of_game:
                                            if game_language == util.Language.HUNGARIAN.name:
                                                util.play_sound("out_of_game_luck", 0, dir="out_of_game", timer=True)
                                            util.play_sound("claps", 0, general=True, timer=True)
                                            return False

                                        else:
                                            return True
                        else:
                            if prize_seconds == 3 and len(prize_group) == 0:
                                if not out_of_game:
                                    play_incorrect_sounds(level)
                                prize_group.add(TableElement("prize", get_prize(level, correct_answer=False)))
                            if prize_event != 0:
                                if prize_seconds == 0:
                                    if out_of_game:
                                        if game_language == util.Language.HUNGARIAN.name:
                                            util.play_sound("good_to_stop", 0, dir="out_of_game", timer=True)
                                        util.clear_screen()
                                        time.sleep(2)
                                        if util.game_language == util.Language.HUNGARIAN.name:
                                            sorry_sounds = ["so_sorry", "terribly_sorry"]
                                            sound = random.choice(sorry_sounds)
                                            util.play_sound(sound, 0, dir="out_of_game", timer=True)
                                        time.sleep(1)
                                        util.play_sound("claps", 0, general=True, timer=True)
                                    return False

                        prize_event = pygame.USEREVENT + 8
                help_group.draw(screen)
                help_group.update(correct_answer_key)

                if prize_event != 0:
                    screen.fill((0, 0, 0))
                    screen.blit(in_game_bg, (0, 0))
                    prize_group.draw(screen)
                    prize_group.update(selected, correct_answer_key)
                if phone_event != 0:
                    screen.fill((0, 0, 0))

                    x_pos = 1121
                    y_pos = 180
                    font = pygame.font.SysFont('Sans', 41)
                    game_message = font.render(str(phone_seconds), True, (255, 255, 255))
                    game_message_rect = game_message.get_rect(center=(x_pos, y_pos))
                    clock_surf = pygame.image.load('./data/graphics/clock.png').convert_alpha()
                    clock_rect = clock_surf.get_rect(center=(x_pos, y_pos))
                    screen.blit(clock_surf, clock_rect)
                    screen.blit(game_message, game_message_rect)

                    r = 37
                    for i in range((30 - phone_seconds) * int(361 / 30), 361):
                        pygame.draw.circle(screen, (236, 155, 47),
                                           (int(r * cos(radians(i - 90)) + x_pos),
                                            int(r * sin(radians(i - 90)) + y_pos)), 3)

                if audience_event != 0:

                    x_pos = 1140
                    y_pos = 150
                    if audience_res != {}:
                        font = pygame.font.SysFont('Sans', 30)
                        game_message = font.render(audience_text, True, (255, 255, 255))
                        game_message_rect = game_message.get_rect(center=(x_pos, y_pos))
                        screen.blit(game_message, game_message_rect)

                        x_pos = 1055
                        y_pos = 420
                        width = 25
                        color = (92, 175, 255)
                        table_length = 240
                        answers = ["a", "b", "c", "d"]
                        for key in answers:
                            if key in audience_res and audience_res[key] != 0:
                                line = [(x_pos, y_pos), (x_pos, y_pos - table_length / 10 * (audience_res[key] / 10))]
                                pygame.draw.line(screen, color, line[0], line[1], width=width)
                            x_pos += 50
                obstacle_group.draw(screen)
                obstacle_group.update(selected, correct_answer_key, type)

        else:
            screen.fill((0, 0, 0))
            screen.blit(in_game_menu_bg, (0, 0))
            util.pause_music()
            if menu.options:
                if menu.lang_selection:
                    lang_group.draw(screen)
                    lang_group.update()
                else:
                    settings_option_group.draw(screen)
                    settings_option_group.update()
            else:
                menu_group.draw(screen)
                menu_group.update()

            if exit_game: return False

        pygame.display.update()
        clock.tick(60)


def show_game_structure():
    in_game_menu_bg = pygame.image.load('./data/graphics/in_game_menu_bg.jpg').convert_alpha()

    global clock
    clock = pygame.time.Clock()

    global screen
    # screen = pygame.display.set_mode((1024, 768))
    # pygame.FULLSCREEN
    if util.full_screen:
        screen = pygame.display.set_mode((1366, 768), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((1366, 768))

    global game_active
    dbclock = pygame.time.Clock()
    DOUBLECLICKTIME = 500

    pygame.time.set_timer(pygame.USEREVENT, 400)  #
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  #
    pygame.time.set_timer(pygame.USEREVENT + 2, 1000)  #

    counter = 3

    menu_group = pygame.sprite.Group()
    menu_group.add(MenuOption("resume", 0, 300))
    menu_group.add(MenuOption("exit", 1, 300))
    game_active = True

    global exit_game
    exit_game = True

    prizes_event = pygame.USEREVENT
    if util.game_language == util.Language.HUNGARIAN.name:
        prize_seconds = util.get_sound_length("prizes_description", dir="intro")
    else:
        prize_seconds = util.get_sound_length("start")

    prize = 0
    current_prize = pygame.image.load('./data/graphics/question_0_prize.png').convert_alpha()
    x_pos = 920
    y_pos = 0

    sky_surface = pygame.image.load('./data/graphics/bg_medium.jpg').convert_alpha()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_active = False

            if event.type == prizes_event:

                if util.game_language == util.Language.HUNGARIAN.name:

                    if prize_seconds == util.get_sound_length("prizes_description", dir="intro"):
                        util.play_sound("prizes_description", 0, dir="intro")
                else:
                    if prize_seconds == util.get_sound_length("start"):
                        util.play_sound("start", 0)

                prize_seconds -= 1
                if prize < 16:
                    current_prize = pygame.image.load(
                        './data/graphics/question_' + str(prize) + '_prize.png').convert_alpha()
                elif prize == 17:
                    current_prize = pygame.image.load(
                        './data/graphics/question_' + str(5) + '_prize.png').convert_alpha()
                elif prize == 19:
                    current_prize = pygame.image.load(
                        './data/graphics/question_' + str(10) + '_prize.png').convert_alpha()
                elif prize == 21:
                    if util.game_language == util.Language.HUNGARIAN.name:
                        util.play_sound("help_modules", 0, dir="intro")
                    current_prize = pygame.image.load(
                        './data/graphics/halving_desc.png').convert_alpha()
                    time.sleep(1)

                elif prize == 23:
                    current_prize = pygame.image.load(
                        './data/graphics/telephone_desc.png').convert_alpha()
                    time.sleep(1)

                elif prize == 26:
                    current_prize = pygame.image.load(
                        './data/graphics/audience_desc.png').convert_alpha()
                    time.sleep(1)

                elif prize == 30:
                    current_prize = pygame.image.load('./data/graphics/question_0_prize.png').convert_alpha()
                    if util.game_language == util.Language.HUNGARIAN.name:
                        util.play_sound("prologue_end", 0, dir="intro", timer=True)
                elif prize == 33:
                    return


                else:
                    pass
                    # current_prize = pygame.image.load('./data/graphics/question_0_prize.png').convert_alpha()
                prize += 1

            if game_active:
                pass

            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_active = False
        if game_active:

            screen.blit(sky_surface, (0, 0))
            screen.blit(current_prize, (x_pos, y_pos))


        else:
            screen.fill((0, 0, 0))
            screen.blit(in_game_menu_bg, (0, 0))
            util.pause_music()
            menu_group.draw(screen)
            menu_group.update()

            if exit_game: return False

        pygame.display.update()
        clock.tick(60)


def phone_dial():
    if util.game_language == util.Language.HUNGARIAN.name:
        dial_sound = "colleagues_are_dialing"
        util.play_sound(dial_sound, 0, dir="phone", timer=True)


def play_select_sounds(level: int, selected="", last_input="", out_of_game=False):
    global mark_seconds
    global counter
    util.stop_sound()
    if not out_of_game:
        util.pause_music()
    if util.game_language == util.Language.HUNGARIAN.name:
        counter = play_marked_sound(selected, level, last_one=last_input)

    global mark_event
    mark_event = pygame.USEREVENT + 2


def play_incorrect_sounds(level: int):
    util.play_sound("bad_answer", 0, general=True)
    time.sleep(2)
    if game_language == util.Language.HUNGARIAN.name:
        util.play_sound("so_sorry", 0, dir="out_of_game", timer=True)
        time.sleep(1)
        util.play_sound("claps", 0, general=True, timer=True)


def play_correct_sounds(level: int):
    if level < 14:
        if level == 5:
            util.play_sound("sixth_correct_answer", 0, general=True)
        else:
            util.play_sound("correct_answer", 0, general=True)
        if util.game_language == util.Language.HUNGARIAN.name:
            play_prize_sound(level)
        if level == 4:
            util.play_sound("won_hundred_bucks", 0, general=True)
        elif level == 9:
            time.sleep(3)
            if util.game_language == util.Language.HUNGARIAN.name:
                util.play_sound("now_comes_hard_part", 0, dir="random")
        else:
            util.play_sound("claps", 0, general=True)
    else:
        if util.game_language == util.Language.HUNGARIAN.name:
            util.play_sound("after_marking", 0, dir="lets_see")
            time.sleep(4)
            util.play_sound("great_logic", 0, dir="correct")
        time.sleep(1)
        util.play_sound("winning_theme", 0, general=True)


def play_prize_sound(level: int):
    if level in [4, 7, 9, 11, 12]:
        util.play_sound("level_" + str(level), 0, dir="prize")


def play_question_prologue(level: int):
    sounds_list = [
        ["here_is_the_first_question_one", "here_is_the_first_question_two", "here_is_the_first_question_three"],
        ["here_is_the_second_question_one"],
        ["here_is_the_third_question_one", "here_is_the_third_question_two", "here_is_the_third_question_three"],
        ["here_is_the_fourth_question_one", "here_is_the_fourth_question_two", "here_is_the_fourth_question_three"],
        ["here_is_the_fifth_question_one", "here_is_the_fifth_question_two", "here_is_the_fifth_question_three"],
        ["here_is_the_sixth_question_one", "here_is_the_sixth_question_two", "here_is_the_sixth_question_three",
         "here_is_the_sixth_question_four", "here_is_the_sixth_question_five", "here_is_the_sixth_question_six"],
        ["here_is_the_seventh_question_one", "here_is_the_seventh_question_two", "here_is_the_seventh_question_three",
         "here_is_the_seventh_question_four"],
        ["here_is_the_eighths_question_one", "here_is_the_eighths_question_two", "here_is_the_eighths_question_three",
         "here_is_the_eighths_question_four", "here_is_the_eighths_question_five", "here_is_the_eighths_question_six"],
        ["here_is_the_nineth_question_one", "here_is_the_nineth_question_two", "here_is_the_nineth_question_three"],
        ["here_is_the_tenth_question_one", "here_is_the_tenth_question_two", "here_is_the_tenth_question_three"],
        ["here_is_the_eleventh_question_one", "here_is_the_eleventh_question_two",
         "here_is_the_eleventh_question_three"],
        ["here_is_the_twelfth_question_one", "here_is_the_twelfth_question_two", "here_is_the_twelfth_question_three",
         "here_is_the_twelfth_question_four"],
        ["here_is_the_thirteenth_question_one", "here_is_the_thirteenth_question_two"],
        ["here_is_the_fourteenth_question_one"]
    ]

    if level == 7:
        if list(help_types.values()).count(True) == len(
                help_types) - 2 and help_types["telephone"]:
            sounds_list[7].append("here_is_the_eighths_question_with_phone")
    if level == 8:
        if list(help_types.values()).count(True) == len(
                help_types) - 1:
            sounds_list[8].append("here_is_the_nineth_question_two_with_two_helps")
        if list(help_types.values()).count(True) == len(
                help_types):
            sounds_list[8].append("here_is_the_nineth_question_with_three_helps")

    sound_file = random.choice(sounds_list[level])
    util.play_sound(sound_file, 0, dir="question_prologue")

    chance = random.randrange(0, 10)
    if chance > 7:
        if level == 3:
            util.play_sound("at_4", 0, dir="question_prologue")
        elif level == 4:
            util.play_sound("at_5", 0, dir="question_prologue")
        elif level == 5:
            util.play_sound("at_6", 0, dir="question_prologue")
        elif level == 6:
            util.play_sound("at_7", 0, dir="question_prologue")
        elif level == 7:
            util.play_sound("at_8", 0, dir="question_prologue")
        elif level == 8:
            util.play_sound("at_9", 0, dir="question_prologue")
        elif level == 9:
            util.play_sound("at_10", 0, dir="question_prologue")
        elif level == 10:
            util.play_sound("at_11", 0, dir="question_prologue")
        elif level == 11:
            util.play_sound("at_12", 0, dir="question_prologue")
        elif level == 12:
            util.play_sound("at_13", 0, dir="question_prologue")
        else:
            pass


def play_question_intro(level: int):
    sound_file = ""
    if level == 0:
        sound_file = "before_question"
    if level == 6:
        sound_file = "before_seventh_question"
    elif level == 8:
        sound_file = "before_nineth_question"

    util.play_sound(sound_file, 0, general=True, timer=True)


def play_help_sounds(help_types: {}):
    sound_file = ""
    help_assets = ["you_still_have_help", "you_have_helps_if_unsure", "you_still_have_helps_dont_worry"]

    if list(help_types.values()).count(True) == len(
            help_types):
        all_help_sounds = ["you_still_have_three_helps", "still_have_all_helps", "yet_having_three_helps",
                           "still_have_three_helps_2", "still_have_3_lifelines"]
        sound_file = random.choice(all_help_sounds)
    elif list(help_types.values()).count(True) == len(
            help_types) - 1:
        two_help_sounds = ["and_still_have_two_helps", "still_have_two_helps_i_take_it"]
        if help_types["telephone"] and help_types["audience"]:
            two_help_sounds.append("you_still_have_two_helps_phone_audience")
        sound_file = random.choice(two_help_sounds)
    elif list(help_types.values()).count(True) == len(
            help_types) - 2:
        help_assets.append("you_waste_a_lot")
        if help_types["telephone"]:
            phone_left_sounds = ["you_have_a_phone_help_left", "you_have_a_phone_but_make_you_mad"]
            for sound in phone_left_sounds:
                help_assets.append(sound)
        else:
            one_help_sounds = ["oh_god_got_one_help", "you_still_have_one_help", "whatever_you_say_theres_1_help"]
            for sound in one_help_sounds:
                help_assets.append(sound)
        sound_file = random.choice(help_assets)
    else:
        no_help_sounds = ["no_more_helps", "without_help", "sorry_no_more_helps", "since_lost_helps",
                          "fighting_without_helps", "but_no_more_helps"]
        sound_file = random.choice(no_help_sounds)

    util.play_sound(sound_file, 0, dir="help", timer=True)


def fastest_fingers_first():
    global clock
    clock = pygame.time.Clock()

    global screen
    # screen = pygame.display.set_mode((1024, 768))
    # pygame.FULLSCREEN
    if util.full_screen:
        screen = pygame.display.set_mode((1366, 768), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((1366, 768))

    global player
    player = "player"
    # start_game()
    global game_language, question_lines_easy, question_lines_medium, question_lines_hard
    game_language = util.game_language

    data = requests.get(
        'https://ygzk643gpxbnmvsblbtkg764uu0arpld.lambda-url.eu-north-1.on.aws/')

    if data is None:
        return

    question = {
        "text": data.json()[0][game_language[:2].lower()]['text'],
        "answers": [data.json()[0][game_language[:2].lower()]['answers'][0],
                    data.json()[0][game_language[:2].lower()]['answers'][1],
                    data.json()[0][game_language[:2].lower()]['answers'][2],
                    data.json()[0][game_language[:2].lower()]['answers'][3]],
        "correct_order": data.json()[0][game_language[:2].lower()]['correct_order']
    }

    if game_language == util.Language.ENGLISH:
        util.play_sound("start", 0)
    answers = {"a": question['answers'][0], "b": question['answers'][1], "c": question['answers'][2],
               "d": question['answers'][3]}
    answer_list = list(answers.values())
    # random.shuffle(answer_list)
    # shuffled_answers = dict(zip(answers, answer_list))
    shuffled_answers = answers
    if game_language == util.Language.HUNGARIAN.name:
        util.play_sound("lets_look_at_the_fastest_fingers_question", 0, dir="fastest_fingers")
        time.sleep(2)
    util.play_sound("fastest_fingers_first", 0, general=True)

    start = time.time()

    correct_answer_keys = question["correct_order"]

    global game_active

    dbclock = pygame.time.Clock()
    DOUBLECLICKTIME = 500

    pygame.time.set_timer(pygame.USEREVENT, 1000)  # SELECT EVENT
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  # MARK EVENT
    pygame.time.set_timer(pygame.USEREVENT + 2, 1000)  # RESULT EVENT
    pygame.time.set_timer(pygame.USEREVENT + 3, 1000)  # PRIZE EVENT

    counter = 3
    sprite_group = ['question', "a", "b", "c", "d"]
    global selected
    selected = ""
    global type
    type = "fastest_fingers_select"
    texts = [question['text'], answer_list[0], answer_list[1], answer_list[2], answer_list[3]]
    obstacle_group = pygame.sprite.Group()
    for index in range(len(sprite_group)):
        obstacle_group.add(TableElement(sprite_group[index], texts[index]))
    global help_group

    global mark_seconds
    mark_seconds = 5
    global mark_event
    mark_event = 0

    prize_group = pygame.sprite.GroupSingle()

    prize_seconds = 5

    prize_event = 0
    menu_group = pygame.sprite.Group()

    menu_group.add(MenuOption("resume", 0, 300))
    menu_group.add(MenuOption("exit", 2, 300))

    global exit_game
    exit_game = False

    game_active = True

    sky_surface = pygame.image.load('./data/graphics/bg_medium.jpg').convert_alpha()
    fastest_result_bg = pygame.image.load('./data/graphics/fastest_result_bg.png').convert_alpha()

    global fastest_fingers_result
    global fastest_fingers_mark_event

    fastest_fingers_mark_event = 0
    fastest_fingers_result = ""

    in_game_menu_bg = pygame.image.load('./data/graphics/in_game_menu_bg.jpg').convert_alpha()

    result_group = pygame.sprite.Group()
    for i in range(4):
        result_group.add(FastestFingersResult("abcd"[int(question['correct_order'][i])],
                                              question['answers'][int(question['correct_order'][i])], i))
    result_event = 0
    result_seconds = 5

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_active = False
            if event.type == pygame.USEREVENT and selected != "" and type == "select":
                counter -= 1
                if counter < 1:
                    play_select_sounds(level, selected, last_input, out_of_game)
                    type = "mark"
            if event.type == fastest_fingers_mark_event:
                mark_seconds -= 1

            if event.type == prize_event:
                if prize_seconds > 0:
                    prize_seconds -= 1

            if time.time() - start > 28:
                type = "fastest_fingers_mark"
                fastest_fingers_mark_event = pygame.USEREVENT + 1
                mark_seconds = 0

            if game_active:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if dbclock.tick() < DOUBLECLICKTIME:
                        for ob in obstacle_group.sprites():
                            if ob.type != 'question':
                                if ob.rect.collidepoint(event.pos) and pygame.mouse.get_pressed()[0]:
                                    selected = ob.type

            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_active = False
        if game_active:
            util.continue_music()

            screen.blit(sky_surface, (0, 0))

            if type == "fastest_fingers_mark":
                if mark_seconds < 1:
                    end = time.time()

                    for ob in obstacle_group.sprites():
                        obstacle_group.remove(ob)

                    obstacle_group.add(
                        TableElement('fastest_fingers_result', str(player).capitalize() + " : " + str(end - start)[:5]))
                    for ob in obstacle_group.sprites():
                        ob.image = pygame.image.load('./data/graphics/fastest_fingers_win.png').convert_alpha()
                        font = pygame.font.SysFont('Sans', 33)
                        text = font.render(str(player).capitalize() + " : " + str(end - start)[:5], True,
                                           (255, 255, 255))
                        text_rect_1 = text.get_rect(center=(1366 / 2, 48))

                        ob.image.blit(text, text_rect_1)

                    util.stop_sound()

                    if game_language == util.Language.HUNGARIAN.name:
                        if os.path.isfile(
                                "./data/sound_files/hungarian/fastest_fingers" + correct_answer_keys + ".wav"):
                            util.play_sound(correct_answer_keys, 0)
                        time.sleep(1)
                        util.play_sound("lets_see_who_is_correct", 0, dir="fastest_fingers")

                    # time.sleep(2)
                    result_event = pygame.USEREVENT + 2
                    screen.blit(fastest_result_bg, (0, 0))
                    result_group.draw(screen)
                    result_group.update()

                    font = pygame.font.SysFont('Sans', 25)

                    if len(question['text']) > 42:
                        text_1 = font.render(question['text'][:42], True, (255, 255, 255))
                        text_rect_1 = text_1.get_rect(center=(1000, 48))
                        screen.blit(text_1, text_rect_1)

                        text_2 = font.render(question['text'][42:], True, (255, 255, 255))
                        text_rect_2 = text_2.get_rect(center=(1000, 68))
                        screen.blit(text_2, text_rect_2)
                    else:
                        text = font.render(question['text'], True, (255, 255, 255))
                        text_rect_1 = text.get_rect(center=(1000, 48))
                        screen.blit(text, text_rect_1)
                    pygame.display.update()
                    time.sleep(result_seconds)

                    answer_dict = {"0": "a", "1": "b", "2": "c", "3": "d"}

                    correct_answer_letters = ""
                    for letter in correct_answer_keys:
                        correct_answer_letters += answer_dict[letter]

                    if correct_answer_letters == fastest_fingers_result:
                        util.play_sound("fastest_fingers_correct", 0, general=True)
                        time.sleep(2)
                        player_in_game = "player"
                        if game_language == util.Language.HUNGARIAN.name:
                            for name in os.listdir(
                                    util.get_data_path() + "/sound_files/" + str(game_language).lower() + "/players"):
                                if player.lower() == name[:-4]:
                                    player_in_game = player.lower()
                            util.play_sound(player_in_game, 0, dir="players", timer=True)

                        obstacle_group.draw(screen)
                        obstacle_group.update(selected, correct_answer_keys, type)
                        pygame.display.update()

                        util.play_sound("fastest_fingers_win", 0, general=True)
                        time.sleep(15)


                    else:
                        util.play_sound("fastest_fingers_bad", 0, general=True)
                        time.sleep(2)

                    quit_fastest_fingers()
                    return

                    # prize_event = pygame.USEREVENT + 8
            obstacle_group.draw(screen)
            obstacle_group.update(selected, correct_answer_keys, type)
            if prize_event != 0:
                screen.fill((0, 0, 0))
                screen.blit(sky_surface, (0, 0))
                prize_group.draw(screen)
                prize_group.update(selected, correct_answer_keys)


        else:
            screen.fill((0, 0, 0))
            screen.blit(in_game_menu_bg, (0, 0))
            util.pause_music()
            menu_group.draw(screen)
            menu_group.update()

            if exit_game: return False

        pygame.display.update()
        clock.tick(60)


def get_prize(round_number: int, correct_answer=True) -> str:
    global out_of_game

    prizes = language_dictionary[util.game_language].quiz.prizes

    if out_of_game:
        if round_number > 0:
            return prizes[round_number - 1]
        else:
            if util.game_language == util.Language.HUNGARIAN.name:
                return "0 Ft"
            elif util.game_language == util.Language.DEUTSCH.name:
                return "€0"
            else:
                return "£0"
    else:
        if not correct_answer:
            if round_number > 9:
                return prizes[9]
            elif round_number > 4:
                return prizes[4]
            else:
                if util.game_language == util.Language.HUNGARIAN.name:
                    return "0 Ft"
                elif util.game_language == util.Language.DEUTSCH.name:
                    return "€0"
                else:
                    return "£0"
        else:
            return prizes[round_number]


def halving_before_sounds():
    if util.game_language == util.Language.HUNGARIAN.name:
        before_halving_sounds = ["before_halving", "before_halving_2", "before_halving_3", "before_halving_4",
                                 "before_halving_5", "before_halving_6", "halv", "lets_even_half", "lets_halv",
                                 "lets_see_which_two", "lets_take_two",
                                 "lets_take_two_1", "lets_take_two_2", "lets_take_two_3", "two_of_four"]
        sound = random.choice(before_halving_sounds)
        util.play_sound(sound, 0, dir="halving", timer=True)
    time.sleep(2)
    util.play_sound("halving", 0, general=True)


def write_content_to_file(filename: str, content: {}):
    if os.path.isfile(filename):
        with open(filename, 'r+') as file:
            file_data = json.load(file)
            file_data.append(content)
            file.seek(0)
            json.dump(file_data, file)

    else:
        with open(filename, "w", encoding="UTF-8") as outfile:
            json.dump([content], outfile)


def play_music(round: int):
    if round < 5:
        util.play_background_music(str(5), 0)
    else:
        util.play_background_music(str(round), 0)


def play_marked_sound(choise: str, level: int, last_one="") -> int:
    sounds = []
    seconds = 0

    for answer in ["a", "b", "c", "d"]:
        if choise == answer:
            if choise == last_one and level > 0:
                sounds.append("mark_" + choise + "_again")
            else:
                sounds.append("mark_" + choise)
                sounds.append("mark_" + choise + "_1")
                sounds.append("mark_" + choise + "_2")
                if choise == "b":
                    sounds.append("poke_b")
                if choise in ["b", "d"]:
                    sounds.append("mark_" + choise + "_3")
                    sounds.append("mark_" + choise + "_4")

    sound = random.choice(sounds)
    util.play_sound(sound, 0, dir="mark", timer=True)
    seconds += util.get_sound_length(sound, dir="mark")

    sounds = []
    if level == 7:
        sounds = ["lets_see_500", "lets_see_500_1"]
    elif level == 8:
        sounds = ["lets_see_800", "lets_see_800_2"]
    elif level == 10:
        sounds = ["lets_see_3_million", "lets_see_3_million_2", "lets_see_3_million_3"]
    elif level == 13:
        sounds = ["lets_see_10_million"]
    else:
        sounds = ["lets_see"]
        for i in range(24):
            sounds.append("lets_see_" + str(i + 1))

    sound = random.choice(sounds)
    util.play_sound(sound, 0, dir="lets_see", timer=True)
    seconds += util.get_sound_length(sound, dir="lets_see")

    return seconds


def get_sound_list(attitude: str) -> {}:
    correct_sounds = ["you_must_mark", "you_came_for_money", "dont_sigh_yet", "hurry_up", "dont_let_me_speak",
                      "dont_listen_to_me", "whatever_you_say_wow", "that_was_fast", "what_you_say_will_be",
                      "watch_out_more_im_not_always_evil", "you_may_feel_im_hurrying", "final_or"]
    bad_sounds = ["you_mark_anyways", "i_wont_help_more", "calm", "look_at_my_eyes", "dont_want_to_say_dummy", "nooo",
                  "dont_be_impatient", "so_you_gonna_poke", "but_i_helped_you"]
    other_sounds = ['be_careful_is_it_final', "in_this_show_i_have_to_ask_is_it_final", "i_must_ask_is_it_final",
                    "final_or_final",
                    "take_that_as_final", "last_one_final", "take_the_risk", "i_dont_help_more_if_you_wish_we_mark",
                    "pay_attention_to_the_quizmaster", "so_what_to_do",
                    "you_see_clueless"]

    if attitude == util.QuizMasterAttitude.FRIENDLY.name:
        for i in range(2):
            correct_sounds.append(other_sounds[i])
            bad_sounds.append(other_sounds[i])
        return {"correct_sounds": correct_sounds, "bad_sounds": bad_sounds}
    elif attitude == util.QuizMasterAttitude.NEUTRAL.name:
        for sound in other_sounds:
            correct_sounds.append(sound)
            bad_sounds.append(sound)
        return {"correct_sounds": correct_sounds, "bad_sounds": bad_sounds}
    elif attitude == util.QuizMasterAttitude.HOSTILE.name:
        return {"correct_sounds": other_sounds, "bad_sounds": other_sounds}
    else:
        return {"correct_sounds": [], "bad_sounds": []}


def quit_quiz(score: int, name: str, topic, end=False):
    if not end:
        util.play_sound("time_end_horn", 0, general=True, timer=True)
        util.stop_music()
        if game_language == util.Language.HUNGARIAN.name:
            exit_sounds = ["exit_epilogue", "delay", "what_a_game_it_was", "how_ugly_sound_it_has"]
            if score < 5:
                exit_sounds.append("this_not_ended_well")
            sound = random.choice(exit_sounds)
            util.play_sound(sound, 0, dir="out_of_game")
    else:
        util.play_sound("what_a_game_it_was", 0, dir="out_of_game")
        util.stop_music()

    if score > 0:
        write_content_to_file("scores.json",
                              {"user": name, "topic": topic, "score": score, "time": time.ctime(time.time())})
    util.stop_sound()


def quit_fastest_fingers():
    util.stop_sound()
