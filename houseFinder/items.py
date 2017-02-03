# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseFinderItem(scrapy.Item):
    # Primary fields
    title = scrapy.item.Field()
    price = scrapy.item.Field()
    description = scrapy.item.Field()
    address = scrapy.item.Field()
    imgage_urls = scrapy.item.Field()

    # Secondary Fields
    days_on_market = scrapy.item.Field()
    image_url = scrapy.item.Field()
    photo_count = scrapy.item.Field()
    price = scrapy.item.Field()
    address = scrapy.item.Field()
    url = scrapy.item.Field()
    status = scrapy.item.Field()

    beds = scrapy.item.Field()
    baths = scrapy.item.Field()
    sqft = scrapy.item.Field()

    # Locational Data
    streetAddress = scrapy.item.Field()
    addressCity = scrapy.item.Field()
    addressRegion = scrapy.item.Field()
    postalCode = scrapy.item.Field()
    longitude = scrapy.item.Field()
    latitude = scrapy.item.Field()

    EXPORT_FIELDS = ['bed', 'bath', 'car', 'price', 'address', 'url']

    # Housekeeping fields
    urlSource = scrapy.item.Field()
    project = scrapy.item.Field()
    spider = scrapy.item.Field()
    server = scrapy.item.Field()
    date = scrapy.item.Field()

    pass
