# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoomsdayindexItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

class DoomItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    paragraph = scrapy.Field()
    published_time = scrapy.Field()