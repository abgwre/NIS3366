'''
time name emotion rank plat
create table hot(
    time datetime,
    name char(30),
    emotion float(6,4),
    ranking int(2),
    plat char(10)
);
'''

import pymysql
import time

def get_current_time():
    current_time = time.strftime('%Y-%m-%d', time.localtime())
    hr = time.strftime('%H', time.localtime())

    if 0 <= int(hr) < 3:
        current_time = current_time + " " + '0:00-2:59'
    elif 3 <= int(hr) < 6:
        current_time = current_time + " " + '3:00-5:59'
    elif 6 <= int(hr) < 9:
        current_time = current_time + " " + '6:00-8:59'
    elif 9 <= int(hr) < 12:
        current_time = current_time + " " + '9:00-11:59'
    elif 12 <= int(hr) < 15:
        current_time = current_time + " " + '12:00-14:59'
    elif 15 <= int(hr) < 18:
        current_time = current_time + " " + '15:00-17:59'
    elif 18 <= int(hr) < 21:
        current_time = current_time + " " + '18:00-20:59'
    elif 21 <= int(hr) < 24:
        current_time = current_time + " " + '21:00-23:59'

    return current_time

def insert_info(hot_name, emotion, ranking, plat):                      #分析结果输入数据库
    current_time = get_current_time()
    '''hot_name = 'test2'
    emotion = 0.35
    ranking = 1
    plat = 'wb'
    '''

    conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', database='nis', charset='utf8')

    cur = conn.cursor()

    sql_insert = "insert into hot values ('" + current_time + "','" + hot_name + "'," + str(emotion) + "," + str(ranking) \
                 + ",'" + plat + "');"

    i = cur.execute(sql_insert)
    print(i)

    conn.commit()

    conn.close()

def read_certain_info(hot_name, plat):                                  #获取指定平台指定热搜在数据库中的信息
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', database='nis', charset='utf8')

    cur = conn.cursor()

    sql_select = '''
        SELECT
            name,
            AVG(emotion) AS avg_emotion,
            time,
            ranking,
            plat
        FROM hot ''' + \
        "WHERE name = '" + hot_name + "' AND plat = '" + plat + "' "\
        '''GROUP BY name, time, ranking, plat
        ORDER BY time;'''
    #print(sql_select)

    row_count = cur.execute(sql_select)

    fetch = cur.fetchall()

    conn.close()

    for line in fetch:
        print(line)

    return fetch


    # 获取所有数据用法
    #for line in fetch():        line即为元组
    #    print(line)


def read_hot_now(plat):                                                 #获取当前时段热搜信息
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', database='nis', charset='utf8')

    cur = conn.cursor()

    current_time = get_current_time()

    sql_select = '''
            SELECT
                name,
                AVG(emotion) AS avg_emotion,
                time,
                ranking,
                plat
            FROM hot ''' + \
            "WHERE time = '" + current_time + "' AND plat = '" + plat + "' "\
            '''GROUP BY name, time, ranking, plat
            ORDER BY time;'''
    # print(sql_select)

    row_count = cur.execute(sql_select)

    fetch = cur.fetchall()

    conn.close()

    for line in fetch:
        print(line)

    return fetch
