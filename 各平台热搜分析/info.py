'''
time name emotion rank plat
create table hot(
    time char(40),
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

    conn = pymysql.connect(host='172.29.25.151', port=3307, user='root', password='123456', database='nis', charset='utf8')

    cur = conn.cursor()

    sql_exist = "SELECT EXISTS(SELECT * FROM hot WHERE name = %s AND time = %s);"
    sql_del = "DELETE FROM hot WHERE name = %s AND time = %s"

    value0 = (hot_name, current_time)

    if cur.execute(sql_exist, value0):                                  #更新数据
        cur.execute(sql_del, value0)
        conn.commit()

    sql_insert = "INSERT INTO hot values (%s, %s, %s, %s, %s);"

    value = (current_time, hot_name, str(emotion), str(ranking), plat)

    i = cur.execute(sql_insert, value)
    print(i)

    conn.commit()

    conn.close()

def read_certain_info(hot_name, plat):                                  #获取指定平台指定热搜在数据库中的信息
    conn = pymysql.connect(host='172.29.25.151', port=3307, user='root', password='123456', database='nis', charset='utf8')

    cur = conn.cursor()

    sql_select = '''
        SELECT
            name,
            AVG(emotion) AS avg_emotion,
            time,
            ranking,
            plat
        FROM hot 
        WHERE name = %s AND plat = %s
        GROUP BY name, time, ranking, plat
        ORDER BY time;'''
    #print(sql_select)

    value = (hot_name, plat)

    row_count = cur.execute(sql_select, value)

    fetch = cur.fetchall()

    conn.close()

    return fetch


    # 获取所有数据用法
    #for line in fetch():        line即为元组
    #    print(line)


def read_hot_now(plat):                                                 #获取当前时段热搜信息
    conn = pymysql.connect(host='172.29.25.151', port=3307, user='root', password='123456', database='nis', charset='utf8')

    cur = conn.cursor()

    current_time = get_current_time()

    sql_select = '''
        SELECT
            name,
            AVG(emotion) AS avg_emotion,
            time,
            ranking,
            plat
        FROM hot
        WHERE time = %s AND plat = %s 
        GROUP BY name, time, ranking, plat
        ORDER BY ranking;'''
    # print(sql_select)

    value = (current_time, plat)

    row_count = cur.execute(sql_select, value)

    fetch = cur.fetchall()

    conn.close()

    return fetch


def select_hot_name(hot_name, plat):                                    #模糊查询
    conn = pymysql.connect(host='172.29.25.151', port=3307, user='root', password='123456', database='nis', charset='utf8')

    cur = conn.cursor()

    sql_select = '''
        SELECT
            name,
            AVG(emotion) AS avg_emotion,
            time,
            ranking,
            plat
        FROM hot 
        WHERE name LIKE %s AND plat = %s
        GROUP BY name, time, ranking, plat
        ORDER BY time;'''
    # print(sql_select)

    hot_name = "%" + hot_name + "%"

    value = (hot_name, plat)

    row_count = cur.execute(sql_select, value)

    fetch = cur.fetchall()

    conn.close()

    return fetch
