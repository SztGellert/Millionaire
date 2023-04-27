import os
import random
import json
import time
from sty import Style, RgbFg, fg, bg, rs
import millionaire.menu.menu as menu
import millionaire.util.util as util
import millionaire.menu.helpers as helpers
import threading
import pygame

operating_system = os.name
fg.purple = Style(RgbFg(148, 0, 211))
fg.orange = Style(RgbFg(255, 150, 50))
fg.green = Style(RgbFg(0, 255, 0))
bg.orange = bg(255, 150, 50)
languages = util.available_languages
language_dictionary = util.language_dictionary
table_length = 113
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
            self.pre_marked_option = pygame.image.load( './data/graphics/option_a_pre_marked.png').convert_alpha()

            x_pos = 342
            y_pos = 643

        elif type == "b":

            self.frame = pygame.image.load('./data/graphics/option_b.png').convert_alpha()
            self.selected_option = pygame.image.load('./data/graphics/option_b_marked.png').convert_alpha()
            self.pre_marked_option = pygame.image.load( './data/graphics/option_b_pre_marked.png').convert_alpha()

            x_pos = 1021
            y_pos = 643

        elif type == "c":
            self.text_x = 165
            self.text_y = self.text_y - 5

            self.frame = pygame.image.load('./data/graphics/option_c.png').convert_alpha()
            self.selected_option = pygame.image.load('./data/graphics/option_c_marked.png').convert_alpha()
            self.pre_marked_option = pygame.image.load( './data/graphics/option_c_pre_marked.png').convert_alpha()

            x_pos = 342
            y_pos = 719

        elif type == "d":
            self.text_x = 115
            self.text_y = self.text_y - 5

            self.frame = pygame.image.load('./data/graphics/option_d.png').convert_alpha()
            self.selected_option = pygame.image.load('./data/graphics/option_d_marked.png').convert_alpha()
            self.pre_marked_option = pygame.image.load( './data/graphics/option_d_pre_marked.png').convert_alpha()

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
        global  type

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
            self.image  = pygame.image.load('./data/graphics/question_' + str(game_level) +'_prize.png').convert_alpha()
        else:
            self.image = pygame.image.load('./data/graphics/question_' + str(game_level+1) +'_prize.png').convert_alpha()




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
            x_pos = 1130
            y_pos = 160
        elif type == "audience_table":
            self.frame = pygame.image.load('./data/graphics/audience_table.png').convert_alpha()
            x_pos = 1130
            y_pos = 235
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
                global phone_event
                global dial_event
                global intro_duration
                if self.is_dialed == False:
                    dial_event = pygame.USEREVENT + 5
                    self.is_dialed = True
                elif dial_event != 0:
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
                    if phone_event != 0 and self.is_dialed == True:
                        # if intro_duration < 1:
                        for ob in help_group.sprites():
                            if ob.type in ["teacher", "chewbacca", "random"]:
                                help_group.remove(ob)

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
        if util.game_language == util.Language.HUNGARIAN.name:
            dial_sound = "colleagues_are_dialing"
            util.play_sound(dial_sound, 0, dir="phone", timer=True)

    def phone_intro(self) -> int:
        target = self.type
        if target == "teacher":
            util.play_sound("teacher_intro", 0, dir="phone")
            return util.get_sound_length("teacher_intro", dir="phone")
        if target == "chewbacca":
            util.play_sound("chewbacca_intro", 0, dir="phone")
            return util.get_sound_length("chewbacca_intro", dir="phone")
        if target == "random":
            util.play_sound("weekly_seven_intro", 0, dir="phone")
            return util.get_sound_length("weekly_seven_intro", dir="phone")

    def phone(self):
        global call_duration
        if self.type == "teacher":
            util.play_sound("teacher", 0, dir="phone", timer=True)
            call_duration = util.get_sound_length("teacher", dir="phone")
        if self.type == "chewbacca":
            util.play_sound("chewbacca", 0, dir="phone")
            call_duration = util.get_sound_length("chewbacca", dir="phone")
            util.play_background_sound("phone_call", 0, general=True)
        if self.type == "random":
            util.play_sound("weekly_seven", 0, dir="phone")
            call_duration = util.get_sound_length("weekly_seven", dir="phone")

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
        elif type == "question_difficulty_option":
            text = language_dictionary[util.game_language].menu.question_difficulty_levels[order]
        elif type == "quizmaster_attitude_option":
            text = language_dictionary[util.game_language].menu.quizmaster_attitudes[order]
        elif type == "language_option":
            text = [language_dictionary[util.game_language].en, language_dictionary[util.game_language].hu][order]
        else:
            print(type)
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


