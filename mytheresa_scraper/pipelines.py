# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import sqlite3
from scrapy.exceptions import DropItem
from mytheresa_scraper.items import MytheresaScraperItem

class MytheresaScraperPipeline:
    def __init__(self, db_settings):
        self.db_settings = db_settings
        self.conn = None
        self.cursor = None

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict('DATABASE')
        return cls(db_settings)

    def open_spider(self, spider):
        self.conn = sqlite3.connect(self.db_settings['database'])
        self.cursor = self.conn.cursor()
        self.create_table()

    def close_spider(self, spider):
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def create_table(self):
        # Create table if it does not exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS mytheresa_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                breadcrumbs TEXT,
                image_url TEXT,
                brand TEXT,
                product_name TEXT,
                listing_price TEXT,
                offer_price TEXT,
                discount TEXT,
                product_id TEXT,
                sizes TEXT,
                description TEXT,
                other_images TEXT
            )
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            self.cursor.execute("""
                INSERT INTO mytheresa_data (breadcrumbs, image_url, brand, product_name, listing_price, offer_price, discount, product_id, sizes, description, other_images)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ','.join(item['breadcrumbs']) if item['breadcrumbs'] else '',
                item['image_url'],
                item['brand'],
                item['product_name'],
                item['listing_price'],
                item['offer_price'],
                item['discount'],
                item['product_id'],
                ','.join(item['sizes']) if item['sizes'] else '',
                item['description'],
                ','.join(item['other_images']) if item['other_images'] else ''
            ))
            self.conn.commit()
        except sqlite3.Error as e:
            spider.logger.error(f"Error saving item to SQLite database: {e}")
            raise DropItem(f"Error saving item to SQLite database: {e}")

        return item
