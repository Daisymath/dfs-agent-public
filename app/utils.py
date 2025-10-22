import os
import csv
from datetime import datetime

LOG_FILE = "logs.csv"

def log_interaction(user_query, ai_response):
    """Append interactions to a CSV log."""
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "query", "response"])
        writer.writerow([datetime.now().isoformat(), user_query, ai_response])

def clean_sql_output(ai_response_text: str) -> str:
    """Remove code fences or prefixes from AI SQL output."""
    sql = ai_response_text.lstrip().removeprefix("sql").strip()
    if sql.startswith("```sql"):
        sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql

def load_schema_prompt() -> str:
    """Load schema and context for the AI model."""
    with open("app/schema_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()
