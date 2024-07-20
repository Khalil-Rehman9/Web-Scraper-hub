# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime

import mysql.connector
from .items import LeagueItem

class LeaguePipeline:
    def __int__(self):
        pass

    def create_connection(self):
        pass

    def process_item(self, item, spider):
        self.store_to_db(item)
        return item

    def store_to_db(self, item):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='webixhub',
            password='9TNg6ICfEKWOowh7',
            database='webixhub'
        )
        # self.conn = mysql.connector.connect(
        #     host='localhost',
        #     user='root',
        #     password='q1122',
        #     database='webixhub'
        # )
        now = datetime.now()
        self.curr = self.conn.cursor()
        self.curr.execute("""INSERT INTO sports_footballleague
                                (`name`,
                                `season`,
                                `league_id`,
                                `league_img`,
                                `league_standing`,
                                `created_at`,
                                `updated_at`)
                             VALUES (%s,%s,%s,%s,%s,%s,%s)""", (
            item['league_name'],
            item['season'],
            item['league_id'],
            item['league_img'],
            item['league_standings'],
            now.strftime('%Y-%m-%d %H:%M:%S'),
            now.strftime('%Y-%m-%d %H:%M:%S')
        )
                          )
        self.conn.commit()