def init_threads(level: int):
    global base_threads
    global a_threads
    global b_threads
    global c_threads
    global d_threads
    global threads

    if level > 0:
        thread_random(level, working=False)
    threads = []

    for i in range(5):
        options = []
        for j in range(4):
            options.append(threading.Timer(15.0 * (j + 1), play_random_quizmaster_sound, args=(level,)))
        threads.append(options)

    base_threads = threads[0]
    a_threads = threads[1]
    b_threads = threads[2]
    c_threads = threads[3]
    d_threads = threads[4]


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
    question_lines = []
    question_lines_easy = []
    question_lines_medium = []
    question_lines_hard = []
    if question_topics == util.Topics.ALL.name:
        for topic in util.Topics:
            if topic.name != util.Topics.ALL.name and question_difficulty != util.Difficulty.ALL.name:
                for level in util.Difficulty:
                    if question_difficulty == level.name:
                        for line in util.open_file(str(level.name).lower(), "r", ";",
                                                   "/text_files/topics/" + str(game_language).lower() + "/" + str(
                                                       topic.name).lower() + "/" + str(level.name).lower() + "/"):
                            question_lines.append(line)
            else:
                if topic.name != util.Topics.ALL.name:
                    for line in util.open_file(str(util.Difficulty.EASY.name).lower(), "r", ";",
                                               "/text_files/topics/" + str(game_language).lower() + "/" + str(
                                                   topic.name).lower() + "/" + str(
                                                   util.Difficulty.EASY.name).lower() + "/"):
                        question_lines_easy.append(line)
                    for line in util.open_file(str(util.Difficulty.MEDIUM.name).lower(), "r", ";",
                                               "/text_files/topics/" + str(game_language).lower() + "/" + str(
                                                   topic.name).lower() + "/" + str(
                                                   util.Difficulty.MEDIUM.name).lower() + "/"):
                        question_lines_medium.append(line)
                    for line in util.open_file(str(util.Difficulty.HARD.name).lower(), "r", ";",
                                               "/text_files/topics/" + str(game_language).lower() + "/" + str(
                                                   topic.name).lower() + "/" + str(
                                                   util.Difficulty.HARD.name).lower() + "/"):
                        question_lines_hard.append(line)
    else:
        for level in util.Difficulty:
            if question_difficulty == level.name and level.name != util.Difficulty.ALL.name:
                for line in util.open_file(str(level.name).lower(), "r", ";",
                                           "/text_files/topics/" + str(game_language).lower() + "/" + str(
                                               question_topics).lower() + "/" + str(level.name).lower() + "/"):
                    question_lines.append(line)
            else:
                if level.name != util.Difficulty.ALL.name:
                    for line in util.open_file(str(util.Difficulty(level).name).lower(), "r", ";",
                                               "/text_files/topics/" + str(game_language).lower() + "/" + str(
                                                   question_topics).lower() + "/" + str(level.name).lower() + "/"):
                        if level.name == util.Difficulty.EASY.name:
                            question_lines_easy.append(line)
                        if level.name == util.Difficulty.MEDIUM.name:
                            question_lines_medium.append(line)
                        if level.name == util.Difficulty.HARD.name:
                            question_lines_hard.append(line)
    random.shuffle(question_lines)
    random.shuffle(question_lines_easy)
    random.shuffle(question_lines_medium)
    random.shuffle(question_lines_hard)
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
    global sky_surface
    sky_surface = pygame.image.load('./data/graphics/bg.jpg').convert_alpha()
    global obstacle_group
    obstacle_group = pygame.sprite.Group()
    global prizes_table
    prizes_table = pygame.sprite.GroupSingle()
    global in_game_menu_bg
    in_game_menu_bg = pygame.image.load('./data/graphics/in_game_menu_bg.jpg').convert_alpha()

    game_levels = 15
    level = 0
    init_threads(level)
    if question_difficulty == util.Difficulty.ALL.name:
        if level < 5:
            question_lines = question_lines_easy
        elif level < 10:
            question_lines = question_lines_medium
        else:
            question_lines = question_lines_hard
    answers = {"a": question_lines[level][1], "b": question_lines[level][2], "c": question_lines[level][3],
               "d": question_lines[level][4]}
    answer_list = list(answers.values())
    random.shuffle(answer_list)
    shuffled_answers = dict(zip(answers, answer_list))
    obstacle_group = pygame.sprite.Group()
    global player, player_in_game
    player = "player"
    player_in_game = "player"
    # DEBUG COMMENT HERE
    '''
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
     '''

    global game_level
    score = 0
    is_active = True
    end = False
    for i in range(game_levels):
        game_level = i

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
                if event.key not in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER, pygame.K_ESCAPE,
                                     pygame.KMOD_CTRL]:
                    player += pygame.key.name(event.key)
                else:
                    return
            else:
                pass

            display_ = pygame.sprite.GroupSingle()
            display_.add(TableElement('question',
                                  f'{language_dictionary[util.game_language].quiz.player_name_prompt} {player.capitalize()}'))
            display_.draw(screen)

        pygame.display.update()
        clock.tick(60)


