import json


def export_csv_to_json(topic, difficulty, id):

    file_path = "../../data/text_files/topics/english/"+topic+"/" + difficulty + "/" + difficulty + ".txt"
    with open(file_path, "r", encoding="UTF-8") as file:
        list_of_file = []
        for line in file:
            line = line.split(";")
            list_of_file.append(line)

    dictList = []
    for line in list_of_file:
        id+= 1
        if "\n" in line[4]:
            line[4] = line[4][:-1]
        mydict = {"value": line[0], "answers": [line[1], line[2], line[3], line[4]], "correct_answer": line[1], "difficulty": difficulty, "topic": topic, "id": id}
        dictList.append(mydict)

    with open("json_log.json", 'a') as fout:
        json.dump(dictList, fout, indent=4)


export_csv_to_json("biology", "hard" , 170)

