import json
import os
import sys

import pygame
from sty import Style, RgbFg, fg, bg, rs

import millionaire.quiz_game.quiz_game as quiz
import millionaire.util.util as util

fg.purple = Style(RgbFg(148, 0, 211))
bg.orange = bg(255, 150, 50)
language_dictionary = util.language_dictionary
default_width = 40
screen_distance = 60
bg.dark_blue = bg(0, 0, 155)
bg.darkest_blue = bg(42, 45, 112)


def intro():
    if util.game_language == util.Language.HUNGARIAN.name:
        util.play_sound("intro", 0, dir="intro", volume=1)
    else:
        util.play_sound("intro", 0)


def show_title():
    line_length = default_width + 3
    util.clear_screen()
    print(screen_distance * " " + "=" * line_length)
    print(screen_distance * " " + fg.purple + language_dictionary[util.game_language].menu.title_first_line + fg.rs)
    print(screen_distance * " " + "=" * line_length)
    print(screen_distance * " " + fg.yellow + "|" * line_length + fg.rs)
    print(screen_distance * " " + fg.purple + language_dictionary[util.game_language].menu.title_second_line + fg.rs)
    print(screen_distance * " " + fg.yellow + "|" * line_length + fg.rs)
    print(screen_distance * " " + "=" * line_length)
    print(screen_distance * " " + fg.purple + language_dictionary[util.game_language].menu.title_first_line + fg.rs)
    print(screen_distance * " " + "=" * line_length + "\n\n")


def select_help():
    quiz.show_game_structure()
    util.clear_screen()
    file = (util.open_file("tutorial_" + str(util.game_language).lower(), 'r'))
    print("\n")
    for line in file:
        print("   " + line[0])
    print("\n")


def update_settings_file():
    filename = "settings.json"
    content = {"language": util.game_language, "topic": util.question_topics, "difficulty": util.question_difficulty,
               "volume": util.system_volume, "quizmaster_attitude": util.quizmaster_attitude}
    with open(filename, "w", encoding="UTF-8") as outfile:
        json.dump(content, outfile)


