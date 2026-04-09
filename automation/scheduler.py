"""
Production Scheduler for Automated Data Collection
Uses APScheduler for cron-like job scheduling
"""

import schedule
import time
import subprocess
import logging
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/automation.log'),
        logging.StreamHandler()
    ]
)

class QuoteAutomation:
    """Automated data collection and reporting system"""
    
    def __init__(self):
        self.setup_directories()
        
    def setup_directories(self):
        """Create necessary directories"""
        os.makedirs('logs', exist_ok=True)
        os.makedirs('reports', exist_ok=True)
    
    def run_scrapy_crawler(self):
        """Execute Scrapy crawler"""
        logging.info("🕷️ Starting scheduled crawler...")
        try:
            result = subprocess.run(
                ["scrapy", "crawl", "quotes", "-o", f"data/raw/scheduled_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"],
                cwd="quote_crawler",
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                logging.info("✅ Crawler completed successfully")
                return True
            else:
                logging.error(f"❌ Crawler failed: {result.stderr}")
                return False
        except Exception as e:
            logging.error(f"❌ Error running crawler: {e}")
            return False
    
    def run_etl_pipeline(self):
        """Execute ETL pipeline"""
        logging.info("🔄 Running ETL pipeline...")
        try:
            result = subprocess.run(
                ["python", "pipeline/etl_pipeline.py"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                logging.info("✅ ETL pipeline completed")
                return True
            else:
                logging.error(f"❌ ETL failed: {result.stderr}")
                return False
        except Exception as e:
            logging.error(f"❌ Error running ETL: {e}")
            return False
    
    def generate_report(self):
        """Generate daily report"""
        logging.info("📊 Generating daily report...")
        
        # Fetch statistics from API
        import requests
        try:
            stats = requests.get("http://localhost:8000/stats").json()
            sentiment = requests.get("http://localhost:8000/stats/sentiment").json()
            
            report = f"""
            ========================================
            QUOTE INTELLIGENCE PLATFORM - DAILY REPORT
            ========================================
            Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            📊 COLLECTION STATISTICS:
            - Total Quotes: {stats.get('total_quotes', 0)}
            - Unique Authors: {stats.get('total_authors', 0)}
            - Average Quote Length: {stats.get('average_quote_length', 0):.1f} chars
            
            🎭 SENTIMENT ANALYSIS:
            - Average Sentiment: {sentiment.get('average_sentiment', 0):.3f}
            - Most Positive Author: {sentiment.get('most_positive_author', 'N/A')}
            - Most Negative Author: {sentiment.get('most_negative_author', 'N/A')}
            
            🏷️ TOP TAGS:
            """
            for tag in stats.get('top_tags', [])[:5]:
                report += f"\n  - #{tag['tag']}: {tag['count']} times"
            
            report += "\n\n✅ Report generated successfully"
            
            # Save report
            report_file = f"reports/daily_report_{datetime.now().strftime('%Y%m%d')}.txt"
            with open(report_file, 'w') as f:
                f.write(report)
            
            logging.info(f"✅ Report saved to {report_file}")
            return report
            
        except Exception as e:
            logging.error(f"❌ Error generating report: {e}")
            return None
    
    def full_automation_pipeline(self):
        """Complete automated pipeline"""
        logging.info("="*60)
        logging.info("🚀 STARTING AUTOMATED PIPELINE")
        logging.info("="*60)
        
        # Step 1: Run crawler
        if self.run_scrapy_crawler():
            # Step 2: Run ETL
            if self.run_etl_pipeline():
                # Step 3: Generate report
                self.generate_report()
        
        logging.info("="*60)
        logging.info("✅ AUTOMATED PIPELINE COMPLETE")
        logging.info("="*60)

def main():
    """Setup and run scheduler"""
    automation = QuoteAutomation()
    
    # Schedule jobs
    schedule.every().day.at("09:00").do(automation.full_automation_pipeline)
    schedule.every().day.at("17:00").do(automation.full_automation_pipeline)
    
    logging.info("📅 Scheduler started")
    logging.info("⏰ Scheduled jobs: 9:00 AM and 5:00 PM daily")
    
    # Also run immediately for testing
    logging.info("🔄 Running initial test...")
    automation.full_automation_pipeline()
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()