"""
ETL Pipeline: Extract, Transform, Load
Processes raw scraped data into structured database
"""

import pandas as pd
import json
import os
import glob
from datetime import datetime
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import init_database, get_session, Quote, Author
from sqlalchemy import func

class ETLPipeline:
    """Extract, Transform, Load pipeline for quote data"""
    
    def __init__(self, db_path="data/quotes.db"):
        """Initialize ETL pipeline with database connection"""
        self.engine = init_database(db_path)
        self.session = get_session(self.engine)
        print(f"🚀 ETL Pipeline initialized")
    
    def extract_from_csv(self, csv_path=None):
        """
        Extract data from CSV file
        If no path provided, find the latest CSV file
        """
        if csv_path is None:
            # Find latest CSV file from Scrapy output
            scrapy_files = glob.glob("quote_crawler/data/raw/quotes_scrapy.csv")
            stage1_files = glob.glob("data/raw/quotes_*.csv")
            
            all_files = scrapy_files + stage1_files
            if not all_files:
                raise FileNotFoundError("No CSV files found!")
            
            csv_path = max(all_files, key=os.path.getctime)
        
        print(f"📂 Extracting from: {csv_path}")
        df = pd.read_csv(csv_path)
        print(f"✅ Extracted {len(df)} records")
        
        return df
    
    def extract_from_json(self, json_path=None):
        """Extract data from JSON file"""
        if json_path is None:
            # Find latest JSON file
            scrapy_files = glob.glob("quote_crawler/data/raw/quotes_scrapy.json")
            stage1_files = glob.glob("data/raw/quotes_*.json")
            
            all_files = scrapy_files + stage1_files
            if not all_files:
                raise FileNotFoundError("No JSON files found!")
            
            json_path = max(all_files, key=os.path.getctime)
        
        print(f"📂 Extracting from: {json_path}")
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        df = pd.DataFrame(data)
        print(f"✅ Extracted {len(df)} records")
        
        return df
    
    def transform_data(self, df):
        """
        Transform and clean the data
        - Handle missing values
        - Standardize formats
        - Add derived features
        - Deduplicate
        """
        print("\n🔄 Transforming data...")
        original_count = len(df)
        
        # Make a copy to avoid warnings
        df = df.copy()
        
        # 1. Handle missing values
        df['quote_text'] = df['quote_text'].fillna('No quote text')
        df['author'] = df['author'].fillna('Unknown')
        df['tags'] = df['tags'].fillna('')
        
        # 2. Clean text fields
        df['quote_text'] = df['quote_text'].str.strip('"“”').str.strip()
        df['author'] = df['author'].str.strip()
        
        # 3. Ensure numeric fields are proper
        if 'tags_count' in df.columns:
            df['tags_count'] = pd.to_numeric(df['tags_count'], errors='coerce').fillna(0).astype(int)
        else:
            # Calculate tags count if not present
            df['tags_count'] = df['tags'].apply(lambda x: len(x.split(', ')) if x else 0)
        
        if 'quote_length' in df.columns:
            df['quote_length'] = pd.to_numeric(df['quote_length'], errors='coerce').fillna(0).astype(int)
        else:
            df['quote_length'] = df['quote_text'].str.len()
        
        # 4. Standardize date columns
        if 'collected_at' in df.columns:
            df['collected_at'] = pd.to_datetime(df['collected_at'], errors='coerce')
            df['collected_at'] = df['collected_at'].fillna(datetime.now())
        else:
            df['collected_at'] = datetime.now()
        
        # 5. Add page_number if missing
        if 'page_number' not in df.columns:
            df['page_number'] = 1
        
        # 6. Add source_url if missing
        if 'source_url' not in df.columns:
            df['source_url'] = 'http://quotes.toscrape.com'
        
        # 7. Remove duplicates (same quote text and author)
        df = df.drop_duplicates(subset=['quote_text', 'author'], keep='first')
        
        after_dedup = len(df)
        print(f"   - Removed {original_count - after_dedup} duplicate quotes")
        
        # 8. Filter out very short or invalid quotes
        df = df[df['quote_length'] > 10]  # At least 10 characters
        print(f"   - Removed {after_dedup - len(df)} very short quotes (<10 chars)")
        
        print(f"✅ Transformation complete: {len(df)} records ready for loading")
        
        return df
    
    def load_to_database(self, df):
        """
        Load transformed data to database
        """
        print("\n💾 Loading data to database...")
        
        # Clear existing data (optional - remove if you want to keep historical)
        # self.session.query(Quote).delete()
        # self.session.query(Author).delete()
        
        loaded_count = 0
        updated_authors = set()
        
        for _, row in df.iterrows():
            # Check if quote already exists
            existing_quote = self.session.query(Quote).filter_by(
                quote_text=row['quote_text'],
                author=row['author']
            ).first()
            
            if not existing_quote:
                # Create new quote
                quote = Quote(
                    quote_text=row['quote_text'],
                    author=row['author'],
                    tags=row['tags'],
                    tags_count=row['tags_count'],
                    quote_length=row['quote_length'],
                    source_url=row.get('source_url', ''),
                    page_number=row.get('page_number', 1),
                    collected_at=row['collected_at'] if isinstance(row['collected_at'], datetime) else datetime.now()
                )
                self.session.add(quote)
                loaded_count += 1
                updated_authors.add(row['author'])
        
        # Commit quotes first
        self.session.commit()
        print(f"   - Loaded {loaded_count} new quotes")
        
        # Update author statistics
        for author_name in updated_authors:
            # Get or create author
            author = self.session.query(Author).filter_by(name=author_name).first()
            if not author:
                author = Author(name=author_name)
                self.session.add(author)
            
            # Update quote count
            author.quote_count = self.session.query(Quote).filter_by(author=author_name).count()
            author.last_seen = datetime.now()
        
        self.session.commit()
        print(f"   - Updated {len(updated_authors)} authors")
        
        print(f"✅ Successfully loaded {loaded_count} quotes to database")
        
        return loaded_count
    
    def generate_statistics(self):
        """Generate database statistics"""
        print("\n📊 DATABASE STATISTICS")
        print("="*50)
        
        total_quotes = self.session.query(Quote).count()
        total_authors = self.session.query(Author).count()
        
        print(f"Total quotes: {total_quotes}")
        print(f"Total authors: {total_authors}")
        
        if total_quotes > 0:
            # Average quote length
            avg_length = self.session.query(func.avg(Quote.quote_length)).scalar()
            print(f"Average quote length: {avg_length:.1f} characters")
            
            # Top authors
            top_authors = self.session.query(
                Author.name, Author.quote_count
            ).order_by(Author.quote_count.desc()).limit(5).all()
            
            print("\nTop 5 Authors:")
            for name, count in top_authors:
                print(f"  {name[:30]:30} | {count} quotes")
        
        print("="*50)
    
    def run_complete_pipeline(self, source_type='csv'):
        """
        Run complete ETL pipeline
        """
        print("\n" + "="*60)
        print("🚀 RUNNING COMPLETE ETL PIPELINE")
        print("="*60)
        
        start_time = datetime.now()
        
        # Extract
        if source_type == 'csv':
            df = self.extract_from_csv()
        else:
            df = self.extract_from_json()
        
        # Transform
        df = self.transform_data(df)
        
        # Load
        loaded = self.load_to_database(df)
        
        # Generate statistics
        self.generate_statistics()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n⏱️ Pipeline completed in {duration:.2f} seconds")
        print(f"✅ Successfully processed {loaded} quotes")
        
        return loaded

def main():
    """Run ETL pipeline from command line"""
    pipeline = ETLPipeline()
    pipeline.run_complete_pipeline(source_type='csv')

if __name__ == "__main__":
    main()