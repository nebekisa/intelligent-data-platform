# quote_crawler/quote_crawler/items.py
import scrapy

class QuoteItem(scrapy.Item):
    """Define the structure of our scraped data"""
    quote_text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    tags_count = scrapy.Field()
    quote_length = scrapy.Field()
    source_url = scrapy.Field()
    collected_at = scrapy.Field()
    page_number = scrapy.Field()
    processed_at = scrapy.Field()