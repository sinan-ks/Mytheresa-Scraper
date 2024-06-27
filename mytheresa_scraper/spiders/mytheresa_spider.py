import scrapy


class MytheresaSpider(scrapy.Spider):
    name = 'mytheresa'
    allowed_domains = ['mytheresa.com']
    start_urls = ['https://www.mytheresa.com/int_en/men/shoes.html']

    def parse(self, response):
        #Extracting product URLs from the start URL
        product_urls = response.css('a.item__link::attr(href)').getall()
        for url in product_urls:
            # Extracted URLs join with the base URL
            absolute_url = response.urljoin(url)
            yield scrapy.Request(url=absolute_url)

