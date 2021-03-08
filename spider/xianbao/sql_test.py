import pymysql

import sys
sys.path.append(r'E:\项目\xianbao')


from xianbao.settings import MYSQL_SETTINGS

conn = pymysql.connect(
            host=MYSQL_SETTINGS['host'],
            user=MYSQL_SETTINGS['user'],
            password=MYSQL_SETTINGS['password'],
            database=MYSQL_SETTINGS['database'],
            charset=MYSQL_SETTINGS['charset'],
            port=MYSQL_SETTINGS['port'],
        )
cur = conn.cursor()

item = ['http://www.0818tuan.com/xbhd/9562481.html',
        'e164732fd136a706791319daa9f61302',
        '不咋用买单吧，刚看了下23万积分。咋用',
        '2021-03-07 21:57']

sql = 'select * from news order by releaseTime desc limit 40'
cur.execute(sql)
result = cur.fetchall()
print(result)

cur.close()
conn.close()