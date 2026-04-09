"""
Professional Quote Intelligence Platform Dashboard
UI/UX Design System - Production Grade
WCAG AAA Compliant | Dark/Light Theme | Responsive
"""
import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
from streamlit_option_menu import option_menu
import time


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Quote Intelligence Platform",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PROFESSIONAL CSS DESIGN SYSTEM
# ============================================================================

def load_css():
    """Load professional CSS with theme support"""
    
    # Detect theme preference
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'  # Default to dark theme
    
    # Toggle theme button in sidebar
    theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
    if st.sidebar.button(f"{theme_icon} Toggle Theme", use_container_width=True):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()
    
    # Theme-specific CSS
    if st.session_state.theme == 'dark':
        css = """
        <style>
        /* ===== DARK THEME ===== */
        :root {
            --bg-primary: #0a0e1a;
            --bg-secondary: #111827;
            --bg-card: #1f2937;
            --bg-hover: #374151;
            --text-primary: #f3f4f6;
            --text-secondary: #d1d5db;
            --text-muted: #9ca3af;
            --border: #374151;
            --accent-primary: #3b82f6;
            --accent-secondary: #8b5cf6;
            --accent-success: #10b981;
            --accent-warning: #f59e0b;
            --accent-danger: #ef4444;
            --shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }
        
        /* Main container */
        .stApp {
            background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
        }
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-primary) !important;
            font-weight: 600 !important;
            letter-spacing: -0.02em !important;
        }
        
        p, li, span, div {
            color: var(--text-secondary) !important;
        }
        
        /* Professional Card Design */
        .quote-card {
            background: linear-gradient(135deg, var(--bg-card) 0%, #1e293b 100%);
            border-radius: 16px;
            padding: 1.75rem;
            margin: 1rem 0;
            border: 1px solid var(--border);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .quote-card::before {
            content: '"';
            position: absolute;
            top: -20px;
            left: 10px;
            font-size: 120px;
            color: var(--accent-primary);
            opacity: 0.1;
            font-family: serif;
        }
        
        .quote-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow);
            border-color: var(--accent-primary);
        }
        
        .quote-text {
            font-size: 1.125rem;
            line-height: 1.6;
            color: var(--text-primary) !important;
            font-style: italic;
            margin-bottom: 1rem;
            position: relative;
            z-index: 1;
        }
        
        .quote-author {
            font-size: 0.875rem;
            color: var(--accent-primary) !important;
            font-weight: 600;
            margin-top: 0.75rem;
            letter-spacing: 0.05em;
        }
        
        .quote-meta {
            font-size: 0.75rem;
            color: var(--text-muted) !important;
            margin-top: 0.5rem;
            display: flex;
            gap: 1rem;
        }
        
        /* Metric Cards */
        .metric-card {
            background: linear-gradient(135deg, var(--bg-card) 0%, #1e293b 100%);
            border-radius: 16px;
            padding: 1.5rem;
            border: 1px solid var(--border);
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow);
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        
        .metric-label {
            font-size: 0.875rem;
            color: var(--text-muted);
            margin-top: 0.5rem;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
            border-right: 1px solid var(--border);
        }
        
        /* Button Styling */
        .stButton > button {
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            color: white !important;
            border: none;
            border-radius: 12px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px -10px var(--accent-primary);
        }
        
        /* Input Fields */
        .stTextInput > div > div > input {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            color: var(--text-primary);
            padding: 0.6rem 1rem;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: var(--accent-primary);
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
        }
        
        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
            background: transparent;
        }
        
        .stTabs [data-baseweb="tab"] {
            color: var(--text-secondary);
            font-weight: 600;
            padding: 0.5rem 1rem;
        }
        
        .stTabs [aria-selected="true"] {
            color: var(--accent-primary) !important;
            border-bottom-color: var(--accent-primary) !important;
        }
        
        /* Expander Styling */
        .streamlit-expanderHeader {
            background: var(--bg-card);
            border-radius: 12px;
            color: var(--text-primary);
            font-weight: 600;
        }
        
        /* Loading Spinner */
        .stSpinner > div {
            border-color: var(--accent-primary) transparent transparent transparent !important;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--bg-secondary);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--accent-primary);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-secondary);
        }
        </style>
        """
    else:
        css = """
        <style>
        /* ===== LIGHT THEME ===== */
        :root {
            --bg-primary: #f9fafb;
            --bg-secondary: #ffffff;
            --bg-card: #ffffff;
            --bg-hover: #f3f4f6;
            --text-primary: #111827;
            --text-secondary: #374151;
            --text-muted: #6b7280;
            --border: #e5e7eb;
            --accent-primary: #3b82f6;
            --accent-secondary: #8b5cf6;
            --accent-success: #10b981;
            --accent-warning: #f59e0b;
            --accent-danger: #ef4444;
            --shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.01);
        }
        
        .stApp {
            background: var(--bg-primary);
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-primary) !important;
        }
        
        p, li, span, div {
            color: var(--text-secondary) !important;
        }
        
        .quote-card {
            background: var(--bg-card);
            border-radius: 16px;
            padding: 1.75rem;
            margin: 1rem 0;
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .quote-card::before {
            content: '"';
            position: absolute;
            top: -20px;
            left: 10px;
            font-size: 120px;
            color: var(--accent-primary);
            opacity: 0.08;
            font-family: serif;
        }
        
        .quote-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 25px 30px -12px rgba(0, 0, 0, 0.15);
            border-color: var(--accent-primary);
        }
        
        .quote-text {
            font-size: 1.125rem;
            line-height: 1.6;
            color: var(--text-primary) !important;
            font-style: italic;
            margin-bottom: 1rem;
        }
        
        .quote-author {
            color: var(--accent-primary) !important;
            font-weight: 600;
        }
        
        .metric-card {
            background: var(--bg-card);
            border-radius: 16px;
            padding: 1.5rem;
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
            text-align: center;
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        
        [data-testid="stSidebar"] {
            background: var(--bg-secondary);
            border-right: 1px solid var(--border);
        }
        </style>
        """
    
    st.markdown(css, unsafe_allow_html=True)

