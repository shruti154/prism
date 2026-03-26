import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import schedule
import time
from datetime import datetime
from rag import query, query_media

# Questions Prism asks itself every morning
FINTECH_QUESTIONS = [
    "What are the key risks facing UK neobanks right now?",
    "What is the latest news about Monzo or Revolut?",
    "What regulatory changes are affecting UK fintech?"
]

MEDIA_QUESTIONS = [
    "What are the latest trends in digital news subscriptions?",
    "How is AI changing newsrooms and journalism?",
]

def generate_daily_brief():
    """Generate and save a daily intelligence briefing."""
    print(f"\n{'='*60}")
    print(f"PRISM DAILY BRIEF — {datetime.now().strftime('%A %d %B %Y, %H:%M')}")
    print(f"{'='*60}\n")

    brief = []
    brief.append(f"# 🔷 Prism Daily Intelligence Brief")
    brief.append(f"**Generated:** {datetime.now().strftime('%A %d %B %Y at %H:%M')}\n")
    brief.append("---\n")

    # Fintech section
    brief.append("## 🏦 Fintech Intelligence\n")
    for question in FINTECH_QUESTIONS:
        print(f"Querying: {question}")
        try:
            response = query(question)
            brief.append(f"### {question}\n")
            brief.append(response)
            brief.append("\n---\n")
        except Exception as e:
            brief.append(f"### {question}\n")
            brief.append(f"Query failed: {e}\n")
            brief.append("\n---\n")

    # Media section
    brief.append("## 📰 Media Intelligence\n")
    for question in MEDIA_QUESTIONS:
        print(f"Querying: {question}")
        try:
            response = query_media(question)
            brief.append(f"### {question}\n")
            brief.append(response)
            brief.append("\n---\n")
        except Exception as e:
            brief.append(f"### {question}\n")
            brief.append(f"Query failed: {e}\n")
            brief.append("\n---\n")

    # Save the brief
    brief_dir = os.path.join(os.path.dirname(__file__), "briefs")
    os.makedirs(brief_dir, exist_ok=True)
    
    filename = f"brief_{datetime.now().strftime('%Y_%m_%d')}.md"
    filepath = os.path.join(brief_dir, filename)
    
    with open(filepath, 'w') as f:
        f.write('\n'.join(brief))
    
    print(f"\n✅ Brief saved: {filepath}")
    return filepath

def run_scheduler():
    """Run the daily brief on a schedule."""
    print("🔷 Prism Scheduler Started")
    print("Daily brief scheduled for 08:00 every morning")
    print("Press Ctrl+C to stop\n")
    
    # Schedule for 8am every day
    schedule.every().day.at("08:00").do(generate_daily_brief)
    
    # Also run immediately for testing
    print("Running brief now for testing...")
    generate_daily_brief()
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    run_scheduler()