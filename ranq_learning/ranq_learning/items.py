# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RanqLearningItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    title =scrapy.Field()
    description =scrapy.Field()
    user_id =scrapy.Field()
    category =scrapy.Field()
    view =scrapy.Field()