def game_loop(level: int, question_array: {}):
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
    '''
    # DEBUG COMMENT HERE
    if level in [0, 6, 8]:
        play_question_intro(level)
    if util.game_language == util.Language.HUNGARIAN.name and level < 14:
        play_question_prologue(level)
        play_music(level)
    '''
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

    counter = 3
    sprite_group = ['question', "a", "b", "c", "d"]
    global selected
    selected = ""
    global type
    type = "select"
    texts = [question, answer_list[0], answer_list[1], answer_list[2], answer_list[3]]
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
    menu_group.add(MenuOption("exit", 2, 300))

    prizes_table.add(Prizes())
    global exit_game
    exit_game = False
    out_of_game_started = False
    global prize_table_event
    prize_table_event = pygame.USEREVENT + 9
    global prize_table_seconds

    prize_table_seconds = 5
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_active = False
            if event.type == pygame.USEREVENT and selected != "" and type == "select":
                if audience_event != 0:
                    audience_event = 0
                    for ob in help_group.sprites():
                        if ob.type == "audience_table":
                            help_group.remove(ob)
                counter -= 1
                if counter < 1:
                    play_select_sounds(level, selected, last_input, out_of_game)
                    type = "mark"
            if event.type == mark_event:
                mark_seconds -= 1
            if event.type == after_halving_event:
                halving_time -= 1
                if halving_time < 1:
                    after_halving_sounds = ["after_halving", "after_halving_2", "after_halving_3",
                                            "your_guess_stayed", "you_have_fifty_percent",
                                            "im_not_surprised"]
                    sound = random.choice(after_halving_sounds)
                    util.play_sound(sound, 0, dir="halving")
                    after_halving_event = 0
            if event.type == phone_event:
                if len(help_group) == 3 and not clock_added:
                    help_group.add(Help("clock"))
                    clock_added = True
                if phone_seconds > 0 and phone_seconds > 30 - call_duration:
                    phone_seconds -= 1
                else:
                    util.stop_music()
                    util.play_sound("phone_call_return", 0, general=True)
                    phone_event = 0

            if event.type == dial_event:
                if dial_seconds > 0:
                    dial_seconds -= 1
                if dial_seconds < 1 and phone_event == 0:
                    phone_intro_event = pygame.USEREVENT + 6
                    dial_event = 0

            if event.type == phone_intro_event:
                if intro_duration > 0:
                    intro_duration -= 1

                else:
                    phone_event = pygame.USEREVENT + 3
                    phone_intro_event = 0
            if event.type == audience_intro_event:
                if audience_intro_duration > 0:
                    audience_intro_duration -= 1
                if audience_intro_duration < 1:
                    audience_event = pygame.USEREVENT + 4
                    audience_intro_event = 0
            if event.type == audience_event:
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



            if event.type == prize_event:
                if prize_seconds > 0:
                    prize_seconds -= 1

            if event.type == prize_table_event:
                if prize_table_seconds > 0:
                    prize_table_seconds -= 1
                if prize_table_seconds == 0:
                    prize_table_event = 0

            if game_active:
                if event.type == pygame.MOUSEBUTTONDOWN and selected == "":
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
            if out_of_game and not out_of_game_started:
                answer_out_of_game(level)
                out_of_game_started = True

            screen.blit(sky_surface, (0, 0))
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
                                if prize_seconds == 0 and not out_of_game:
                                    return False
                                else:
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
                obstacle_group.draw(screen)
                obstacle_group.update(selected, correct_answer_key, type)
                if prize_event != 0:
                    screen.fill((0, 0, 0))
                    screen.blit(sky_surface, (0, 0))
                    prize_group.draw(screen)
                    prize_group.update(selected, correct_answer_key)
                if phone_event != 0:
                    x_pos = 1130
                    y_pos = 160
                    font = pygame.font.SysFont('Sans', 33, bold=True)
                    game_message = font.render(str(phone_seconds), True, (255, 255, 255))
                    game_message_rect = game_message.get_rect(center=(x_pos, y_pos))
                    screen.blit(game_message, game_message_rect)
                if audience_event != 0:
                    x_pos = 1140
                    y_pos = 95
                    if audience_res != {}:
                        font = pygame.font.SysFont('Sans', 30)
                        game_message = font.render(audience_text, True, (255, 255, 255))
                        game_message_rect = game_message.get_rect(center=(x_pos, y_pos))
                        screen.blit(game_message, game_message_rect)

                        x_pos = 1055
                        y_pos = 365
                        width = 25
                        color = (92, 175, 255)
                        table_length = 240
                        answers = ["a", "b", "c", "d"]
                        for key in answers:
                            if key in audience_res and audience_res[key] != 0:
                                line = [(x_pos, y_pos), (x_pos, y_pos - table_length / 10 * (audience_res[key] / 10))]
                                pygame.draw.line(screen, color, line[0], line[1], width=width)
                            x_pos += 50

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
    util.stop_sound()
    # thread_random(level, working=False)
    if not out_of_game:
        util.pause_music()
    if util.game_language == util.Language.HUNGARIAN.name:
        play_marked_sound(selected, level, last_one=last_input)
    global mark_event
    mark_event = pygame.USEREVENT + 2


