import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import time
import chromadb
from anthropic import Anthropic as AnthropicClient
from config import (
    ANTHROPIC_API_KEY, CHROMA_PERSIST_DIR,
    LLM_MODEL, TOP_K_RESULTS
)
from agent import fetch_news, format_news_context
from tracker import init_db, log_query

ANALYST_PROMPT = """You are Prism, a senior fintech analyst.
You have been given real excerpts from fintech company documents and live news.

Your job is to answer the question using ONLY the provided context.
Be specific — cite exact figures, percentages, and facts from the documents.
Be concise — no padding, no generic statements.

Format exactly like this:

**Summary:** (2-3 sentences with specific facts and figures)

**Key Insights:**
- (specific insight with exact data point)
- (specific insight with exact data point)
- (specific insight with exact data point)

**Live Signals:** (what live news adds — or "No relevant live signals found")

**Sources:** (which documents contained this information)

DOCUMENT EXCERPTS:
{doc_context}

LIVE NEWS:
{news_context}

Question: {query}
"""

MEDIA_PROMPT = """You are Prism, a senior media and publishing analyst.
You have been given real excerpts from media industry documents and live news.

Answer the question using ONLY the provided context.
Be specific — cite exact figures, percentages, and facts.
Be concise — no padding, no generic statements.

Format exactly like this:

**Summary:** (2-3 sentences with specific facts and figures)

**Key Insights:**
- (specific insight with exact data point)
- (specific insight with exact data point)
- (specific insight with exact data point)

**Live Signals:** (what live news adds — or "No relevant live signals found")

**Sources:** (which documents contained this information)

DOCUMENT EXCERPTS:
{doc_context}

LIVE NEWS:
{news_context}

Question: {query}
"""

def load_client():
    """Load fintech ChromaDB client."""
    print("Loading Prism's fintech knowledge base...")
    chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    collection = chroma_client.get_or_create_collection("prism_fintech")
    print(f"Knowledge base loaded. {collection.count()} chunks available.")
    return collection

def query(question: str) -> str:
    """Query Prism fintech knowledge base."""
    init_db()
    start_time = time.time()

    collection = load_client()
    results = collection.query(
        query_texts=[question],
        n_results=TOP_K_RESULTS
    )

    doc_context = ""
    for i, doc in enumerate(results['documents'][0]):
        doc_context += f"\n[Excerpt {i+1}]:\n{doc}\n"

    search_query = question.replace("What are", "").replace("What does", "").replace("How is", "").replace("?", "").strip()[:50]
    news_articles = fetch_news(search_query)
    news_context = format_news_context(news_articles)

    client = AnthropicClient(api_key=ANTHROPIC_API_KEY)

    prompt = ANALYST_PROMPT.format(
        doc_context=doc_context,
        news_context=news_context,
        query=question
    )

    message = client.messages.create(
        model=LLM_MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    response = message.content[0].text
    response_time = time.time() - start_time

    log_query(
        mode="fintech",
        question=question,
        response=response,
        input_tokens=message.usage.input_tokens,
        output_tokens=message.usage.output_tokens,
        response_time=response_time
    )

    return response

def query_media(question: str) -> str:
    """Query Prism media knowledge base."""
    init_db()
    start_time = time.time()

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MEDIA_CHROMA_DIR = os.path.join(BASE_DIR, "chroma_media_db")

    chroma_client = chromadb.PersistentClient(path=MEDIA_CHROMA_DIR)
    collection = chroma_client.get_or_create_collection("prism_media")

    results = collection.query(
        query_texts=[question],
        n_results=TOP_K_RESULTS
    )

    doc_context = ""
    for i, doc in enumerate(results['documents'][0]):
        doc_context += f"\n[Excerpt {i+1}]:\n{doc}\n"

    search_query = question.replace("What are", "").replace("What does", "").replace("How is", "").replace("?", "").strip()[:50]
    news_articles = fetch_news(search_query)
    news_context = format_news_context(news_articles)

    client = AnthropicClient(api_key=ANTHROPIC_API_KEY)

    prompt = MEDIA_PROMPT.format(
        doc_context=doc_context,
        news_context=news_context,
        query=question
    )

    message = client.messages.create(
        model=LLM_MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    response = message.content[0].text
    response_time = time.time() - start_time

    log_query(
        mode="media",
        question=question,
        response=response,
        input_tokens=message.usage.input_tokens,
        output_tokens=message.usage.output_tokens,
        response_time=response_time
    )

    return response

if __name__ == "__main__":
    questions = [
        "What was Revolut's revenue in 2023 and how did it grow?",
        "What are the key risks facing UK neobanks?",
    ]

    for q in questions:
        print(f"\n{'='*60}")
        print(f"QUESTION: {q}")
        print('='*60)
        print(query(q))