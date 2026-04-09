# quote_crawler/quote_crawler/pipelines.py
from datetime import datetime
import logging

class QuotePipeline:
    """
    Process and validate scraped quotes before saving
    """
    
    def process_item(self, item, spider):
        """
        Called for each scraped item
        """
        # Clean and validate data
        if item.get('quote_text'):
            # Remove quotes and extra whitespace
            item['quote_text'] = item['quote_text'].strip('"“”').strip()
        
        if item.get('author'):
            item['author'] = item['author'].strip()
        
        # Add processing timestamp
        item['processed_at'] = datetime.now().isoformat()
        
        # Log progress every 10 items
        if hasattr(spider, 'items_processed'):
            spider.items_processed += 1
            if spider.items_processed % 10 == 0:
                spider.logger.info(f"Processed {spider.items_processed} quotes so far")
        else:
            spider.items_processed = 1
        
        return item