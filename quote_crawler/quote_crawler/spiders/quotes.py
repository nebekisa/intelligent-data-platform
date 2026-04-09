# quote_crawler/quote_crawler/spiders/quotes.py
import scrapy
from datetime import datetime
import sys
import os

# Add parent directory to path to import items
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from items import QuoteItem
except ImportError:
    # Fallback if items import fails
    class QuoteItem(dict):
        pass

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com"]
    
    def parse(self, response):
        """
        Parse each page and extract quotes
        """
        print(f"\n🕷️  Crawling: {response.url}")
        
        # Extract quotes from current page
        quotes = response.css('div.quote')
        print(f"   Found {len(quotes)} quotes on this page")
        
        for quote in quotes:
            # Create item using dictionary (simpler approach)
            item = {
                'quote_text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': ', '.join(quote.css('div.tags a.tag::text').getall()),
                'tags_count': len(quote.css('div.tags a.tag::text').getall()),
                'quote_length': 0,
                'source_url': response.url,
                'collected_at': datetime.now().isoformat(),
                'page_number': 1
            }
            
            # Calculate quote length
            if item['quote_text']:
                item['quote_length'] = len(item['quote_text'])
                # Clean up quote text
                item['quote_text'] = item['quote_text'].strip('"“”').strip()
            
            # Extract page number from URL
            if 'page' in response.url:
                try:
                    item['page_number'] = int(response.url.split('/')[-2])
                except:
                    item['page_number'] = 1
            
            yield item
        
        # Follow pagination link
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            print(f"   Following next page: {next_page}")
            yield response.follow(next_page, callback=self.parse)