def play_incorrect_sounds(level: int):
    thread_random(level, working=False)
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
            time.sleep(7)
        elif level == 9:
            time.sleep(3)
            if util.game_language == util.Language.HUNGARIAN.name:
                util.play_sound("now_comes_hard_part", 0, dir="random")
        else:
            util.play_sound("claps", 0, general=True)
            # time.sleep(2)
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


def thread_random(level: int, selected="", last_one="", working=True):
    global base_threads
    global a_threads
    global b_threads
    global c_threads
    global d_threads
    global threads

    if working == True:
        if last_one == "a":
            for thread in a_threads:
                thread.cancel()
        elif last_one == "b":
            for thread in b_threads:
                thread.cancel()
        elif last_one == "c":
            for thread in c_threads:
                thread.cancel()
        elif last_one == "d":
            for thread in d_threads:
                thread.cancel()
        elif last_one == "base":
            pass
        else:
            for thread in base_threads:
                thread.cancel()

        if selected == "a":
            for thread in a_threads:
                if not thread.finished.is_set():
                    thread.start()

                else:
                    a_threads = []
                    threads[1] = []
                    for i in range(4):
                        a_threads.append(threading.Timer(15.0 * (i + 1), play_random_quizmaster_sound, args=(level,)))
                    for thread_ in a_threads:
                        thread_.start()
                    threads[1] = a_threads
                    return
        elif selected == "b":
            for thread in b_threads:
                if not thread.finished.is_set():
                    thread.start()
                else:
                    b_threads = []
                    threads[2] = []

                    for i in range(4):
                        b_threads.append(threading.Timer(15.0 * (i + 1), play_random_quizmaster_sound, args=(level,)))
                    for thread_ in b_threads:
                        thread_.start()
                    threads[2] = b_threads

                    return
        elif selected == "c":
            for thread in c_threads:
                if not thread.finished.is_set():
                    thread.start()

                else:
                    c_threads = []
                    threads[3] = []

                    for i in range(4):
                        c_threads.append(threading.Timer(15.0 * (i + 1), play_random_quizmaster_sound, args=(level,)))
                    for thread_ in c_threads:
                        thread_.start()
                    threads[3] = c_threads

                    return
        elif selected == "d":
            for thread in d_threads:
                if not thread.finished.is_set():
                    thread.start()
                else:
                    d_threads = []
                    threads[4] = []

                    for i in range(4):
                        d_threads.append(threading.Timer(15.0 * (i + 1), play_random_quizmaster_sound, args=(level,)))
                    for thread_ in d_threads:
                        thread_.start()
                    threads[4] = d_threads

                    return
        else:
            for thread in base_threads:
                if not thread.finished.is_set():
                    thread.start()
                else:
                    base_threads = []
                    threads[0] = []
                    for i in range(4):
                        base_threads.append(
                            threading.Timer(15.0 * (i + 1), play_random_quizmaster_sound, args=(level,)))
                    for thread_ in base_threads:
                        thread_.start()
                    threads[0] = base_threads
                    return

    else:
        for list in threads:
            for thread in list:
                thread.cancel()


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


