# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TestDev256ComItem( scrapy.Item ):
    # define the fields for your item here like:
    url = scrapy.Field()
    status = scrapy.Field()
    referer = scrapy.Field()
    title = scrapy.Field()
    h1 = scrapy.Field()
    ahref = scrapy.Field()
    pass
