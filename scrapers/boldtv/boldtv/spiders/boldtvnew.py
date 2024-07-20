import json
from datetime import datetime

import scrapy
from ..items import BoldtvItem
import hashlib

class BoldtvnewSpider(scrapy.Spider):
    name = 'boldtvnew'
    allowed_domains = ['www.bold.dk','amazonaws.com']
    start_urls = ['https://www.bold.dk/tv']
    def parse(self, response):
        items = BoldtvItem()
        baseurl = 'https://www.bold.dk';
        # danish_month = {'januar': '01', 'februar': '02', 'marts': '03', 'april': '04', 'maj': '05', 'juni': '06', 'juli': '07', 'august': '08', 'september': '09', 'oktober': '10', 'november': '11', 'december': '12'}
        # danish_month = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'ma': '05', 'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'okt': '10', 'nov': '11', 'dec': '12'}
        # danish_month_2 = dict(zip(danish_month.values(), danish_month.keys()))
        list_games = response.css('.list-games')
        h2s = response.css('.header-column ::text').extract()
        # if h2s[0] == 'I dag':
        #     today = datetime.today()
        #     h2s[0] = 'day ' + today.strftime('%d') + '. ' + danish_month_2[today.strftime('%m')]
        i = 0
        for list_game in list_games:
            matches = list_game.css('.matchesbar-link')
            # match_date = h2s[i]
            # if match_date.find('I morgen') != -1:
            #     i = i + 1
            #     continue
            for match in matches:
                # items['match_date'] = match_date
                # match_time = match.css('.time span ::text').extract_first().strip()
                # if match_time == 'FT':
                #     continue
                # elif match_time == 'HT':
                #     continue
                # date = items['match_date'].strip().split(' ')
                # if len(date) > 3:
                #     date.pop(0)
                try:
                    # day = date[1].replace('.', '')
                    # day = day.zfill(2)
                    # month = danish_month[date[2]]
                    # current_year = datetime.now().strftime('%Y')
                    # flat_date = current_year + month + day
                    # if flat_date < datetime.now().strftime('%Y%m%d'):
                    #     current_year = int(current_year) + 1
                    # parsed_date_time = str(current_year) + '-' + month + '-' + day + ' ' + match_time + ':00'
                    # items['parsed_match_date_time'] = parsed_date_time
                    # items['match_time'] = match_time
                    match_url = match.css('::attr(href)').extract_first().strip()
                    items['match_unique_id'] = hashlib.md5(match_url.encode('utf-8')).hexdigest()
                    items['match_url'] = baseurl + match_url
                    items['bolddk_match_id'] = match_url.split('/')[-1].strip()
                    items['home_team'] = match.css('.home .teamname ::text').extract_first().strip()
                    items['away_team'] = match.css('.away .teamname ::text').extract_first().strip()
                    items['game'] = items['home_team'] + ' - ' + items['away_team']
                    league_flag_img_url = match.css('.tournament img::attr(src)').extract_first().strip()
                    items['league_flag_img_url'] = 'league_flag/' + league_flag_img_url.split('/')[-1]
                    items['league'] = match.css('.tournament small::text').extract_first().strip()
                    items['league_url'] = match.css('.tournament small::text').extract_first().strip()
                    channel_img_url = match.css('.tv img::attr(src)').extract_first().strip()
                    if len(channel_img_url) > 0:
                        items['channel_img_url'] = 'channels/' + channel_img_url.split('/')[-1]
                        items['channel_title'] = channel_img_url.split('/')[-1].split('.')[0]
                    else:
                        items['channel_img_url'] = None
                        items['channel_title'] = None
                    yield scrapy.Request(league_flag_img_url, callback=self.parse_league_image)
                    yield scrapy.Request(channel_img_url, callback=self.parse_image)
                    yield items
                except (TypeError, AttributeError) as e:
                    print(e)
            i = i+1

    def parse_image(self, response):
        # filename1 = '/var/www/html/test/Adfsd/Tewre/thomas/django_webix_hub/core/media/channels/'+response.url.split('/')[-1]
        filename1 = '/var/www/webixhub/www/webixhub/core/media/channels/'+response.url.split('/')[-1]
        filename = filename1.split('?')[0]
        with open(filename, 'wb') as f:
            f.write(response.body)

    def parse_league_image(self, response):
        # filename1 = '/var/www/html/test/Adfsd/Tewre/thomas/django_webix_hub/core/media/league_flag/'+response.url.split('/')[-1]
        filename1 = '/var/www/webixhub/www/webixhub/core/media/league_flag/'+response.url.split('/')[-1]
        filename = filename1.split('?')[0]
        with open(filename, 'wb') as f:
            f.write(response.body)