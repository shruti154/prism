import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import chromadb
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.anthropic import Anthropic
from config import (
    ANTHROPIC_API_KEY, CHROMA_PERSIST_DIR,
    EMBED_MODEL, LLM_MODEL, TOP_K_RESULTS
)
from agent import fetch_news, format_news_context

ANALYST_PROMPT = """You are Prism, a senior fintech analyst assistant.
You have access to two sources of information:

1. DOCUMENT KNOWLEDGE: Excerpts from real fintech company reports and blogs
2. LIVE NEWS: Recent news articles fetched in real time

Using BOTH sources, answer the following question in a structured 
analyst brief.

Format your response exactly like this:

**Summary:** (2-3 sentences combining document knowledge and live signals)

**Key Insights:**
- (insight 1)
- (insight 2)
- (insight 3)

**Live Signals:** (what the news is saying right now)

**Source Context:** (mention which documents and news sources informed this)

Important: Clearly distinguish between what comes from documents 
vs what comes from live news. Never guess or hallucinate.

DOCUMENT CONTEXT:
{doc_context}

LIVE NEWS CONTEXT:
{news_context}

Question: {query}
"""

@st.cache_resource
def load_index():
    """Load the existing ChromaDB index."""
    print("Loading Prism's knowledge base...")
    embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL)
    llm = Anthropic(model=LLM_MODEL, api_key=ANTHROPIC_API_KEY)
    Settings.embed_model = embed_model
    Settings.llm = llm

    chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    chroma_collection = chroma_client.get_or_create_collection("prism_fintech")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store)
    print("Knowledge base loaded.")
    return index

def query(question: str) -> str:
    """Query Prism using both RAG and live news."""
    
    # Step 1 — Get document context from RAG
    index = load_index()
    query_engine = index.as_query_engine(
        similarity_top_k=TOP_K_RESULTS
    )
    doc_response = query_engine.query(question)
    doc_context = str(doc_response)
    
    # Step 2 — Get live news context from agent
    # Extract short search query from the full question
    search_query = question.replace("What are", "").replace("What does", "").replace("How is", "").replace("?", "").strip()[:50]
    news_articles = fetch_news(search_query)
    news_context = format_news_context(news_articles)
    
    # Step 3 — Synthesise both with Claude
    from anthropic import Anthropic as AnthropicClient
    client = AnthropicClient(api_key=ANTHROPIC_API_KEY)
    
    final_prompt = ANALYST_PROMPT.format(
        doc_context=doc_context,
        news_context=news_context,
        query=question
    )
    
    message = client.messages.create(
        model=LLM_MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": final_prompt}]
    )
    
    return message.content[0].text

if __name__ == "__main__":
    questions = [
        "What are the key risks facing UK neobanks?",
        "What does it mean that Revolut is now a bank in the UK?",
    ]

    for q in questions:
        print(f"\n{'='*60}")
        print(f"QUESTION: {q}")
        print('='*60)
        print(query(q))
        print()