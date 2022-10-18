def file_opening(filename, mode):
    with open(filename, mode) as file:
            list_of_file = []
            for line in file:
                line = line.strip().split(',')
                list_of_file.append(line)
    return list_of_file

text=file_opening("data/text_files/yoda_master_phone.txt", 'r')
if text[2][0] == 'I call the Force for help!':
    print(''.join(text[0]))
    print(good_answer+"\n")
    print(''.join(text[5]))
print(text[2])
