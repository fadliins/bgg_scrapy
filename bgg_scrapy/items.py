# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from pydoc import describe
import scrapy


class BggScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    rank = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    rating = scrapy.Field()
    shop_link = scrapy.Field()
    link = scrapy.Field()
