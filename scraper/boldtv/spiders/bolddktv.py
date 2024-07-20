from datetime import datetime

import scrapy
from ..items import BoldtvItem
import hashlib

class BolddktvSpider(scrapy.Spider):
    name = 'bolddktv'
    allowed_domains = ['www.bold.dk','amazonaws.com']
    start_urls = ['http://www.bold.dk/tv']
    def parse(self, response):
        items = BoldtvItem()
        danish_month = {'januar': '01', 'februar': '02', 'marts': '03', 'april': '04', 'maj': '05', 'juni': '06', 'juli': '07', 'august': '08', 'september': '09', 'oktober': '10', 'november': '11', 'december': '12'}
        tv = response.css('#tv_left')
        h2s = tv.xpath('//*[@id="tv_left"]/h2/text()').extract()
        tables = tv.xpath('//*[@id="tv_left"]/table')
        i = 0
        j = 0
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
                    items['match_url'] = "http://www.bold.dk"+match_url
                    items['game'] = game.strip()
                    league_flag_img_url = league_flag_img_url.strip()
                    items['league_flag_img_url'] = 'league_flag/'+league_flag_img_url.split('/')[-1]
                    items['league'] = league.strip()
                    items['league_url'] = "http://www.bold.dk"+league_url.strip()
                    channel_img_url = channel_img_url.strip()
                    items['channel_img_url'] = 'channels/'+channel_img_url.split('/')[-1]
                    items['channel_title'] = channel_title.strip()
                    yield scrapy.Request(league_flag_img_url, callback=self.parse_league_image)
                    yield scrapy.Request(channel_img_url, callback=self.parse_image)
                    yield items
                    j = j + 1
            i = i + 1
        pass

    def parse_image(self,response):
        # filename1 = '/var/www/html/test/Adfsd/Tewre/thomas/django_webix_hub/core/media/channels/'+response.url.split('/')[-1]
        filename1 = '/var/www/webixhub/www/webixhub/core/media/channels/'+response.url.split('/')[-1]
        filename = filename1.split('?')[0]
        with open(filename, 'wb') as f:
            f.write(response.body)
            
    def parse_league_image(self,response):
        # filename1 = '/var/www/html/test/Adfsd/Tewre/thomas/django_webix_hub/core/media/league_flag/'+response.url.split('/')[-1]
        filename1 = '/var/www/webixhub/www/webixhub/core/media/league_flag/'+response.url.split('/')[-1]
        filename = filename1.split('?')[0]
        with open(filename, 'wb') as f:
            f.write(response.body)
