import json
from datetime import datetime

import scrapy
from ..items import BoldtvItem
    # , BodtvItemTeam, BodtvItemLeague
import hashlib

class BolddktvSpider(scrapy.Spider):
    name = 'bolddktv'
    allowed_domains = ['www.bold.dk','amazonaws.com']
    start_urls = ['https://www.bold.dk/tv']
    def parse(self, response):
        items = BoldtvItem()
        danish_month = {'januar': '01', 'februar': '02', 'marts': '03', 'april': '04', 'maj': '05', 'juni': '06', 'juli': '07', 'august': '08', 'september': '09', 'oktober': '10', 'november': '11', 'december': '12'}
        tv = response.css('#tv_left')
        h2s = tv.xpath('//*[@id="tv_left"]/h2/text()').extract()
        tables = tv.xpath('//*[@id="tv_left"]/table')
        i = 0
        j = 0
        print('aa --------------------###################')
        print(tables)
        for table in tables:
            trs = table.xpath('tr')
            for tr in trs:
                kampstart = tr.xpath(".//*[contains(@class,'kampstart')]//a/text()").extract_first()
                match_url = tr.xpath(".//*[contains(@class,'kampstart')]//a/@href").extract_first()
                game = tr.xpath(".//*[contains(@class,'game')]//a/text()").extract_first()
                league = tr.xpath(".//*[contains(@class,'league')]//a/text()").extract_first()
                league_url = tr.xpath(".//*[contains(@class,'league')]//a/@href").extract_first()
                league_flag_img_url = tr.xpath(".//*[contains(@class,'flag')]//a/img/@src").extract_first()
                channel_img_url = tr.xpath(".//*[contains(@class,'channel')]//img/@src").extract_first()
                channel_title = tr.xpath(".//*[contains(@class,'channel')]//img/@title").extract_first()
                if kampstart:
                    items['match_date'] = h2s[i]
                    match_time = kampstart.strip()
                    date = items['match_date'].split(' ')
                    day = date[1].replace('.','')
                    day = day.zfill(2)
                    month = danish_month[date[2]]
                    current_year = datetime.now().strftime('%Y')
                    flat_date = current_year+month+day
                    if flat_date < datetime.now().strftime('%Y%m%d'):
                        current_year = int(current_year)+1
                    parsed_date_time = str(current_year)+'-'+month+'-'+day+' '+match_time+':00'
                    items['parsed_match_date_time'] = parsed_date_time
                    items['match_time'] = match_time
                    match_url = match_url.strip()
                    items['match_unique_id'] = hashlib.md5(match_url.encode('utf-8')).hexdigest()
                    items['match_url'] = "https://www.bold.dk"+match_url
                    items['game'] = game.strip()
                    league_flag_img_url = league_flag_img_url.strip()
                    items['league_flag_img_url'] = 'league_flag/'+league_flag_img_url.split('/')[-1]
                    items['league'] = league.strip()
                    full_league_url = "https://www.bold.dk"+league_url.strip()
                    items['league_url'] = "https://www.bold.dk"+league_url.strip()
                    items['league_id'] = hashlib.md5(full_league_url.encode('utf-8')).hexdigest()
                    channel_img_url = channel_img_url.strip()
                    items['channel_img_url'] = 'channels/'+channel_img_url.split('/')[-1]
                    items['channel_title'] = channel_title.strip()
                    # yield scrapy.Request(league_flag_img_url, callback=self.parse_league_image)
                    # yield scrapy.Request(channel_img_url, callback=self.parse_image)
                    yield scrapy.Request(items['match_url'], callback=self.parse_match_details,meta={'items':items})
                    yield scrapy.Request(items['league_url'], callback=self.parse_league_details)
                    print('--------------------###################')
                    print(i)
                    print(j)
                    print('--------------------###################')
                    j = j + 1
            i = i + 1

    def parse_image(self,response):
        filename1 = '/var/www/html/test/Adfsd/Tewre/thomas/django_webix_hub/core/media/channels/'+response.url.split('/')[-1]
        # filename1 = '/var/www/webixhub/www/webixhub/core/media/channels/'+response.url.split('/')[-1]
        filename = filename1.split('?')[0]
        with open(filename, 'wb') as f:
            f.write(response.body)
            
    def parse_league_image(self,response):
        filename1 = '/var/www/html/test/Adfsd/Tewre/thomas/django_webix_hub/core/media/league_flag/'+response.url.split('/')[-1]
        # filename1 = '/var/www/webixhub/www/webixhub/core/media/league_flag/'+response.url.split('/')[-1]
        filename = filename1.split('?')[0]
        with open(filename, 'wb') as f:
            f.write(response.body)

    def parse_match_details(self,response):
        teams = response.css('.match a::attr(href)').extract()
        aBoldtvItem = response.meta['items']
        if len(teams) > 0:
            team1_url = "https://www.bold.dk"+teams[0]
            aBoldtvItem['team_1_id'] = hashlib.md5(team1_url.encode('utf-8')).hexdigest()
            yield scrapy.Request(team1_url, callback=self.parse_team_details, meta={'items': ''})
        if len(teams) > 1:
            aBoldtvItem['team_2_id'] = teams[1]
            team1_url = "https://www.bold.dk" + teams[1]
            aBoldtvItem['team_2_id'] = hashlib.md5(team1_url.encode('utf-8')).hexdigest()
            yield scrapy.Request(team1_url, callback=self.parse_team_details, meta={'items': ''})
        if len(teams) > 2:
            aBoldtvItem['prev_match'] = response.css('.prev_match ::text').extract_first()
        else:
            aBoldtvItem['prev_match'] = None
        match_update_div = response.css('#match_update')
        match_detail_subjects = match_update_div.css('.subject ::text').extract()
        match_detail_results = match_update_div.css('.result ::text').extract()
        match_details = {}
        i = 0
        if len(match_detail_subjects):
            for match_detail_subject in match_detail_subjects :
                match_details[match_detail_subject] = match_detail_results[i]
                i = i+1
        aBoldtvItem['match_details'] = json.dumps(match_details)
        aBoldtvItem['odds'] = response.css('.oddstable').extract_first()
        yield aBoldtvItem

    def parse_team_details(self,response):
        # team = BodtvItemTeam()
        # team['name'] = response.css('.col1 h2:first-of-type ::text').extract_first()
        # team['img'] = response.css('.col1 img::attr(src)').extract_first()
        # team['team_unique_id'] = hashlib.md5(response.url.encode('utf-8')).hexdigest()
        # team_info_col1 = response.css('#klubinfotablev1 .col1 ::text').extract()
        # team_info_col2 = response.css('#klubinfotablev1 .col2 ::text').extract()
        # team_info = {}
        # i = 0
        # if len(team_info_col1):
        #     for col in team_info_col1:
        #         team_info[col] = team_info_col2[i]
        #         i = i + 1
        # team['team_info'] = json.dumps(team_info)
        # yield team
        pass

    def parse_league_details(self,response):
        # league = BodtvItemLeague()
        # league['league_id'] = hashlib.md5(response.url.encode('utf-8')).hexdigest()
        # league['name'] = response.css('.title_box_container_container h1 ::text').extract_first()
        # league['league_standing'] = response.css('.standing').extract_first()
        # league['league_history'] = response.css('.sort-by-date').extract_first()
        # yield league
        pass