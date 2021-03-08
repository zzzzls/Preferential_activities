# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import hashlib
import pymysql
from .settings import MYSQL_SETTINGS
from datetime import datetime, date


class XianbaoPipeline:
    def open_spider(self, spider):
        self.date_str = date.today().strftime('%Y-%m-%d')

        # 连接 mysql 数据库
        self.conn = pymysql.connect(
            host=MYSQL_SETTINGS['host'],
            user=MYSQL_SETTINGS['user'],
            password=MYSQL_SETTINGS['password'],
            database=MYSQL_SETTINGS['database'],
            charset=MYSQL_SETTINGS['charset'],
            port=MYSQL_SETTINGS['port']
        )
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        item_lst = list(item.values())
        # 格式化时间
        item_lst[2] = self.date_str + ' ' + item_lst[2]
        item_lst.append(self.md5Encrypt(item_lst[1]))
        if self.query_data(item_lst[-1]):
            self.insert_data(item_lst)
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def query_data(self, url_md5):
        """查询数据是否存在"""
        sql = 'SELECT count(id) FROM news WHERE url_md5 = %s LIMIT 1;'
        self.cur.execute(sql, [url_md5])
        result = self.cur.fetchone()
        if result and len(result) > 0:
            return not bool(result[0])
        else:
            raise ValueError('error：sql数据检测失败！')

    def insert_data(self, item):
        """插入数据"""
        sql = 'INSERT INTO news (title, url, releaseTime, url_md5) values(%s, %s, %s, %s)'
        self.cur.execute(sql, item)
        self.conn.commit()

    def md5Encrypt(self, obj):
        md5 = hashlib.md5()
        md5.update(obj.encode())
        return md5.hexdigest()