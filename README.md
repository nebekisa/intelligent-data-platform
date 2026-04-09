<div align="center">

# 📚 Quote Intelligence Platform

### AI-Powered Quote Analytics & Recommendation System

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen.svg)]()

**An intelligent platform that collects quotes, analyzes sentiment using AI, provides smart recommendations, and visualizes insights through an interactive dashboard.**

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🎯 What This Project Does](#-what-this-project-does)
- [📊 Data Statistics](#-data-statistics)
- [🛠️ Technology Stack](#️-technology-stack)
- [🚀 Quick Start Guide](#-quick-start-guide)
- [🌐 Access Your Platform](#-access-your-platform)
- [📡 API Endpoints](#-api-endpoints)
- [🎨 Dashboard Features](#-dashboard-features)
- [📁 Project Structure](#-project-structure)
- [❓ Troubleshooting](#-troubleshooting)
- [📈 Future Enhancements](#-future-enhancements)
- [📝 License](#-license)

---

## ✨ Features

### 🤖 AI & Analytics
| Feature | Description |
|---------|-------------|
| **Sentiment Analysis** | Multi-method NLP (TextBlob + VADER) - determines if quotes are positive/negative/neutral |
| **Smart Recommendations** | TF-IDF based similarity - finds quotes similar to any quote |
| **Author Profiling** | Analyzes sentiment patterns for each author |
| **Real-time Processing** | Instant sentiment scoring as you browse |

### 🕷️ Data Collection
| Feature | Description |
|---------|-------------|
| **Web Scraping** | Professional Scrapy crawler with polite rate limiting |
| **Data Extraction** | Extracts quotes, authors, and tags |
| **100+ Quotes** | Successfully collected from quotes.toscrape.com |
| **Multiple Formats** | Export to CSV, JSON, or Excel |

### 🗄️ Backend API
| Feature | Description |
|---------|-------------|
| **RESTful API** | 12+ well-documented endpoints |
| **Fast Performance** | <100ms response time |
| **Auto Documentation** | Interactive Swagger UI at /docs |
| **Filtering** | Search by author, tags, sentiment, length |

### 📊 Dashboard
| Feature | Description |
|---------|-------------|
| **Interactive UI** | Built with Streamlit and Plotly |
| **Dark/Light Theme** | Toggle between themes |
| **Live Analytics** | Real-time charts and statistics |
| **Quote Explorer** | Search and browse all quotes |

---

## 🎯 What This Project Does

This platform solves the problem of manually collecting and analyzing quotes by:

1. **Automatically collecting** quotes from websites
2. **Analyzing sentiment** to understand emotional tone
3. **Finding similar quotes** using AI recommendations
4. **Visualizing insights** through an easy-to-use dashboard
5. **Providing an API** for developers to integrate with other applications

### Real-World Applications
- 📊 **Content Curation** - Automatically discover and categorize quotes
- 🎭 **Brand Monitoring** - Track sentiment across content
- 📚 **Educational Tool** - Learn AI, data engineering, and web scraping
- 💼 **Portfolio Project** - Demonstrate full-stack AI development skills

---

## 📊 Data Statistics

Currently the platform manages:

| Metric | Value |
|--------|-------|
| **Total Quotes** | 100 |
| **Unique Authors** | 50 |
| **Average Quote Length** | 122 characters |
| **Average Sentiment Score** | 0.15 (Positive) |
| **Most Positive Author** | Mark Twain |
| **Most Popular Tag** | love (14 occurrences) |


### Sentiment Distribution
Very Positive ██████████ 10%
Positive ██████████████████████████████████ 34%
Neutral ██████████████████████████████████████████ 42%
Negative ████████████ 12%
Very Negative ██ 2%

---

## 🛠️ Technology Stack

| Category | Technologies Used |
|----------|-------------------|
| **Backend** | FastAPI, Python 3.11 |
| **Frontend** | Streamlit, Plotly |
| **Database** | SQLite, SQLAlchemy ORM |
| **AI/ML** | NLTK, TextBlob, Scikit-learn |
| **Web Scraping** | Scrapy, BeautifulSoup, Requests |
| **Data Processing** | Pandas, NumPy |
| **DevOps** | Git, Virtual Environment |

---

## 🚀 Quick Start Guide

### Prerequisites
- Windows 10/11, macOS, or Linux
- Python 3.11 or higher installed
- Git (optional, for cloning)

### Installation (3 Simple Steps)

#### Step 1: Get the Code

```bash
# Clone the repository
git clone https://github.com/nebekisa/intelligent-data-platform.git
cd intelligent-data-platform

# OR download ZIP from GitHub and extract
step 2: Set Up Python Environment
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
Step 3: Run the Platform
For Windows Users (Easiest):
# Double-click this file or run:
simple_start.bat
For Manual Start (All Platforms):

Open TWO terminal windows:

Terminal 1 - Start the API:
python api/main.py
Terminal 2 - Start the Dashboard:
streamlit run dashboard/app.py