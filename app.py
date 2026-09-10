import streamlit as st
import duckdb
import pandas as pd

# Page setup
st.set_page_config(page_title="CX Ticket Escalation Intelligence", layout="wide")

st.title("🚨 Support Ticket Escalation & Sentiment Dashboard")
st.markdown("Powered by **DuckDB + dbt + Gemini AI**")

# Query DuckDB for the enriched fact table created in Step 5
con = duckdb.connect("ticket_analytics.duckdb")
df = con.execute("SELECT * FROM fct_ticket_enriched").df()

# 1. Executive KPI Metrics Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tickets", len(df))
col2.metric("Enterprise Tickets", len(df[df['account_tier'] == 'Enterprise']))
col3.metric("SLA Breaches (>24h)", len(df[df['is_sla_breached'] == True]))
col4.metric("Negative Sentiment", len(df[df['sentiment'] == 'Negative']))

st.divider()

# 2. High-Risk Escalations Table
st.subheader("⚠️ High-Risk Escalations (Enterprise + Negative Sentiment / SLA Breach)")
filtered_df = df[
    (df['account_tier'] == 'Enterprise') & 
    ((df['sentiment'] == 'Negative') | (df['is_sla_breached'] == True))
]

st.dataframe(
    filtered_df[[
        'ticket_id', 'customer_id', 'resolution_time_hours', 
        'sentiment', 'root_cause_category', 'executive_summary'
    ]],
    use_container_width=True
)

st.divider()

# 3. Root Cause Distribution Chart
st.subheader("Root Cause Breakdown")
st.bar_chart(df['root_cause_category'].value_counts())