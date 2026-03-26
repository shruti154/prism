import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
from config import NEWS_API_KEY, NEWS_LANGUAGE, NEWS_PAGE_SIZE

def fetch_news(query: str) -> list:
    """Fetch live news articles relevant to a query."""
    print(f"Fetching live news for: {query}")
    
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": NEWS_LANGUAGE,
        "pageSize": NEWS_PAGE_SIZE,
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        articles = []
        for article in data.get("articles", []):
            articles.append({
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "source": article.get("source", {}).get("name", ""),
                "published": article.get("publishedAt", ""),
                "url": article.get("url", "")
            })
        
        print(f"Found {len(articles)} articles.")
        return articles
        
    except Exception as e:
        print(f"News fetch failed: {e}")
        return []

def format_news_context(articles: list) -> str:
    """Format news articles into a readable context string."""
    if not articles:
        return "No recent news found."
    
    context = "LIVE NEWS SIGNALS:\n\n"
    for i, article in enumerate(articles, 1):
        context += f"{i}. {article['title']}\n"
        context += f"   Source: {article['source']}\n"
        context += f"   Published: {article['published'][:10]}\n"
        if article['description']:
            context += f"   Summary: {article['description']}\n"
        context += "\n"
    
    return context

if __name__ == "__main__":
    # Test the agent
    test_queries = [
        "Monzo Revolut UK neobank",
        "UK fintech regulation 2026",
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print('='*60)
        articles = fetch_news(query)
        print(format_news_context(articles))