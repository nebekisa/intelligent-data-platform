"""
Basic Web Scraper for Quotes Data
Stage 1: Simple data collection with requests and BeautifulSoup

Target Site: http://quotes.toscrape.com
Data to extract: Quotes, Authors, Tags
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional
import os
# Fix for Windows console Unicode issues
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configure logging for professional monitoring
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

class BasicQuoteScraper:
    """
    A polite web scraper for collecting quotes from quotes.toscrape.com.
    This demonstrates how to adapt parsers to specific website structures.
    """
    
    def __init__(self, delay: float = 1.0):
        """
        Initialize scraper with polite crawling settings.
        
        Args:
            delay: Seconds to wait between requests (default: 1.0)
        """
        self.delay = delay
        self.session = requests.Session()
        # Set a real User-Agent to be respectful to websites
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Ensure data directories exist
        os.makedirs('data/raw', exist_ok=True)
        os.makedirs('data/processed', exist_ok=True)
        
        logging.info(f"Scraper initialized with {delay}s delay between requests")
    
    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch HTML content from a URL with error handling.
        
        Args:
            url: The webpage URL to fetch
            
        Returns:
            HTML content as string, or None if failed
        """
        try:
            logging.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            logging.info(f"Successfully fetched {url}")
            return response.text
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed for {url}: {str(e)}")
            return None
    
    def parse_quotes(self, html: str) -> List[Dict]:
        """
        Parse HTML to extract quotes from quotes.toscrape.com.
        
        Structure of quotes.toscrape.com:
        - Each quote is in a <div class="quote">
        - Quote text is in <span class="text">
        - Author is in <small class="author">
        - Tags are in <div class="tags"> -> <a class="tag">
        
        Args:
            html: HTML content to parse
            
        Returns:
            List of dictionaries containing quote data
        """
        soup = BeautifulSoup(html, 'lxml')
        quotes = []
        
        # Find all quote containers
        quote_elements = soup.find_all('div', class_='quote')
        
        logging.info(f"Found {len(quote_elements)} quote elements on the page")
        
        for element in quote_elements:
            try:
                # Extract quote text (the actual quote content)
                quote_text_element = element.find('span', class_='text')
                quote_text = quote_text_element.get_text(strip=True) if quote_text_element else "No quote text found"
                
                # Extract author name
                author_element = element.find('small', class_='author')
                author = author_element.get_text(strip=True) if author_element else "Unknown author"
                
                # Extract tags (there can be multiple tags per quote)
                tags = []
                tags_container = element.find('div', class_='tags')
                if tags_container:
                    tag_elements = tags_container.find_all('a', class_='tag')
                    tags = [tag.get_text(strip=True) for tag in tag_elements]
                
                # Create a structured record
                quote_data = {
                    'quote_text': quote_text,
                    'author': author,
                    'tags': ', '.join(tags),  # Convert list to string for CSV
                    'tags_count': len(tags),
                    'quote_length': len(quote_text),
                    'source_url': 'http://quotes.toscrape.com',
                    'collected_at': datetime.now().isoformat(),
                    'page': 1  # We'll implement pagination later
                }
                
                quotes.append(quote_data)
                logging.debug(f"Extracted quote from {author}: {quote_text[:50]}...")
                
            except Exception as e:
                logging.error(f"Error parsing quote element: {str(e)}")
                continue
        
        return quotes
    
    def scrape_multiple_pages(self, max_pages: int = 3):
        """
        Scrape quotes from multiple pages.
        
        Args:
            max_pages: Maximum number of pages to scrape
        """
        all_quotes = []
        base_url = "http://quotes.toscrape.com"
        
        for page_num in range(1, max_pages + 1):
            # Construct URL for each page
            if page_num == 1:
                url = base_url
            else:
                url = f"{base_url}/page/{page_num}/"
            
            logging.info(f"\n📄 Scraping page {page_num}: {url}")
            
            # Fetch the page
            html = self.fetch_page(url)
            
            if not html:
                logging.warning(f"Failed to fetch page {page_num}, stopping...")
                break
            
            # Parse quotes from this page
            page_quotes = self.parse_quotes(html)
            
            if not page_quotes:
                logging.info(f"No quotes found on page {page_num}, assuming end of content")
                break
            
            # Update page number in data
            for quote in page_quotes:
                quote['page'] = page_num
            
            all_quotes.extend(page_quotes)
            logging.info(f"Collected {len(page_quotes)} quotes from page {page_num}")
            
            # Be polite - wait between page requests
            if page_num < max_pages:
                time.sleep(self.delay)
        
        return all_quotes
    
    def save_to_csv(self, quotes: List[Dict], filename: str = None):
        """
        Save quotes to CSV file.
        
        Args:
            quotes: List of quote dictionaries
            filename: Output filename (auto-generated if None)
        """
        if not quotes:
            logging.warning("No quotes to save")
            return None
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/raw/quotes_{timestamp}.csv"
        
        df = pd.DataFrame(quotes)
        df.to_csv(filename, index=False, encoding='utf-8')
        logging.info(f"✅ Saved {len(quotes)} quotes to {filename}")
        return filename
    
    def save_to_json(self, quotes: List[Dict], filename: str = None):
        """
        Save quotes to JSON file.
        
        Args:
            quotes: List of quote dictionaries
            filename: Output filename (auto-generated if None)
        """
        if not quotes:
            logging.warning("No quotes to save")
            return None
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/raw/quotes_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(quotes, f, indent=2, ensure_ascii=False)
        
        logging.info(f"✅ Saved {len(quotes)} quotes to {filename}")
        return filename
    
    def generate_summary_stats(self, quotes: List[Dict]):
        """
        Generate and display summary statistics about collected data.
        
        Args:
            quotes: List of quote dictionaries
        """
        if not quotes:
            return
        
        df = pd.DataFrame(quotes)
        
        print("\n" + "="*60)
        print("📊 DATA COLLECTION SUMMARY")
        print("="*60)
        print(f"Total quotes collected: {len(quotes)}")
        print(f"Unique authors: {df['author'].nunique()}")
        print(f"Average quote length: {df['quote_length'].mean():.0f} characters")
        print(f"Average tags per quote: {df['tags_count'].mean():.2f}")
        
        # Top 5 authors
        top_authors = df['author'].value_counts().head(5)
        print("\n🏆 Top 5 Authors:")
        for author, count in top_authors.items():
            print(f"  - {author}: {count} quotes")
        
        # Sample a random quote
        sample_quote = df.sample(n=1).iloc[0]
        print("\n✨ Sample Quote:")
        print(f"  \"{sample_quote['quote_text']}\"")
        print(f"  — {sample_quote['author']}")
        print(f"  Tags: {sample_quote['tags']}")
        print("="*60)

