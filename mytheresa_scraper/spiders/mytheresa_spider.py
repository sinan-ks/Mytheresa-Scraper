import scrapy

class MytheresaSpider(scrapy.Spider):
    name = 'mytheresa'
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 1  
    }
    allowed_domains = ["mytheresa.com"]
    start_urls = ['https://www.mytheresa.com/int_en/men/shoes.html']

    def parse(self, response):
        # Extracting product URLs from the start URL
        product_urls = response.css('div.item a::attr(href)').getall()
        seen_urls = set()  # To avoid duplication

        for url in product_urls:
            if url not in seen_urls:
                seen_urls.add(url)
                # yield {
                #     'product_url': response.urljoin(url)
                # } 
                yield response.follow(url, callback=self.parse_product)

        # Handle Pagination
        next_page = response.xpath('//a[contains(@class, "pagination__item") and contains(@class, "pagination__item__icon") and contains(@class, "icon__next--active")]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        item = {
            'breadcrumbs': response.xpath('//div[contains(@class, "breadcrumb__item")]/a/text()').getall(),
            'image_url': response.xpath('//div[@class="photocarousel__items"]//img[contains(@class, "product__gallery__carousel__image")]/@src').get(),
            'brand': response.xpath('//div[contains(@class, "product__area__branding__designer")]//a/text()').get(),
            'product_name': response.xpath('//div[contains(@class, "product__area__branding__name")]/text()').get(),
            'listing_price': self.get_price(response, '//span[contains(@class, "pricing__prices__value--original")]//span[contains(@class, "pricing__prices__price")]/text()'),
            'offer_price': self.get_price(response, '//span[contains(@class, "pricing__prices__value--discount")]//span[contains(@class, "pricing__prices__price")]/text()'),
            'discount': response.xpath('//span[contains(@class, "pricing__info__percentage")]/text()').get(),
            'product_id': self.extract_item_number(response),
            'sizes': response.xpath('//div[contains(@class, "sizeitem")]//span[contains(@class, "sizeitem__label")]/text()').getall(),
            'description': self.extract_description(response),
            'other_images': self.extract_other_images(response)
        }      
        yield item

    def get_price(self, response, xpath_selector):
        prices = response.xpath(xpath_selector).getall()
        if len(prices) > 1:
            return prices[1]
        return prices[0] if prices else None

    def extract_item_number(self, response):
        # Locate item number
        item_number = response.xpath('//div[contains(@class, "accordion__body__content")]//ul//li').re_first(r'Item number:\s*(\w+)')
        return item_number
    
    def extract_description(self, response):
        # Converted description list to string
        description_items = response.xpath('//div[contains(@class, "accordion__body__content")]//ul//li/text()').getall()
        description = ' '.join(description_items).strip()
        return description
    
    def extract_other_images(self, response):
        main_image_url = response.xpath('//div[@class="photocarousel__items"]//img[contains(@class, "product__gallery__carousel__image")]/@src').get()
        other_images = response.xpath('//div[contains(@class, "swiper-wrapper")]//div[contains(@class, "swiper-slide")]//img[contains(@class, "product__gallery__carousel__image")]/@src').getall()
        
        # Remove duplicates and exclude main image
        unique_images = list(set(other_images) - set([main_image_url])) if main_image_url else list(set(other_images))
        
        return unique_images
    
    
    
   

