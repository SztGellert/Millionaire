import random
import sys
import os
from sty import Style, RgbFg, fg, bg
import time
import pygame

operatingSystem = os.name


def game_start():
    fg.purple = Style(RgbFg(148, 0, 211))
    pygame.mixer.init()
    clear_screen(operatingSystem)
    play_sound("data/sound_files/loim_intro.wav", 0)
    time.sleep(2)
    print("This is the game of games..\nIn the arena..\nMr Steven Vágó is awaiting You!\n" + fg.purple + "Become the next Millionaire!\n" + fg.rs)
    time.sleep(5)


def play_sound(filename, starting_time):
    filepath = "./data/sound_files/"
    pygame.mixer.init()
    pygame.mixer.music.load(filepath + filename)
    pygame.mixer.music.set_volume(0.07)
    pygame.mixer.music.play(0, starting_time)


def open_file(filename, mode):
    with open(filename, mode) as file:
        list_of_file = []
        for line in file:
            line = line.strip().split(',')
            list_of_file.append(line)
    return list_of_file


"""

def open_drawing(filename, mode):
    with open(filename, mode) as file:
        list_of_file = []
        for line in file:
            line = line.split(',')
            list_of_file.append(line)
    return list_of_file
"""


def safe_input(input_text, allowed_list_of_letters):
    answer = input(input_text)
    while answer not in allowed_list_of_letters:
        print("Error! Only letters: " + ' '.join(allowed_list_of_letters) + " allowed!")
        answer = input("Select the correct answer!")
    return answer


