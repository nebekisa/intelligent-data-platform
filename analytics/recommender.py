"""
Quote Recommendation Engine
Finds similar quotes based on content and sentiment
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import init_database, get_session, Quote
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

class QuoteRecommender:
    """Recommend quotes based on similarity"""
    
    def __init__(self):
        """Initialize recommender with all quotes"""
        self.engine = init_database()
        self.session = get_session(self.engine)
        self.load_quotes()
        self.build_similarity_matrix()
    
    def load_quotes(self):
        """Load all quotes from database"""
        quotes = self.session.query(Quote).all()
        self.quotes = quotes
        self.quote_texts = [q.quote_text for q in quotes]
        self.quote_ids = [q.id for q in quotes]
        self.authors = [q.author for q in quotes]
        print(f"✅ Loaded {len(self.quotes)} quotes for recommendations")
    
    def build_similarity_matrix(self):
        """Build TF-IDF similarity matrix"""
        print("🔨 Building similarity matrix...")
        
        # Create TF-IDF vectors
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=1000,
            ngram_range=(1, 2)
        )
        
        tfidf_matrix = self.vectorizer.fit_transform(self.quote_texts)
        self.similarity_matrix = cosine_similarity(tfidf_matrix)
        print(f"✅ Similarity matrix built: {self.similarity_matrix.shape}")
    
    def recommend_similar_quotes(self, quote_id, top_n=5):
        """
        Recommend quotes similar to a given quote
        """
        # Find quote index
        try:
            idx = self.quote_ids.index(quote_id)
        except ValueError:
            print(f"Quote ID {quote_id} not found")
            return []
        
        # Get similarity scores
        sim_scores = list(enumerate(self.similarity_matrix[idx]))
        
        # Sort by similarity (excluding itself)
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n+1]  # Skip the first (itself)
        
        # Get recommended quotes
        recommendations = []
        for i, score in sim_scores:
            quote = self.quotes[i]
            recommendations.append({
                'id': quote.id,
                'quote_text': quote.quote_text[:150],
                'author': quote.author,
                'similarity_score': round(score, 3),
                'tags': quote.tags
            })
        
        return recommendations
    
    def recommend_by_author(self, author_name, top_n=5):
        """
        Recommend top quotes by a specific author
        """
        author_quotes = [q for q in self.quotes if q.author == author_name]
        
        if not author_quotes:
            print(f"No quotes found for author: {author_name}")
            return []
        
        # Sort by sentiment score (if available) or quote length
        author_quotes.sort(key=lambda x: x.sentiment_score, reverse=True)
        
        recommendations = []
        for quote in author_quotes[:top_n]:
            recommendations.append({
                'id': quote.id,
                'quote_text': quote.quote_text[:150],
                'author': quote.author,
                'sentiment_score': quote.sentiment_score,
                'tags': quote.tags
            })
        
        return recommendations
    
    def recommend_by_tags(self, tags, top_n=5):
        """
        Recommend quotes containing specific tags
        """
        tags_list = tags.split(',') if isinstance(tags, str) else tags
        
        matching_quotes = []
        for quote in self.quotes:
            quote_tags = quote.tags.split(', ') if quote.tags else []
            if any(tag.strip() in quote_tags for tag in tags_list):
                matching_quotes.append(quote)
        
        # Sort by sentiment (positive first)
        matching_quotes.sort(key=lambda x: x.sentiment_score, reverse=True)
        
        recommendations = []
        for quote in matching_quotes[:top_n]:
            recommendations.append({
                'id': quote.id,
                'quote_text': quote.quote_text[:150],
                'author': quote.author,
                'tags': quote.tags,
                'sentiment_score': quote.sentiment_score
            })
        
        return recommendations
    
    def get_random_quote(self):
        """Get a random quote"""
        import random
        quote = random.choice(self.quotes)
        return {
            'id': quote.id,
            'quote_text': quote.quote_text,
            'author': quote.author,
            'tags': quote.tags,
            'sentiment_score': quote.sentiment_score
        }

def main():
    """Demo recommendation engine"""
    print("\n" + "="*60)
    print("🎯 QUOTE RECOMMENDATION ENGINE")
    print("="*60)
    
    recommender = QuoteRecommender()
    
    # Get random quote
    random_quote = recommender.get_random_quote()
    print(f"\n📖 Random Quote:")
    print(f"   \"{random_quote['quote_text'][:100]}...\"")
    print(f"   — {random_quote['author']}")
    
    # Recommend similar quotes
    print(f"\n🔍 Similar Quotes:")
    similar = recommender.recommend_similar_quotes(random_quote['id'], top_n=3)
    for i, rec in enumerate(similar, 1):
        print(f"   {i}. {rec['quote_text'][:80]}...")
        print(f"      Similarity: {rec['similarity_score']} | Author: {rec['author']}")
    
    # Recommend by author
    print(f"\n👤 Top quotes by Albert Einstein:")
    einstein_quotes = recommender.recommend_by_author("Albert Einstein", top_n=3)
    for i, rec in enumerate(einstein_quotes, 1):
        print(f"   {i}. {rec['quote_text'][:80]}...")
    
    print("\n" + "="*60)
    print("✅ RECOMMENDATION ENGINE READY")
    print("="*60)

if __name__ == "__main__":
    main() 
