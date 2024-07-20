# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ClubscraperItem(scrapy.Item):
    # define the fields for your item here like:
    bold_team_id = scrapy.Field()
    name = scrapy.Field()
    img = scrapy.Field()
    team_info = scrapy.Field()
    results = scrapy.Field()
    fixtures = scrapy.Field()
    players = scrapy.Field()
    pass
