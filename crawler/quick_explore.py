"""
Quick data exploration for Stage 1 quotes
Run this directly in terminal
"""

import pandas as pd
import glob
import os
from collections import Counter
from datetime import datetime

def quick_explore():
    """Quick exploration of collected data"""
    
    # Find latest data file
    data_dir = "data/raw"
    files = glob.glob(os.path.join(data_dir, "quotes_*.csv"))
    
    if not files:
        print("❌ No data files found!")
        print("Please run: python crawler/basic_scraper.py")
        return
    
    # Get latest file
    latest_file = max(files, key=os.path.getctime)
    
    print("="*60)
    print("📊 QUICK DATA EXPLORATION")
    print("="*60)
    print(f"File: {latest_file}")
    print(f"Size: {os.path.getsize(latest_file):,} bytes")
    print(f"Created: {datetime.fromtimestamp(os.path.getctime(latest_file))}")
    
    # Load data
    df = pd.read_csv(latest_file)
    
    print(f"\n✅ DATA SUMMARY:")
    print(f"   Total quotes: {len(df)}")
    print(f"   Unique authors: {df['author'].nunique()}")
    print(f"   Date range: {df['collected_at'].min()} to {df['collected_at'].max()}")
    
    print(f"\n📝 SAMPLE QUOTES:")
    for i, row in df.head(3).iterrows():
        print(f"\n   Quote {i+1}:")
        print(f"   Author: {row['author']}")
        print(f"   Text: {row['quote_text'][:100]}...")
        print(f"   Tags: {row['tags']}")
    
    print(f"\n🏆 TOP 10 AUTHORS:")
    author_counts = df['author'].value_counts()
    for i, (author, count) in enumerate(author_counts.head(10).items(), 1):
        print(f"   {i:2}. {author[:30]:30} | {count:2} quotes")
    
    print(f"\n🔥 TOP 15 TAGS:")
    all_tags = []
    for tags in df['tags'].dropna():
        if tags:
            all_tags.extend(tags.split(', '))
    
    tag_counts = Counter(all_tags)
    for i, (tag, count) in enumerate(tag_counts.most_common(15), 1):
        bar = "█" * min(30, count)
        print(f"   {i:2}. #{tag:20} | {count:2} times {bar}")
    
    print(f"\n📏 QUOTE LENGTH STATISTICS:")
    print(f"   Shortest: {df['quote_length'].min()} chars")
    print(f"   Longest: {df['quote_length'].max()} chars")
    print(f"   Average: {df['quote_length'].mean():.1f} chars")
    print(f"   Median: {df['quote_length'].median():.1f} chars")
    
    print("\n" + "="*60)
    print("✅ EXPLORATION COMPLETE")
    print("="*60)
    print("\n📁 Data files are ready in data/raw/")
    print("🚀 Ready to proceed to Stage 2!")

if __name__ == "__main__":
    quick_explore()