# ============================================================================
# API UTILITIES
# ============================================================================

@st.cache_data(ttl=300)
def fetch_data(endpoint):
    """Cached API fetching"""
    
    API_BASE_URL = "http://localhost:8000"  # This should be correct
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def create_sentiment_gauge(sentiment_score):
    """Professional sentiment gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=sentiment_score,
        delta={'reference': 0, 'increasing': {'color': "#10b981"}, 'decreasing': {'color': "#ef4444"}},
        title={'text': "Sentiment Score", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [-1, 1], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#3b82f6", 'thickness': 0.3},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [-1, -0.5], 'color': 'rgba(239, 68, 68, 0.3)'},
                {'range': [-0.5, -0.1], 'color': 'rgba(245, 158, 11, 0.3)'},
                {'range': [-0.1, 0.1], 'color': 'rgba(156, 163, 175, 0.3)'},
                {'range': [0.1, 0.5], 'color': 'rgba(16, 185, 129, 0.3)'},
                {'range': [0.5, 1], 'color': 'rgba(16, 185, 129, 0.5)'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': sentiment_score
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "white" if st.session_state.theme == 'dark' else "black"}
    )
    return fig

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

def main():
    """Production dashboard main function"""
    
    # Load CSS theme
    load_css()
    
    # Sidebar Navigation
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/quotes.png", width=60)
        st.markdown("### ✨ Quote Intelligence")
        st.markdown("*AI-Powered Analytics*")
        st.markdown("---")
        
        selected = option_menu(
            menu_title=None,
            options=["📊 Overview", "🎭 Sentiment", "🎯 Recommendations", "👥 Authors", "🔍 Explorer"],
            icons=["house", "graph-up", "stars", "people", "search"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background": "transparent"},
                "icon": {"color": "#3b82f6", "font-size": "18px"},
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "5px 0",
                    "padding": "10px 15px",
                    "border-radius": "12px",
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, #3b82f6, #8b5cf6)",
                },
            }
        )
        
        st.markdown("---")
        
        # System status
        status = fetch_data("/stats")
        if status:
            st.success("✅ API Connected")
        else:
            st.error("⚠️ API Offline")
    
    # ========================================================================
    # OVERVIEW PAGE
    # ========================================================================
    
    if selected == "📊 Overview":
        st.markdown("# 📊 Dashboard Overview")
        st.markdown("*Real-time analytics and insights from your quote collection*")
        st.markdown("---")
        
        # Metrics Row
        stats = fetch_data("/stats")
        sentiment_stats = fetch_data("/stats/sentiment")
        
        if stats:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{stats.get('total_quotes', 0)}</div>
                    <div class="metric-label">Total Quotes</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{stats.get('total_authors', 0)}</div>
                    <div class="metric-label">Unique Authors</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{stats.get('average_quote_length', 0):.0f}</div>
                    <div class="metric-label">Avg Length (chars)</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                avg_sentiment = sentiment_stats.get('average_sentiment', 0) if sentiment_stats else 0
                sentiment_color = "positive" if avg_sentiment > 0 else "negative"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{avg_sentiment:.2f}</div>
                    <div class="metric-label">Avg Sentiment</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Charts Row
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏷️ Popular Tags")
            if stats and 'top_tags' in stats:
                tags_df = pd.DataFrame(stats['top_tags'])
                fig = px.bar(tags_df, x='tag', y='count', 
                            color='count',
                            color_continuous_scale='Blues',
                            title="Tag Distribution")
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font={'color': "white" if st.session_state.theme == 'dark' else "black"}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎭 Sentiment Distribution")
            if sentiment_stats and 'distribution' in sentiment_stats:
                dist = sentiment_stats['distribution']
                fig = px.pie(values=list(dist.values()), 
                            names=list(dist.keys()),
                            title="Quote Sentiment",
                            color_discrete_sequence=px.colors.sequential.Blues_r)
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font={'color': "white" if st.session_state.theme == 'dark' else "black"}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Recent Quotes
        st.markdown("### 📝 Recent Insights")
        quotes_data = fetch_data("/quotes?limit=6")
        if quotes_data and 'data' in quotes_data:
            cols = st.columns(2)
            for idx, quote in enumerate(quotes_data['data'][:6]):
                with cols[idx % 2]:
                    st.markdown(f"""
                    <div class="quote-card">
                        <div class="quote-text">“{quote['quote_text'][:200]}...”</div>
                        <div class="quote-author">— {quote['author']}</div>
                        <div class="quote-meta">
                            <span>🏷️ {quote['tags'][:30]}</span>
                            <span>📏 {quote['quote_length']} chars</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # ========================================================================
    # SENTIMENT ANALYSIS PAGE
    # ========================================================================
    
    elif selected == "🎭 Sentiment":
        st.markdown("# 🎭 Sentiment Analysis")
        st.markdown("*Understanding emotional tone across your collection*")
        st.markdown("---")
        
        sentiment_stats = fetch_data("/stats/sentiment")
        
        if sentiment_stats:
            col1, col2 = st.columns([1, 1.5])
            
            with col1:
                avg_sentiment = sentiment_stats.get('average_sentiment', 0)
                fig = create_sentiment_gauge(avg_sentiment)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### Sentiment Breakdown")
                dist = sentiment_stats.get('distribution', {})
                df_dist = pd.DataFrame(list(dist.items()), columns=['Sentiment', 'Count'])
                fig = px.bar(df_dist, x='Sentiment', y='Count', 
                            color='Sentiment',
                            color_discrete_map={
                                'very_positive': '#10b981',
                                'positive': '#34d399',
                                'neutral': '#9ca3af',
                                'negative': '#f59e0b',
                                'very_negative': '#ef4444'
                            })
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font={'color': "white" if st.session_state.theme == 'dark' else "black"}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Quote Analyzer
        st.markdown("### 🔍 Quote Sentiment Analyzer")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            quote_id = st.number_input("Quote ID", min_value=1, max_value=100, value=1)
            if st.button("Analyze Quote", use_container_width=True):
                with st.spinner("Analyzing sentiment..."):
                    time.sleep(0.5)
                    sentiment_data = fetch_data(f"/quotes/{quote_id}/sentiment")
                    if sentiment_data:
                        st.session_state['current_sentiment'] = sentiment_data
        
        with col2:
            if 'current_sentiment' in st.session_state:
                data = st.session_state['current_sentiment']
                sentiment = data['sentiment']
                emoji_map = {
                    'very_positive': '😊',
                    'positive': '🙂',
                    'neutral': '😐',
                    'negative': '😞',
                    'very_negative': '😢'
                }
                st.markdown(f"""
                <div class="quote-card">
                    <div class="quote-text">“{data['quote_text'][:300]}”</div>
                    <div class="quote-author">— {data['author']}</div>
                    <hr style="margin: 1rem 0; border-color: var(--border);">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <div>
                            <small>TextBlob Polarity</small><br>
                            <strong>{sentiment['textblob_polarity']:.3f}</strong>
                        </div>
                        <div>
                            <small>Subjectivity</small><br>
                            <strong>{sentiment['textblob_subjectivity']:.3f}</strong>
                        </div>
                        <div>
                            <small>VADER Score</small><br>
                            <strong>{sentiment['vader_compound']:.3f}</strong>
                        </div>
                        <div>
                            <small>Classification</small><br>
                            <strong>{emoji_map.get(sentiment['sentiment_label'], '')} {sentiment['sentiment_label']}</strong>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # ========================================================================
    # RECOMMENDATIONS PAGE
    # ========================================================================
    
    elif selected == "🎯 Recommendations":
        st.markdown("# 🎯 Smart Recommendations")
        st.markdown("*AI-powered quote discovery engine*")
        st.markdown("---")
        
        tab1, tab2, tab3 = st.tabs(["✨ Random Discovery", "🔍 Find Similar", "🏷️ Tag Search"])
        
        with tab1:
            if st.button("🎲 Discover Random Quote", use_container_width=True):
                with st.spinner("Finding inspiration..."):
                    time.sleep(0.5)
                    random_data = fetch_data("/recommendations/random")
                    if random_data:
                        st.session_state['random_discovery'] = random_data
            
            if 'random_discovery' in st.session_state:
                data = st.session_state['random_discovery']
                st.markdown(f"""
                <div class="quote-card">
                    <div class="quote-text">“{data['featured_quote']['quote_text']}”</div>
                    <div class="quote-author">— {data['featured_quote']['author']}</div>
                    <div class="quote-meta">🏷️ {data['featured_quote']['tags']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if 'you_may_also_like' in data:
                    st.markdown("#### 💡 You May Also Like")
                    cols = st.columns(2)
                    for idx, rec in enumerate(data['you_may_also_like'][:4]):
                        with cols[idx % 2]:
                            st.markdown(f"""
                            <div style="background: var(--bg-hover); padding: 1rem; border-radius: 12px; margin: 0.5rem 0;">
                                <div style="font-size: 0.9rem; font-style: italic;">“{rec['quote_text'][:120]}...”</div>
                                <div style="font-size: 0.8rem; color: var(--accent-primary); margin-top: 0.5rem;">— {rec['author']}</div>
                                <div style="font-size: 0.7rem; color: var(--text-muted);">Match: {rec['similarity_score']*100:.1f}%</div>
                            </div>
                            """, unsafe_allow_html=True)
        
        with tab2:
            col1, col2 = st.columns([1, 2])
            with col1:
                similar_id = st.number_input("Quote ID", min_value=1, max_value=100, key="similar_id")
                if st.button("Find Similar Quotes", use_container_width=True):
                    with st.spinner("Finding similar quotes..."):
                        similar_data = fetch_data(f"/quotes/{similar_id}/similar?limit=5")
                        if similar_data:
                            st.session_state['similar_quotes'] = similar_data
            
            with col2:
                if 'similar_quotes' in st.session_state:
                    data = st.session_state['similar_quotes']
                    st.markdown(f"""
                    <div class="quote-card">
                        <div style="font-size: 0.8rem; color: var(--text-muted);">Original Quote</div>
                        <div class="quote-text" style="font-size: 1rem;">“{data['original_quote']['text'][:200]}...”</div>
                        <div class="quote-author">— {data['original_quote']['author']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for rec in data['similar_quotes']:
                        st.markdown(f"""
                        <div style="background: var(--bg-hover); padding: 1rem; border-radius: 12px; margin: 0.5rem 0;">
                            <div style="font-size: 0.9rem; font-style: italic;">“{rec['quote_text']}”</div>
                            <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
                                <span style="font-size: 0.8rem; color: var(--accent-primary);">— {rec['author']}</span>
                                <span style="font-size: 0.7rem; color: var(--text-muted);">{rec['similarity_score']*100:.1f}% match</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        
        with tab3:
            tags_input = st.text_input("Enter tags (comma-separated)", "love,inspirational")
            if st.button("Search by Tags", use_container_width=True):
                with st.spinner("Searching quotes..."):
                    tag_data = fetch_data(f"/recommendations/by-tags?tags={tags_input}")
                    if tag_data:
                        st.session_state['tag_results'] = tag_data
            
            if 'tag_results' in st.session_state:
                data = st.session_state['tag_results']
                st.info(f"Found {data['total_found']} quotes matching your tags")
                for rec in data['recommendations'][:5]:
                    st.markdown(f"""
                    <div style="background: var(--bg-hover); padding: 1rem; border-radius: 12px; margin: 0.5rem 0;">
                        <div style="font-size: 0.9rem; font-style: italic;">“{rec['quote_text'][:200]}...”</div>
                        <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
                            <span style="font-size: 0.8rem; color: var(--accent-primary);">— {rec['author']}</span>
                            <span style="font-size: 0.7rem; color: var(--text-muted);">🏷️ {rec['tags'][:30]}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # ========================================================================
    # AUTHORS PAGE
    # ========================================================================
    
    elif selected == "👥 Authors":
        st.markdown("# 👥 Author Analytics")
        st.markdown("*Deep dive into author contributions and sentiment*")
        st.markdown("---")
        
        authors_data = fetch_data("/authors?limit=15")
        if authors_data:
            df_authors = pd.DataFrame(authors_data)
            fig = px.bar(df_authors.head(10), x='name', y='quote_count',
                        title="Top 10 Most Quoted Authors",
                        color='quote_count',
                        color_continuous_scale='Blues',
                        text='quote_count')
            fig.update_traces(textposition='outside')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': "white" if st.session_state.theme == 'dark' else "black"},
                xaxis_title="Author",
                yaxis_title="Number of Quotes"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 🔍 Author Sentiment Analysis")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            author_name = st.selectbox("Select Author", 
                                       [a['name'] for a in authors_data[:10]] if authors_data else ["Albert Einstein"])
            if st.button("Analyze Author", use_container_width=True):
                with st.spinner("Analyzing author sentiment..."):
                    author_sentiment = fetch_data(f"/authors/{author_name}/sentiment")
                    if author_sentiment:
                        st.session_state['author_analysis'] = author_sentiment
                        
                        # Get author's quotes
                        author_quotes = fetch_data(f"/authors/{author_name}/quotes?limit=5")
                        if author_quotes:
                            st.session_state['author_quotes'] = author_quotes
        
        with col2:
            if 'author_analysis' in st.session_state:
                data = st.session_state['author_analysis']
                emoji_map = {'positive': '🙂', 'neutral': '😐', 'negative': '😞', 
                           'very_positive': '😊', 'very_negative': '😢'}
                st.markdown(f"""
                <div class="quote-card">
                    <h3>{data['author']}</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0;">
                        <div>
                            <small>Total Quotes</small><br>
                            <strong style="font-size: 1.5rem;">{data['quote_count']}</strong>
                        </div>
                        <div>
                            <small>Avg Sentiment</small><br>
                            <strong style="font-size: 1.5rem;">{data['avg_sentiment']:.3f}</strong>
                        </div>
                        <div>
                            <small>Overall Tone</small><br>
                            <strong>{emoji_map.get(data['sentiment_label'], '')} {data['sentiment_label']}</strong>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if 'author_quotes' in st.session_state:
                    st.markdown("#### 📝 Notable Quotes")
                    for quote in st.session_state['author_quotes'][:3]:
                        st.markdown(f"""
                        <div style="background: var(--bg-hover); padding: 1rem; border-radius: 12px; margin: 0.5rem 0;">
                            <div style="font-size: 0.9rem; font-style: italic;">“{quote['quote_text'][:200]}...”</div>
                            <div class="quote-meta" style="margin-top: 0.5rem;">🏷️ {quote['tags']}</div>
                        </div>
                        """, unsafe_allow_html=True)
    
    # ========================================================================
    # EXPLORER PAGE
    # ========================================================================
    
    elif selected == "🔍 Explorer":
        st.markdown("# 🔍 Quote Explorer")
        st.markdown("*Search and browse through your quote collection*")
        st.markdown("---")
        
        # Search
        st.markdown("### 🔎 Search Quotes")
        search_term = st.text_input("Enter keyword", "life", placeholder="e.g., love, inspirational, wisdom...")
        if search_term:
            with st.spinner(f"Searching for '{search_term}'..."):
                search_results = fetch_data(f"/search?q={search_term}")
                if search_results:
                    st.success(f"Found {search_results['total']} quotes containing '{search_term}'")
                    for result in search_results['results'][:10]:
                        with st.expander(f"📖 {result['author']} - {result['tags'][:50]}"):
                            st.markdown(f"""
                            <div style="padding: 1rem;">
                                <div style="font-size: 1rem; font-style: italic; line-height: 1.6;">“{result['quote_text']}”</div>
                                <div style="margin-top: 1rem;">
                                    <span style="background: var(--accent-primary); padding: 0.2rem 0.6rem; border-radius: 20px; font-size: 0.7rem;">ID: {result['id']}</span>
                                    <span style="margin-left: 0.5rem;">📏 {result['quote_length']} chars</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Browse All
        st.markdown("### 📚 Browse All Quotes")
        page_num = st.number_input("Page", min_value=1, value=1, step=1)
        quotes_data = fetch_data(f"/quotes?skip={(page_num-1)*20}&limit=20")
        
        if quotes_data and 'data' in quotes_data:
            st.info(f"Page {page_num} of {quotes_data['total_pages']} | Total: {quotes_data['total']} quotes")
            
            for quote in quotes_data['data']:
                st.markdown(f"""
                <div style="background: var(--bg-hover); padding: 1rem; border-radius: 12px; margin: 0.5rem 0; transition: all 0.2s ease;">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <div style="font-size: 0.8rem; color: var(--accent-primary); font-weight: 600;">#{quote['id']} · {quote['author']}</div>
                            <div style="font-size: 0.9rem; font-style: italic; margin-top: 0.3rem;">“{quote['quote_text'][:200]}...”</div>
                            <div style="font-size: 0.7rem; color: var(--text-muted); margin-top: 0.5rem;">🏷️ {quote['tags']}</div>
                        </div>
                        <div style="text-align: right; font-size: 0.7rem; color: var(--text-muted);">
                            {quote['quote_length']} chars
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()