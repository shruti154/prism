import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "prism_tracker.db")

def init_db():
    """Create the tracking database and table if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS query_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            mode TEXT NOT NULL,
            question TEXT NOT NULL,
            response_length INTEGER,
            input_tokens INTEGER,
            output_tokens INTEGER,
            estimated_cost_usd REAL,
            response_time_seconds REAL
        )
    """)
    conn.commit()
    conn.close()
    print("Tracking database ready.")

def log_query(mode: str, question: str, response: str, 
              input_tokens: int, output_tokens: int, 
              response_time: float):
    """Log a query to the database."""
    # Claude Sonnet pricing: $3 per million input, $15 per million output
    input_cost = (input_tokens / 1_000_000) * 3.0
    output_cost = (output_tokens / 1_000_000) * 15.0
    total_cost = input_cost + output_cost

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO query_log 
        (timestamp, mode, question, response_length, 
         input_tokens, output_tokens, estimated_cost_usd, response_time_seconds)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        mode,
        question,
        len(response),
        input_tokens,
        output_tokens,
        round(total_cost, 6),
        round(response_time, 2)
    ))
    conn.commit()
    conn.close()

def get_all_queries():
    """Retrieve all logged queries."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, mode, question, input_tokens, 
               output_tokens, estimated_cost_usd, response_time_seconds
        FROM query_log 
        ORDER BY timestamp DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_stats():
    """Get summary statistics."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM query_log")
    total_queries = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(estimated_cost_usd) FROM query_log")
    total_cost = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT AVG(response_time_seconds) FROM query_log")
    avg_response_time = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT AVG(estimated_cost_usd) FROM query_log")
    avg_cost = cursor.fetchone()[0] or 0
    
    cursor.execute("""
        SELECT mode, COUNT(*) as count 
        FROM query_log 
        GROUP BY mode
    """)
    mode_breakdown = cursor.fetchall()
    
    conn.close()
    
    return {
        "total_queries": total_queries,
        "total_cost": round(total_cost, 4),
        "avg_response_time": round(avg_response_time, 2),
        "avg_cost": round(avg_cost, 6),
        "mode_breakdown": mode_breakdown
    }

if __name__ == "__main__":
    init_db()
    print("Database initialised at:", DB_PATH)