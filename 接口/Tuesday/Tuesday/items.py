# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TuesdayItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class LianjiaLItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()

class DoubanItem(scrapy.Item):
    title = scrapy.Field()
    year = scrapy.Field()
    director = scrapy.Field()
    bianju_list = scrapy.Field()
