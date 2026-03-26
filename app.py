import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import streamlit as st
from rag import query, query_media

# Page config
st.set_page_config(
    page_title="Prism — Intelligence Platform",
    page_icon="🔷",
    layout="wide"
)

# Header
st.markdown("""
    <h1 style='color: #4A90D9;'>🔷 Prism</h1>
    <p style='font-size: 18px; color: #888;'>
        AI Intelligence Platform — RAG + Live News + Claude
    </p>
    <hr/>
""", unsafe_allow_html=True)

# Mode selector
mode = st.radio(
    "Select Mode",
    ["🏦 Fintech", "📰 Media"],
    horizontal=True
)

# Sidebar
with st.sidebar:
    if mode == "🏦 Fintech":
        st.markdown("### 📂 Fintech Knowledge Base")
        st.success("9 documents loaded")
        st.markdown("- Monzo Annual Report 2024")
        st.markdown("- Revolut Annual Reports 2023/24")
        st.markdown("- 3 Monzo blog posts")
        st.markdown("- 3 Revolut blog posts")
        st.markdown("---")
        st.markdown("### 💡 Example Questions")
        st.markdown("- What was Revolut's revenue in 2023?")
        st.markdown("- What are the key risks facing UK neobanks?")
        st.markdown("- How is Monzo approaching profitability?")
        st.markdown("- What does Revolut becoming a bank mean?")
    else:
        st.markdown("### 📂 Media Knowledge Base")
        st.success("5 documents loaded")
        st.markdown("- Guardian Annual Report 2024/25")
        st.markdown("- Reuters Institute Digital News Report 2024")
        st.markdown("- 3 Press Gazette articles")
        st.markdown("---")
        st.markdown("### 💡 Example Questions")
        st.markdown("- How are news publishers growing digital subscriptions?")
        st.markdown("- What is the Guardian's digital revenue strategy?")
        st.markdown("- How is AI being used in newsrooms?")
        st.markdown("- What are the key trends in digital media 2024?")

    st.markdown("---")
    st.markdown("### ⚡ Live Agent")
    st.success("NewsAPI connected")

# Main interface
st.markdown(f"### Ask Prism — {'Fintech' if mode == '🏦 Fintech' else 'Media'} Mode")

question = st.text_input(
    label="Your question",
    placeholder="Ask a question about your selected industry...",
    label_visibility="collapsed"
)

col1, col2 = st.columns([1, 5])
with col1:
    ask_button = st.button("🔍 Analyse", type="primary")

if ask_button and question:
    with st.spinner("Prism is thinking — querying documents and live news..."):
        if mode == "🏦 Fintech":
            response = query(question)
        else:
            response = query_media(question)

    st.markdown("---")
    st.markdown("### 📊 Analyst Brief")
    st.markdown(response)
    st.markdown("---")
    st.caption("Powered by Claude + RAG + NewsAPI | Prism v1.0")

elif ask_button and not question:
    st.warning("Please enter a question first.")