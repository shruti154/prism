import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import streamlit as st
from rag import query

# Page config
st.set_page_config(
    page_title="Prism — Fintech Intelligence",
    page_icon="🔷",
    layout="wide"
)

# Header
st.markdown("""
    <h1 style='color: #4A90D9;'>🔷 Prism</h1>
    <p style='font-size: 18px; color: #888;'>
        Fintech Intelligence Platform — RAG + Live News
    </p>
    <hr/>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📂 Knowledge Base")
    st.success("9 documents loaded")
    st.markdown("- Monzo Annual Report 2024")
    st.markdown("- Revolut Annual Reports 2023/24")
    st.markdown("- 3 Monzo blog posts")
    st.markdown("- 3 Revolut blog posts")
    st.markdown("---")
    st.markdown("### ⚡ Live Agent")
    st.success("NewsAPI connected")
    st.markdown("---")
    st.markdown("### 💡 Example Questions")
    st.markdown("- What are the key risks facing UK neobanks?")
    st.markdown("- How is Monzo approaching profitability?")
    st.markdown("- What does Revolut becoming a bank mean?")
    st.markdown("- How do neobanks protect customer funds?")

# Main interface
st.markdown("### Ask Prism")

question = st.text_input(
    label="Your question",
    placeholder="e.g. What are the key risks facing UK neobanks?",
    label_visibility="collapsed"
)

col1, col2 = st.columns([1, 5])
with col1:
    ask_button = st.button("🔍 Analyse", type="primary")

if ask_button and question:
    with st.spinner("Prism is thinking — querying documents and live news..."):
        response = query(question)
    
    st.markdown("---")
    st.markdown("### 📊 Analyst Brief")
    st.markdown(response)
    
    st.markdown("---")
    st.caption("Powered by Claude + RAG + NewsAPI | Prism v1.0")

elif ask_button and not question:
    st.warning("Please enter a question first.")