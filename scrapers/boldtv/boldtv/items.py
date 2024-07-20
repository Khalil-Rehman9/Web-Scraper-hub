# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BoldtvItem(scrapy.Item):
    # define the fields for your item here like:
    # match_date = scrapy.Field()
    # match_time = scrapy.Field()
    match_url = scrapy.Field()
    game = scrapy.Field()
    league_flag_img_url = scrapy.Field()
    league = scrapy.Field()
    league_url = scrapy.Field()
    channel_img_url = scrapy.Field()
    channel_title = scrapy.Field()
    parsed_match_date_time = scrapy.Field()
    match_unique_id = scrapy.Field()
    bolddk_match_id = scrapy.Field()
    home_team = scrapy.Field()
    away_team = scrapy.Field()
