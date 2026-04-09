"""
FastAPI Application for Quote Platform
Provides REST API endpoints for querying quotes
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analytics.sentiment_analyzer import SentimentAnalyzer
from analytics.recommender import QuoteRecommender
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional


# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import init_database, get_session, Quote, Author
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from api.schemas import QuoteResponse, AuthorResponse, PaginatedResponse

# Initialize FastAPI app
app = FastAPI(
    title="Quote Intelligence Platform API",
    description="REST API for accessing and analyzing quotes data",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc documentation
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Initialize NLP components (add after app initialization)
sentiment_analyzer = SentimentAnalyzer()
quote_recommender = None  # Will initialize on first use

def get_recommender():
    """Lazy initialization of recommender"""
    global quote_recommender
    if quote_recommender is None:
        quote_recommender = QuoteRecommender()
    return quote_recommender

# Database dependency
def get_db():
    """Dependency to get database session"""
    engine = init_database()
    session = get_session(engine)
    try:
        yield session
    finally:
        session.close()

@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "name": "Quote Intelligence Platform",
        "version": "1.0.0",
        "description": "Intelligent data collection and analytics platform",
        "endpoints": {
            "quotes": "/quotes",
            "quotes_by_id": "/quotes/{quote_id}",
            "authors": "/authors",
            "search": "/search",
            "stats": "/stats"
        },
        "documentation": "/docs"
    }

@app.get("/quotes", response_model=PaginatedResponse)
def get_quotes(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of records to return"),
    author: Optional[str] = Query(None, description="Filter by author name"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    min_length: Optional[int] = Query(None, ge=0, description="Minimum quote length"),
    db: Session = Depends(get_db)
):
    """
    Get quotes with pagination and filtering
    """
    query = db.query(Quote)
    
    # Apply filters
    if author:
        query = query.filter(Quote.author.ilike(f"%{author}%"))
    
    if tag:
        query = query.filter(Quote.tags.ilike(f"%{tag}%"))
    
    if min_length:
        query = query.filter(Quote.quote_length >= min_length)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    quotes = query.offset(skip).limit(limit).all()
    
    # Calculate total pages
    total_pages = (total + limit - 1) // limit if total > 0 else 1
    current_page = (skip // limit) + 1 if limit > 0 else 1
    
    return PaginatedResponse(
        total=total,
        page=current_page,
        per_page=limit,
        total_pages=total_pages,
        data=[QuoteResponse.model_validate(quote) for quote in quotes]
    )

@app.get("/quotes/{quote_id}", response_model=QuoteResponse)
def get_quote_by_id(quote_id: int, db: Session = Depends(get_db)):
    """
    Get a single quote by ID
    """
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail=f"Quote with ID {quote_id} not found")
    return QuoteResponse.model_validate(quote)

@app.get("/authors", response_model=List[AuthorResponse])
def get_authors(
    limit: int = Query(20, ge=1, le=100),
    min_quotes: int = Query(1, ge=1, description="Minimum number of quotes"),
    db: Session = Depends(get_db)
):
    """
    Get all authors with their quote counts
    """
    authors = db.query(Author).filter(
        Author.quote_count >= min_quotes
    ).order_by(Author.quote_count.desc()).limit(limit).all()
    
    return [AuthorResponse.model_validate(author) for author in authors]

@app.get("/authors/{author_name}/quotes", response_model=List[QuoteResponse])
def get_quotes_by_author(
    author_name: str,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """
    Get all quotes by a specific author
    """
    quotes = db.query(Quote).filter(
        Quote.author.ilike(f"%{author_name}%")
    ).limit(limit).all()
    
    if not quotes:
        raise HTTPException(status_code=404, detail=f"No quotes found for author: {author_name}")
    
    return [QuoteResponse.model_validate(quote) for quote in quotes]

@app.get("/search")
def search_quotes(
    q: str = Query(..., min_length=2, description="Search query"),
    db: Session = Depends(get_db)
):
    """
    Search quotes by text content
    """
    results = db.query(Quote).filter(
        or_(
            Quote.quote_text.ilike(f"%{q}%"),
            Quote.author.ilike(f"%{q}%"),
            Quote.tags.ilike(f"%{q}%")
        )
    ).limit(50).all()
    
    return {
        "query": q,
        "total": len(results),
        "results": [QuoteResponse.model_validate(quote) for quote in results]
    }

@app.get("/stats")
def get_statistics(db: Session = Depends(get_db)):
    """
    Get platform statistics
    """
    total_quotes = db.query(Quote).count()
    total_authors = db.query(Author).count()
    
    # Average quote length
    avg_length = db.query(func.avg(Quote.quote_length)).scalar() or 0
    
    # Most common tags (requires parsing, simplified)
    tags_data = db.query(Quote.tags).all()
    all_tags = []
    for tags_str in tags_data:
        if tags_str[0]:
            all_tags.extend(tags_str[0].split(', '))
    
    from collections import Counter
    tag_counts = Counter(all_tags)
    top_tags = tag_counts.most_common(5)
    
    return {
        "total_quotes": total_quotes,
        "total_authors": total_authors,
        "average_quote_length": round(avg_length, 1),
        "top_tags": [{"tag": tag, "count": count} for tag, count in top_tags],
        "most_prolific_author": db.query(Author).order_by(Author.quote_count.desc()).first().name if total_authors > 0 else None
    }

@app.get("/quotes/{quote_id}/sentiment")
def get_quote_sentiment(quote_id: int, db: Session = Depends(get_db)):
    """
    Get detailed sentiment analysis for a specific quote
    """
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail=f"Quote with ID {quote_id} not found")
    
    # Analyze sentiment
    result = sentiment_analyzer.analyze_quote(quote.quote_text)
    
    return {
        "quote_id": quote.id,
        "quote_text": quote.quote_text,
        "author": quote.author,
        "sentiment": result
    }

@app.get("/quotes/{quote_id}/similar")
def get_similar_quotes(
    quote_id: int, 
    limit: int = Query(5, ge=1, le=10),
    db: Session = Depends(get_db)
):
    """
    Get quotes similar to a given quote
    """
    # Verify quote exists
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail=f"Quote with ID {quote_id} not found")
    
    # Get recommendations
    recommender = get_recommender()
    similar = recommender.recommend_similar_quotes(quote_id, top_n=limit)
    
    return {
        "original_quote": {
            "id": quote.id,
            "text": quote.quote_text,
            "author": quote.author
        },
        "similar_quotes": similar
    }

@app.get("/authors/{author_name}/sentiment")
def get_author_sentiment(author_name: str, db: Session = Depends(get_db)):
    """
    Get sentiment analysis for a specific author
    """
    result = sentiment_analyzer.analyze_author_sentiment(author_name)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Author '{author_name}' not found")
    
    return result

@app.get("/recommendations/random")
def get_random_recommendation(db: Session = Depends(get_db)):
    """
    Get a random quote with similar recommendations
    """
    recommender = get_recommender()
    random_quote = recommender.get_random_quote()
    
    # Get similar quotes
    similar = recommender.recommend_similar_quotes(random_quote['id'], top_n=3)
    
    return {
        "featured_quote": random_quote,
        "you_may_also_like": similar
    }

@app.get("/recommendations/by-tags")
def recommend_by_tags(
    tags: str = Query(..., description="Comma-separated tags (e.g., love,inspirational)"),
    limit: int = Query(5, ge=1, le=10),
    db: Session = Depends(get_db)
):
    """
    Get quotes by specific tags
    """
    recommender = get_recommender()
    recommendations = recommender.recommend_by_tags(tags, top_n=limit)
    
    return {
        "tags_searched": tags.split(','),
        "total_found": len(recommendations),
        "recommendations": recommendations
    }

@app.get("/stats/sentiment")
def get_sentiment_stats(db: Session = Depends(get_db)):
    """
    Get overall sentiment statistics
    """
    quotes = db.query(Quote).all()
    
    if not quotes:
        return {"message": "No quotes found"}
    
    sentiments = [q.sentiment_score for q in quotes if q.sentiment_score != 0]
    
    sentiment_labels = []
    for score in sentiments:
        if score >= 0.5:
            sentiment_labels.append("very_positive")
        elif score >= 0.1:
            sentiment_labels.append("positive")
        elif score >= -0.1:
            sentiment_labels.append("neutral")
        elif score >= -0.5:
            sentiment_labels.append("negative")
        else:
            sentiment_labels.append("very_negative")
    
    from collections import Counter
    distribution = Counter(sentiment_labels)
    
    return {
        "total_analyzed": len(sentiments),
        "average_sentiment": round(sum(sentiments) / len(sentiments), 3) if sentiments else 0,
        "distribution": dict(distribution),
        "most_positive_author": db.query(Quote).order_by(Quote.sentiment_score.desc()).first().author if sentiments else None,
        "most_negative_author": db.query(Quote).order_by(Quote.sentiment_score.asc()).first().author if sentiments else None
    }
    

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🚀 STARTING QUOTE INTELLIGENCE API")
    print("="*60)
    print(f"📚 API Documentation: http://localhost:8000/docs")
    print(f"📖 ReDoc: http://localhost:8000/redoc")
    print(f"🔗 API Base URL: http://localhost:8000")
    print("="*60 + "\n")
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"    
    )