import scrapy
import json


class MytheresaSpider(scrapy.Spider):
    name = 'mytheresa'
    allowed_domains = ['mytheresa.com']
    start_urls = ['https://www.mytheresa.com/int_en/men/shoes.html']

