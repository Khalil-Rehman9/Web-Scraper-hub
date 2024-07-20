# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LeagueItem(scrapy.Item):
    # define the fields for your item here like:
    season = scrapy.Field()
    league_name = scrapy.Field()
    league_img = scrapy.Field()
    league_id = scrapy.Field()
    league_standings = scrapy.Field()