class MenuOption(pygame.sprite.Sprite):

    def __init__(self, type, order, base_height):
        super().__init__()

        x_pos = 0
        y_pos = base_height + (order * 35)

        self.frame = pygame.image.load('./data/graphics/settings_option.png').convert_alpha()
        self.font = pygame.font.SysFont('Sans', 25)
        self.type = type
        self.text_color = (255, 255, 255)
        self.text_x = 30
        self.text_y = 0
        if type == "main_menu_option":
            text = language_dictionary[util.game_language].menu.main_menu_options[order]
            self.name = text

        elif type == "settings_menu_option":
            self.text_x = 50
            self.text_y = 5

            #if len(language_dictionary[util.game_language].menu.settings_menu_options) > order:

                #text = language_dictionary[util.game_language].menu.settings_menu_options[order]
               # self.name = text

            #else:
            x_pos = 0
            base_height = 545
            y_pos = base_height + ((order-8) * 45)

            if order == 0:
                if util.game_language[:2].lower() == "hu":
                    text = language_dictionary[util.game_language].menu.settings_menu_options[0]+ ": " + language_dictionary[util.game_language].hu
                    self.name = language_dictionary[util.game_language].menu.settings_menu_options[0]

                else:
                    text = language_dictionary[util.game_language].menu.settings_menu_options[0]+ ": " + language_dictionary[util.game_language].en
                    self.name = language_dictionary[util.game_language].menu.settings_menu_options[0]

            elif order == 1:
                self.name = language_dictionary[util.game_language].menu.settings_menu_options[1]

                text = language_dictionary[util.game_language].sounds + ": "
                if util.system_volume:
                    text += language_dictionary[util.game_language].true
                else:
                    text += language_dictionary[util.game_language].false

            elif order == 2:
                text = language_dictionary[util.game_language].menu.settings_menu_options[2] + ": "
                if util.full_screen:
                    text += language_dictionary[util.game_language].true
                else:
                    text += language_dictionary[util.game_language].false

                self.name = language_dictionary[util.game_language].menu.settings_menu_options[2]

            elif order == 3:
                text = language_dictionary[util.game_language].topic + ": " + str(util.question_topics)
                self.name = language_dictionary[util.game_language].menu.settings_menu_options[3]

            elif order == 4:
                text = language_dictionary[util.game_language].menu.settings_menu_options[4] + ": " + str(util.question_difficulty)
                self.name = language_dictionary[util.game_language].menu.settings_menu_options[4]

            elif order == 5:
                text = language_dictionary[util.game_language].menu.settings_menu_options[5] + ": " + str(util.quizmaster_attitude)
                self.name = language_dictionary[util.game_language].menu.settings_menu_options[5]


            elif order == 6:
                text = language_dictionary[util.game_language].menu.settings_menu_options[-2] + ": "
                if util.system_volume:
                    text += language_dictionary[util.game_language].true
                else:
                    text += language_dictionary[util.game_language].false

                self.name = language_dictionary[util.game_language].menu.settings_menu_options[-2]
            else:
                text = language_dictionary[util.game_language].menu.settings_menu_options[-1]
                self.name = text

        elif type == "topic_option":
            text = language_dictionary[util.game_language].menu.settings_menu_question_topics[order]
            self.name = text

        elif type == "question_difficulty_option":
            text = language_dictionary[util.game_language].menu.question_difficulty_levels[order]
            self.name = text

        elif type == "quizmaster_attitude_option":
            text = language_dictionary[util.game_language].menu.quizmaster_attitudes[order]
            self.name = text

        elif type == "language_option":
            text = [language_dictionary[util.game_language].en, language_dictionary[util.game_language].hu][order]
            self.name = text

        elif type == "tutorial_option":
            text = language_dictionary[util.game_language].menu.settings_menu_options[-1]
            self.name = text
        elif type == "scores_paging":
            text = language_dictionary[util.game_language].next_page
            self.name = text

        else:
            text = ""

        self.text = self.font.render(text, True, (255, 255, 255))
        self.image = self.frame
        self.image.blit(self.text, [self.text_x, self.text_y])
        self.rect = self.image.get_rect(topleft=(x_pos, y_pos))
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
            if self.type == "settings_menu_option":
                self.image = pygame.image.load('./data/graphics/settings_option_marked.png').convert_alpha()
            else:
                self.image = pygame.image.load('./data/graphics/option_marked.png').convert_alpha()
            self.image.blit(self.text, [self.text_x, self.text_y])


        else:
            if self.type == "settings_menu_option":
                self.image = pygame.image.load('./data/graphics/settings_option.png').convert_alpha()
            else:
                self.image = pygame.image.load('./data/graphics/option.png').convert_alpha()
            self.image.blit(self.text, [self.text_x, self.text_y])

        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint((pygame.mouse.get_pos())):
            print(self.name)
            import time
            time.sleep(0.2)
            if self.name in language_dictionary[util.game_language].menu.main_menu_options:
                if self.name == language_dictionary[util.game_language].menu.main_menu_options[0]:
                    quiz.play()
                if self.name == language_dictionary[util.game_language].menu.main_menu_options[2]:
                    text_screen("tutorial")
                if self.name == language_dictionary[util.game_language].menu.main_menu_options[3]:
                    global options
                    options = True
                if self.name == language_dictionary[util.game_language].menu.main_menu_options[4]:
                    text_screen("credits")
                if self.name == language_dictionary[util.game_language].menu.main_menu_options[5]:
                    text_screen("scores")
                if self.name == language_dictionary[util.game_language].menu.main_menu_options[-1]:
                    pygame.quit()
                    exit()

            if self.name in language_dictionary[util.game_language].menu.settings_menu_options:

                if self.name == language_dictionary[util.game_language].menu.settings_menu_options[0]:
                    global lang_selection
                    lang_selection = True
                if self.name == language_dictionary[util.game_language].menu.settings_menu_options[1]:
                    if util.system_volume:
                        util.system_volume = False
                    else:
                        util.system_volume = True
                if self.name == language_dictionary[util.game_language].menu.settings_menu_options[2]:
                    global screen

                    if util.full_screen:
                        util.full_screen = False
                        screen = pygame.display.set_mode((1366, 768))
                    else:
                        util.full_screen = True
                        screen = pygame.display.set_mode((1366, 768), pygame.FULLSCREEN)
                if self.name == language_dictionary[util.game_language].menu.settings_menu_options[3]:
                    global topics
                    topics = True

                if self.name == language_dictionary[util.game_language].menu.settings_menu_options[4]:
                    global difficulties
                    difficulties = True

                if self.name == language_dictionary[util.game_language].menu.settings_menu_options[5]:
                    global attitudes
                    attitudes = True
                if self.name == language_dictionary[util.game_language].menu.settings_menu_options[-2]:
                    util.init_settings(util.Language.ENGLISH.name, reset_settings=True)

                if self.name == language_dictionary[util.game_language].menu.settings_menu_options[-1]:
                    if self.type == "tutorial_option":
                        global screen_active
                        screen_active = False
                    else:
                        options = False
                        update_settings_file()

            elif self.name == language_dictionary[util.game_language].next_page:
                global scores_paging
                scores_paging += 1

            if self.name in [language_dictionary[util.game_language].en,
                             language_dictionary[util.game_language].hu]:
                if self.name == language_dictionary[util.game_language].hu:
                    util.set_game_language(util.Language.HUNGARIAN.name)
                else:
                    util.set_game_language(util.Language.ENGLISH.name)
                lang_selection = False

            if self.name in language_dictionary[util.game_language].menu.settings_menu_question_topics:
                if util.question_topics != str(
                        list(language_dictionary[util.game_language].menu.settings_menu_question_topics).index(
                                self.name)).lower():
                    util.set_question_topics(util.Topics(
                        list(language_dictionary[util.game_language].menu.settings_menu_question_topics).index(
                            self.name)).name)
                topics = False

            if self.name in language_dictionary[util.game_language].menu.question_difficulty_levels:
                if util.difficulty_levels != self.name:
                    if self.name != language_dictionary[util.game_language].menu.question_difficulty_levels[0]:
                        util.set_question_difficulty(util.Difficulty(language_dictionary[util.game_language].menu.question_difficulty_levels.index(self.name)).name)
                    else:
                        util.set_question_difficulty(util.Difficulty.ALL.name)
                difficulties = False

            if self.name in language_dictionary[util.game_language].menu.quizmaster_attitudes:
                if util.quizmaster_attitudes != self.name:
                    util.set_quizmaster_attitude(util.QuizMasterAttitude(
                        language_dictionary[util.game_language].menu.quizmaster_attitudes.index(self.name)).name)
                attitudes = False

    def update(self):
        if self.type == "main_menu_option":
            text = language_dictionary[util.game_language].menu.main_menu_options[self.order]
            self.name = text
        elif self.type == "settings_menu_option":
            if self.order == 0:
                if util.game_language[:2].lower() == "hu":
                    text = language_dictionary[util.game_language].menu.settings_menu_options[0] + ": " + language_dictionary[util.game_language].hu
                    self.name = language_dictionary[util.game_language].menu.settings_menu_options[0]

                else:
                    text = language_dictionary[util.game_language].menu.settings_menu_options[0] + ": " + language_dictionary[util.game_language].en
                    self.name = language_dictionary[util.game_language].menu.settings_menu_options[0]

            elif self.order == 1:
                text = language_dictionary[util.game_language].sounds + ": "
                if util.system_volume:
                    text += language_dictionary[util.game_language].true
                else:
                    text += language_dictionary[util.game_language].false
                self.name = language_dictionary[util.game_language].menu.settings_menu_options[self.order]


            elif self.order == 2:
                text = language_dictionary[util.game_language].menu.settings_menu_options[2] + ": "
                if util.full_screen:
                    text += language_dictionary[util.game_language].true
                else:
                    text += language_dictionary[util.game_language].false
                self.name = language_dictionary[util.game_language].menu.settings_menu_options[self.order]

            elif self.order == 3:
                text = language_dictionary[util.game_language].topic + ": " + list(language_dictionary[util.game_language].menu.settings_menu_question_topics)[util.Topics[util.question_topics].value]
                self.name = language_dictionary[util.game_language].menu.settings_menu_options[self.order]

            elif self.order == 4:
                text = language_dictionary[util.game_language].menu.settings_menu_options[self.order] + ": " + list(language_dictionary[util.game_language].menu.question_difficulty_levels)[util.Difficulty[util.question_difficulty].value]
                self.name = language_dictionary[util.game_language].menu.settings_menu_options[self.order]

            elif self.order == 5:
                text = language_dictionary[util.game_language].menu.settings_menu_options[self.order] + ": " + list(language_dictionary[util.game_language].menu.quizmaster_attitudes)[util.QuizMasterAttitude[util.quizmaster_attitude].value]
                self.name = language_dictionary[util.game_language].menu.settings_menu_options[self.order]

            elif self.order == 6:
                text = language_dictionary[util.game_language].menu.settings_menu_options[self.order] + ": "
                if util.default_settings():
                    text += language_dictionary[util.game_language].true
                else:
                    text += language_dictionary[util.game_language].false
                self.name = language_dictionary[util.game_language].menu.settings_menu_options[self.order]

            else:
                text = language_dictionary[util.game_language].menu.settings_menu_options[self.order]
                self.name = language_dictionary[util.game_language].menu.settings_menu_options[self.order]
        elif self.type == "topic_option":
            text = language_dictionary[util.game_language].menu.settings_menu_question_topics[self.order]
            self.name = text

        elif self.type == "question_difficulty_option":
            text = language_dictionary[util.game_language].menu.question_difficulty_levels[self.order]
            self.name = text

        elif self.type == "quizmaster_attitude_option":
            text = language_dictionary[util.game_language].menu.quizmaster_attitudes[self.order]
            self.name = text

        elif self.type == "language_option":
            langs = [language_dictionary[util.game_language].en, language_dictionary[util.game_language].hu]
            text = langs[self.order]
            self.name = langs[self.order]
        elif self.type == "tutorial_option":
            text = language_dictionary[util.game_language].menu.settings_menu_options[-1]
            self.name = text
        elif self.type == "scores_paging":

            text = language_dictionary[util.game_language].next_page
            self.name = text
        else:
            text = ""

        self.text = self.font.render(text, True, (255, 255, 255))
        self.lang = util.game_language
        self.player_input()


