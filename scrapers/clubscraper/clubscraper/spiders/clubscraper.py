import json
from datetime import datetime

import scrapy
# from ..items import BoldtvItem
import hashlib

from ..items import ClubscraperItem
import mysql.connector
import os.path


class ClubscraperSpider(scrapy.Spider):
    name = 'clubscraper'
    allowed_domains = ['www.bold.dk', 'amazonaws.com']

    def start_requests(self):
        conn = mysql.connector.connect(
            host='localhost',
            user='webixhub',
            password='9TNg6ICfEKWOowh7',
            database='webixhub'
        )
        # conn = mysql.connector.connect(
        #     host='localhost',
        #     user='root',
        #     password='q1122',
        #     database='webixhub'
        # )
        cursor = conn.cursor()
        cursor.execute('''
SELECT home_team_id
    FROM sports_footballmatch
    LEFT JOIN sports_footballteam on sports_footballteam.bold_team_id = home_team_id
WHERE sports_footballteam.id IS NULL
UNION
SELECT away_team_id
    FROM sports_footballmatch
    LEFT JOIN sports_footballteam on sports_footballteam.bold_team_id = away_team_id
WHERE sports_footballteam.id IS NULL
LIMIT 50;
                        ''')
        rows = cursor.fetchall()
        for row in rows:
            url = 'https://bold.dk/fodbold/klubber/' + row[0]
            yield scrapy.Request(url=url)

    def parse(self, response):
        item = ClubscraperItem()
        img = response.css('.logo-bg img ::attr(src)').extract_first()
        item['bold_team_id'] = response.url.split('/')[-1]
        name = response.css('.name ::text').extract_first()
        club_img_id = img.strip().split('/')[-1] if img else None
        club_img_name = name+'.png'
        item['name'] = name.strip() if name else None
        item['img'] = club_img_name
        # club  info
        place = response.css('.place').xpath('text()').extract_first()
        stadium = response.xpath(
            '//*[@id="__layout"]/div/section[1]/div/div[4]/div/div[1]/div[1]/div/div/ul/li[2]/text()').extract_first()
        capacity = response.xpath(
            '//*[@id="__layout"]/div/section[1]/div/div[4]/div/div[1]/div[1]/div/div/ul/li[3]/span/text()').extract_first()
        coach = response.xpath(
            '//*[@id="__layout"]/div/section[1]/div/div[4]/div/div[1]/div[1]/div/div/ul/li[4]/text()').extract_first()
        item['team_info'] = json.dumps({
            'place': place.strip() if place else None,
            'stadium': stadium.strip() if stadium else None,
            'capacity': capacity.strip() if capacity else None,
            'coach': coach.strip() if coach else None,
        })
        # results
        results = []
        # for i, result in enumerate(rslt_bold_link):
        #     results.append({
        #         'bold_link': rslt_bold_link[i].extract().strip() if rslt_bold_link[i] else None,
        #         'time_and_league': rslt_date[i].extract().strip() if rslt_date[i] else None,
        #         'home_team': rslt_home_teams[i].extract().strip() if rslt_home_teams[i] else None,
        #         'away_team': rslt_away_teams[i].extract().strip() if rslt_away_teams[i] else None,
        #         'home_team_score': rslt_home_teams_scores[i].extract() if rslt_home_teams_scores[i] else None,
        #         'away_team_score': rslt_away_teams_scores[i].extract() if rslt_away_teams_scores[i] else None
        #     })
        # fixtures
        fixtures = []
        # for i, result in enumerate(fixtr_bold_link):
        #     fixtures.append({
        #         'bold_link': fixtr_bold_link[i].extract().strip() if fixtr_bold_link[i] else None,
        #         'time_and_league': time_and_league[i].extract().strip() if time_and_league[i] else None,
        #         'home_team': fixtr_home_teams[i].extract().strip() if fixtr_home_teams[i] else None,
        #         'away_team': fixtr_away_teams[i].extract().strip() if fixtr_away_teams[i] else None
        #     })
        # players
        list_player_items = response.css('.list-player-item')
        players = []
        for i, list_player_item in enumerate(list_player_items):
            if len(list_player_item.css('.player-name ::text')):
                player_link = list_player_item.css('a ::attr(href)').extract_first() if list_player_item.css(
                    'a ::attr(href)').extract_first() else ''
                player_type = list_player_item.css('.player-position ::text').extract_first() if list_player_item.css(
                    '.player-position ::text').extract_first() else ''
                player_rank = list_player_item.css('.rank ::text').extract_first() if list_player_item.css(
                    '.rank ::text').extract_first() else ''
                try:
                    player_img_id = list_player_item.css('.player-name img ::attr(src)').extract_first().strip().split('/')[-1]
                    player_img_name = hashlib.md5(player_img_id.encode('utf-8')).hexdigest()+'.png'
                    # server_path = '/var/www/html/test/Adfsd/Tewre/thomas/django_webix_hub/core/media/'
                    server_path = '/var/www/webixhub/www/webixhub/core/media/'
                    if not os.path.isfile(server_path+'players/'+player_img_name):
                        player_img_ulr = 'https://s3.eu-central-1.amazonaws.com/static.bold.dk/img/tag/128x128/' + player_img_id
                        yield scrapy.Request(player_img_ulr, callback=self.parse_player_image,
                                             meta={'player_img_name': player_img_name})
                except (TypeError, AttributeError) as e:
                    print(e)
                    player_img_name = None
                players.append({
                    'player_name': list_player_item.css('.player-name ::text').extract_first().strip(),
                    'player_bold_link': player_link.strip(),
                    'player_type': player_type.strip(),
                    'player_rank': player_rank.strip(),
                    'player_img': player_img_name,
                })
        item['players'] = json.dumps(players)
        item['results'] = json.dumps(results)
        item['fixtures'] = json.dumps(fixtures)
        yield item
        try:
            club_img_ulr = 'https://s3.eu-central-1.amazonaws.com/static.bold.dk/img/tag/128x128/'+club_img_id
            yield scrapy.Request(club_img_ulr, callback=self.parse_club_image, meta={'club_img_name': club_img_name})
        except (TypeError, AttributeError) as e:
            print(e)

    def parse_club_image(self, response):
        club_img_name = response.meta.get('club_img_name')
        # server_path = '/var/www/html/test/Adfsd/Tewre/thomas/django_webix_hub/core/media/'
        server_path = '/var/www/webixhub/www/webixhub/core/media/'
        filename_path = server_path+'clubs/'+club_img_name
        filename = filename_path.split('?')[0]
        with open(filename, 'wb') as f:
            f.write(response.body)

    def parse_player_image(self, response):
        player_img_name = response.meta.get('player_img_name')
        # server_path = '/var/www/html/test/Adfsd/Tewre/thomas/django_webix_hub/core/media/'
        server_path = '/var/www/webixhub/www/webixhub/core/media/'
        filename_path = server_path+'players/'+player_img_name
        filename = filename_path.split('?')[0]
        with open(filename, 'wb') as f:
            f.write(response.body)
