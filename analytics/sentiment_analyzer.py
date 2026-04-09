"""
Sentiment Analysis Module
Analyzes emotional tone of quotes using multiple methods
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import init_database, get_session, Quote, Author
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from datetime import datetime

# Download required NLTK data
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

class SentimentAnalyzer:
    """Multi-method sentiment analysis for quotes"""
    
    def __init__(self):
        """Initialize sentiment analyzers"""
        self.sia = SentimentIntensityAnalyzer()
        print("✅ Sentiment Analyzer initialized")
    
    def analyze_textblob(self, text):
        """
        Analyze sentiment using TextBlob
        Returns: polarity (-1 to 1), subjectivity (0 to 1)
        """
        blob = TextBlob(text)
        return {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }
    
    def analyze_vader(self, text):
        """
        Analyze sentiment using VADER (Valence Aware Dictionary)
        Better for social media and short texts
        """
        scores = self.sia.polarity_scores(text)
        return {
            'compound': scores['compound'],
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu']
        }
    
    def classify_sentiment(self, polarity_score):
        """
        Classify sentiment into categories
        """
        if polarity_score >= 0.5:
            return "very_positive", "😊"
        elif polarity_score >= 0.1:
            return "positive", "🙂"
        elif polarity_score >= -0.1:
            return "neutral", "😐"
        elif polarity_score >= -0.5:
            return "negative", "😞"
        else:
            return "very_negative", "😢"
    
    def analyze_quote(self, quote_text):
        """
        Complete sentiment analysis for a single quote
        """
        # Get TextBlob analysis
        textblob_result = self.analyze_textblob(quote_text)
        
        # Get VADER analysis
        vader_result = self.analyze_vader(quote_text)
        
        # Classify based on TextBlob polarity
        sentiment_label, sentiment_emoji = self.classify_sentiment(
            textblob_result['polarity']
        )
        
        return {
            'quote_text': quote_text[:100] + "..." if len(quote_text) > 100 else quote_text,
            'textblob_polarity': round(textblob_result['polarity'], 3),
            'textblob_subjectivity': round(textblob_result['subjectivity'], 3),
            'vader_compound': round(vader_result['compound'], 3),
            'sentiment_label': sentiment_label,
            'sentiment_emoji': sentiment_emoji
        }
    
    def analyze_all_quotes(self, update_database=True):
        """
        Analyze sentiment for all quotes in database
        """
        print("\n" + "="*60)
        print("🎭 RUNNING SENTIMENT ANALYSIS ON ALL QUOTES")
        print("="*60)
        
        engine = init_database()
        session = get_session(engine)
        
        quotes = session.query(Quote).all()
        print(f"📊 Analyzing {len(quotes)} quotes...")
        
        results = []
        sentiment_distribution = {
            'very_positive': 0,
            'positive': 0,
            'neutral': 0,
            'negative': 0,
            'very_negative': 0
        }
        
        for quote in quotes:
            # Analyze sentiment
            textblob_result = self.analyze_textblob(quote.quote_text)
            sentiment_label, _ = self.classify_sentiment(textblob_result['polarity'])
            
            # Update distribution
            sentiment_distribution[sentiment_label] += 1
            
            # Store result
            result = {
                'id': quote.id,
                'author': quote.author,
                'quote_text': quote.quote_text[:100],
                'sentiment_score': textblob_result['polarity'],
                'sentiment_label': sentiment_label
            }
            results.append(result)
            
            # Update database if requested
            if update_database:
                quote.sentiment_score = textblob_result['polarity']
        
        if update_database:
            session.commit()
            print(f"✅ Updated {len(quotes)} quotes with sentiment scores")
        
        # Display statistics
        print("\n📊 SENTIMENT DISTRIBUTION:")
        for label, count in sentiment_distribution.items():
            percentage = (count / len(quotes)) * 100
            bar = "█" * int(percentage / 2)
            print(f"   {label:15} | {count:3} quotes | {percentage:5.1f}% {bar}")
        
        # Show examples
        print("\n📝 SENTIMENT EXAMPLES:")
        
        # Most positive
        positive_example = max(results, key=lambda x: x['sentiment_score'])
        print(f"\n   😊 MOST POSITIVE:")
        print(f"   Quote: {positive_example['quote_text']}...")
        print(f"   Author: {positive_example['author']}")
        print(f"   Score: {positive_example['sentiment_score']:.3f}")
        
        # Most negative
        negative_example = min(results, key=lambda x: x['sentiment_score'])
        print(f"\n   😞 MOST NEGATIVE:")
        print(f"   Quote: {negative_example['quote_text']}...")
        print(f"   Author: {negative_example['author']}")
        print(f"   Score: {negative_example['sentiment_score']:.3f}")
        
        session.close()
        return results
    
    def analyze_author_sentiment(self, author_name):
        """
        Analyze sentiment for a specific author's quotes
        """
        engine = init_database()
        session = get_session(engine)
        
        quotes = session.query(Quote).filter(Quote.author == author_name).all()
        
        if not quotes:
            print(f"No quotes found for author: {author_name}")
            return None
        
        print(f"\n📊 Sentiment Analysis for {author_name}")
        print("-" * 40)
        
        sentiments = []
        for quote in quotes:
            textblob_result = self.analyze_textblob(quote.quote_text)
            sentiments.append(textblob_result['polarity'])
        
        avg_sentiment = sum(sentiments) / len(sentiments)
        sentiment_label, emoji = self.classify_sentiment(avg_sentiment)
        
        print(f"Total quotes: {len(quotes)}")
        print(f"Average sentiment: {avg_sentiment:.3f}")
        print(f"Overall tone: {emoji} {sentiment_label}")
        
        session.close()
        return {
            'author': author_name,
            'quote_count': len(quotes),
            'avg_sentiment': avg_sentiment,
            'sentiment_label': sentiment_label
        }

def main():
    """Run sentiment analysis on all quotes"""
    analyzer = SentimentAnalyzer()
    
    # Analyze all quotes
    results = analyzer.analyze_all_quotes(update_database=True)
    
    # Analyze specific author
    analyzer.analyze_author_sentiment("Albert Einstein")
    analyzer.analyze_author_sentiment("Marilyn Monroe")
    
    print("\n" + "="*60)
    print("✅ SENTIMENT ANALYSIS COMPLETE")
    print("="*60)
    print("\n💡 Sentiment scores added to database!")
    print("   Access via API: GET /quotes")

if __name__ == "__main__":
    main()