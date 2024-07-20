import scrapy
import json
from scrapy.crawler import CrawlerProcess
from scrapy_playwright.page import PageCoroutine, PageMethod
import mysql.connector
import time
from ..items import LeagueItem


class LeagueSpider(scrapy.Spider):
    name = 'league'
    allowed_domains = ['www.bold.dk']

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
SELECT * FROM (
SELECT sports_footballmatch.league_id FROM `sports_footballmatch` 
    LEFT JOIN sports_footballleague on sports_footballleague.league_id = sports_footballmatch.league_id AND DATE(sports_footballleague.updated_at) = DATE(NOW())
    WHERE sports_footballmatch.parsed_match_date_time > (NOW() - INTERVAL 1 MONTH) 
    AND sports_footballmatch.league_id IS NOT NULL 
    AND sports_footballleague.id IS NULL
    ORDER BY sports_footballmatch.league_id ASC
) leagues
group by leagues.league_id
ORDER BY league_id DESC;
                        ''')
        rows = cursor.fetchall()
        for row in rows:
            try:
                url = 'https://bold.dk/fodbold/stillinger/' + row[0]
                yield scrapy.Request(url=url,
                                     meta=dict(
                                            playwright=True,
                                            playwright_include_page=True,
                                            playwright_timeout=600000,
                                            playwright_page_methods=[
                                                PageMethod("wait_for_selector", "div.LeagueStandings"),
                                            ],
                                            # playwright_page_coroutines=[
                                            #     PageCoroutine("wait_for_selector", "div.table-responsive"),
                                            # ]
                                     )
                                     )
            except (TypeError, AttributeError) as e:
                print(e)

    async def parse(self, response):
        league_id = response.url.split('/')[-1]
        season = response.css('#seasonSelector ::text').extract_first().strip() if response.css('#seasonSelector ::text') else None
        league_name = response.css('.name ::text').extract_first().strip() if response.css('.name ::text') else None
        league_img = 'league_flag/'+response.css('.logo-bg img ::attr(src)').extract_first().strip().split('/')[-1] if response.css('.logo-bg img ::attr(src)') else None
        league_standings = []
        clubs = response.css('.LeagueStandings tbody tr')
        for club in clubs:
            club_name = club.css('a span ::text').extract_first().strip() if club.css('a span ::text').extract_first() else None
            club_id = club.css('a ::attr(href)').extract_first().strip().split('/')[-1] if club.css('a ::attr(href)').extract_first() else None
            points = [s.strip() for s in club.css('.data ::text').extract()] if club.css('.data ::text').extract() else None
            league_standings.append({
                'club_name': club_name,
                'club_id': club_id,
                'points': points
            })
        yield {
            'season': season,
            'league_id': league_id,
            'league_name': league_name,
            'league_img': league_img,
            'league_standings': json.dumps(league_standings)
        }
