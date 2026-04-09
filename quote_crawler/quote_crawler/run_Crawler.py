# run_crawler.py (place this in quote_crawler/quote_crawler/ directory)
import os
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def main():
    """Run the Scrapy crawler"""
    print("\n" + "="*60)
    print("🚀 STARTING SCRAPY CRAWLER - STAGE 2")
    print("="*60)
    
    # Get the project root directory (2 levels up from this file)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)  # This is quote_crawler/
    main_project_root = os.path.dirname(project_root)  # This is intelligent-data-platform/
    
    # Create directories in the main project
    data_dir = os.path.join(main_project_root, 'data', 'raw')
    logs_dir = os.path.join(main_project_root, 'logs')
    
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)
    
    print(f"📂 Data will be saved to: {data_dir}")
    print(f"📂 Logs will be saved to: {logs_dir}")
    
    # Change to the scrapy project directory
    os.chdir(project_root)
    
    # Get settings and update paths
    settings = get_project_settings()
    
    # Update FEEDS to use correct paths
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    settings.set('FEEDS', {
        os.path.join(data_dir, f'quotes_{timestamp}.csv'): {
            'format': 'csv',
            'encoding': 'utf8',
        },
        os.path.join(data_dir, f'quotes_{timestamp}.json'): {
            'format': 'json',
            'encoding': 'utf8',
        },
    })
    
    # Run crawler
    process = CrawlerProcess(settings)
    process.crawl('quotes')
    process.start()
    
    print("\n" + "="*60)
    print("✅ CRAWLING COMPLETE")
    print("="*60)
    print(f"📁 Data saved to: {data_dir}")
    print("📄 Check the files above for your collected data")

if __name__ == "__main__":
    main()