# 🔷 Prism — Fintech Intelligence Platform

> AI-powered analyst platform combining RAG, live news agents, 
> and Claude to generate structured fintech intelligence briefs.

## What is Prism?

Prism is an agentic intelligence platform that answers complex 
fintech questions by combining two sources simultaneously:

1. **Document Knowledge** — RAG pipeline on real fintech documents 
   (Monzo & Revolut annual reports, regulatory filings, blog posts)
2. **Live Signals** — Real-time news agent pulling the latest 
   market developments

Claude synthesises both into structured analyst briefs — the kind 
a junior analyst would spend hours producing manually.

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Claude (Anthropic) |
| RAG Framework | LlamaIndex |
| Vector Database | ChromaDB |
| Embeddings | HuggingFace (BAAI/bge-small-en-v1.5) |
| Live News | NewsAPI |
| Frontend | Streamlit |
| Language | Python 3.10 |

## Features

- RAG pipeline on real fintech documents
- Live news agent with real-time signal retrieval
- Structured analyst briefs with Summary, Key Insights, Live Signals
- Clean Streamlit dashboard
- Honest sourcing — never hallucinates, cites sources

## Project Structure
```
prism/
├── data/documents/     # Fintech knowledge base
├── src/
│   ├── config.py      # Centralised configuration
│   ├── ingest.py      # Document embedding pipeline
│   ├── rag.py         # RAG + agent synthesis
│   └── agent.py       # Live news agent
├── app.py             # Streamlit dashboard
└── requirements.txt
```

## Setup

1. Clone the repo
2. Create a conda environment:
```bash
conda create -n prism python=3.10
conda activate prism
pip install -r requirements.txt
```

3. Add your API keys to `.env`:
```
ANTHROPIC_API_KEY=your_key
NEWS_API_KEY=your_key
```

4. Ingest documents:
```bash
cd src
python ingest.py
```

5. Run the dashboard:
```bash
streamlit run app.py
```

## Example Questions

- What are the key risks facing UK neobanks?
- How is Monzo approaching profitability?
- What does Revolut becoming a bank mean for customers?
- How do neobanks protect customer funds?

## Built By

Shruti 
[GitHub](https://github.com/shruti154)

---
*Powered by Claude + LlamaIndex + ChromaDB + NewsAPI*