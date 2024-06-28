import scrapy

class MytheresaSpider(scrapy.Spider):
    name = 'mytheresa'
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 1  # Delay between requests in seconds
    }
    start_urls = ['https://www.mytheresa.com/int_en/men/shoes.html']

    def parse(self, response):
        # Extracting product URLs from the start URL
        product_urls = response.css('div.item a::attr(href)').getall()
        seen_urls = set()  # To Avoid duplication

        for url in product_urls:
            if url not in seen_urls:
                seen_urls.add(url)
                yield {
                    'product_url': response.urljoin(url)
                }

        #Handle Pagination
        next_page = response.css('a.pagination__item.pagination__item__icon.icon__next.pagination__item.pagination__item__icon.icon__next--active::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        

