import scrapy

class MytheresaSpider(scrapy.Spider):
    name = 'mytheresa'
    start_urls = ['https://www.mytheresa.com/int_en/men/shoes.html']

    def parse(self, response):
        # Extracting product URLs from the start URL
        product_urls = response.css('div.item.item--sale a::attr(href)').getall()
        seen_urls = set()  # To Avoid duplication

        for url in product_urls:
            if url not in seen_urls:
                seen_urls.add(url)
                yield {
                    'product_url': response.urljoin(url)
                }

        

