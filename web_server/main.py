import pymysql
from flask import Flask, g, make_response, jsonify, request, redirect

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


def customize_response_cros(data):
    """定制跨域响应体"""
    response = make_response(jsonify(data))
    # 设置响应请求头
    response.headers["Access-Control-Allow-Origin"] = '*'  # 允许使用响应数据的域。也可以利用请求header中的host字段做一个过滤器。
    response.headers["Access-Control-Allow-Methods"] = 'POST'  # 允许的请求方法
    response.headers["Access-Control-Allow-Headers"] = "x-requested-with,content-type"  # 允许的请求header

    return response


@app.route('/query_data')
def get_news():
    args = request.args
    kw = args.get('kw', '').strip()
    # 检测用户是否有输入内容
    if kw == '':
        data = query_data_from_mysql(g.cur)
    else:
        data = query_data_from_mysql(g.cur, search_key=kw, time_fmt='%m-%d %H:%M')
    if data and len(data) > 0:
        result = {'codes': 200, "data": data}
    else:
        result = {'codes': 500, "data": []}

    return customize_response_cros(result)


def query_data_from_mysql(cur, search_key=None, limit=30, time_fmt='%H:%M'):
    if not search_key:
        sql = f'SELECT title,url,releaseTime FROM news ORDER BY releaseTime DESC limit {limit}'
    else:
        sql = f'SELECT title,url,releaseTime FROM news where LOCATE("{search_key}", title)>0 ORDER BY releaseTime DESC limit {limit}'
    cur.execute(sql)
    result = cur.fetchall()
    new_result = []
    for item in list(result):
        title = item[0][:37] + '...' if len(item[0]) > 39 else item[0]
        releaseTime = item[2].strftime(time_fmt)
        new_result.append([title, item[1], releaseTime])
    return new_result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
