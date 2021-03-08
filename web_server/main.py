import pymysql
from flask import Flask, g, make_response, jsonify

app = Flask(__name__)

MYSQL_SETTINGS = {
    'host': '81.70.46.54',
    'user': 'root',
    'password': 'root',
    'database': 'flaskDemo',
    'charset': 'utf8',
    'port': 3306
}


@app.before_request
def first_request():
    # 连接数据库
    conn = pymysql.connect(
        host=MYSQL_SETTINGS['host'],
        user=MYSQL_SETTINGS['user'],
        password=MYSQL_SETTINGS['password'],
        database=MYSQL_SETTINGS['database'],
        charset=MYSQL_SETTINGS['charset'],
        port=MYSQL_SETTINGS['port']
    )
    cur = conn.cursor()
    g.conn = conn
    g.cur = cur


@app.after_request
def after_request(environ):
    # 断开数据库连接
    g.cur.close()
    g.conn.close()
    return environ


@app.route('/query_new_data')
def get_news():
    data = query_data_from_mysql(g.cur)
    if data and len(data) > 0:
        result = {'codes': 200, "data": data}
    else:
        result = {'codes': 500, "data": []}

    response = make_response(jsonify(result))
    # 设置响应请求头
    response.headers["Access-Control-Allow-Origin"] = '*'  # 允许使用响应数据的域。也可以利用请求header中的host字段做一个过滤器。
    response.headers["Access-Control-Allow-Methods"] = 'POST'  # 允许的请求方法
    response.headers["Access-Control-Allow-Headers"] = "x-requested-with,content-type"  # 允许的请求header

    return response


def query_data_from_mysql(cur):
    sql = 'SELECT title,url,releaseTime FROM news ORDER BY releaseTime DESC limit 40'
    cur.execute(sql)
    result = cur.fetchall()
    new_result = []
    for item in list(result):
        title = item[0][:37] + '...' if len(item[0]) > 39 else item[0]
        releaseTime = item[2].strftime('%H:%M')
        new_result.append([title, item[1], releaseTime])
    return new_result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
