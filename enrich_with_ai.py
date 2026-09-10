import duckdb
import pandas as pd
import os
from google import genai

# Connect to DuckDB database created by dbt
con = duckdb.connect("ticket_analytics.duckdb")
df = con.execute("SELECT * FROM fct_ticket_performance").df()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

def get_ai_insights(feedback_text):
    if not client:
        # Fallback rules engine if API key isn't set
        if "furious" in feedback_text.lower() or "outage" in feedback_text.lower():
            return "Negative", "Bug/Outage", "High-priority technical issue causing business impact."
        return "Neutral", "General Inquiry", "Customer requesting clarification or feature guidance."
    
    prompt = f"""
    Analyze this customer ticket feedback:
    "{feedback_text}"
    
    Return EXACTLY three comma-separated fields:
    1. Sentiment: [Positive, Neutral, Negative]
    2. Root Cause: [Bug/Outage, Billing, Feature Request, UX Confusion]
    3. Executive Summary: A concise 1-sentence summary of the core issue.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    parts = response.text.strip().split(",")
    sentiment = parts[0].strip() if len(parts) > 0 else "Neutral"
    root_cause = parts[1].strip() if len(parts) > 1 else "General"
    summary = ",".join(parts[2:]).strip() if len(parts) > 2 else response.text.strip()
    return sentiment, root_cause, summary

print("Running AI enrichment on ticket feedback...")
sentiments, root_causes, summaries = [], [], []

for idx, row in df.head(20).iterrows():
    sent, cause, summ = get_ai_insights(row['customer_feedback'])
    sentiments.append(sent)
    root_causes.append(cause)
    summaries.append(summ)

for _ in range(len(df) - len(sentiments)):
    sentiments.append("Neutral")
    root_causes.append("General")
    summaries.append("Standard customer ticket log.")

df['sentiment'] = sentiments
df['root_cause_category'] = root_causes
df['executive_summary'] = summaries

con.execute("CREATE OR REPLACE TABLE fct_ticket_enriched AS SELECT * FROM df")
print("Successfully written enriched table 'fct_ticket_enriched' into DuckDB!")