def main():
    """Main execution function"""
    print("\n🚀 Starting Intelligent Data Platform - Stage 1")
    print("Target: http://quotes.toscrape.com\n")
    
    # Create scraper instance with 1 second delay between requests
    scraper = BasicQuoteScraper(delay=1.0)
    
    # Scrape quotes from multiple pages
    print("📥 Collecting quotes from multiple pages...\n")
    all_quotes = scraper.scrape_multiple_pages(max_pages=5)
    
    if all_quotes:
        # Save in both formats
        csv_file = scraper.save_to_csv(all_quotes)
        json_file = scraper.save_to_json(all_quotes)
        
        # Generate summary statistics
        scraper.generate_summary_stats(all_quotes)
        
        print(f"\n✅ SUCCESS: Collected {len(all_quotes)} quotes")
        print(f"📁 Data saved to:")
        print(f"   - {csv_file}")
        print(f"   - {json_file}")
        print("\n📂 Check the 'data/raw/' directory for your collected data")
    else:
        print("\n⚠️  No quotes were collected. Please check:")
        print("   1. Your internet connection")
        print("   2. The website is accessible: http://quotes.toscrape.com")
        print("   3. Check scraper.log for detailed errors")
    
    print("\n✨ Stage 1 completed! Ready for Stage 2")

if __name__ == "__main__":
    main()