def main():
    pygame.init()
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
    pygame.time.set_timer(pygame.USEREVENT + 2, 1000)

    global screen
    if util.full_screen:
        screen = pygame.display.set_mode((1366, 768), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((1366, 768))
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) NATIVE
    # screen = pygame.display.set_mode((1024, 768), pygame.FULLSCREEN) SET RESOLUTION


    pygame.display.set_caption(language_dictionary[util.game_language].title)

    millioniareIcon = pygame.image.load('./data/graphics/loim.png')
    pygame.display.set_icon(millioniareIcon)

    global clock
    clock = pygame.time.Clock()
    global sky_surface

    sky_surface = pygame.image.load('./data/graphics/menu_bg.jpg').convert_alpha()
    settings_surface =  pygame.image.load('./data/graphics/settings_menu_bg.png').convert_alpha()
    # sky_surface_rect = sky_surface.get_rect(midtop=(400, 20))
    # subsurface = sky_surface.subsurface(0,0,800,400)

    main_menu_base_y = 475

    menu_option_group = sprite_group_init(language_dictionary[util.game_language].menu.main_menu_options,
                                          "main_menu_option", main_menu_base_y)

    settings_menu_base_y = 245
    topic_menu_base_y = 75

    settings_group = []
    for option in language_dictionary[util.game_language].menu.settings_menu_options:
        settings_group.append(option)


    settings_option_group = sprite_group_init(settings_group,
                                              "settings_menu_option", settings_menu_base_y)


    lang_group = sprite_group_init(util.available_languages, "language_option", settings_menu_base_y)

    topic_group = sprite_group_init(language_dictionary[util.game_language].menu.settings_menu_question_topics,
                                    "topic_option", topic_menu_base_y)
    question_difficulty_group = sprite_group_init(
        language_dictionary[util.game_language].menu.question_difficulty_levels, "question_difficulty_option",
        settings_menu_base_y)
    quizmaster_attitude_group = sprite_group_init(language_dictionary[util.game_language].menu.quizmaster_attitudes,
                                                  "quizmaster_attitude_option", settings_menu_base_y)

    global options, lang_selection, topics, difficulties, attitudes
    options = False
    lang_selection = False
    topics = False
    difficulties = False
    attitudes = False

    sprite_group_flags = [options, lang_selection, topics, difficulties, attitudes]
    sprite_groups = [settings_option_group, lang_group, topic_group, question_difficulty_group,
                     quizmaster_attitude_group]

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # screen.blit(subsurface, (0, -20), sky_surface_rect)
        screen.blit(sky_surface, (0, 0))

        if options:
            screen.blit(settings_surface, (0,0))
            if lang_selection:

                lang_group.draw(screen)
                lang_group.update()

                # if event.type == pygame.MOUSEBUTTONDOWN:
                #    lang_selection = False
            elif topics:

                topic_group.draw(screen)
                topic_group.update()

            elif difficulties:

                question_difficulty_group.draw(screen)
                question_difficulty_group.update()

            elif attitudes:

                quizmaster_attitude_group.draw(screen)
                quizmaster_attitude_group.update()

            else:

                settings_option_group.draw(screen)
                settings_option_group.update()


        else:
            screen.fill((0, 0, 0))
            # screen.blit(subsurface, (0, -20), sky_surface_rect)
            screen.blit(sky_surface, (0, 0))

            menu_option_group.draw(screen)
            menu_option_group.update()

        pygame.display.update()
        clock.tick(60)


