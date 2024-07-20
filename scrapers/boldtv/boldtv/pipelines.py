# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime

from itemadapter import ItemAdapter
import mysql.connector

from .items import BoldtvItem


class BoldtvPipeline:

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
        self.curr.execute("""INSERT INTO sports_footballmatch
                                (`source_id`,
                                # `match_date`,
                                # `match_time`,
                                `match_unique_id`,
                                `bolddk_match_id`,
                                `match_url`,
                                `home_team`,
                                `away_team`,
                                `game`,
                                `league`,
                                `league_img`,
                                `channel_title`,
                                `channel_img`,
                                # `parsed_match_date_time`,
                                `created_at`)
                             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(
                                1,
                                # item['match_date'],
                                # item['match_time'],
                                item['match_unique_id'],
                                item['bolddk_match_id'],
                                item['match_url'],
                                item['home_team'],
                                item['away_team'],
                                item['game'],
                                item['league'],
                                item['league_flag_img_url'],
                                item['channel_title'],
                                item['channel_img_url'],
                                # item['parsed_match_date_time'],
                                now.strftime('%Y-%m-%d %H:%M:%S')
                            )
                          )
        self.conn.commit()

    def store_team_to_db(self,item):
        # self.conn = mysql.connector.connect(
        #     host='localhost',
        #     user='webixhub',
        #     password='9TNg6ICfEKWOowh7',
        #     database='webixhub'
        # )
        # self.conn = mysql.connector.connect(
        #     host='localhost',
        #     user='root',
        #     password='q1122',
        #     database='hub.webixaps'
        # )
        # now = datetime.now()
        # self.curr = self.conn.cursor()
        # self.curr.execute("""INSERT INTO sports_footballteam
        #                         (`team_unique_id`,
        #                         `name`,
        #                         `img`,
        #                         `team_info`,
        #                         `created_at`)
        #                      VALUES (%s,%s,%s,%s,%s)""",(
        #                         item['team_unique_id'],
        #                         item['name'],
        #                         item['img'],
        #                         item['team_info'],
        #                         now.strftime('%Y-%m-%d %H:%M:%S')
        #                     )
        #                   )
        # self.conn.commit()
        pass

    def store_league_to_db(self,item):
        # self.conn = mysql.connector.connect(
        #     host='localhost',
        #     user='webixhub',
        #     password='9TNg6ICfEKWOowh7',
        #     database='webixhub'
        # )
        # self.conn = mysql.connector.connect(
        #     host='localhost',
        #     user='root',
        #     password='q1122',
        #     database='hub.webixaps'
        # )
        # now = datetime.now()
        # self.curr = self.conn.cursor()
        # self.curr.execute("""INSERT INTO sports_footballleague
        #                         (`league_id`,
        #                         `name`,
        #                         `league_standing`,
        #                         `league_history`,
        #                         `created_at`)
        #                      VALUES (%s,%s,%s,%s,%s)""",(
        #                         item['league_id'],
        #                         item['name'],
        #                         item['league_standing'],
        #                         item['league_history'],
        #                         now.strftime('%Y-%m-%d %H:%M:%S')
        #                     )
        #                   )
        # self.conn.commit()
        pass