def fastest_finger_first():
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
    start_game()
    global game_language, question_lines_easy, question_lines_medium, question_lines_hard
    game_language = util.game_language
    global question_topics
    question_topics = util.question_topics
    global question_difficulty
    question_difficulty = util.question_difficulty
    question_lines = []
    question_lines_easy = []
    question_lines_medium = []
    question_lines_hard = []
    for line in util.open_file("questions", "r", ";",
                               "/text_files/fastest_fingers_first/" + str(game_language).lower() + "/"):
        question_lines.append(line)
    random.shuffle(question_lines)
    total_answer = ""
    util.clear_screen()
    if game_language == util.Language.ENGLISH:
        util.play_sound("start", 0)
    question = question_lines[0][0]
    answers = {"a": question_lines[0][1], "b": question_lines[0][2], "c": question_lines[0][3],
               "d": question_lines[0][4]}
    answer_list = list(answers.values())
    #random.shuffle(answer_list)
    # shuffled_answers = dict(zip(answers, answer_list))
    shuffled_answers = answers
    if game_language == util.Language.HUNGARIAN.name:
        util.play_sound("lets_look_at_the_fastest_fingers_question", 0, dir="fastest_fingers")
        time.sleep(2)
    start = time.time()

    # total_answer += answer

    correct_answer_keys = question_lines[0][5]

    global game_active


    dbclock = pygame.time.Clock()
    DOUBLECLICKTIME = 500

    pygame.time.set_timer(pygame.USEREVENT, 1000)  # SELECT EVENT
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  # MARK EVENT
    pygame.time.set_timer(pygame.USEREVENT + 2, 1000)  # PRIZE EVENT

    counter = 3
    sprite_group = ['question', "a", "b", "c", "d"]
    global selected
    selected = ""
    global type
    type = "fastest_fingers_select"
    texts = [question, answer_list[0], answer_list[1], answer_list[2], answer_list[3]]
    obstacle_group = pygame.sprite.Group()
    for index in range(len(sprite_group)):
        obstacle_group.add(TableElement(sprite_group[index], texts[index]))
    global help_group

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



    sky_surface = pygame.image.load('./data/graphics/bg.jpg').convert_alpha()

    global fastest_fingers_result
    global fastest_fingers_mark_event

    fastest_fingers_mark_event = 0
    fastest_fingers_result = ""


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

                    obstacle_group.add(TableElement('fastest_fingers_result', str(player).capitalize() + " : " + str(end - start)[:5]))
                    for ob in obstacle_group.sprites():
                        ob.image = pygame.image.load('./data/graphics/fastest_fingers_win.png').convert_alpha()
                        font = pygame.font.SysFont('Sans', 33)
                        text = font.render(str(player).capitalize() + " : " + str(end - start)[:5], True, (255, 255, 255))
                        text_rect_1 = text.get_rect(center=(1366 / 2, 48))

                        ob.image.blit(text, text_rect_1)

                    util.stop_sound()

                    if game_language == util.Language.HUNGARIAN.name:
                        if os.path.isfile(
                                "./data/sound_files/hungarian/fastest_fingers" + correct_answer_keys + ".wav"):
                            util.play_sound(correct_answer_keys, 0)
                        time.sleep(1)
                        util.play_sound("lets_see_who_is_correct", 0, dir="fastest_fingers")

                    time.sleep(2)
                    if fastest_fingers_result == correct_answer_keys:


                        util.play_sound("fastest_fingers_correct", 0, general=True)
                        # print_prizes_with_quizmaster(0, False, special_text="♦ " + player_name + " : " + str(end - start)[:5] + " ♦",
                        #                             bg_color=bg.green)
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


                        #prize_event = pygame.USEREVENT + 8
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

    prizes = util.open_file("prizes_" + str(game_language).lower(), "r")

    if out_of_game:
        if round_number > 0:
            return prizes[round_number - 1][0]
        else:
            if util.game_language == util.Language.HUNGARIAN.name:
                return "0 Ft"
            else:
                return "£0"
    else:
        if not correct_answer:
            if round_number > 9:
                return prizes[9][0]
            elif round_number > 4:
                return prizes[4][0]
            else:
                if util.game_language == util.Language.HUNGARIAN.name:
                    return "0 Ft"
                else:
                    return "£0"
        else:
            return prizes[round_number][0]


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


