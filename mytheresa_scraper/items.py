# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MytheresaScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    breadcrumbs = scrapy.Field()
    image_url = scrapy.Field()
    brand = scrapy.Field()
    product_name = scrapy.Field()
    listing_price = scrapy.Field()
    offer_price = scrapy.Field()
    discount = scrapy.Field()
    product_id = scrapy.Field()
    sizes = scrapy.Field()
    description = scrapy.Field()
    other_images = scrapy.Field()
