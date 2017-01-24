# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

from scrapy import log
from scrapy.conf import settings

from scrapycrawler.items import HouseDetailItem


# class ZonePipeline(object):
#
#     def process_item(self, item, spider):
#         if isinstance(item, ZoneItem):
#             pass


class HouseDetailPipeline(object):
    def __init__(self):
        self.server = settings['MONGODB_SERVER']
        self.port = settings['MONGODB_PORT']
        self.db = settings['MONGODB_DB']
        self.col = settings['MONGODB_COLLECTION']
        client = pymongo.MongoClient(self.server, self.port)
        db = client[self.db]
        self.collection = db[self.col]

    def process_item(self, item, spider):
        if isinstance(item, HouseDetailItem):
            log.msg('Item written to MongoDB database %s/%s' % (self.db, self.col), level=log.DEBUG, spider=spider)
            return item