"""
def choose_random_from_list(list_):

    return random.choice(list_)


def audience_help(answers, current_line, question, table_line_length, choises, shuffled_line, Help_available):
    play_sound("data/sound_files/kozonseg.mp3", 0)
    for i in range(5):
        print_quizmaster_with_audinence_help(Help_available, table_line_length, shuffled_line,current_line)
        if i < 4:
            quiz_table(table_line_length, choises, question, shuffled_line, addition=2)
            time.sleep(1)
            clear_screen(operating_system)
    time.sleep(1)


def print_quizmaster_with_audinence_help(Help_available, table_line_length,shuffled_line,current_line, head='vago2.txt'):

    betuk = ["A: ", "B: ", "C: ", "D: "]
    vago_feje_sorai = open_drawing(head, 'r')


    price_number=0
    prices_line=len("40.000.000 Ft    ")*"_"
    prices_line_sec=len("40.000.000 Ft    ")*"‾"
    Aud = "👥  "
    Tel = bg.black+"📞 "
    Halv = "50:50 "
    for helps in Help_available:
        if not helps:
            if helps == Help_available[0]:
                Aud = bg.red+"👥 "+bg.rs
            if helps == Help_available[1]:
                Tel = bg.red+"📞 "+bg.rs
            if helps == Help_available[2]:
                Halv = bg.red+"50:50 "+bg.rs
    help_line="|"+" "+"50:50 "+"∥"+"📞 "+"∥"+"👥 "+"|"
    help_length=len(help_line)
    price_length=len("40.000.000 Ft")
    print(bg.black+(vago_feje_sorai[0][0]).rstrip().center((table_line_length), ' ')+prices_line)
    print(bg.black+(vago_feje_sorai[1][0]).rstrip().center((table_line_length), ' ')+bg.black+"▏"+" "+Halv+"∥"+Tel+" ∥"+Aud+bg.black+"▕"+bg.rs)
    print(bg.black+(vago_feje_sorai[2][0]).rstrip().center((table_line_length), ' ')+prices_line_sec)
    print(bg.black+(vago_feje_sorai[3][0]).rstrip().center((table_line_length), ' ')+prices_line)
    audience_number=0
    w, h = 13, 15
    audience = [[' ' for x in range(w)] for y in range(h)]
    #audience[13]="==============="
    audience[14]=fg.orange+"A ◆ B ◆ C ◆ D"+fg.rs
    
    percents=give_audience_choises()
    rounds=[]
    var=0
    good_percents=[' ',' ',' ',' ']
    

    for i in range(len(shuffled_line)):
        if shuffled_line[i] == current_line[0]:
            good_percents[i] = percents[0]
        if shuffled_line[i] != current_line[0]:
            if i < 3:
                good_percents[i] = percents[i+1]
            else:
                good_percents[i] = percents[i]

    for percent in range(len(good_percents)):
        
        if int(good_percents[percent]) < 10:
            good_percents[percent]=10
        rounds.append(good_percents[percent]//10)
    for percentage in rounds:
        index=12
        for f in range(0,percentage):
            audience[index-f][var]=audience[index-f][var].replace(' ',fg.blue+"X"+fg.rs)
            
        
        var+=4
                        
    for length in range(len(good_percents)):
        if good_percents[length]<10:
            good_percents[length]=" "+str(length)
            audience[0]=str(good_percents[0])+"%"+" "+str(good_percents[1])+"%"+" "+str(good_percents[2])+"%"+" "+str(good_percents[3])+"%"
        else:
            audience[0]=str(good_percents[0])+"%"+" "+str(good_percents[1])+"%"+" "+str(good_percents[2])+"%"+" "+str(good_percents[3])+"%"
    


    for head_lines in range(4,len(vago_feje_sorai)):
        if head_lines < (len(vago_feje_sorai)-2):
            price_length=len("40.000.000 Ft") 
            if head_lines==4:
                print(bg.black+(vago_feje_sorai[head_lines][0]).rstrip().center((table_line_length), ' ')+"▏"+''.join(audience[audience_number])+"▕")
            else:
                print(bg.black+(vago_feje_sorai[head_lines][0]).rstrip().center((table_line_length), ' ')+"▏ "+''.join(audience[audience_number])+" ▕")
            audience_number+=1
        else:
            print(bg.black+(vago_feje_sorai[head_lines][0]).rstrip().center((table_line_length), ' ')+prices_line_sec)
            print(bg.black+(vago_feje_sorai[head_lines][0]).rstrip().center((table_line_length), ' ')+len(prices_line)*" ")
            break

def quiz_table(table_line_length, choises, question, shuffled_line, addition=0):

    lengths = []
    choice_length = []
    choise_lengths=[]
    for i in range(4):
        lengths.append((len(choises[i].letter)+len(choises[i].answer)+len(choises[i].mark)+len(choises[i].f_end)+len(choises[i].s_end)+len(choises[i].spaces)))
        choice_length.append(len(choises[i].letter)+len(choises[i].answer)+len(choises[i].mark)+len(choises[i].quote)+len(choises[i].spaces))
    spaces_ = table_line_length-(lengths[0]+lengths[1]+4)
    spaces__ = table_line_length-(lengths[2]+lengths[3]+4)
    answer_line_length = table_line_length-4
    
    print(bg.black+"   "+choises[0].slash+bg.black+answer_line_length*"‾"+bg.black+choises[0].slash_+(14+addition)*" "+bg.rs)
    print(bg.black+"  "+choises[0].slash+bg.black+(table_line_length-2)*" "+bg.black+choises[0].slash_+(13+addition)*" "+bg.rs)
    print(bg.black+" -◀"+bg.black+choises[0].slash_+bg.black+''.join(question).center((answer_line_length), ' ')+bg.black+choises[0].slash+"▶-"+(12+addition)*" "+bg.rs)
    print(bg.black+"  "+choises[0].slash+bg.black+(table_line_length-3)*" "+bg.black+choises[0].slash+" "+(13+addition)*" "+bg.rs)
    print(bg.black+"   "+choises[0].slash+bg.black+answer_line_length*"_"+bg.black+choises[0].slash_+" "+(13+addition)*" "+bg.rs)
    print(bg.black+"    "+choice_length[0]*"_"+(spaces_+2)*" "+choice_length[1]*"_"+bg.black+(15+addition)*" "+bg.rs)
    print(bg.black+"  "+choises[0].line+choises[0].f_end+choises[0].firstpart+choises[0].mark+choises[0].additional+choises[0].quote+choises[0].letter+choises[0].secondpart+choises[0].answer+choises[0].spaces+bg.rs+bg.black+choises[0].s_end+spaces_*"-"+choises[1].f_end+choises[1].firstpart+choises[1].mark+choises[1].additional+choises[1].quote+choises[1].letter+choises[1].secondpart+choises[1].answer+choises[1].spaces+bg.rs+bg.black+choises[1].s_end+choises[2].line+bg.black+(13+addition)*" "+bg.rs)
    print(bg.black+"    "+choice_length[0]*"‾"+(spaces_+2)*" "+choice_length[1]*"‾"+bg.black+(15+addition)*" "+bg.rs)
    print(bg.black+"    "+choice_length[2]*"_"+(spaces__+2)*" "+choice_length[3]*"_"+bg.black+(15+addition)*" "+bg.rs)
    print(bg.black+"  "+choises[2].line+choises[2].f_end+choises[2].firstpart+choises[2].mark+choises[2].additional+choises[2].quote+choises[2].letter+choises[2].secondpart+choises[2].answer+choises[2].spaces+bg.rs+bg.black+choises[2].s_end+spaces__*"-"+choises[3].f_end+choises[3].firstpart+choises[3].mark+choises[3].additional+choises[3].quote+choises[3].letter+choises[3].secondpart+choises[3].answer+choises[3].spaces+bg.rs+bg.black+choises[3].s_end+choises[3].line+bg.black+(13+addition)*" "+bg.rs)
    print(bg.black+"    "+choice_length[2]*"‾"+(spaces__+2)*" "+choice_length[3]*"‾"+bg.black+(15+addition)*" "+bg.rs)
    print(bg.rs)

def print_lists(Help_available, table_line_length, head='vago2.txt', file='./data/prices.txt'):
    vago_feje_sorai = open_drawing(head, 'r')
    prices_table=open_file(file,'r')
    price_number=0
    prices_line=len(prices_table[0])*"_"
    prices_line_sec=len(prices_table[0])*"‾"
    Aud = "👥 "
    Tel = bg.black+"📞 "
    Halv = "50:50 "
    for helps in Help_available:
        if not helps:
            if helps == Help_available[0]:
                Aud = bg.red+"👥 "+bg.rs
            if helps == Help_available[1]:
                Tel = bg.red+"📞 "+bg.rs
            if helps == Help_available[2]:
                Halv = bg.red+"50:50 "+bg.rs
    help_line="|"+" "+"50:50 "+"∥"+"📞 "+"∥"+"👥 "+"|"
    help_length=len(help_line)
    print(bg.black+(vago_feje_sorai[0][0]).rstrip().center((table_line_length), ' ')+prices_line)
    print(bg.black+(vago_feje_sorai[1][0]).rstrip().center((table_line_length), ' ')+bg.black+"▏"+" "+Halv+"∥"+Tel+"∥"+Aud+bg.black+"▕"+bg.rs)
    print(bg.black+(vago_feje_sorai[2][0]).rstrip().center((table_line_length), ' ')+prices_line_sec)
    print(bg.black+(vago_feje_sorai[3][0]).rstrip().center((table_line_length), ' ')+prices_line)
    for head_lines in range(4,len(vago_feje_sorai)):
        if head_lines < (len(vago_feje_sorai)-2):
            price_length=len(prices_table[0][price_number])
            print(bg.black+(vago_feje_sorai[head_lines][0]).rstrip().center((table_line_length), ' ')+"▏"+prices_table[0][price_number]+(help_length-price_length-2)*" "+"▕")
            price_number+=1
        else:
            print(bg.black+(vago_feje_sorai[head_lines][0]).rstrip().center((table_line_length), ' ')+prices_line_sec)
            print(bg.black+(vago_feje_sorai[head_lines][0]).rstrip().center((table_line_length), ' ')+len(prices_line)*" ")
            break
def help_modules(answers, current_line, question, table_line_length, shuffled_line, choises, Help_available, prices, prices1, prices2, counter):
    
    help_ = safe_input(": ", ["a","t","h"])
    if help_.lower() == "a":
        if Help_available[0]:
            clear_screen(operating_system)
            audience_help(answers, current_line, question, table_line_length, choises, shuffled_line, Help_available)
            Help_available[0] = False
            quiz_table(table_line_length, choises, question, shuffled_line, addition=2)
        else:
            print("You have already used the audience's help!")

    if help_.lower() == "t":
        if Help_available[1]:
            telephone_help(question, current_line)
            Help_available[1] = False
        else:
            print("You have already used the telephone help!")

    if help_.lower() == "h":
        if Help_available[2]:
            halving(table_line_length, question, shuffled_line, choises, current_line, answers)
            Help_available[2] = False
            print_lists(Help_available, table_line_length, 'vago_helping.txt')
            quiz_table(table_line_length, choises, question, shuffled_line)
        else:
            print("You have already used the halving help!")
    return Help_available


def give_audience_choises():
   
    percents = []
    percents.append(random.randrange(40, 89))
    percents.append(random.randrange(0, 100-percents[0]))
    percents.append(random.randrange(0, 100-percents[0]-percents[1]))
    percents.append(100-(percents[0]+percents[1]+percents[2]))
    if percents[0]+percents[1]+percents[2]+percents[3] != 100:
        print(" AUDIENCE HELP IS BROKEN!!!")
    return percents


def print_phone_conversation(text, question, good_answer):
    
    play_sound("data/sound_files/telhiv.mp3", 0)
    time.sleep(2)
    play_sound("data/sound_files/telefon.mp3", 0)
    then = time.time() 
    print(fg.orange+str(30-int(time.time()-then))+fg.rs)
    time.sleep(2)
    print(''.join(text[0]))
    print("\n"+''.join(question))
    print(fg.orange+str(30-int(time.time()-then))+fg.rs)
    time.sleep(2)
    print(''.join(text[1]))
    print(fg.orange+str(30-int(time.time()-then))+fg.rs)
    time.sleep(2)
    print(fg.red+''.join(text[2])+fg.rs)
    print(fg.orange+str(30-int(time.time()-then))+fg.rs)
    time.sleep(2)
    print(''.join(text[3]))
    if text[2][0] == 'I call the Force for help!':
        print(''.join(text[4]))
        print(good_answer+"\n")
        print(''.join(text[5]))
    else:
        print(''.join(text[4]))
        print(good_answer+"\n")
    print(fg.orange+str(30-int(time.time()-then))+fg.rs)
    now = time.time()
    # play_sound('telefon.mp3', 54.0)
    time.sleep(1)
    print("Call Duration: ", int(now-then), " seconds\\ 30 a")


def telephone_help(question, current_line):
    phone = safe_input("Who'd you like to call?\nfor mum, press 'm'\nfor dad press 'd'\nfor old teacher from high school press 't'\nfor Maester Yoda press 'y': ", ["m", "d", "t", "y"])
    call_list = ['m', 'd', 't', 'y']
    call_files_directory = "./data/phone_help_scenarios/"
    call_text_files = ["mum.txt", "dad.txt", "teacher.txt", "yoda_master.txt"]
    for letter in range(len(call_list)):
        if phone.lower() == call_list[letter]:
            call_text_files[letter] = call_files_directory + call_text_files[letter]
            text = (open_file(call_text_files[letter], 'r'))
            print_phone_conversation(text, question, current_line[0])


def halving(table_line_length, question, shuffled_line, choises, current_line, answers):
    clear_screen(operating_system)
    time.sleep(2)
    play_sound("data/sound_files/felezo.mp3", 0)
    possibilities = []
    for shuffled_element in shuffled_line:
        if shuffled_element == current_line[0]:
            possibilities.append(shuffled_element)
            for index in range(1):
                if shuffled_element == answers[0]:
                    possibilities.append(random.choice([answers[1], answers[2], answers[3]]))
                elif shuffled_element == answers[1]:
                    possibilities.append(random.choice([answers[0], answers[2], answers[3]]))
                elif shuffled_element == answers[2]:
                    possibilities.append(random.choice([answers[0], answers[1], answers[3]]))
                elif shuffled_element == answers[3]:
                    possibilities.append(random.choice([answers[0], answers[1], answers[2]]))
    if answers[0] not in possibilities:
        choises[0].answer =" "*(len(choises[0].answer)-1)+"▕"
    if answers[1] not in possibilities:
        choises[1].answer = " "*(len(choises[1].answer)-1)+"▕"
    if answers[2] not in possibilities:
        choises[2].answer = " "*(len(choises[2].answer)-1)+"▕"
    if answers[3] not in possibilities:
        choises[3].answer = " "*(len(choises[3].answer)-1)+"▕"


def marking(Choise, answer, current_line, answers, choises, table_line_length, shuffled_line, question, Help_available):
    letterses = ['a', 'b', 'c', 'd']
    abcd = [' A: ', ' B: ', ' C: ', ' D: ']
    choise_lengths=[]
    for n in range(4):
            choise_lengths.append(len(shuffled_line[n]))
    choise_lengths=max(choise_lengths)
    for letters_ in range(len(letterses)):
        if answer.lower() == letterses[letters_]:
            answer = answers[letters_]
            choises[letters_] = Choise(abcd[letters_], shuffled_line[letters_], '\x1b[48;2;255;150;50m', '\x1b[39m', '\x1b[49m', '\x1b[30m',choise_lengths)

    return choises, answer


def check_answer(answer, current_line, answers, choises, table_line_length, shuffled_line, question):
    betuk = [' A: ', ' B: ', ' C: ', ' D: ']
    choise_lengths=[]
    for n in range(4):
            choise_lengths.append(len(shuffled_line[n]))
    choise_lengths=max(choise_lengths)
    for pos in range(len(answers)):
        if shuffled_line[pos] == current_line[0]:
            index = shuffled_line.index(shuffled_line[pos])
    if answer == current_line[0]:
        choises[index] = betuk[index], shuffled_line[index], '\x1b[42m', '\x1b[39m', '\x1b[49m', '\x1b[30m',choise_lengths
        fg.green = Style(RgbFg(0, 255, 0))
        time.sleep(2)
        clear_screen(operating_system)
        play_sound("data/sound_files/jo valasz.mp3", 0)
        print(fg.green + "Well done!" + fg.rs)
    else:
        play_sound("data/sound_files/rossz valasz.mp3", 0)
        time.sleep(2)
        fg.red = Style(RgbFg(255, 0, 0))
        print(fg.red+answer+"\nBetter luck next time!"+fg.rs)
        ask = safe_input("Would you like to play again? ('y'/'n')", ['y'])
        if ask == 'y':
            game_start()
            quiz()
        else:
            sys.exit(0)

    return choises


def calculate_quiz_table_size(question_lines, list_of_answers):
    max_question_length = 0
    answer_lengths = []
    for question_ in range(len(question_lines)):
        if len(question_lines[question_][0]) > max_question_length:
            max_question_length = len(question_lines[question_][0])
    for answer in list_of_answers:
        for element in answer:
            if element != answer[0]:
                answer_lengths.append(len(element))
                answer_lengths.sort()
    if answer_lengths[-1]*2 > max_question_length:
        table_line_length = answer_lengths[-1]*2
    else:
        table_line_length = max_question_length

    return table_line_length


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


def pressed_h_key(answer, answers, current_line, question, table_line_length, shuffled_line, choises, Help_available, prices, prices1, prices2, counter):
    if answer.lower() == 'h':
            clear_screen(operating_system)
            print_lists(Help_available, table_line_length, head='vago_helping.txt')
            quiz_table(table_line_length, choises, question, shuffled_line)
            Help_available = help_modules(answers, current_line, question, table_line_length, shuffled_line, choises, Help_available, prices, prices1, prices2, counter)
            Audience = Help_available[0]
            Telephone = Help_available[1]
            Halving = Help_available[2]

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
    clear_screen(operatingSystem)
    for i in range(15):
        question_lines = open_file('questions.txt', "r")
        print(question_lines[i][0])
        answers = {'a': question_lines[i][1], 'b': question_lines[i][2], 'c': question_lines[i][3],
                   'd': question_lines[i][4]}
        answer_list = list(answers.values())
        random.shuffle(answer_list)
        shuffled_answers = dict(zip(answers, answer_list))
        for k in range(len(answer_list)):
            print(list(answers.keys())[k] + ": " + answer_list[k])
        answer = safe_input("\nSelect the correct answer (a,b,c,d)! ", ["a", "b", "c", "d"])
        play_sound("marked.mp3", 0)
        time.sleep(2)
        if answer == get_dictionary_key_by_value(shuffled_answers, question_lines[i][1]):
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
                    clear_screen(operatingSystem)
                    bg.orange = bg(255, 150, 50)
                    print(bg.orange + show_price(i) + bg.rs)
                    time.sleep(2)
            else:
                clear_screen(operatingSystem)
                print(fg.purple + "Congratulations! You have won 40 000 000 Ft!" + fg.rs)
                time.sleep(2)
                sys.exit(0)
        else:
            print(fg.red + "Bad answer! Better luck next time!" + fg.rs)
            if safe_input("Would you like to play again? ('y'/'n')", ['y']) == 'y':
                clear_screen(operatingSystem)
                main()
            else:
                sys.exit(0)
        clear_screen(operatingSystem)

    """
    list_of_answers = open_file('questions.txt', "r")
    starting_range = 0
    ending_range = 4
    letters_ = [" A: ", " B: ", " C: ", " D: "]
    for i in range(15):
        counter = i
        random_question = []
        random_question = random.choice(list_of_answers[starting_range:ending_range])
        question = random_question[0]
        time.sleep(2)
        clear_screen(operating_system)
        current_line = random_question[1:5]
        copy_of_list_of_answers = copy.deepcopy(random_question)
        shuffled_line = copy_of_list_of_answers[1:5]
        random.shuffle(shuffled_line)
        a = shuffled_line[0]
        b = shuffled_line[1]
        c = shuffled_line[2]
        d = shuffled_line[3]
        choise_lengths=[]
        answers = [a, b, c, d]
        choises = [' ', ' ', ' ', ' ']
        for n in range(4):
            choise_lengths.append(len(shuffled_line[n]))
        choise_lengths=max(choise_lengths)
        for letter_ in range(len(letters_)):
            choises[letter_] = letters_[letter_],shuffled_line[letter_],'\x1b[40m','\x1b[39m','\x1b[49m','\x1b[38;2;255;150;50m',choise_lengths
        fg.orange = Style(RgbFg(255, 150, 50))
        table_line_length = calculate_quiz_table_size(question_lines,list_of_answers)
        print_lists(Help_available, table_line_length)
        quiz_table(table_line_length, choises, question, shuffled_line)
        answer = safe_input("\nSelect the correct answer (a,b,c,d) or 'h' for help! ", ["a", "b", "c", "d", "h", "s"])
        pressed_h_key(answer,answers, current_line, question, table_line_length, shuffled_line, choises, Help_available, prices, prices1, prices2, counter)
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


def main():
    clear_screen(operatingSystem)
    #game_start()
    quiz()


if __name__ == "__main__":
    main()
