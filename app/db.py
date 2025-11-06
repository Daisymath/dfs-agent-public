import pandas as pd
from sqlalchemy import create_engine, event, text
import streamlit as st

pg = st.secrets.get("postgres", {})

DATABASE_URL = (
    f"postgresql+psycopg2://{pg['user']}:{pg['password']}"
    f"@{pg['host']}:{pg['port']}/{pg['dbname']}?sslmode=require"
)

@st.cache_resource
def get_engine():
    """Create and cache a SQLAlchemy engine."""
    return create_engine(DATABASE_URL, pool_pre_ping=True)

engine = get_engine()

@event.listens_for(engine, "connect")
def set_session_settings(dbapi_connection, connection_record):
    """Apply safety and timeout settings to DB sessions."""
    with dbapi_connection.cursor() as cur:
        cur.execute("SET SESSION transaction_read_only = on;")
        cur.execute("SET SESSION statement_timeout = '15s';")
        cur.execute("SET SESSION lock_timeout = '2s';")
        cur.execute("SET SESSION idle_in_transaction_session_timeout = '5s';")


def safe_execute_query(sql_query):
    # Normalize query text
    normalized = sql_query.strip().lower()
    
    # Only allow SELECT statements
    if not (normalized.startswith("select") or normalized.startswith("with")):
        raise ValueError("Unsafe query blocked: only SELECT statements are allowed.")

    with engine.connect() as conn:
        df = pd.read_sql_query(sql_query, conn)
    return df

def get_latest_week(table_name):
    query = text(f"SELECT MAX(week) AS latest_week FROM {table_name};")
    with engine.connect() as conn:
        result = conn.execute(query).scalar()
    return result if result else "N/A"

