# Dockerfile for Quote Intelligence Platform
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including build tools
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon'); nltk.download('stopwords')"

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data logs reports data/raw data/processed

# Expose ports
EXPOSE 8000 8501

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/')" || exit 1

# Default command (can be overridden)
CMD ["python", "api/main.py"]