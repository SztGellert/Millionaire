import json


def export_csv_to_json(topic, difficulty, id):
    file_path = "../../data/text_files/topics/english/" + topic + "/" + difficulty + "/" + difficulty + ".txt"
    with open(file_path, "r", encoding="UTF-8") as file:
        list_of_file = []
        for line in file:
            line = line.split(";")
            list_of_file.append(line)

    dictList = []
    for line in list_of_file:
        id += 1
        if len(line) != 5:
            print(line)
        if "\n" in line[4]:
            line[4] = line[4][:-1]
        mydict = {"value": line[0], "answers": [line[1], line[2], line[3], line[4]], "correct_answer": line[1],
                  "difficulty": difficulty, "topic": topic, "id": id}
        dictList.append(mydict)

    with open(topic + "_" + difficulty + ".json", 'a') as fout:
        json.dump(dictList, fout, indent=4)


def transform_json_schema():
    new_schema = []

    with open('quiz.questions.json', "r", encoding="UTF-8") as f:
        en = json.load(f)

        for line in en:
            new_schema.append(
                {"id": line['id'], "en": {"text": line['value'], "answers": line['answers'], "correct_answer_index": 0}})
        f.close()

    with open('quiz.questions.de.json', "r", encoding="UTF-8") as f:
        de = json.load(f)
        i = 0
        for line in de:
            print(line['en']['text'])
            new_schema[i]["de"] = {"text": line['en']['text'], "answers": line['en']['answers'], "correct_answer_index": 0}
            i+=1

        f.close()

    with open('quiz.questions.hun.json', "r", encoding="UTF-8") as f:
        hun = json.load(f)
        i = 0

        for line in hun:
            new_schema[i]["hu"] = {"text": line['en']['text'], "answers": line['en']['answers'],
                                   "correct_answer_index": 0}
            i += 1

        f.close()

    with open('quiz.questions.json', "r", encoding="UTF-8") as f:
        en = json.load(f)
        i = 0
        for line in en:
            new_schema[i]["difficulty"] = line['difficulty']
            new_schema[i]["topic"] = line['topic']
            i+=1
        f.close()

    with open("quiz.questions(2).json", 'a') as fout:
        json.dump(new_schema, fout, indent=4)


transform_json_schema()
