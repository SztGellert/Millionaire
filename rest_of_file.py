"""     vago_feje_sorai = open_drawing(head, 'r')
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
    n = 0
    print((80*" ")+bg.black+(len(prices[-1])+2)*"-".rstrip() + bg.rs)
    print((80*" ")+bg.black+"|"+" "+Halv+"∥"+Tel+"∥"+Aud+(len(prices[-1])-(len(Halv)+len(Tel)+len(Aud)+4))*" "+bg.black+"|"+bg.rs)
    print((80*" ")+bg.black+(len(prices[-1])+2)*"-"+bg.rs)
    print((80*" ")+bg.black+(len(prices[-1])+2)*"-"+bg.rs)
    for head_lines in range(15):
        bg.orange = bg(255, 150, 50)
        spaces_ = (len(prices1[0])-len(prices1[head_lines]))*" "
        if prices2[head_lines] == prices2[0]:
            prices2[0] = bg.black+fg.white+prices1[0]
        if counter == 14:
            prices2[0] = bg.orange+fg.black+prices1[0]
        if prices2[head_lines] == prices2[counter]:
            prices2[14-counter] = bg.orange+fg.black+prices1[14-counter]
            if counter >= 1:
                prices2[14-counter+1] = bg.black+fg.orange+prices1[14-counter+1]
            for n in range(counter+1, 15):
                if n in [5, 10, 14]:
                    prices2[n] = bg.black+fg.white+prices2[n]
                prices2[n] = bg.black+fg.orange+prices2[n]                
        print(''.join(vago_feje_sorai[head_lines]).strip('\n')+bg.black+"|"+fg.rs+bg.rs+prices2[head_lines]+spaces_+fg.white+bg.black+"|"+bg.rs+fg.rs)
    print(''.join(vago_feje_sorai[15]).rstrip()+31*" "+bg.black+(len(prices[:-1])+1)*"-"+bg.rs)
    for art in range(16, 20):
        print(''.join(vago_feje_sorai[art]).rstrip())
def audience_help(answers, current_line, question, table_line_length, choises, shuffled_line):
    
    play_sound("./sound_files/kozonseg.mp3", 0)
    for choise in [answers]:
        if choise == current_line[0]:
            if choise == a:
                a_percent = random.randrange(40, 89)
                b_percent = random.randrange(0, (100-a_percent))
                c_percent = random.randrange(0, (100-a_percent-b_percent))
                d_percent = 100-(a_percent+b_percent+c_percent)
            if choise == b:
                b_percent = random.randrange(40, 89)
                a_percent = random.randrange(0, (100-b_percent))
                c_percent = random.randrange(0, (100-b_percent-a_percent))
                d_percent = 100-(a_percent+b_percent+c_percent)
            if choise == c:
                c_percent = random.randrange(40, 89)
                b_percent = random.randrange(0, (100-c_percent))
                a_percent = random.randrange(0, (100-c_percent-b_percent))
                d_percent = 100-(a_percent+b_percent+c_percent)
            if choise == d:
                d_percent = random.randrange(40, 89)
                b_percent = random.randrange(0, (100-d_percent))
                c_percent = random.randrange(0, (100-d_percent-b_percent))
                a_percent = 100-(d_percent+b_percent+c_percent)
            time.sleep(4)
            os.system('cls')
            for choise_ in [answers]:
                if choise == current_line[0]:
                    if choise_ == a:
                        fake_a_percent = random.randrange(40, 89)
                        fake_b_percent = random.randrange(0, (100 - fake_a_percent))
                        fake_c_percent = random.randrange(0, (100 - fake_a_percent-fake_b_percent))
                        fake_d_percent = 100-(fake_a_percent + fake_b_percent + fake_c_percent)
                    if choise_ == b:
                        fake_b_percent = random.randrange(40, 89)
                        fake_a_percent = random.randrange(0, (100 - fake_b_percent))
                        fake_c_percent = random.randrange(0, (100 - fake_b_percent-fake_a_percent))
                        fake_d_percent = 100 - (fake_a_percent+fake_b_percent + fake_c_percent)
                    if choise_ == c:
                        fake_c_percent = random.randrange(40, 89)
                        fake_b_percent = random.randrange(0, (100-fake_c_percent))
                        fake_a_percent = random.randrange(0, (100-fake_c_percent-fake_b_percent))
                        fake_d_percent = 100-(fake_a_percent+fake_b_percent+fake_c_percent)
                    if choise_ == d:
                        fake_d_percent = random.randrange(40, 89)
                        fake_b_percent = random.randrange(0, (100-fake_d_percent))
                        fake_c_percent = random.randrange(0, (100-fake_d_percent-fake_b_percent))
                        fake_a_percent = 100-(fake_d_percent+fake_b_percent+fake_c_percent)
                    if fake_a_percent+fake_b_percent+fake_c_percent+fake_d_percent != 100:
                        print("Sheibe")
                print("A:"+bg.blue+fake_a_percent*" "+" "+str(fake_a_percent)+"%"+"\n"+bg.rs+"B:"+bg.blue+fake_b_percent*" "+" "+str(fake_b_percent)+"%"+"\n"+bg.rs+"C:"+bg.blue+fake_c_percent*" "+" "+str(fake_c_percent)+"%"+"\n"+bg.rs+"D:"+bg.blue+fake_d_percent*" "+" "+str(fake_d_percent)+"%"+"\n"+bg.rs)
                time.sleep(4)
                os.system('cls')
                sys.stdout.write("\033[F")
            elems = [a_percent, b_percent, c_percent, d_percent]
            max_element = max(elems[0], elems[1], elems[2], elems[3])
            a__ = (f'{(table_line_length+1)*" "+bg.black+"|"+fg.orange}  A: {bg.rs+bg.blue+a_percent*" "+bg.black+fg.rs+str(a_percent)}%')
            b__ = (f'{(table_line_length+1)*" "+bg.black+"|"+fg.orange}  B: {bg.rs+bg.blue+b_percent*" "+bg.black+fg.rs+str(b_percent)}%')
            c__ = (f'{(table_line_length+1)*" "+bg.black+"|"+fg.orange}  C: {bg.rs+bg.blue+c_percent*" "+bg.black+fg.rs+str(c_percent)}%')
            d__ = (f'{(table_line_length+1)*" "+bg.black+"|"+fg.orange}  D: {bg.rs+bg.blue+d_percent*" "+bg.black+fg.rs+str(d_percent)}%')
            print((table_line_length+1)*" " + bg.black + (max_element+11)*"-" + bg.rs)
            print(a__+(((max_element)-a_percent)+3)*" "+"|"+bg.rs)
            time.sleep(1)
            print(b__+(((max_element)-b_percent)+2)*" "+"|"+bg.rs)
            time.sleep(1)
            print(c__+(((max_element)-c_percent)+2)*" "+"|"+bg.rs)
            time.sleep(1)
            print(d__+(((max_element)-d_percent)+3)*" "+"|"+bg.rs)
            print((table_line_length+1)*" "+bg.black+(max_element+11)*"-" + bg.rs)
"""     """ print(answers)
    play_sound("./sound_files/jo valasz.mp3", 0)
    fg.green = Style(RgbFg(0, 255, 0))
    print(fg.green + "Well done!" + fg.rs)
    time.sleep(2)
    os.system('cls')
    else:
        print(answer)
        print()
        print(current_line[0])
        print(answers)
        play_sound("./sound_files/rossz valasz.mp3", 0)
        time.sleep(2)
        fg.red = Style(RgbFg(255, 0, 0))
        print(fg.red+answer+"\nBetter luck next time!"+fg.rs)
        sys.exit(0) """ """
   
    if answer == answers[0]:
        if answers[0] == current_line[0]:
            choises[0] = bg.green + fg.orange + '◆ A: ' + fg.rs + ''.join(answers[0]) + "  " + bg.black
        else:
            choises[0] = bg.red + fg.orange + '◆ A: ' + fg.rs + ''.join(answers[0]) + "  " + bg.black
    if answer == answers[1]:
        if answers[1] == current_line[0]:
            choises[1] = bg.green + fg.orange + '◆ B: ' + fg.rs + ''.join(answers[1]) + "  " + bg.black
        else:
            choises[1] = bg.red + fg.orange + '◆ B: ' + fg.rs + ''.join(answers[1]) + "  " + bg.black
    if answer == answers[2]:
        if answers[2] == current_line[0]:
            choises[2] = bg.green + fg.orange + '◆ C: ' + fg.rs + ''.join(answers[2]) + "  " + bg.black
        else:
            choises[2] = bg.red + fg.orange + '◆ C: ' + fg.rs + ''.join(answers[2]) + "  " + bg.black
    if answer == answers[3]:
        if answers[3] == current_line[0]:
            choises[3] = bg.green + fg.orange + '◆ D: ' + fg.rs + ''.join(answers[3]) + "  " + bg.black
        else:
            choises[3] = bg.red + fg.orange + '◆ D: ' + fg.rs + ''.join(answers[3]) + "  " + bg.black
    if answer != current_line[0]:
        for pos in [answers]:
            if pos == current_line[0]:
                if pos == answers[0]:
                    choises[0] = bg.green + choises[0] + "  " + bg.black
                if pos == answers[1]:
                    choises[1] = bg.green + choises[1] + "  " + bg.black
                if pos == answers[2]:
                    choises[2] = bg.green + choises[2] + "  " + bg.black
                if pos == answers[3]:
                    choises[3] = bg.green + choises[3] + "  " + bg.black
    time.sleep(1)
    os.system('cls')
    if answer == current_line[0]:
        play_sound("./sound_files/jo valasz.mp3", 0)
        fg.green = Style(RgbFg(0, 255, 0))
        print(fg.green + "Well done!" + fg.rs)
        time.sleep(2)
        os.system('cls')
    else:
        play_sound("./sound_files/rossz valasz.mp3", 0)
        time.sleep(2)
        fg.red = Style(RgbFg(255, 0, 0))
        print(fg.red+answer+"\nBetter luck next time!"+fg.rs)
        sys.exit(0)
        

                print("A:"+bg.blue+fake_a_percent*" "+" "+str(fake_a_percent)+"%"+"\n"+bg.rs+"B:"+bg.blue+fake_b_percent*" "+" "+str(fake_b_percent)+"%"+"\n"+bg.rs+"C:"+bg.blue+fake_c_percent*" "+" "+str(fake_c_percent)+"%"+"\n"+bg.rs+"D:"+bg.blue+fake_d_percent*" "+" "+str(fake_d_percent)+"%"+"\n"+bg.rs)
                time.sleep(4)
                os.system('cls')
                sys.stdout.write("\033[F")
            elems = [a_percent, b_percent, c_percent, d_percent]
            max_element = max(elems[0], elems[1], elems[2], elems[3])
            a__ = (f'{(table_line_length+1)*" "+bg.black+"|"+fg.orange}  A: {bg.rs+bg.blue+a_percent*" "+bg.black+fg.rs+str(a_percent)}%')
            b__ = (f'{(table_line_length+1)*" "+bg.black+"|"+fg.orange}  B: {bg.rs+bg.blue+b_percent*" "+bg.black+fg.rs+str(b_percent)}%')
            c__ = (f'{(table_line_length+1)*" "+bg.black+"|"+fg.orange}  C: {bg.rs+bg.blue+c_percent*" "+bg.black+fg.rs+str(c_percent)}%')
            d__ = (f'{(table_line_length+1)*" "+bg.black+"|"+fg.orange}  D: {bg.rs+bg.blue+d_percent*" "+bg.black+fg.rs+str(d_percent)}%')
            print((table_line_length+1)*" " + bg.black + (max_element+11)*"-" + bg.rs)
            print(a__+(((max_element)-a_percent)+3)*" "+"|"+bg.rs)
            time.sleep(1)
            print(b__+(((max_element)-b_percent)+2)*" "+"|"+bg.rs)
            time.sleep(1)
            print(c__+(((max_element)-c_percent)+2)*" "+"|"+bg.rs)
            time.sleep(1)
            print(d__+(((max_element)-d_percent)+3)*" "+"|"+bg.rs)
            print((table_line_length+1)*" "+bg.black+(max_element+11)*"-" + bg.rs)

                                                                                                     ▏40.000.000 Ft▕
                                  ##||łłłłłł|ł|||łłłłłł||##                                  ▏20.000.000 Ft▕
                                  łłłłł o   łłłłłłł o   łłłłł                                ▏10.000.000 Ft▕
                                  #|||łłłłłł|łł||łłłłłł|||#                                  ▏5.000.000 Ft ▕
                                  |||||||||||łłłł||||||||||                                  ▏3.000.000 Ft ▕
                                  |||||||||||||||||||||||||                                  ▏1.500.000 Ft ▕
                                    ||||||##########|||||                                    ▏800.000 Ft   ▕
                                      |||##        ##|||                                     ▏500.000 Ft   ▕
                                       ||||########||||                                      ▏300.000 Ft   ▕
                                        |||||####||||                                        ▏             ▕
                                          ||||||||||                                         ▏             ▕
                                           |||||||                                           ▏             ▕
                                         XXłłłłłłłXXX                                        ▏             ▕
                                      XX###  ł   #####XX                                     ▏             ▕
                                   XX####    łł    ######XX                                  ▏             ▕
                                                                                             ▏A ◆ B ◆ C ◆ D▕

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
    index=12
    
    percents=give_audience_choises()
    good_percents=[' ',' ',' ',' ']
    for i in range(len(shuffled_line)):
        if shuffled_line[i] == current_line[0]:
            good_percents[i] = percents[0]
            del percents[0]
        else:
            a=random.choice(percents)
            good_percents[i]=a
            index=percents.index(a)
            del percents[index]
    rounds=[]
    var=1

    for percent in good_percents:
        if percent < 10:
            percent=10
        rounds.append(percent//10)
    for percentage in rounds:
        for f in range(0,percentage):
            audience[(index-f)][var]=fg.blue+"X"+fg.rs
                        
        var+=3
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
            break                                            """      