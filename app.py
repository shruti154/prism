import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import streamlit as st
import pandas as pd
from rag import query, query_media
from tracker import init_db, get_all_queries, get_stats

# Initialise DB
init_db()

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

# Main tabs
tab1, tab2, tab3 = st.tabs(["🏦 Fintech", "📰 Media", "📊 LLM Dashboard"])

# ── FINTECH TAB ──────────────────────────────────────────
with tab1:
    col1, col2 = st.columns([1, 3])

    with col1:
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
        st.markdown("- What was Revolut's revenue in 2023?")
        st.markdown("- What are the key risks facing UK neobanks?")
        st.markdown("- How is Monzo approaching profitability?")
        st.markdown("- What does Revolut becoming a bank mean?")

    with col2:
        st.markdown("### Ask Prism — Fintech Mode")
        question_ft = st.text_input(
            "Fintech question",
            placeholder="e.g. What was Revolut's revenue in 2023?",
            label_visibility="collapsed",
            key="ft_input"
        )
        if st.button("🔍 Analyse", type="primary", key="ft_btn"):
            if question_ft:
                with st.spinner("Querying documents and live news..."):
                    response = query(question_ft)
                st.markdown("---")
                st.markdown("### 📊 Analyst Brief")
                st.markdown(response)
                st.markdown("---")
                st.caption("Powered by Claude + RAG + NewsAPI | Prism v1.0")
            else:
                st.warning("Please enter a question first.")

# ── MEDIA TAB ────────────────────────────────────────────
with tab2:
    col1, col2 = st.columns([1, 3])

    with col1:
        st.markdown("### 📂 Knowledge Base")
        st.success("5 documents loaded")
        st.markdown("- Guardian Annual Report 2024/25")
        st.markdown("- Reuters Institute Digital News Report 2024")
        st.markdown("- 3 Press Gazette articles")
        st.markdown("---")
        st.markdown("### ⚡ Live Agent")
        st.success("NewsAPI connected")
        st.markdown("---")
        st.markdown("### 💡 Example Questions")
        st.markdown("- How are publishers growing digital subscriptions?")
        st.markdown("- What is the Guardian's digital revenue strategy?")
        st.markdown("- How is AI being used in newsrooms?")
        st.markdown("- What are the key trends in digital media 2024?")

    with col2:
        st.markdown("### Ask Prism — Media Mode")
        question_med = st.text_input(
            "Media question",
            placeholder="e.g. How are news publishers growing subscriptions?",
            label_visibility="collapsed",
            key="med_input"
        )
        if st.button("🔍 Analyse", type="primary", key="med_btn"):
            if question_med:
                with st.spinner("Querying documents and live news..."):
                    response = query_media(question_med)
                st.markdown("---")
                st.markdown("### 📊 Analyst Brief")
                st.markdown(response)
                st.markdown("---")
                st.caption("Powered by Claude + RAG + NewsAPI | Prism v1.0")
            else:
                st.warning("Please enter a question first.")

# ── LLM DASHBOARD TAB ────────────────────────────────────
with tab3:
    st.markdown("### 📊 LLM Management Dashboard")
    st.markdown("Real-time visibility into Prism's AI usage, cost, and performance.")
    st.markdown("---")

    stats = get_stats()
    queries = get_all_queries()

    if stats["total_queries"] == 0:
        st.info("No queries logged yet. Ask Prism some questions first, then come back here!")
    else:
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Queries", stats["total_queries"])
        with col2:
            st.metric("Total Cost", f"${stats['total_cost']:.4f}")
        with col3:
            st.metric("Avg Response Time", f"{stats['avg_response_time']}s")
        with col4:
            st.metric("Avg Cost/Query", f"${stats['avg_cost']:.6f}")

        st.markdown("---")

        # Mode breakdown
        st.markdown("#### Queries by Mode")
        if stats["mode_breakdown"]:
            mode_df = pd.DataFrame(
                stats["mode_breakdown"],
                columns=["Mode", "Count"]
            )
            st.bar_chart(mode_df.set_index("Mode"))

        st.markdown("---")

        # Query history table
        st.markdown("#### Query History")
        if queries:
            df = pd.DataFrame(queries, columns=[
                "Timestamp", "Mode", "Question",
                "Input Tokens", "Output Tokens",
                "Cost (USD)", "Response Time (s)"
            ])
            df["Timestamp"] = pd.to_datetime(df["Timestamp"]).dt.strftime("%Y-%m-%d %H:%M")
            df["Cost (USD)"] = df["Cost (USD)"].apply(lambda x: f"${x:.6f}")
            st.dataframe(df, use_container_width=True)

        st.markdown("---")

        # Cost over time
        st.markdown("#### Cost Per Query Over Time")
        if queries:
            cost_df = pd.DataFrame(queries, columns=[
                "Timestamp", "Mode", "Question",
                "Input Tokens", "Output Tokens",
                "Cost", "Response Time"
            ])
            cost_df["Timestamp"] = pd.to_datetime(cost_df["Timestamp"])
            cost_df = cost_df.sort_values("Timestamp")
            st.line_chart(cost_df.set_index("Timestamp")["Cost"])

        st.caption("Model: Claude Sonnet | Pricing: $3/M input tokens, $15/M output tokens")