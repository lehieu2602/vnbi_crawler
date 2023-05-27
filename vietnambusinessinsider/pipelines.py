# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector
from dateutil.parser import parse


class VietnambusinessinsiderPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="vnbinsider",
        )
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""DROP TABLE IF EXISTS post""")
        self.cur.execute("""
        CREATE TABLE post(
        ID INT NOT NULL PRIMARY KEY,
        author varchar(50),
        author_url varchar(150),
        title varchar(200),
        date_post DATE,
        time_post TIME,
        link varchar(150)
        )
        """)

    def process_item(self, item, spider):
        self.cur.execute(
            """INSERT INTO post (ID, author, author_url, title, date_post, time_post, link) VALUES (%s,%s,%s,%s,%s,%s,%s)""",
            (int(item['ID']), str(item['author']), str(item['author_url']), str(item['title']),
             parse(item['date_post']).date(), parse(item['time_post']).time(), item['link']))
        self.conn.commit()
        return item