def text_screen(screen_type: str):
    pygame.init()
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    global screen
    if util.full_screen:
        screen = pygame.display.set_mode((1366, 768), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((1366, 768))

    pygame.display.set_caption(language_dictionary[util.game_language].title)

    millioniareIcon = pygame.image.load('./data/graphics/loim.png')
    pygame.display.set_icon(millioniareIcon)

    global clock
    clock = pygame.time.Clock()

    global screen_active
    screen_active = True
    tutorial_group = sprite_group_init([language_dictionary[util.game_language].menu.settings_menu_options[-1]], "tutorial_option", 700)
    is_added = False
    global scores_paging
    scores_paging = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN or not screen_active:
                return
        screen.fill((7, 24, 173))

        y = 20

        if screen_type in ["tutorial", "credits"]:
            font = pygame.font.SysFont('Sans', 25)

            text_array = []
            if screen_type == "tutorial":
                text_array = language_dictionary[util.game_language].tutorial.text_list
            else:
                text_array = language_dictionary[util.game_language].credits.text_list

            for line in text_array:
                text = font.render(line, True, (255, 148, 0))

                screen.blit(text, [200, y])
                y += 50

        else:
            font = pygame.font.SysFont('Sans', 18)

            if os.path.isfile("scores.json"):
                showed_text = ""
                f = open("scores.json")
                data = json.load(f)
                scores_sorted = sorted(data, key=lambda d: d['score'], reverse=True)
                if len(scores_sorted) > 15 and not is_added:
                    tutorial_group.add(MenuOption("scores_paging", 0, 500))
                    is_added = True
                if len(scores_sorted) >= scores_paging*15:
                    if scores_paging == 0:
                        scores_sorted = sorted(data, key=lambda d: d['score'], reverse=True)[:15]
                        showed_text = "1 - 15"
                    else:
                        scores_sorted = sorted(data, key=lambda d: d['score'], reverse=True)[((scores_paging-1)*15):(scores_paging*15)]
                        showed_text = str(((scores_paging-1)*15)+1) + " - " + str(scores_paging*15)
                elif len(scores_sorted) < scores_paging*15 and len(scores_sorted) > ((scores_paging-1)*15):
                    showed_text = str(((scores_paging - 1) * 15)+1) + " - " + str(len(scores_sorted))
                    scores_sorted = sorted(data, key=lambda d: d['score'], reverse=True)[
                                    ((scores_paging - 1) * 15):(scores_paging * 15)]
                else:
                    scores_paging = 1

                i = 0
                for item in scores_sorted:
                    screen_x = 0
                    for k, v in item.items():
                        if k == "topic":
                            v = list(language_dictionary[util.game_language].menu.settings_menu_question_topics)[util.Topics[v].value]
                        text = font.render(str(k) + ": " + str(v), True, (255, 148, 0))
                        screen.blit(text, [screen_x, 0+ (i*25)])

                        screen_x += 200

                    i += 1
                f.close()

                text = font.render(language_dictionary[util.game_language].showed + ": " + showed_text, True, (255, 148, 0))
                screen.blit(text, [668, 450])
            else:
                text = font.render(language_dictionary[util.game_language].menu.empty_scores, True, (255, 148, 0))
                screen.blit(text, [0, 0])


        tutorial_group.draw(screen)
        tutorial_group.update()


        pygame.display.update()
        clock.tick(60)

def sprite_group_init(sprite_group: list, sprite_group_type: str, y_height: int):
    sprit_group_instance = pygame.sprite.Group()

    for index in range(len(sprite_group)):
        sprit_group_instance.add(MenuOption(sprite_group_type, index, y_height))

    return sprit_group_instance
