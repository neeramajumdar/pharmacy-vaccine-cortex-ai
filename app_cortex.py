import streamlit as st
from cortex_analyst_engine import ask_cortex_analyst

st.set_page_config(page_title="CXE Self-Service Cortex Agent", layout="wide")

st.title("💬 CX Operational Self-Service Data Assistant")
st.markdown("Powered by **Snowflake Cortex Analyst Architecture (Semantic Models + Text-to-SQL)**")

st.info("Ask ad-hoc operational questions in plain English to get immediate SQL results without waiting on data teams!")

sample_query = st.selectbox(
    "Or select a common operational question:",
    [
        "Custom question...",
        "What is the SLA breach rate by account tier?",
        "Show me all Enterprise accounts with negative sentiment.",
        "What are the top root causes for SLA breaches?",
        "What is the average resolution time for Bug/Outage tickets?"
    ]
)

user_input = st.text_input("Enter your operational question:", value="" if sample_query == "Custom question..." else sample_query)

if st.button("Ask Cortex Analyst"):
    if user_input:
        with st.spinner("Cortex Analyst is translating question into Semantic SQL..."):
            sql_generated, result = ask_cortex_analyst(user_input)
            
            st.subheader("Generated Semantic SQL Query")
            st.code(sql_generated, language="sql")
            
            st.subheader("QueryResult Data")
            if isinstance(result, str):
                st.error(result)
            else:
                st.dataframe(result, use_container_width=True)
                if len(result.columns) == 2 and (result.dtypes[1] in ['int64', 'float64']):
                    st.bar_chart(result.set_index(result.columns[0]))