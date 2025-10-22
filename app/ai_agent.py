import streamlit as st
from google import genai
from app.utils import load_schema_prompt, clean_sql_output, log_interaction

api_key = st.secrets.get("google", {}).get("api_key")
if not api_key:
    raise ValueError("Missing GOOGLE_API_KEY in secrets.toml")

client = genai.Client(api_key=api_key)

def generate_sql_from_user_input(user_query: str) -> str:
    """Use Gemini to generate SQL from the user's natural language query."""
    schema_prompt = load_schema_prompt()
    prompt = f"{schema_prompt}\n\nUser question: {user_query}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    ai_response_text = response.text.strip()
    log_interaction(user_query, ai_response_text)
    return clean_sql_output(ai_response_text)
