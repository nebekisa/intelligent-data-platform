"""
Database Models for Quote Platform
Using SQLAlchemy ORM for database abstraction
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Create base class for models
Base = declarative_base()

class Quote(Base):
    """Quote model representing our scraped quotes"""
    __tablename__ = 'quotes'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Quote data
    quote_text = Column(Text, nullable=False)
    author = Column(String(200), nullable=False, index=True)
    tags = Column(String(500))
    tags_count = Column(Integer, default=0)
    quote_length = Column(Integer, default=0)
    
    # Metadata
    source_url = Column(String(500))
    page_number = Column(Integer)
    collected_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, default=datetime.utcnow)
    
    # Analytics fields (will be filled in Stage 4)
    sentiment_score = Column(Float, default=0.0)
    readability_score = Column(Float, default=0.0)
    
    def to_dict(self):
        """Convert model to dictionary for API responses"""
        return {
            'id': self.id,
            'quote_text': self.quote_text,
            'author': self.author,
            'tags': self.tags.split(', ') if self.tags else [],
            'tags_count': self.tags_count,
            'quote_length': self.quote_length,
            'source_url': self.source_url,
            'page_number': self.page_number,
            'collected_at': self.collected_at.isoformat() if self.collected_at else None,
            'sentiment_score': self.sentiment_score,
            'readability_score': self.readability_score
        }

class Author(Base):
    """Author model for author-specific analytics"""
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), unique=True, nullable=False, index=True)
    quote_count = Column(Integer, default=0)
    average_sentiment = Column(Float, default=0.0)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)

def init_database(db_path="data/quotes.db"):
    """Initialize database and create tables"""
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Create database engine
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    print(f"✅ Database initialized: {db_path}")
    print(f"📊 Tables created: {', '.join(Base.metadata.tables.keys())}")
    
    return engine

def get_session(engine):
    """Get database session"""
    Session = sessionmaker(bind=engine)
    return Session()

if __name__ == "__main__":
    # Test database creation
    engine = init_database()
    print("\n📁 Database file created at: data/quotes.db")