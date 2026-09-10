import duckdb
import os
from google import genai

con = duckdb.connect("ticket_analytics.duckdb")

SEMANTIC_CONTEXT = """
TABLE: fct_ticket_enriched
COLUMNS:
  - ticket_id (VARCHAR): Unique ticket identifier
  - customer_id (VARCHAR): Account identifier
  - account_tier (VARCHAR): 'Enterprise', 'Mid-Market', 'Free'
  - created_at (TIMESTAMP): Ticket creation date
  - resolution_time_hours (DOUBLE): Hours taken to resolve ticket
  - is_sla_breached (BOOLEAN): TRUE if resolution_time_hours > 24, else FALSE
  - sentiment (VARCHAR): 'Positive', 'Neutral', 'Negative'
  - root_cause_category (VARCHAR): 'Bug/Outage', 'Billing', 'Feature Request', 'UX Confusion'
  - executive_summary (VARCHAR): AI summary of customer issue

BUSINESS METRICS & RULES:
  - Total Tickets: COUNT(ticket_id)
  - SLA Breach Rate (%): (COUNT(CASE WHEN is_sla_breached THEN 1 END) * 100.0 / COUNT(*))
  - Average Resolution Time: AVG(resolution_time_hours)
  - High-Risk Accounts: account_tier = 'Enterprise' AND (sentiment = 'Negative' OR is_sla_breached = TRUE)
"""

def ask_cortex_analyst(user_question):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # Fallback query if API key isn't provided
        return "SELECT account_tier, COUNT(*) as ticket_count, AVG(resolution_time_hours) as avg_hours FROM fct_ticket_enriched GROUP BY 1", con.execute("SELECT account_tier, COUNT(*) as ticket_count, AVG(resolution_time_hours) as avg_hours FROM fct_ticket_enriched GROUP BY 1").df()

    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are Snowflake Cortex Analyst—an AI engine converting plain English operational questions into valid DuckDB SQL queries.
    
    Semantic Business Context:
    {SEMANTIC_CONTEXT}
    
    User Question: "{user_question}"
    
    INSTRUCTIONS:
    1. Output ONLY the executable DuckDB SQL query. Do not wrap in markdown code blocks (` ```sql `), do not add explanations.
    2. Always use clear column aliases.
    """

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    sql_query = response.text.strip().replace("```sql", "").replace("```", "").strip()
    
    try:
        results_df = con.execute(sql_query).df()
        return sql_query, results_df
    except Exception as e:
        return sql_query, f"Execution Error: {str(e)}"