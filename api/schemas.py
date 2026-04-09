"""
Pydantic Schemas for API Request/Response Validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class QuoteBase(BaseModel):
    """Base quote schema"""
    quote_text: str
    author: str
    tags: Optional[str] = ""
    tags_count: int = 0
    quote_length: int = 0
    source_url: Optional[str] = ""
    page_number: Optional[int] = 1

class QuoteCreate(QuoteBase):
    """Schema for creating a new quote"""
    pass

class QuoteResponse(QuoteBase):
    """Schema for API response"""
    id: int
    collected_at: datetime
    sentiment_score: Optional[float] = 0.0
    readability_score: Optional[float] = 0.0
    
    class Config:
        from_attributes = True  # SQLAlchemy to dict conversion

class AuthorResponse(BaseModel):
    """Schema for author response"""
    id: int
    name: str
    quote_count: int
    average_sentiment: float
    
    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    """Schema for paginated responses"""
    total: int
    page: int
    per_page: int
    total_pages: int
    data: List[QuoteResponse]