def show_game_structure():
    import time, msvcrt
    # TODO: only works on win
    timeout = 2
    startTime = time.time()
    inp = None
    print(language_dictionary[util.game_language].quiz.skip_prompt)
    while True:
        if msvcrt.kbhit():
            global game_language
            inp = msvcrt.getch()
            break
        elif time.time() - startTime > timeout:
            break
    util.clear_screen()
    if inp:
        return

    game_language = util.game_language
    prizes = util.open_file("prizes_" + str(game_language).lower(), "r")
    if game_language == util.Language.HUNGARIAN.name:
        util.play_sound("prizes_description", 0, dir="intro")
        print_helps()
        print("\n\n")
        for i in range(len(prizes)):
            for j in range(len(prizes)):
                round_number = str(len(prizes) - j)
                if len(prizes) - j < 10:
                    round_number = " " + round_number
                if i == len(prizes) - j - 1:
                    print(round_number + " ♦ " + bg.orange + fg.black + prizes[::-1][j][0] + fg.rs + bg.rs)
                else:
                    if j == 5 or j == 10 or j == 0:
                        print(round_number + " ♦ " + prizes[::-1][j][0])
                    else:
                        print(round_number + " ♦ " + fg.orange + prizes[::-1][j][0] + fg.rs)
            if os.name == "nt":
                time.sleep(0.3)
            else:
                time.sleep(0.4)
            if i != 14:
                util.clear_screen()
                print_helps()
                print("\n\n")
        if os.name == "posix":
            time.sleep(2)
        else:
            time.sleep(0.7)
        util.clear_screen()
        print_helps()
        print("\n\n")
        for a in range(2):
            for b in range(len(prizes)):
                round_number = str(len(prizes) - b)
                if len(prizes) - b < 10:
                    round_number = " " + round_number
                if a == 0 and b == 10 or a == 1 and b == 5:
                    print(round_number + " ♦ " + bg.orange + fg.black + prizes[::-1][b][0] + fg.rs + bg.rs)
                else:
                    if b == 0 or b == 5 or b == 10:
                        print(round_number + " ♦ " + prizes[::-1][b][0])
                    else:
                        print(round_number + " ♦ " + fg.orange + prizes[::-1][b][0] + fg.rs)
            time.sleep(1)
            if a == 1 and os.name == "nt":
                time.sleep(0.4)
            util.clear_screen()
            print_helps()
            print("\n\n")
        util.play_sound("help_modules", 0, dir="intro")
        util.clear_screen()
        list_helps()
        time.sleep(3)
        util.clear_screen()
        print_helps()
        print("\n\n")
        print_prizes()
        util.play_sound("prologue_end", 0, dir="intro", timer=True)
        util.clear_screen()
    else:
        print_helps()
        print("\n\n")
        print_prizes()
        util.play_sound("start", 0, timer=True)
        util.clear_screen()


