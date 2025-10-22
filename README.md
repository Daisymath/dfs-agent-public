# DFS Football AI Agent

## Overview
The DFS Football AI Agent allows users to ask **natural language questions** about fantasy football data and get **PostgreSQL query results** instantly.  

It connects to a database containing DFS player stats, projections, and schedules, generates SQL queries using Google Gemini AI, and displays the results in a clean Streamlit interface.

> Note: The scraping/ETL pipeline is separate — this agent only reads data from the database.

---

## Modules
app/db.py

- Creates a cached SQLAlchemy engine
- Applies session safety settings
- Executes only SELECT queries or CTEs

app/utils.py

- Logs interactions (logs.csv)
- Cleans AI-generated SQL
- Loads schema prompt from schema_prompt.txt

app/ai_agent.py

- Uses Google Gemini AI to convert natural language to SQL
- Logs AI responses automatically

app/schema_prompt.txt

- Contains table definitions, relationships, and context for the AI model
  
##  Live Demo
[Launch App](https://garybolduc-ai-sql-agent.streamlit.app)

## Next Steps
The next version of this will use the Google ADK (https://google.github.io/adk-docs/) to create a more sophisticated agent that can:
- Have a conversation
- Create DFS lineups
- Export DFS lineups
