from snownlp import SnowNLP
import csv
import info

def output(filepath):
    f = open(filepath, 'r', encoding='utf-8')
    r = csv.reader(f)
    count = 0
    emotion = 0
    for item in r:
        if r.line_num == 1:
            continue
        text = item[13]
        #print(text)
        if text != '':
            s = SnowNLP(text)
            emotion += float(s.sentiments)
            count += 1

    if count == 0:
        return 1

    return emotion/count

def read(filepath, time):
    dataset_list = []
    f = open(filepath, 'r', encoding='utf-8')
    r = csv.reader(f)
    ranking = 1
    for item in r:
        if r.line_num == 1:
            continue
        dataset_list.append(item)
        path = item[2] + '.csv'
        emotion = output(path)
        info.insert_info(item[2], emotion, ranking, item[0])
        ranking += 1


#print(output('调休.csv'))
#output('调休.csv')
read('热搜2024-04-07 13_59_33.csv')
#print(output('test.csv'))