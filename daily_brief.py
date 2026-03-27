import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from rag import query, query_media

# ── EMAIL CONFIG ─────────────────────────────────────────
EMAIL_SENDER = "shruti.mesh1@gmail.com"        # Your Gmail
EMAIL_PASSWORD = "kvgy odwr xhxx hbgg"    # Your 16-char app password
EMAIL_RECEIVER = "shruti.mesh1@gmail.com"      # Where to send (can be same)

# ── QUESTIONS ────────────────────────────────────────────
FINTECH_QUESTIONS = [
    "What are the key risks facing UK neobanks right now?",
    "What is the latest news about Monzo or Revolut?",
    "What regulatory changes are affecting UK fintech?"
]

MEDIA_QUESTIONS = [
    "What are the latest trends in digital news subscriptions?",
    "How is AI changing newsrooms and journalism?",
]

def send_email(subject: str, body: str):
    """Send the daily brief via Gmail."""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        # Plain text version
        text_part = MIMEText(body, "plain")
        msg.attach(text_part)

        # Send via Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

        print(f"✅ Email sent to {EMAIL_RECEIVER}")
        return True

    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False

def generate_daily_brief():
    """Generate and save a daily intelligence briefing."""
    print(f"\n{'='*60}")
    print(f"PRISM DAILY BRIEF — {datetime.now().strftime('%A %d %B %Y, %H:%M')}")
    print(f"{'='*60}\n")

    brief = []
    brief.append(f"🔷 PRISM DAILY INTELLIGENCE BRIEF")
    brief.append(f"Generated: {datetime.now().strftime('%A %d %B %Y at %H:%M')}")
    brief.append("=" * 60)
    brief.append("")

    # Fintech section
    brief.append("🏦 FINTECH INTELLIGENCE")
    brief.append("-" * 40)
    for question in FINTECH_QUESTIONS:
        print(f"Querying: {question}")
        try:
            response = query(question)
            # Strip markdown for email
            clean_response = response.replace("**", "").replace("##", "")
            brief.append(f"\n{question}")
            brief.append(clean_response)
            brief.append("")
        except Exception as e:
            brief.append(f"\n{question}")
            brief.append(f"Query failed: {e}")
            brief.append("")

    # Media section
    brief.append("=" * 60)
    brief.append("📰 MEDIA INTELLIGENCE")
    brief.append("-" * 40)
    for question in MEDIA_QUESTIONS:
        print(f"Querying: {question}")
        try:
            response = query_media(question)
            clean_response = response.replace("**", "").replace("##", "")
            brief.append(f"\n{question}")
            brief.append(clean_response)
            brief.append("")
        except Exception as e:
            brief.append(f"\n{question}")
            brief.append(f"Query failed: {e}")
            brief.append("")

    brief.append("=" * 60)
    brief.append("Powered by Prism — AI Intelligence Platform")

    full_brief = "\n".join(brief)

    # Save as markdown file
    brief_dir = os.path.join(os.path.dirname(__file__), "briefs")
    os.makedirs(brief_dir, exist_ok=True)
    filename = f"brief_{datetime.now().strftime('%Y_%m_%d')}.md"
    filepath = os.path.join(brief_dir, filename)
    with open(filepath, 'w') as f:
        f.write(full_brief)
    print(f"\n✅ Brief saved: {filepath}")

    # Send email
    subject = f"🔷 Prism Daily Brief — {datetime.now().strftime('%A %d %B %Y')}"
    send_email(subject, full_brief)

    return filepath

def run_scheduler():
    """Run the daily brief on a schedule."""
    print("🔷 Prism Scheduler Started")
    print("Daily brief scheduled for 08:00 every morning")
    print("Press Ctrl+C to stop\n")

    schedule.every().day.at("08:00").do(generate_daily_brief)

    print("Running brief now for testing...")
    generate_daily_brief()

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    run_scheduler()