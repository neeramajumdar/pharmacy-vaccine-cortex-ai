import streamlit as st
import pandas as pd
import requests
import json

# ============================================================================
# Streamlit Configuration & Custom Styling
# ============================================================================
st.set_page_config(
    page_title="Pharmacy CX Vaccine Analytics | Cortex Analyst",
    page_icon="💉",
    layout="wide"
)

st.title("💉 Retail Pharmacy Vaccine CX Analytics")
st.caption("Powered by Snowflake Cortex AI & dbt Semantic Layer")

# Sidebar - Database Connection Info & Context
with st.sidebar:
    st.header("⚙️ Configuration & Metadata")
    st.markdown("**Environment:** Snowflake `PHARMACY_DB.ANALYTICS`")
    st.markdown("**Semantic Model:** `semantic_models.yml`")
    
    st.divider()
    st.markdown("### 💡 Example Questions to Ask:")
    st.markdown("- *What is the overall no show rate?*")
    st.markdown("- *What are the top root cause categories for missed appointments?*")
    st.markdown("- *Show me the total no shows by channel.*")
    st.markdown("- *What is the average sentiment score when a reminder was not sent?*")

# ============================================================================
# Session State Initialization
# ============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I am your Cortex Analyst Assistant. Ask me any question about vaccine appointment no-shows, channel adoption, or customer survey feedback."
        }
    ]

# Display previous chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "data" in message:
            st.dataframe(message["data"], use_container_width=True)

# ============================================================================
# Snowflake Cortex Analyst REST API Call Function
# ============================================================================
def query_cortex_analyst(prompt: str):
    """
    Sends natural language prompt to Snowflake Cortex Analyst REST API endpoint
    and returns generated SQL along with query results.
    """
    # Replace with your actual Snowflake Account credentials / secrets
    SNOWFLAKE_ACCOUNT = st.secrets.get("SNOWFLAKE_ACCOUNT", "my_account")
    API_TOKEN = st.secrets.get("SNOWFLAKE_TOKEN", "my_token")
    
    url = f"https://{SNOWFLAKE_ACCOUNT}.snowflakecomputing.com/api/v2/cortex/analyst/message"
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ],
        "semantic_model_file": "@PHARMACY_DB.ANALYTICS.PHARMACY_CSV_STAGE/semantic_models.yml"
    }
    
    # Send request to Cortex Analyst REST API
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": str(e)}

# ============================================================================
# Chat Interaction Logic
# ============================================================================
if prompt := st.chat_input("Ask a question about vaccine survey analytics..."):
    # 1. Display User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Process Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Cortex Analyst interpreting prompt against Semantic Model..."):
            
            # Call Cortex Analyst API
            api_response = query_cortex_analyst(prompt)
            
            if "error" in api_response:
                response_text = f"⚠️ **Connection Note:** Running in demo mode. (API Response: {api_response['error']})"
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            else:
                # Extract response text and SQL from API response payload
                response_content = api_response.get("message", {}).get("content", [])
                
                for item in response_content:
                    if item.get("type") == "text":
                        text_res = item.get("text")
                        st.markdown(text_res)
                        st.session_state.messages.append({"role": "assistant", "content": text_res})
                        
                    elif item.get("type") == "sql":
                        generated_sql = item.get("statement")
                        st.markdown("**Generated SQL Query:**")
                        st.code(generated_sql, language="sql")
                        
                        # Display results dataframe if data is returned
                        if "results" in item:
                            df = pd.DataFrame(item["results"])
                            st.dataframe(df, use_container_width=True)
                            st.session_state.messages.append({
                                "role": "assistant", 
                                "content": "Here are the query results:",
                                "data": df
                            })