def play_music(round: int):
    if round < 5:
        util.play_background_music(str(5), 0)
    else:
        util.play_background_music(str(round), 0)


def play_marked_sound(choise: str, level: int, last_one=""):
    sounds = []

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


def handle_user_input(question: str, answers: dict, correct_answer: str, level=0, final_color="orange",
                      out_of_game=False,
                      help=False) -> str:
    select_text = language_dictionary[game_language].quiz.select_answer
    last_input = ""
    sound_dir = ""
    if util.game_language == util.Language.HUNGARIAN.name:
        sound_list_dict = get_sound_list(util.quizmaster_attitude)
        bad_sounds = sound_list_dict['bad_sounds']
        correct_sounds = sound_list_dict['correct_sounds']

    if out_of_game:
        select_text = language_dictionary[game_language].quiz.select_answer_out

    while True:
        user_input = get_user_input()
        if not help:
            user_inputs = [[b'a', "a"], [b'b', "b"], [b'c', "c"], [b'd', "d"]]
            for input_ in user_inputs:
                if user_input == input_[0] or user_input == input_[1]:
                    if util.game_language == util.Language.HUNGARIAN.name:
                        sound_dir = "random"
                        thread_random(level, selected=input_[1], last_one=last_input)
                        if util.quizmaster_attitude != util.QuizMasterAttitude.NONE.name:
                            if input_[1] == correct_answer:
                                selected_sound = random.choice(correct_sounds)
                            else:
                                selected_sound = random.choice(bad_sounds)
                    util.clear_screen()
                    print_quiz_table(question, answers, game_level=level, selected=input_[1], color="li_grey")
                    print("\n\n   " + fg.grey + select_text + fg.rs)
                    if not out_of_game:
                        util.pause_music()
                    if util.game_language == util.Language.HUNGARIAN.name and util.quizmaster_attitude != util.QuizMasterAttitude.NONE.name:
                        if selected_sound.find("mark") != -1 or selected_sound.find("final") != -1:
                            sound_dir = "mark"
                        util.play_sound(selected_sound, 0, dir=sound_dir)
                    if not out_of_game:
                        util.continue_music()
                    last_input = input_[1]
                    while True:
                        user_input = get_user_input()
                        util.stop_sound()
                        if user_input == b'\r' or user_input == '<Ctrl-j>':
                            thread_random(level, working=False)
                            util.clear_screen()
                            print_quiz_table(question, answers, input_[1], final_color, game_level=level)
                            if not out_of_game:
                                util.pause_music()
                            if util.game_language == util.Language.HUNGARIAN.name and not out_of_game:
                                play_marked_sound(input_[1], level, last_one=last_input)
                            return input_[1]
                        if user_input not in input_:
                            break

            if not out_of_game:
                if user_input == b'h' or user_input == "h":
                    return "h"
                if user_input == b's' or user_input == "s":
                    return "h"
                if user_input == b'k' or user_input == "k":
                    return "t"
                if user_input == b't' or user_input == "t":
                    return "t"
            if user_input == b'\x1b' or user_input == '<ESC>':
                return "esc"

        else:
            if user_input == b'a' or user_input == "a":
                return "a"
            if user_input == b'd' or user_input == "d":
                return "d"
            if user_input == b'f' or user_input == "f":
                return "h"
            if user_input == b'm' or user_input == "m":
                return "m"
            if user_input == b'p' or user_input == "p":
                return "d"
            if user_input == b't' or user_input == "t":
                return "t"
            if user_input == b'k' or user_input == "k":
                return "a"
            if user_input == b'h' or user_input == "h":
                return "h"
            if user_input == b's' or user_input == "s":
                return "h"
            if user_input == b'y' or user_input == "y":
                return "y"
            if user_input == b'\x1b' or user_input == '<ESC>':
                return "esc"


def quit_quiz(score: int, name: str, topic, end=False):
    #thread_random(score, working=False)
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
