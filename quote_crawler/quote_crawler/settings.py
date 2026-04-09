# quote_crawler/quote_crawler/settings.py

# Add this at the top of settings.py
import os

# Define base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Update the FEEDS setting to use absolute paths
FEEDS = {
    os.path.join(BASE_DIR, 'data/raw/quotes_%(time)s.csv'): {
        'format': 'csv',
        'encoding': 'utf8',
        'overwrite': True,
    },
    os.path.join(BASE_DIR, 'data/raw/quotes_%(time)s.json'): {
        'format': 'json',
        'encoding': 'utf8',
        'overwrite': True,
    },
}
# Scrapy settings for quote_crawler project

BOT_NAME = "quote_crawler"

SPIDER_MODULES = ["quote_crawler.spiders"]
NEWSPIDER_MODULE = "quote_crawler.spiders"

# Crawl responsibly by identifying yourself
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# Configure a delay for requests for the same domain
DOWNLOAD_DELAY = 1.0
RANDOMIZE_DOWNLOAD_DELAY = True

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# Configure item pipelines
ITEM_PIPELINES = {
    "quote_crawler.pipelines.QuotePipeline": 300,
}

# Enable and configure the AutoThrottle extension
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1.0
AUTOTHROTTLE_MAX_DELAY = 10.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 8.0

# Enable showing throttling stats for every response
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Export feeds (where data will be saved)
import os
from datetime import datetime

# Create data directory if it doesn't exist
os.makedirs('../../data/raw', exist_ok=True)
os.makedirs('../../logs', exist_ok=True)

FEEDS = {
    f'../../data/raw/quotes_scrapy_%(time)s.csv': {
        'format': 'csv',
        'encoding': 'utf8',
        'store_empty': False,
    },
    f'../../data/raw/quotes_scrapy_%(time)s.json': {
        'format': 'json',
        'encoding': 'utf8',
        'store_empty': False,
    },
}

# Set logging
LOG_LEVEL = 'INFO'
LOG_FILE = '../../logs/scrapy.log'

# Retry configuration
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# Download timeout
DOWNLOAD_TIMEOUT = 30