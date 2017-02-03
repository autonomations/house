# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# class HousefinderPipeline(object):
#     def process_item(self, item, spider):
#         return item

import pymongo
import json
import os
from settings import OUTPUT_DIRECTORY_JSON
from settings import OUTPUT_DIRECTORY_CSV
from settings import DEBUG_ENV

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter
from scrapy.exporters import JsonLinesItemExporter
from scrapy.exporters import BaseItemExporter
#from logger import logger

class MongoDBPipeline(object):
    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGODB_DATABSE', 'items')
        )

    def open_spider(self, spider):
        #self.client = pymongo.MongoClient(self.mongo_uri)
        self.client = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )


        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item


    # def __init__(self):
    #     # Mongo DB Setup
    #     self.client = pymongo.MongoClient(
    #         settings['MONGODB_SERVER'],
    #         settings['MONGODB_PORT']
    #     )


    # def open_spider(self, spider):
    #     self.db = self.client[settings['MONGODB_DB']]
    #     self.collection = self.db[settings['MONGODB_COLLECTION']]
    #     # This method is called when the spider is opened
    #     # self.client = pymongo.MongoClient(self.mongo_uri)
    #     # self.db = self.client[self.mongo_db]
    #     pass

    # def close_spider(self, spider):
    #     self.client.close()
    #     pass


    # def process_item(self, item, spider):
    #     empty = 'empty'
    #     for data in item:
    #         if not data:
    #             item[data] = valid 
    #             raise DropItem("Missing {0}!".format(data))

    #     self.db[self.collection].insert(dict(item))
    #     return item


class CSVWriterPipeline(CsvItemExporter):
    """ Method to Export CSV Variable
    """
    def __init__(self):
        # CSV DB Setup
        if not os.path.exists(OUTPUT_DIRECTORY_CSV):
            os.makedirs(OUTPUT_DIRECTORY_CSV)

        self.file = open(OUTPUT_DIRECTORY_CSV+'/items.csv', 'wb')
        self.csvExport = CsvItemExporter(file=self.file, include_headers_line=True, join_multivalued=', ')
    
    def open_spider(self, spider):
        self.csvExport.start_exporting()

    def close_spider(self, spider):
        self.csvExport.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        for data in item:
            if not data:
                item[data] = 'empty' 
                raise DropItem("Missing {0}!".format(data))

        self.csvExport.export_item(item)
        return item

        # if DEBUG_ENV = True
        #     return item


class JsonWriterPipeline(JsonLinesItemExporter):
    """ Method to Export JSON Variable
    """

    def __init__(self):
        # JSON DB Setup
        if not os.path.exists(OUTPUT_DIRECTORY_JSON):
            os.makedirs(OUTPUT_DIRECTORY_JSON)

        self.file = open(OUTPUT_DIRECTORY_JSON+'/propertyList.jl', 'wb')
        self.jsonExport = JsonLinesItemExporter(file=self.file)
    
    def open_spider(self, spider):
        self.jsonExport.start_exporting()

    def close_spider(self, spider):
        self.jsonExport.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        for data in item:
            if not data:
                item[data] = 'empty' 
                raise DropItem("Missing {0}!".format(data))

        self.jsonExport.export_item(item)
        return item

        # if DEBUG_ENV = True
        


# class DuplicatesPipeline(object):

#     def __init__(self):
#         self.ids_seen = set()

#     def process_item(self, item, spider):
#         if item['id'] in self.ids_seen:
#             raise DropItem("Duplicate item found: %s" % item)
#         else:
#             self.ids_seen.add(item['id'])
#             #return item



