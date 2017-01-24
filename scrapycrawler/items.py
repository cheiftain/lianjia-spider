# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


# class ZoneItem(Item):
#     id = Field()
#     pinyin = Field()
#     name = Field()


class HouseDetailItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = Field()
    price = Field()
    unit = Field()

    date = Field()
    source = Field()
    floor = Field()
    orientation = Field()
    year = Field()
    building_type = Field()
    fitment = Field()
    purpose = Field()
    region = Field()
    subway = Field()
    heating = Field()
    community = Field()

    pass
