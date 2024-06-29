import scrapy

class MytheresaSpider(scrapy.Spider):
    name = 'mytheresa'
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 1  # Delay between requests in seconds
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
        next_page = response.css('a.pagination__item.pagination__item__icon.icon__next--active::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        item = {
            'breadcrumbs': response.css('div.breadcrumb__item a::text').getall(),
            'image_url': response.css('div.photocarousel__items img.product__gallery__carousel__image::attr(src)').get(),
            'brand': response.css('div.product__area__branding__designer a::text').get(),
            'product_name': response.css('div.product__area__branding__name::text').get(),
            'listing_price': self.get_price(response, 'span.pricing__prices__value--original span.pricing__prices__price::text'),
            'offer_price': self.get_price(response, 'span.pricing__prices__value--discount span.pricing__prices__price::text'),
            'discount': response.css('span.pricing__info__percentage::text').get(),
            'product_id': self.extract_item_number(response),
            'sizes': response.css('div.sizeitem span.sizeitem__label::text').getall(),
            'description': self.extract_description(response),
            'other_images': self.extract_other_images(response)
        }      
        yield item

    def get_price(self, response, css_selector):
        prices = response.css(css_selector).getall()
        if len(prices) > 1:
            return prices[1]
        return prices[0] if prices else None

    def extract_item_number(self, response):
        # Locate item number 
        item_number = response.css('div.accordion__body__content ul li').re_first(r'Item number:\s*(\w+)')
        return item_number
    
    def extract_description(self, response):
        # Extract description from the accordion__body__content, excluding item number
        description_items = response.css('div.accordion__body__content ul li::text').getall()
        description = ' '.join(description_items).replace(self.extract_item_number(response), '').strip()
        return description
    
    def extract_other_images(self, response):
        main_image_url = response.css('div.photocarousel__items img.product__gallery__carousel__image::attr(src)').get()
        other_images = response.css('div.swiper-wrapper div.swiper-slide img.product__gallery__carousel__image::attr(src)').getall()
        
        # Remove duplicates and exclude main image
        unique_images = list(set(other_images) - set([main_image_url])) if main_image_url else list(set(other_images))
        
        return unique_images
    
    
    
   

