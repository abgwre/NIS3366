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
from snownlp import SnowNLP
import pymysql
import time

current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
hot_name = 'test2'
emotion = 0.35
ranking = 1
plat = 'wb'

conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', database='nis', charset='utf8')

cur = conn.cursor()



sql_insert = "insert into hot values ('" + current_time + "','" + hot_name + "'," + str(emotion) + "," + str(ranking) \
             + ",'" + plat + "');"


#print(sql_insert)
sql_select = '''
    SELECT
        name,
        AVG(emotion) AS avg_emotion,
        CONCAT(DATE_FORMAT(time, '%Y-%m-%d'), ' ',
        CASE
            WHEN HOUR(time) BETWEEN 0 AND 2 THEN '0:00-2:59'
            WHEN HOUR(time) BETWEEN 3 AND 5 THEN '3:00-5:59'
            WHEN HOUR(time) BETWEEN 6 AND 8 THEN '6:00-8:59'
            WHEN HOUR(time) BETWEEN 9 AND 11 THEN '9:00-11:59'
            WHEN HOUR(time) BETWEEN 12 AND 14 THEN '12:00-14:59'
            WHEN HOUR(time) BETWEEN 15 AND 17 THEN '15:00-17:59'
            WHEN HOUR(time) BETWEEN 18 AND 20 THEN '18:00-20:59'
            WHEN HOUR(time) BETWEEN 21 AND 23 THEN '21:00-23:59'
        END) AS Time_Range,
        ranking,
        plat
    FROM hot
    GROUP BY name, Time_Range, ranking, plat
    ORDER BY ranking;'''
#print(sql_select)
'''i = cur.execute(sql_insert)
print(i)

conn.commit()'''

row_count = cur.execute(sql_select)
# 获取所有数据
for line in cur.fetchall():
    print(line)

'''
text = "3216146"
s = SnowNLP(text)
print(s.sentiments)

'''

conn.close()
