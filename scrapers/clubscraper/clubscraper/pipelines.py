# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from datetime import datetime

class ClubscraperPipeline:
    def __int__(self):
        pass

    def create_connection(self):
        pass

    def process_item(self, item, spider):
        self.store_match_to_db(item)
        return item

    def store_match_to_db(self,item):
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
        self.curr.execute("""INSERT INTO sports_footballteam
                                (`bold_team_id`,
                                `name`,
                                `img`,
                                `team_info`,
                                `results`,
                                `fixtures`,
                                `players`,
                                `created_at`)
                             VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(
                                item['bold_team_id'],
                                item['name'],
                                item['img'],
                                item['team_info'],
                                item['results'],
                                item['fixtures'],
                                item['players'],
                                now.strftime('%Y-%m-%d %H:%M:%S')
                            )
                          )
        self.conn.commit()